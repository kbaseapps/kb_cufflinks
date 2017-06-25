import time
import traceback
import math
import os
import script_utils
import shutil
from pprint import pprint
import uuid
import errno

from DataFileUtil.DataFileUtilClient import DataFileUtil
from Workspace.WorkspaceClient import Workspace as Workspace
from KBaseReport.KBaseReportClient import KBaseReport
from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil
from ReadsAlignmentUtils.ReadsAlignmentUtilsClient import ReadsAlignmentUtils


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


class CufflinksUtils:
    CUFFLINKS_TOOLKIT_PATH = '/opt/cufflinks/cufflinks'
    
    def __init__(self, config):
        """
        
        :param config: 
        :param logger: 
        :param directory: Working directory 
        :param urls: Service urls
        """
        #BEGIN_CONSTRUCTOR
        self.ws_url = config["workspace-url"]
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.shock_url = config['shock-url']
        self.dfu = DataFileUtil(self.callback_url)
        self.gfu = GenomeFileUtil(self.callback_url)
        self.rau = ReadsAlignmentUtils(self.callback_url)
        self.ws = Workspace(self.ws_url, token=self.token)

        self.scratch = os.path.join(config['scratch'], str(uuid.uuid4()))
        self._mkdir_p(self.scratch)

        self.tool_used = "Cufflinks"
        self.tool_version = os.environ['VERSION']
        #END_CONSTRUCTOR
        pass

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

    def run_cufflinks_app(self, params):
        print('>>>>>>>>>>>>>>>>>came here ')
        return None
        '''
        ws_client = common_params['ws_client']
        #hs = common_params['hs_client']
        logger = self.logger
        token = common_params['user_token']

        s_alignment = task_params['job_id']
        gtf_file = task_params['gtf_file']
        directory = task_params['cufflinks_dir']
        genome_id = task_params['genome_id']
        annotation_id = task_params['annotation_id']
        sample_id = task_params['sample_id']

        ws_id = task_params['ws_id']

        print "Downloading Sample Alignment from workspace {0}".format(s_alignment)
        logger.info("Downloading Sample Alignment from workspace {0}".format(s_alignment))
        alignment_name = ws_client.get_object_info([{"ref": s_alignment}], includeMetadata=None)[0][
            1]
        if not logger:
            logger = script_utils.create_logger(directory, "run_cufflinks_" + alignment_name)
        try:
            alignment = ws_client.get_objects(
                [{'ref': s_alignment}])[0]
            input_direc = os.path.join(directory,
                                       alignment_name.split('_alignment')[0] + "_cufflinks_input")
            if not os.path.exists(input_direc): os.mkdir(input_direc)
            output_name = alignment_name.split('_alignment')[0] + "_cufflinks_expression"
            output_dir = os.path.join(directory, output_name)
            # Download Alignment from shock
            a_file_id = alignment['data']['file']['id']
            a_filename = alignment['data']['file']['file_name']
            condition = alignment['data']['condition']
            try:
                script_utils.download_file_from_shock(logger, shock_service_url=self.urls[
                    'shock_service_url'], shock_id=a_file_id, filename=a_filename,
                                                     directory=input_direc, token=token)
            except Exception, e:
                raise Exception("Unable to download shock file, {0},{1}".format(a_filename, "".join(
                    traceback.format_exc())))

            try:
                input_dir = os.path.join(input_direc, alignment_name)
                if not os.path.exists(input_dir): os.mkdir(input_dir)
                #script_utils.unzip_files(logger, os.path.join(input_direc, a_filename), input_dir)
            except Exception, e:
                raise Exception(e)
                logger.error("".join(traceback.format_exc()))
                raise Exception("Unzip alignment files  error")

            #input_file = os.path.join(input_dir, "accepted_hits.bam.bk")
            input_file = os.path.join(input_direc, a_filename)

            ### Adding advanced options to tophat command
            tool_opts = {k: str(v) for k, v in params.iteritems() if
                         not k in ('ws_id', 'num_threads') and v is not None}
            cufflinks_command = (' -p ' + str(params['num_threads']))
            if 'max_intron_length' in params and params['max_intron_length'] is not None:
                cufflinks_command += (' --max-intron-length ' + str(params['max_intron_length']))
            if 'min_intron_length' in params and params['min_intron_length'] is not None:
                cufflinks_command += (' --min-intron-length ' + str(params['min_intron_length']))
            if 'overhang_tolerance' in params and params['overhang_tolerance'] is not None:
                cufflinks_command += (' --overhang-tolerance ' + str(params['overhang_tolerance']))

            cufflinks_command += " -o {0} -G {1} {2}".format(output_dir, gtf_file, input_file)
            # cufflinks_command += " -o {0} -A {1} -G {2} {3}".format(t_file_name,g_output_file,gtf_file,input_file)
            logger.info("Executing: cufflinks {0}".format(cufflinks_command))
            print "Executing: cufflinks {0}".format(cufflinks_command)
            ret = script_utils.runProgram(logger, "/opt/cufflinks/cufflinks", cufflinks_command, None, directory)
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

            ##Parse output files
            try:
                g_output_file = os.path.join(output_dir, "genes.fpkm_tracking")
                # exp_dict = rnaseq_util.parse_FPKMtracking( g_output_file, 'Cufflinks', 'FPKM' )
                # tpm_exp_dict = script_util.parse_FPKMtracking(g_output_file,'Cufflinks','TPM')
                # Cufflinks doesn't produce TPM, we infer from FPKM
                # (see discussion @ https://www.biostars.org/p/160989/)
                exp_dict, tpm_exp_dict = parse_FPKMtracking_calc_TPM(g_output_file)
            except Exception, e:
                raise Exception(e)
                logger.exception("".join(traceback.format_exc()))
                raise Exception("Error parsing FPKMtracking")
                ##  compress and upload to shock
            try:
                logger.info("Zipping cufflinks output")
                print "Zipping cufflinks output"
                out_file_path = os.path.join(directory, "%s.zip" % output_name)
                script_utils.zip_files(logger, output_dir, out_file_path)
            except Exception, e:
                raise Exception(e)
                logger.exception("".join(traceback.format_exc()))
                raise Exception("Error executing cufflinks")
            try:
                handle = script_utils.upload_file_to_shock(logger, out_file_path)['handle']
            except Exception, e:
                raise Exception(e)
                logger.exception("".join(traceback.format_exc()))
                raise Exception("Error while zipping the output objects: {0}".format(out_file_path))
                ## Save object to workspace
            try:
                logger.info("Saving cufflinks object to workspace")
                es_obj = {'id': output_name,
                          'type': 'RNA-Seq',
                          'numerical_interpretation': 'FPKM',
                          'expression_levels': exp_dict,
                          'tpm_expression_levels': tpm_exp_dict,
                          'processing_comments': "log2 Normalized",
                          'genome_id': genome_id,
                          'annotation_id': annotation_id,
                          'condition': condition,
                          'mapped_rnaseq_alignment': {sample_id: s_alignment},
                          'tool_used': self.tool_used,
                          'tool_version': self.tool_version,
                          'tool_opts': tool_opts,
                          'file': handle
                          }

                res = ws_client.save_objects(
                    {"workspace": ws_id,
                     "objects": [{
                         "type": "KBaseRNASeq.RNASeqExpression",
                         "data": es_obj,
                         "name": output_name}
                     ]})[0]
                expr_id = str(res[6]) + '/' + str(res[0]) + '/' + str(res[4])
            except Exception, e:
                logger.exception("".join(traceback.format_exc()))
                raise Exception("Failed to upload the ExpressionSample: {0}".format(output_name))
        except Exception, e:
            logger.exception("".join(traceback.format_exc()))
            raise Exception(
                "Error executing cufflinks {0},{1}".format(cufflinks_command, directory))
        finally:
            if os.path.exists(out_file_path): os.remove(out_file_path)
            if os.path.exists(output_dir): shutil.rmtree(output_dir)
            if os.path.exists(input_direc): shutil.rmtree(input_direc)
            ret = script_utils.if_obj_exists(None, ws_client, ws_id, "KBaseRNASeq.RNASeqExpression",
                                            [output_name])
            if not ret is None:
                return (output_name, ws_id)
        return None
        '''
        
