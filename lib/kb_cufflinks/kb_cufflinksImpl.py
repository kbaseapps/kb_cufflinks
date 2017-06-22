# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import logging
import time
import sys
import json
from core import script_utils
from core import handler_utils
import os
import logging
import time
import sys
import json
import traceback
from core import script_utils
from core.cuffdiff import CuffDiff

from biokbase.workspace.client import Workspace
#try:
#from biokbase.HandleService.Client import HandleService
#except BaseException:
#    from biokbase.AbstractHandle.Client import AbstractHandle as HandleService

from kb_cufflinks.core.cufflinks_utils import CufflinksUtils
from pprint import pprint
from DataFileUtil.DataFileUtilClient import DataFileUtil
#END_HEADER


class kb_cufflinks:
    '''
    Module Name:
    kb_cufflinks

    Module Description:
    A KBase module: kb_cufflinks
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/kbaseapps/kb_cufflinks.git"
    GIT_COMMIT_HASH = "e756992b9f3b7fe29eb051358d7872253d2c2646"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        if 'auth-service-url' in config:
            self.__AUTH_SERVICE_URL = config['auth-service-url']
        if 'max_cores' in config:
            self.__MAX_CORES = int(config['max_cores'])
        if 'workspace-url' in config:
            self.__WS_URL = config['workspace-url']
        if 'shock-url' in config:
            self.__SHOCK_URL = config['shock-url']
        if 'handle-service-url' in config:
            self.__HS_URL = config['handle-service-url']
        if 'temp_dir' in config:
            self.__TEMP_DIR = config['temp_dir']
        if 'scratch' in config:
            self.__SCRATCH = config['scratch']
            # print self.__SCRATCH
        if 'svc_user' in config:
            self.__SVC_USER = config['svc_user']
        if 'svc_pass' in config:
            self.__SVC_PASS = config['svc_pass']
        if 'scripts_dir' in config:
            self.__SCRIPTS_DIR = config['scripts_dir']
        # if 'rscripts' in config:
        #      self.__RSCRIPTS_DIR = config['rscripts_dir']
        if 'force_shock_node_2b_public' in config:  # expect 'true' or 'false' string
            self.__PUBLIC_SHOCK_NODE = config['force_shock_node_2b_public']
        self.__CALLBACK_URL = os.environ['SDK_CALLBACK_URL']

        self.__SERVICES = {'workspace_service_url': self.__WS_URL,
                           'shock_service_url': self.__SHOCK_URL,
                           'handle_service_url': self.__HS_URL,
                           'callback_url': self.__CALLBACK_URL}
        # logging
        self.__LOGGER = logging.getLogger('KBaseRNASeq')
        if 'log_level' in config:
            self.__LOGGER.setLevel(config['log_level'])
        else:
            self.__LOGGER.setLevel(logging.INFO)
        streamHandler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s")
        formatter.converter = time.gmtime
        streamHandler.setFormatter(formatter)
        self.__LOGGER.addHandler(streamHandler)
        self.__LOGGER.info("Logger was set")

        script_utils.check_sys_stat(self.__LOGGER)
        self.cuffdiff_runner = CuffDiff(config, self.__SERVICES, self.__LOGGER)
        #END_CONSTRUCTOR
        pass


    def CufflinksCall(self, ctx, params):
        """
        :param params: instance of type "CufflinksParams" -> structure:
           parameter "ws_id" of String, parameter "sample_alignment_ref" of
           String, parameter "genome_ref" of String, parameter "num_threads"
           of Long, parameter "min-intron-length" of Long, parameter
           "max-intron-length" of Long, parameter "overhang-tolerance" of Long
        :returns: instance of type "ResultsToReport" (Object for Report type)
           -> structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN CufflinksCall
        print '--->\nRunning kb_cufflinks.CufflinksCall\nparams:'
        print json.dumps(params, indent=1)

        if 'num_threads' not in params:
            params['num_threads'] = 1

        for key, value in params.iteritems():
            if isinstance(value, basestring):
                params[key] = value.strip()

        if not os.path.exists(self.__SCRATCH): os.makedirs(self.__SCRATCH)
        cufflinks_dir = os.path.join(self.__SCRATCH, "tmp")
        handler_utils.setupWorkingDir(self.__LOGGER, cufflinks_dir)
        # Set the common Params
        common_params = {'ws_client': Workspace(url=self.__WS_URL, token=ctx['token']),
#                         'hs_client': HandleService(url=self.__HS_URL, token=ctx['token']),
                         'dfu' : DataFileUtil(self.__CALLBACK_URL),
                         'user_token': ctx['token']
                         }

        # for quick testing, we recover parameters here
        ws_client = common_params['ws_client']
        #hs = common_params['hs_client']
        dfu = common_params['dfu']
        token = common_params['user_token']
        try:
            ################################################################
            sample_alignment_info = ws_client.get_object_info_new({"objects":
                                                                  [{'name': params[
                                                                      'sample_alignment_ref'],
                                                                    'workspace': params[
                                                                        'ws_id']}]})[0]
            print('alignment_info:')
            pprint(sample_alignment_info)

            genome_info = ws_client.get_object_info_new({"objects":
                                                                  [{'name': params[
                                                                      'genome_ref'],
                                                                    'workspace': params[
                                                                        'ws_id']}]})[0]
            print('genome_info:')
            pprint(genome_info)
            sample_alignment_id = str(sample_alignment_info[6]) + '/' + str(
                sample_alignment_info[0]) + '/' + str(
                sample_alignment_info[4])
            sample_name = str(sample_alignment_info[1])
            print('sample_alignemnt_id: ' + str(sample_alignment_id))
            genome_id = str(genome_info[6]) + '/' + str(
                genome_info[0]) + '/' + str(
                genome_info[4])
            genome_name = str(genome_info[1])
            ###################################################################
            '''
            a_sampleset = ws_client.get_objects(
                [{'name': params['alignmentset_id'], 'workspace': params['ws_id']}])[0]

            a_sampleset_info = ws_client.get_object_info_new({"objects":
                                                                  [{'name': params[
                                                                      'alignmentset_id'],
                                                                    'workspace': params[
                                                                        'ws_id']}]})[0]
            '''
        except Exception, e:
            self.__LOGGER.exception("".join(traceback.format_exc()))
            raise Exception("Error Downloading objects from the workspace ")
        # read_sample_id']
        ### Check if the gtf file exists in the workspace. if exists download the file from that
        #genome_id = a_sampleset['data']['genome_id']
        #genome_name = ws_client.get_object_info([{"ref": genome_id}], includeMetadata=None)[0][1]


        ws_gtf = genome_name + "_GTF_Annotation"
        gtf_file = script_utils.check_and_download_existing_handle_obj(self.__LOGGER, ws_client, self.__SERVICES,
                                                                       params['ws_id'], ws_gtf,
                                                                       "KBaseRNASeq.GFFAnnotation",
                                                                       cufflinks_dir, token)
        if gtf_file is None:
            script_utils.create_gtf_annotation_from_genome(self.__LOGGER, ws_client, dfu, self.__SERVICES,
                                                           params['ws_id'], genome_id, genome_name,
                                                           cufflinks_dir, token)
        gtf_info = ws_client.get_object_info_new(
            {"objects": [{'name': ws_gtf, 'workspace': params['ws_id']}]})[0]
        gtf_id = str(gtf_info[6]) + '/' + str(gtf_info[0]) + '/' + str(gtf_info[4])

        #self.tool_opts = {k: str(v) for k, v in params.iteritems() if
        #                  not k in ('ws_id', 'alignmentset_id', 'num_threads') and v is not None}
        #alignment_ids = a_sampleset['data']['sample_alignments']
        #m_alignment_names = a_sampleset['data']['mapped_rnaseq_alignments']
        #self.sampleset_id = a_sampleset['data']['sampleset_id']
        ### Get List of Alignments Names
        #self.align_names = []
        #for d_align in m_alignment_names:
        #    for i, j in d_align.items():
        #        self.align_names.append(j)

        #m_alignment_ids = a_sampleset['data']['mapped_alignments_ids']
        #self.num_jobs = len(alignment_ids)
        #if self.num_jobs < 2:
        #    raise ValueError(
        #        "Please ensure you have atleast 2 alignments to run cufflinks in Set mode")

        #self.__LOGGER.info(" Number of threads used by each process {0}".format(params['num_threads']))
        #count = 0

        #self.task_list = []

        #for i in m_alignment_ids:
        #    for sample_name, alignment_id in i.items():
        task_params = {'job_id': sample_alignment_id,
                              'gtf_file': gtf_file,
                              'ws_id': params['ws_id'],
                              'genome_id': genome_id,
                              'cufflinks_dir': cufflinks_dir,
                              'annotation_id': gtf_id,
                              'sample_id': sample_name
                              }
        #        self.task_list.append(task_param)
        #        count = count + 1

        #task_params = self.task_list[0]

        cufflinks_runner = CufflinksUtils(self.config, self.__LOGGER, cufflinks_dir,
                                          self.__SERVICES)
        returnVal = cufflinks_runner.run_cufflinks_app(params, common_params, task_params)

        return [returnVal]
        #END CufflinksCall

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method CufflinksCall return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def run_Cuffdiff(self, ctx, params):
        """
        :param params: instance of type "CuffdiffInput" (Required input
           parameters for run_Cuffdiff. expressionset_ref           -  
           reference for an expressionset object workspace_name             
           -   workspace name to save the differential expression output
           object diff_expression_obj_name    -   name of the differential
           expression output object) -> structure: parameter
           "expressionset_ref" of type "obj_ref", parameter "workspace_name"
           of String, parameter "diff_expression_obj_name" of String,
           parameter "filtered_expression_matrix_name" of String, parameter
           "library_norm_method" of String, parameter "multi_read_correct" of
           type "boolean" (A boolean - 0 for false, 1 for true. @range (0,
           1)), parameter "time_series" of type "boolean" (A boolean - 0 for
           false, 1 for true. @range (0, 1)), parameter "min_alignment_count"
           of Long
        :returns: instance of type "CuffdiffResult" -> structure: parameter
           "result_directory" of String, parameter "diff_expression_obj_ref"
           of type "obj_ref", parameter "filtered_expression_matrix_ref" of
           type "obj_ref", parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN run_Cuffdiff
        print("In Run Cuffdiff")
        returnVal = self.cuffdiff_runner.run_cuffdiff(params)
        #END run_Cuffdiff

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method run_Cuffdiff return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
