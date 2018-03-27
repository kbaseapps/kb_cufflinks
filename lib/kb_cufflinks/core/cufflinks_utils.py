import time
import math
import os
import uuid
import errno
import json
import re
import subprocess
import traceback
from pathos.multiprocessing import ProcessingPool as Pool
import multiprocessing
import zipfile
import contig_id_mapping as c_mapping
from pprint import pprint

from DataFileUtil.DataFileUtilClient import DataFileUtil
from Workspace.WorkspaceClient import Workspace as Workspace
from KBaseReport.KBaseReportClient import KBaseReport
from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from ReadsAlignmentUtils.ReadsAlignmentUtilsClient import ReadsAlignmentUtils
from ExpressionUtils.ExpressionUtilsClient import ExpressionUtils
from SetAPI.SetAPIClient import SetAPI


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class CufflinksUtils:
    CUFFLINKS_TOOLKIT_PATH = '/opt/cufflinks/'
    GFFREAD_TOOLKIT_PATH = '/opt/cufflinks/'

    def __init__(self, config):
        """

        :param config:
        :param logger:
        :param directory: Working directory
        :param urls: Service urls
        """
        # BEGIN_CONSTRUCTOR
        self.ws_url = config["workspace-url"]
        self.ws_url = config["workspace-url"]
        self.callback_url = config['SDK_CALLBACK_URL']
        self.srv_wiz_url = config['srv-wiz-url']
        self.token = config['KB_AUTH_TOKEN']
        self.shock_url = config['shock-url']
        self.dfu = DataFileUtil(self.callback_url)
        self.gfu = GenomeFileUtil(self.callback_url)
        self.au = AssemblyUtil(self.callback_url)
        self.rau = ReadsAlignmentUtils(self.callback_url)
        self.set_api = SetAPI(self.srv_wiz_url, service_ver='dev')
        self.eu = ExpressionUtils(self.callback_url)
        self.ws = Workspace(self.ws_url, token=self.token)

        self.scratch = os.path.join(config['scratch'], str(uuid.uuid4()))
        self._mkdir_p(self.scratch)

        self.tool_used = "Cufflinks"
        self.tool_version = os.environ['VERSION']
        # END_CONSTRUCTOR
        pass

    def parse_FPKMtracking_calc_TPM(self, filename):
        """
        Generates TPM from FPKM
        :return:
        """
        fpkm_dict = {}
        tpm_dict = {}
        gene_col = 0
        fpkm_col = 9
        sum_fpkm = 0.0
        with open(filename) as f:
            next(f)
            for line in f:
                larr = line.split("\t")
                gene_id = larr[gene_col]
                if gene_id != "":
                    fpkm = float(larr[fpkm_col])
                    sum_fpkm = sum_fpkm + fpkm
                    fpkm_dict[gene_id] = math.log(fpkm + 1, 2)
                    tpm_dict[gene_id] = fpkm

        if sum_fpkm == 0.0:
            log("Warning: Unable to calculate TPM values as sum of FPKM values is 0")
        else:
            for g in tpm_dict:
                tpm_dict[g] = math.log((tpm_dict[g] / sum_fpkm) * 1e6 + 1, 2)

        return fpkm_dict, tpm_dict

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

    def _validate_run_cufflinks_params(self, params):
        """
        _validate_run_cufflinks_params:
                Raises an exception if params are invalid
        """

        log('Start validating run_cufflinks params')

        # check for required parameters
        for p in ['alignment_object_ref', 'workspace_name', 'genome_ref']:
            if p not in params:
                raise ValueError('"{}" parameter is required, but missing'.format(p))

    def _run_command(self, command):
        """
        _run_command: run command and print result
        """

        log('Start executing command:\n{}'.format(command))
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = pipe.communicate()[0]
        exitCode = pipe.returncode

        if (exitCode == 0):
            log('Executed command:\n{}\n'.format(command) +
                'Exit Code: {}\nOutput:\n{}'.format(exitCode, output))
        else:
            error_msg = 'Error running command:\n{}\n'.format(command)
            error_msg += 'Exit Code: {}\nOutput:\n{}'.format(exitCode, output)

            raise ValueError(error_msg)

    def _run_gffread(self, gff_path, gtf_path):
        """
        _run_gffread: run gffread script

        ref: http://cole-trapnell-lab.github.io/cufflinks/file_formats/#the-gffread-utility
        """
        log('converting gff to gtf')
        command = self.GFFREAD_TOOLKIT_PATH + '/gffread '
        command += "-E {0} -T -o {1}".format(gff_path, gtf_path)

        self._run_command(command)

    def _create_gtf_annotation_from_genome(self, genome_ref):
        """
         Create reference annotation file from genome
        """
        ref = self.ws.get_object_subset(
            [{'ref': genome_ref, 'included': ['contigset_ref', 'assembly_ref']}])
        if 'contigset_ref' in ref[0]['data']:
            contig_id = ref[0]['data']['contigset_ref']
        elif 'assembly_ref' in ref[0]['data']:
            contig_id = ref[0]['data']['assembly_ref']
        if contig_id is None:
            raise ValueError(
                "Genome at {0} does not have reference to the assembly object".format(
                    genome_ref))
        print contig_id
        log("Generating GFF file from Genome")
        try:
            ret = self.au.get_assembly_as_fasta({'ref': contig_id})
            output_file = ret['path']
            mapping_filename = c_mapping.create_sanitized_contig_ids(output_file)
            os.remove(output_file)
            # get the GFF
            ret = self.gfu.genome_to_gff({'genome_ref': genome_ref})
            genome_gff_file = ret['file_path']
            c_mapping.replace_gff_contig_ids(genome_gff_file, mapping_filename, to_modified=True)
            gtf_ext = ".gtf"

            if not genome_gff_file.endswith(gtf_ext):
                gtf_path = os.path.splitext(genome_gff_file)[0] + '.gtf'
                self._run_gffread(genome_gff_file, gtf_path)
            else:
                gtf_path = genome_gff_file

            log("gtf file : " + gtf_path)
        except Exception:
            raise ValueError(
                "Generating GTF file from Genome Annotation object Failed :  {}".format(
                    "".join(traceback.format_exc())))
        return gtf_path

    def _get_gtf_file(self, alignment_ref):
        """
        _get_gtf_file: get the reference annotation file (in GTF or GFF3 format)
        """
        result_directory = self.scratch
        alignment_data = self.ws.get_objects2({'objects':
                                               [{'ref': alignment_ref}]})['data'][0]['data']

        genome_ref = alignment_data.get('genome_id')
        # genome_name = self.ws.get_object_info([{"ref": genome_ref}], includeMetadata=None)[0][1]
        # ws_gtf = genome_name+"_GTF_Annotation"

        genome_data = self.ws.get_objects2({'objects':
                                            [{'ref': genome_ref}]})['data'][0]['data']

        gff_handle_ref = genome_data.get('gff_handle_ref')

        if gff_handle_ref:
            log('getting reference annotation file from genome')
            annotation_file = self.dfu.shock_to_file({'handle_id': gff_handle_ref,
                                                      'file_path': result_directory,
                                                      'unpack': 'unpack'})['file_path']
        else:
            annotation_file = self._create_gtf_annotation_from_genome(genome_ref)

        return annotation_file

    def _get_gtf_file_from_genome_ref(self, genome_ref):
        """
        _get_gtf_file: get the reference annotation file (in GTF or GFF3 format)
        """
        result_directory = self.scratch

        genome_data = self.ws.get_objects2({'objects':
                                            [{'ref': genome_ref}]})['data'][0]['data']

        gff_handle_ref = genome_data.get('gff_handle_ref')

        if gff_handle_ref:
            log('getting reference annotation file from genome')
            annotation_file = self.dfu.shock_to_file({'handle_id': gff_handle_ref,
                                                      'file_path': result_directory,
                                                      'unpack': 'unpack'})['file_path']
        else:
            annotation_file = self._create_gtf_annotation_from_genome(genome_ref)

        return annotation_file

    def _get_input_file(self, alignment_ref):
        """
        _get_input_file: get input BAM file from Alignment object
        """

        bam_file_dir = self.rau.download_alignment({'source_ref': alignment_ref})['destination_dir']

        files = os.listdir(bam_file_dir)
        bam_file_list = [file for file in files if re.match(r'.*\_sorted\.bam', file)]
        if not bam_file_list:
            bam_file_list = [file for file in files if re.match(r'.*(?<!sorted)\.bam', file)]

        if not bam_file_list:
            raise ValueError('Cannot find .bam file from alignment {}'.format(alignment_ref))

        bam_file_name = bam_file_list[0]

        bam_file = os.path.join(bam_file_dir, bam_file_name)

        return bam_file

    def _generate_command(self, params):
        """
        _generate_command: generate cufflinks command
        """
        cufflinks_command = '/opt/cufflinks/cufflinks'
        cufflinks_command += (' -q -p ' + str(params.get('num_threads', 1)))
        if 'max_intron_length' in params and params['max_intron_length'] is not None:
            cufflinks_command += (' --max-intron-length ' + str(params['max_intron_length']))
        if 'min_intron_length' in params and params['min_intron_length'] is not None:
            cufflinks_command += (' --min-intron-length ' + str(params['min_intron_length']))
        if 'overhang_tolerance' in params and params['overhang_tolerance'] is not None:
            cufflinks_command += (' --overhang-tolerance ' + str(params['overhang_tolerance']))

        cufflinks_command += " -o {0} -G {1} {2}".format(
            params['result_directory'], params['gtf_file'], params['input_file'])

        log('Generated cufflinks command: {}'.format(cufflinks_command))

        return cufflinks_command

    def _process_rnaseq_alignment_object(self, params):
        """
        _process_alignment_object: process KBaseRNASeq.RNASeqAlignment type input object
        """
        log('start processing RNASeqAlignment object\nparams:\n{}'.format(
            json.dumps(params, indent=1)))
        alignment_ref = params.get('alignment_ref')

        result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_directory)
        params['result_directory'] = str(result_directory)

        # input files
        params['input_file'] = self._get_input_file(alignment_ref)
        if not params.get('gtf_file'):
            params['gtf_file'] = self._get_gtf_file(alignment_ref)

        if '/' not in params['genome_ref']:
            params['genome_ref'] = params['workspace_name']+'/'+params['genome_ref']

        command = self._generate_command(params)
        self._run_command(command)

        expression_obj_ref = self._save_rnaseq_expression(result_directory,
                                                   alignment_ref,
                                                   params.get('workspace_name'),
                                                   params.get('genome_ref'),
                                                   params['gtf_file'],
                                                   params['expression_suffix'])

        returnVal = {'result_directory': result_directory,
                     'expression_obj_ref': expression_obj_ref,
                     'alignment_ref': alignment_ref}

        expression_name = self.ws.get_object_info([{"ref": expression_obj_ref}],
                                                  includeMetadata=None)[0][1]

        widget_params = {"output": expression_name, "workspace": params.get('workspace_name')}
        returnVal.update(widget_params)

        return returnVal

    def _process_kbasesets_alignment_object(self, params):
        """
        _process_alignment_object: process KBaseRNASeq.RNASeqAlignment type input object
        """
        log('start processing KBaseSets object\nparams:\n{}'.format(
            json.dumps(params, indent=1)))
        alignment_ref = params.get('alignment_ref')

        result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_directory)
        params['result_directory'] = str(result_directory)

        # input files
        params['input_file'] = self._get_input_file(alignment_ref)
        if not params.get('gtf_file'):
            params['gtf_file'] = self._get_gtf_file(alignment_ref)

        command = self._generate_command(params)
        self._run_command(command)

        expression_obj_ref = self._save_kbasesets_expression(result_directory,
                                                   alignment_ref,
                                                   params.get('workspace_name'),
                                                   params.get('genome_ref'),
                                                   params.get('gtf_file'),
                                                   params.get('expression_suffix'))

        returnVal = {'result_directory': result_directory,
                     'expression_obj_ref': expression_obj_ref,
                     'alignment_ref': alignment_ref}

        expression_name = self.ws.get_object_info([{"ref": expression_obj_ref}],
                                                  includeMetadata=None)[0][1]

        widget_params = {"output": expression_name, "workspace": params.get('workspace_name')}
        returnVal.update(widget_params)

        return returnVal

    def _generate_html_report(self, result_directory, obj_ref):
        """
        _generate_html_report: generate html summary report
        """
        log('Start generating html report')
        html_report = list()

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)
        result_file_path = os.path.join(output_directory, 'report.html')

        expression_object = self.ws.get_objects2({'objects':
                                                  [{'ref': obj_ref}]})['data'][0]

        expression_object_type = expression_object.get('info')[2]

        Overview_Content = ''
        if re.match('KBaseRNASeq.RNASeqExpression-\d.\d', expression_object_type):
            Overview_Content += '<p>Generated Expression Object:</p><p>{}</p>'.format(
                expression_object.get('info')[1])
        elif re.match('KBaseRNASeq.RNASeqExpressionSet-\d.\d', expression_object_type):
            Overview_Content += '<p>Generated Expression Set Object:</p><p>{}</p>'.format(
                expression_object.get('info')[1])
            Overview_Content += '<br><p>Generated Expression Object:</p>'
            for expression_ref in expression_object['data']['sample_expression_ids']:
                expression_name = self.ws.get_object_info([{"ref": expression_ref}],
                                                          includeMetadata=None)[0][1]
                Overview_Content += '<p>{}</p>'.format(expression_name)
        elif re.match('KBaseSets.ExpressionSet-\d.\d', expression_object_type):
            pprint(expression_object)
            Overview_Content += '<p>Generated Expression Set Object:</p><p>{}</p>'.format(
                expression_object.get('info')[1])
            Overview_Content += '<br><p>Generated Expression Object:</p>'
            for expression_ref in expression_object['data']['items']:
                expression_name = self.ws.get_object_info([{"ref": expression_ref['ref']}],
                                                          includeMetadata=None)[0][1]
                condition = expression_ref['label']
                Overview_Content += '<p>condition:{0}; expression_name: {1}</p>'.format(condition, expression_name)

        with open(result_file_path, 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'report_template.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('<p>Overview_Content</p>',
                                                          Overview_Content)
                result_file.write(report_template)

        html_report.append({'path': result_file_path,
                            'name': os.path.basename(result_file_path),
                            'label': os.path.basename(result_file_path),
                            'description': 'HTML summary report for Cufflinks App'})
        return html_report

    def _save_rnaseq_expression(self, result_directory, alignment_ref,
                                workspace_name, genome_ref, gtf_file,
                                expression_suffix):
        """
        _save_rnaseq_expression: save Expression object to workspace
        """
        log('start saving Expression object')
        alignment_object_name = self.ws.get_object_info([{"ref": alignment_ref}],
                                                        includeMetadata=None)[0][1]

        # set expression name
        if re.match('.*_[Aa]lignment$', alignment_object_name):
            expression_name = re.sub('_[Aa]lignment$',
                                     expression_suffix,
                                     alignment_object_name)
        else:  # assume user specified suffix
            expression_name = alignment_object_name + expression_suffix

        gff_annotation_obj_ref = self._save_gff_annotation(genome_ref, gtf_file, workspace_name)

        expression_ref = self.eu.upload_expression({
            'destination_ref': workspace_name + '/' + expression_name,
            'source_dir': result_directory,
            'alignment_ref': alignment_ref,
            'tool_used': self.tool_used,
            'tool_version': self.tool_version,
            'annotation_ref': gff_annotation_obj_ref,
        })['obj_ref']

        return expression_ref

    def _save_kbasesets_expression(self, result_directory, alignment_ref,
                                   workspace_name, genome_ref, gtf_file,
                                   expression_suffix):
        """
        _save_kbasesets_expression: save Expression object to workspace using ExpressionUtils
        and SetAPI
        """
        log('start saving Expression object')

        alignment_info = self.ws.get_object_info3({'objects': [{"ref": alignment_ref}]})
        alignment_object_name = alignment_info['infos'][0][1]

        # set expression name
        if re.match('.*_[Aa]lignment$', alignment_object_name):
            expression_name = re.sub('_[Aa]lignment$',
                                     expression_suffix,
                                     alignment_object_name)
        else:  # assume user specified suffix
            expression_name = alignment_object_name + expression_suffix

        gff_annotation_obj_ref = self._save_gff_annotation(genome_ref, gtf_file, workspace_name)

        expression_ref = self.eu.upload_expression({
            'destination_ref': workspace_name+'/'+expression_name,
            'source_dir': result_directory,
            'alignment_ref': alignment_ref,
            'tool_used': self.tool_used,
            'tool_version': self.tool_version,
            'annotation_ref': gff_annotation_obj_ref,
        })['obj_ref']

        return expression_ref

    def _save_rnaseq_expression_set(self, alignment_expression_map, alignment_set_ref, workspace_name, expression_set_name):
        """
        _save_rnaseq_expression_set: save ExpressionSet object to workspace
        """
        log('start saving ExpressionSet object')
        if isinstance(workspace_name, int) or workspace_name.isdigit():
            workspace_id = workspace_name
        else:
            workspace_id = self.dfu.ws_name_to_id(workspace_name)

        expression_set_data = self._generate_expression_set_data(alignment_expression_map,
                                                                 alignment_set_ref,
                                                                 expression_set_name)

        object_type = 'KBaseRNASeq.RNASeqExpressionSet'
        save_object_params = {
            'id': workspace_id,
            'objects': [{
                'type': object_type,
                'data': expression_set_data,
                'name': expression_set_name
            }]
        }

        dfu_oi = self.dfu.save_objects(save_object_params)[0]
        expression_set_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        return expression_set_ref

    def _save_kbasesets_expression_set(self, alignment_expression_map,
                                       alignment_set_ref, workspace_name,
                                       expression_set_name):
        """
        _save_kbasesets_expression_set: save ExpressionSet object to workspace
        """
        log('start saving ExpressionSet object')
        if isinstance(workspace_name, int) or workspace_name.isdigit():
            workspace_id = workspace_name
        else:
            workspace_id = self.dfu.ws_name_to_id(workspace_name)

        expression_set_data = self._generate_expression_set_data(alignment_expression_map,
                                                                 alignment_set_ref,
                                                                 expression_set_name)

        object_type = 'KBaseRNASeq.RNASeqExpressionSet'
        save_object_params = {
            'id': workspace_id,
            'objects': [{
                'type': object_type,
                'data': expression_set_data,
                'name': expression_set_name
            }]
        }

        dfu_oi = self.dfu.save_objects(save_object_params)[0]
        expression_set_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        return expression_set_ref

    def _generate_report(self, obj_ref, workspace_name, result_directory,
                         exprMatrix_FPKM_ref=None, exprMatrix_TPM_ref=None):
        """
        _generate_report: generate summary report
        """

        log('creating report')

        output_files = self._generate_output_file_list(result_directory)
        output_html_files = self._generate_html_report(result_directory,
                                                       obj_ref)

        expression_object = self.ws.get_objects2({'objects':
                                                 [{'ref': obj_ref}]})['data'][0]
        expression_info = expression_object['info']
        expression_data = expression_object['data']

        expression_object_type = expression_info[2]
        if re.match('KBaseRNASeq.RNASeqExpression-\d+.\d+', expression_object_type):
            objects_created = [{'ref': obj_ref,
                                'description': 'Expression generated by Cufflinks'}]
        elif re.match('KBaseRNASeq.RNASeqExpressionSet-\d+.\d+', expression_object_type):
            objects_created = [{'ref': obj_ref,
                                'description': 'Expression generated by Cufflinks'}]
        elif re.match('KBaseSets.ExpressionSet-\d+.\d+', expression_object_type):
            objects_created = [{'ref': obj_ref,
                                'description': 'ExpressionSet generated by Cufflinks'}]
            items = expression_data['items']
            for item in items:
                objects_created.append({'ref': item['ref'],
                                        'description': 'Expression generated by Cufflinks'})
            objects_created.append({'ref': exprMatrix_FPKM_ref,
                                    'description': 'FPKM ExpressionMatrix generated by Cufflinks'})
            objects_created.append({'ref': exprMatrix_TPM_ref,
                                    'description': 'TPM ExpressionMatrix generated by Cufflinks'})

        report_params = {'message': '',
                         'workspace_name': workspace_name,
                         'file_links': output_files,
                         'objects_created': objects_created,
                         'html_links': output_html_files,
                         'direct_html_link_index': 0,
                         'html_window_height': 366,
                         'report_object_name': 'kb_cufflinks_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url, token=self.token)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def _parse_FPKMtracking(self, filename, metric):
        result = {}
        pos1 = 0
        if metric == 'FPKM':
            pos2 = 7
        if metric == 'TPM':
            pos2 = 8

        with open(filename) as f:
            next(f)
            for line in f:
                larr = line.split("\t")
                if larr[pos1] != "":
                    try:
                        result[larr[pos1]] = math.log(float(larr[pos2]) + 1, 2)
                    except ValueError:
                        result[larr[pos1]] = math.log(1, 2)

        return result

    def _generate_output_file_list(self, result_directory):
        """
        _generate_output_file_list: zip result files and generate file_links for report
        """
        log('Start packing result files')
        output_files = list()

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)
        result_file = os.path.join(output_directory, 'cufflinks_result.zip')

        with zipfile.ZipFile(result_file, 'w',
                             zipfile.ZIP_DEFLATED,
                             allowZip64=True) as zip_file:
            for root, dirs, files in os.walk(result_directory):
                for file in files:
                    if not (file.endswith('.DS_Store')):
                        zip_file.write(os.path.join(root, file),
                                       os.path.join(os.path.basename(root), file))

        output_files.append({'path': result_file,
                             'name': os.path.basename(result_file),
                             'label': os.path.basename(result_file),
                             'description': 'File(s) generated by Cufflinks App'})

        return output_files

    def _save_gff_annotation(self, genome_id, gtf_file, workspace_name):
        """
        _save_gff_annotation: save GFFAnnotation object to workspace
        """
        log('start saving GffAnnotation object')

        if isinstance(workspace_name, int) or workspace_name.isdigit():
            workspace_id = workspace_name
        else:
            workspace_id = self.dfu.ws_name_to_id(workspace_name)

        genome_data = self.ws.get_objects2({'objects':
                                            [{'ref': genome_id}]})['data'][0]['data']
        genome_name = genome_data.get('id')
        genome_scientific_name = genome_data.get('scientific_name')
        gff_annotation_name = genome_name + "_GTF_Annotation"
        file_to_shock_result = self.dfu.file_to_shock({'file_path': gtf_file,
                                                       'make_handle': True})
        gff_annotation_data = {'handle': file_to_shock_result['handle'],
                               'size': file_to_shock_result['size'],
                               'genome_id': genome_id,
                               'genome_scientific_name': genome_scientific_name}

        object_type = 'KBaseRNASeq.GFFAnnotation'

        save_object_params = {
            'id': workspace_id,
            'objects': [{
                'type': object_type,
                'data': gff_annotation_data,
                'name': gff_annotation_name
            }]
        }

        dfu_oi = self.dfu.save_objects(save_object_params)[0]
        gff_annotation_obj_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        return gff_annotation_obj_ref

    def _generate_expression_data(self, result_directory, alignment_ref,
                                  gtf_file, workspace_name, expression_suffix):
        """
        _generate_expression_data: generate Expression object with cufflinks output files
        """
        alignment_data_object = self.ws.get_objects2({'objects':
                                                      [{'ref': alignment_ref}]})['data'][0]

        # set expression name
        alignment_object_name = alignment_data_object['info'][1]
        if re.match('.*_[Aa]lignment$', alignment_object_name):
            expression_name = re.sub('_[Aa]lignment$',
                                     expression_suffix,
                                     alignment_object_name)
        else:  # assume user specified suffix
            expression_name = alignment_object_name + expression_suffix

        expression_data = {
            'id': expression_name,
            'type': 'RNA-Seq',
            'numerical_interpretation': 'FPKM',
            'processing_comments': 'log2 Normalized',
            'tool_used': self.tool_used,
            'tool_version': self.tool_version
        }
        alignment_data = alignment_data_object['data']

        condition = alignment_data.get('condition')
        expression_data.update({'condition': condition})

        genome_id = alignment_data.get('genome_id')
        expression_data.update({'genome_id': genome_id})

        gff_annotation_obj_ref = self._save_gff_annotation(genome_id, gtf_file, workspace_name)
        expression_data.update({'annotation_id': gff_annotation_obj_ref})

        read_sample_id = alignment_data.get('read_sample_id')
        expression_data.update({'mapped_rnaseq_alignment': {read_sample_id: alignment_ref}})

        exp_dict, tpm_exp_dict = self.parse_FPKMtracking_calc_TPM(
            os.path.join(result_directory, 'genes.fpkm_tracking'))

        expression_data.update({'expression_levels': exp_dict})

        expression_data.update({'tpm_expression_levels': tpm_exp_dict})

        handle = self.dfu.file_to_shock({'file_path': result_directory,
                                         'pack': 'zip',
                                         'make_handle': True})['handle']
        expression_data.update({'file': handle})

        return expression_data

    def _generate_expression_set_data(self, alignment_expression_map,
                                      alignment_set_ref, expression_set_name):
        """
        _generate_expression_set_data: generate ExpressionSet object with cufflinks output files
        """
        alignment_set_data_object = self.ws.get_objects2({'objects':
                                                          [{'ref': alignment_set_ref}]})['data'][0]

        alignment_set_data = alignment_set_data_object['data']

        expression_set_data = {
            'tool_used': self.tool_used,
            'tool_version': self.tool_version,
            'id': expression_set_name,
            'alignmentSet_id': alignment_set_ref,
            'genome_id': alignment_set_data.get('genome_id'),
            'sampleset_id': alignment_set_data.get('sampleset_id')
        }

        sample_expression_ids = []
        mapped_expression_objects = []
        mapped_expression_ids = []

        for alignment_expression in alignment_expression_map:
            alignment_ref = alignment_expression.get('alignment_ref')
            expression_ref = alignment_expression.get('expression_obj_ref')
            sample_expression_ids.append(expression_ref)
            mapped_expression_ids.append({alignment_ref: expression_ref})
            alignment_name = self.ws.get_object_info([{"ref": alignment_ref}],
                                                     includeMetadata=None)[0][1]
            expression_name = self.ws.get_object_info([{"ref": expression_ref}],
                                                      includeMetadata=None)[0][1]
            mapped_expression_objects.append({alignment_name: expression_name})

        expression_set_data['sample_expression_ids'] = sample_expression_ids
        expression_set_data['mapped_expression_objects'] = mapped_expression_objects
        expression_set_data['mapped_expression_ids'] = mapped_expression_ids

        return expression_set_data

    def _process_alignment_set_object(self, params, alignment_object_type):
        """
        _process_alignment_set_object: process KBaseRNASeq.RNASeqAlignmentSet type input object
                                        and KBaseSets.ReadsAlignmentSet type object
        """
        log('start processing KBaseRNASeq.RNASeqAlignmentSet object or KBaseSets.ReadsAlignmentSet object'
            '\nparams:\n{}'.format(
            json.dumps(params, indent=1)))

        alignment_set_ref = params.get('alignment_set_ref')

        if re.match('^KBaseRNASeq.RNASeqAlignmentSet-\d*', alignment_object_type):
            params['gtf_file'] = self._get_gtf_file(alignment_set_ref)
        else:
            if not '/' in params['genome_ref']:
                params['genome_ref'] = params['workspace_name']+'/'+params['genome_ref']

            params['gtf_file'] = self._get_gtf_file_from_genome_ref(params['genome_ref'])

        alignment_set = self.set_api.get_reads_alignment_set_v1({
                                                                'ref': alignment_set_ref,
                                                                'include_item_info': 0,
                                                                'include_set_item_ref_paths': 1
                                                                })
        mul_processor_params = []
        for alignment in alignment_set["data"]["items"]:
            alignment_ref = alignment['ref_path']
            alignment_upload_params = params.copy()
            alignment_upload_params['alignment_ref'] = alignment_ref
            mul_processor_params.append(alignment_upload_params)
            # use the following when you want to run the cmd sequentially
            # self._process_kbasesets_alignment_object(mul_processor_params[0])

        cpus = min(params.get('num_threads'), multiprocessing.cpu_count())
        pool = Pool(ncpus=cpus)
        log('running _process_alignment_object with {} cpus'.format(cpus))
        alignment_expression_map = pool.map(self._process_kbasesets_alignment_object, mul_processor_params)

        result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_directory)

        expression_items = list()
        for proc_alignment_return in alignment_expression_map:
            expression_obj_ref = proc_alignment_return.get('expression_obj_ref')
            alignment_ref = proc_alignment_return.get('alignment_ref')
            alignment_info = self.ws.get_object_info3({'objects': [{"ref": alignment_ref}], 'includeMetadata': 1})
            condition = alignment_info['infos'][0][10]['condition']
            expression_items.append({
                "ref": expression_obj_ref,
                "label": condition,
            })
            expression_name = self.ws.get_object_info([{"ref": expression_obj_ref}],
                                                      includeMetadata=None)[0][1]
            self._run_command('cp -R {} {}'.format(proc_alignment_return.get('result_directory'),
                                                   os.path.join(result_directory, expression_name)))

        expression_set = {
            "description": "generated by kb_cufflinks",
            "items": expression_items
        }

        expression_set_info = self.set_api.save_expression_set_v1({
            "workspace": params['workspace_name'],
            "output_object_name": params['expression_set_name'],
            "data": expression_set
        })

        returnVal = {'result_directory': result_directory,
                     'expression_obj_ref': expression_set_info['set_ref']}

        widget_params = {"output": params.get('expression_set_name'),
                         "workspace": params.get('workspace_name')}
        returnVal.update(widget_params)

        return returnVal

    def _generate_output_object_name(self, params, alignment_object_type, alignment_object_name):
        """
        Generates the output object name based on input object type and name and stores it in
        params with key equal to 'expression' or 'expression_set' based on whether the input
        object is an alignment or alignment_set.

        :param params: module input params
        :param alignment_object_type: input alignment object type
        :param alignment_object_name: input alignment object name
        :param alignment_object_data: input alignment object data
        """
        expression_set_suffix = params['expression_set_suffix']
        expression_suffix = params['expression_suffix']

        if re.match('^KBaseRNASeq.RNASeqAlignment-\d*', alignment_object_type):
            if re.match('.*_[Aa]lignment$', alignment_object_name):
                params['expression_name'] = re.sub('_[Aa]lignment$',
                                                   expression_suffix,
                                                   alignment_object_name)
            else:  # assume user specified suffix
                params['expression_name'] = alignment_object_name+expression_suffix
        if re.match('^KBaseRNASeq.RNASeqAlignmentSet-\d*', alignment_object_type):
            if re.match('.*_[Aa]lignment_[Ss]et$', alignment_object_name):
                # set expression set name
                params['expression_set_name'] = re.sub('_[Aa]lignment_[Ss]et$',
                                                       expression_set_suffix,
                                                       alignment_object_name)
            else:  # assume user specified suffix
                params['expression_set_name'] = alignment_object_name + expression_set_suffix
        if re.match('^KBaseSets.ReadsAlignmentSet-\d*', alignment_object_type):
            if re.match('.*_[Aa]lignment_[Ss]et$', alignment_object_name):

                # set expression set name
                params['expression_set_name'] = re.sub('_[Aa]lignment_[Ss]et$',
                                                       expression_set_suffix,
                                                       alignment_object_name)
            else:  # assume user specified suffix
                params['expression_set_name'] = alignment_object_name + expression_set_suffix

    def _save_expression_matrix(self, expressionset_ref, workspace_name):
        """
        _save_expression_matrix: save FPKM and TPM ExpressionMatrix
        """

        log('start saving ExpressionMatrix object')

        expression_set_name = self.ws.get_object_info([{"ref": expressionset_ref}],
                                                      includeMetadata=None)[0][1]

        output_obj_name_prefix = re.sub('_*[Ee]xpression_*[Ss]et',
                                        '',
                                        expression_set_name)

        upload_expression_matrix_params = {'expressionset_ref': expressionset_ref,
                                           'output_obj_name': output_obj_name_prefix,
                                           'workspace_name': workspace_name}

        expression_matrix_refs = self.eu.get_expressionMatrix(upload_expression_matrix_params)

        return expression_matrix_refs

    def run_cufflinks_app(self, params):
        log('--->\nrunning CufflinksUtil.run_cufflinks_app\n' +
            'params:\n{}'.format(json.dumps(params, indent=1)))

        self._validate_run_cufflinks_params(params)

        alignment_object_ref = params.get('alignment_object_ref')
        alignment_object_info = self.ws.get_object_info3({
            "objects": [{"ref": alignment_object_ref}]})['infos'][0]

        alignment_object_type = alignment_object_info[2]
        alignment_object_name = alignment_object_info[1]

        # get output object name
        self._generate_output_object_name(params, alignment_object_type, alignment_object_name)

        log('--->\nalignment object type: \n' +
            '{}'.format(alignment_object_type))

        if re.match('^KBaseRNASeq.RNASeqAlignment-\d*', alignment_object_type):
            params.update({'alignment_ref': alignment_object_ref})
            returnVal = self._process_rnaseq_alignment_object(params)
            report_output = self._generate_report(returnVal.get('expression_obj_ref'),
                                                  params.get('workspace_name'),
                                                  returnVal.get('result_directory'))
            returnVal.update(report_output)
        elif re.match('^KBaseRNASeq.RNASeqAlignmentSet-\d*', alignment_object_type) or \
             re.match('^KBaseSets.ReadsAlignmentSet-\d*', alignment_object_type):
            params.update({'alignment_set_ref': alignment_object_ref})
            returnVal = self._process_alignment_set_object(params, alignment_object_type)
            expression_matrix_refs = self._save_expression_matrix(returnVal['expression_obj_ref'],
                                                                  params.get('workspace_name'))
            returnVal.update(expression_matrix_refs)

            report_output = self._generate_report(returnVal['expression_obj_ref'],
                                                  params.get('workspace_name'),
                                                  returnVal['result_directory'],
                                                  expression_matrix_refs['exprMatrix_FPKM_ref'],
                                                  expression_matrix_refs['exprMatrix_TPM_ref'])
            returnVal.update(report_output)
        else:
            raise ValueError('None RNASeqAlignment type\nObject info:\n{}'.format(
                alignment_object_info))

        return returnVal
