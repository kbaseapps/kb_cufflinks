import os
import uuid
from pprint import pprint
import multiprocessing as mp

import script_utils
from cuffmerge import CuffMerge

from Workspace.WorkspaceClient import Workspace as Workspace
from DataFileUtil.DataFileUtilClient import DataFileUtil
from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil

class CuffDiff:

    GFFREAD_TOOLKIT_PATH = '/kb/deployment/bin/gffread'

    def _mkdir_p(self, path):
        """
        _mkdir_p: make directory for given path
        """
        if not path:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def _process_params(self, params):
        """
        validates params passed to run_CuffDiff method
        """
        for p in ['expressionset_ref',
                  'workspace_name',
                  'diff_expression_obj_name',
                  'filtered_expression_matrix_name']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))


    def _run_gffread(self, gff_path, gtf_path, result_dir):
        """
        _run_gffread: run gffread script
        ref: http://ccb.jhu.edu/software/stringtie/gff.shtml
        """
        print('converting gff to gtf')
        command = self.GFFREAD_TOOLKIT_PATH + '/gffread '
        command += "-E {0} -T -o {1}".format(gff_path, gtf_path)

        ret = script_utils.runProgram(self.logger, "gffread", command)

    def _create_gtf_file(self, genome_ref):
        """
        _create_gtf_file: create reference annotation file from genome
        """
        result_dir = self.scratch

        genome_gff_file = self.gfu.genome_to_gff({'genome_ref': genome_ref,
                                                  'target_dir': result_dir})['file_path']

        gtf_ext = '.gtf'
        if not genome_gff_file.endswith(gtf_ext):
            gtf_path = os.path.splitext(genome_gff_file)[0] + '.gtf'
            self._run_gffread(genome_gff_file, gtf_path, result_dir)
        else:
            gtf_path = genome_gff_file

        return gtf_path

    def _get_gtf_file(self, genome_ref, result_dir):
        """
        _get_gtf_file: get the reference annotation file (in GTF or GFF3 format)
        """
        genome_data = self.ws_client.get_objects2({'objects':
                                            [{'ref': genome_ref}]})['data'][0]['data']

        gff_handle_ref = genome_data.get('gff_handle_ref')

        if gff_handle_ref:
            annotation_file = self.dfu.shock_to_file({'handle_id': gff_handle_ref,
                                                      'file_path': result_dir,
                                                      'unpack': 'unpack'})['file_path']
        else:
            annotation_file = self._create_gtf_file(genome_ref)
        return annotation_file

    def _gen_diff_expression_data(self, expressionset_data, result_directory):
        """
        _generate_diff_expression_data: generate RNASeqDifferentialExpression object data
        """
        diff_expression_data = {
            'tool_used': 'cuffdiff',
            'tool_version': '2.2.1',
            'expressionSet_id': expressionset_data.get('expressionSet_id'),
            'genome_id': expressionset_data.get('genome_id'),
            'alignmentSet_id': expressionset_data.get('alignmentSet_id'),
            'sampleset_id': expressionset_data.get('sampleset_id')
        }

        #self._generate_diff_expression_csv(result_directory, alpha_cutoff,
                                           #fold_change_cutoff, condition_string)

        handle = self.dfu.file_to_shock({'file_path': result_directory,
                                         'pack': 'zip',
                                         'make_handle': True})['handle']
        diff_expression_data.update({'file': handle})
        diff_expression_data.update({'condition': expressionset_data.get('condition')})

        return diff_expression_data

    def _save_diff_expression(self, params, diff_exp_data):

        workspace_name = params.get('workspace_name')
        output_name = params['diff_expression_obj_name']

        if isinstance(workspace_name, int) or workspace_name.isdigit():
            workspace_id = workspace_name
        else:
            workspace_id = self.dfu.ws_name_to_id(workspace_name)

        dfu_oi = self.ws_client.save_objects({'id': workspace_id,
                                            "objects": [{
                                            "type": "KBaseRNASeq.RNASeqDifferentialExpression",
                                            "data": diff_exp_data,
                                            "name": output_name
                                            }]
                                            })[0]
        diff_expression_obj_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])
        return diff_expression_obj_ref

    def _get_expressionset_data(self, expressionset_ref, result_directory):
        """
        Get data from expressionset object in the form required for input to
        cuffmerge and cuffdiff
        """
        expression_set = self.ws_client.get_objects2(
            {'objects':
                 [{'ref': expressionset_ref}]})['data'][0]

        expression_set_data = expression_set['data']

        output_data = {}
        output_data['expressionSet_id'] = expressionset_ref
        output_data['alignmentSet_id'] = expression_set_data.get('alignmentSet_id')
        output_data['sampleset_id'] = expression_set_data.get('sampleset_id')
        output_data['genome_id'] = expression_set_data.get('genome_id')

        """
        Get gtf file from genome_ref. Used as input to cuffmerge.
        """
        output_data['gtf_file_path'] = self._get_gtf_file(output_data['genome_id'], result_directory)

        condition = []
        bam_files = []

        mapped_expr_ids = expression_set_data.get('mapped_expression_ids')
        """
        assembly_gtf.txt will contain the file paths of all .gtf files in the expressionset.
        Used as input to cuffmerge.
        """
        assembly_file = os.path.join(result_directory, "assembly_gtf.txt")
        list_file = open(assembly_file, 'w')
        for i in mapped_expr_ids:
            for alignment_id, expression_id in i.items():
                expression_data = self.ws_client.get_objects2(
                    {'objects':
                         [{'ref': expression_id}]})['data'][0]['data']

                handle_id = expression_data.get('file').get('hid')
                expression_name = os.path.splitext(expression_data.get('file').get('file_name'))[0]
                tmp_gtf_directory = os.path.join(result_directory, expression_name)
                self._mkdir_p(tmp_gtf_directory)

                self.dfu.shock_to_file({'handle_id': handle_id,
                                        'file_path': tmp_gtf_directory,
                                        'unpack': 'unpack'})

                e_file_path = os.path.join(tmp_gtf_directory, "transcripts.gtf")
                if os.path.exists(e_file_path):
                    print e_file_path
                    print('Adding: ' + e_file_path)
                    list_file.write("{0}\n".format(e_file_path))
                else:
                    raise ValueError(e_file_path + " not found")
                """
                List of bam files in alignment set. Used as input to cuffdiff.
                """
                alignment_data = self.ws_client.get_objects2(
                    {'objects':
                         [{'ref': alignment_id}]})['data'][0]['data']

                handle_id = alignment_data.get('file').get('hid')
                alignment_name, ext = os.path.splitext(alignment_data.get('file').get('file_name'))
                tmp_bam_directory = os.path.join(result_directory, alignment_name)
                self._mkdir_p(tmp_bam_directory)

                self.dfu.shock_to_file({'handle_id': handle_id,
                                        'file_path': tmp_bam_directory,
                                        'unpack': 'unpack'})

                a_file_path = os.path.join(tmp_bam_directory, "accepted_hits.bam")
                if os.path.exists(a_file_path):
                    print a_file_path
                    bam_files.append(a_file_path)
                else:
                    raise ValueError(a_file_path + " not found")

                """
                List of all conditions in expressionset. Used as input to cuffdiff.
                """
                condition.append(expression_data.get('condition'))

        list_file.close()
        output_data['assembly_file'] = assembly_file
        output_data['condition'] = condition
        output_data['bam_files'] = bam_files
        return output_data

    def _assemble_cuffdiff_command(self, params, expressionset_data, merged_gtf, output_dir):

        bam_files = " ".join(expressionset_data.get('bam_files'))
        t_labels = ",".join(expressionset_data.get('condition'))

        # output_dir = os.path.join(cuffdiff_dir, self.method_params['output_obj_name'])

        cuffdiff_command = (' -p ' + str(self.num_threads))
        """
        Set Advanced parameters for Cuffdiff
        """
        if ('time_series' in params and params['time_series'] != 0):
            cuffdiff_command += (' -T ')
        if ('min_alignment_count' in params and
                    params['min_alignment_count'] is not None):
            cuffdiff_command += (' -c ' + str(params['min_alignment_count']))
        if ('multi_read_correct' in params and
                        params['multi_read_correct'] != 0):
            cuffdiff_command += (' --multi-read-correct ')
        if ('library_type' in params and
                    params['library_type'] is not None):
            cuffdiff_command += (' --library-type ' + params['library_type'])
        if ('library_norm_method' in params and
                        params['library_norm_method'] is not None):
            cuffdiff_command += (' --library-norm-method ' + params['library_norm_method'])

        cuffdiff_command += " -o {0} -L {1} -u {2} {3}".format(output_dir,
                                                               t_labels,
                                                               merged_gtf,
                                                               bam_files)
        return cuffdiff_command

    def __init__(self, config, services, logger=None):
        self.config = config
        self.logger = logger
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.scratch = os.path.join(config['scratch'], str(uuid.uuid4()))
        self.ws_url = config['workspace-url']
        self._mkdir_p(self.scratch)
        self.services = services
        self.ws_client = Workspace(self.services['workspace_service_url'])
        self.dfu = DataFileUtil(self.callback_url)
        self.gfu = GenomeFileUtil(self.callback_url)
        self.cuffmerge_utils = CuffMerge(config, logger)
        self.num_threads = mp.cpu_count()

    def run_cuffdiff(self, params):
        """
        Check input parameters
        """
        self._process_params(params)

        expressionset_ref = params.get('expressionset_ref')
        result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_directory)

        """
        Get data from expressionset in a format needed for cuffmerge and cuffdiff
        """
        expressionset_data = self._get_expressionset_data(expressionset_ref, result_directory)

        """
        Run cuffmerge
        """
        cuffmerge_dir = os.path.join(self.scratch, "cuffmerge_" + str(uuid.uuid4()))
        merged_gtf = self.cuffmerge_utils.run_cuffmerge(cuffmerge_dir,
                                                        self.num_threads,
                                                        expressionset_data.get('gtf_file_path'),
                                                        expressionset_data.get('assembly_file'))
        self.logger.info('MERGED GTF FILE: ' + merged_gtf)

        """
        Assemble parameters and run cuffdiff
        """
        cuffdiff_dir = os.path.join(self.scratch, "cuffdiff_" + str(uuid.uuid4()))
        self._mkdir_p(cuffdiff_dir)

        cuffdiff_command = self._assemble_cuffdiff_command(params,
                                                           expressionset_data,
                                                           merged_gtf,
                                                           cuffdiff_dir)
        try:
            ret = script_utils.runProgram(self.logger,
                                          "cuffdiff",
                                          cuffdiff_command,
                                          None,
                                          cuffdiff_dir)
            result = ret["result"]
            for line in result.splitlines(False):
                self.logger.info(line)
                stderr = ret["stderr"]
                prev_value = ''
                for line in stderr.splitlines(False):
                    if line.startswith('> Processing Locus'):
                        words = line.split()
                        cur_value = words[len(words) - 1]
                        if prev_value != cur_value:
                            prev_value = cur_value
                            self.logger.info(line)
                        else:
                            prev_value = ''
                            self.logger.info(line)
        except Exception, e:
            raise Exception("Error executing cuffdiff {0},{1}".format(cuffdiff_command, e))

        """
        Save differential expression object
        """
        diff_exp_data = self._gen_diff_expression_data(expressionset_data, cuffdiff_dir)

        de_obj_ref = self._save_diff_expression(params, diff_exp_data)

        returnVal = {'obj_ref': de_obj_ref}
        return returnVal
