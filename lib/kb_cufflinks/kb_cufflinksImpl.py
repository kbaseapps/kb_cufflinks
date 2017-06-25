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
    GIT_URL = "git@github.com:arfathpasha/kb_cufflinks.git"
    GIT_COMMIT_HASH = "5e6b610482771ffc58a3e258c753f62aaa2355a0"

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


    def run_cufflinks(self, ctx, params):
        """
        :param params: instance of type "CufflinksParams" -> structure:
           parameter "ws_id" of String, parameter "sample_alignment_ref" of
           String, parameter "genome_ref" of String, parameter "num_threads"
           of Long, parameter "min-intron-length" of Long, parameter
           "max-intron-length" of Long, parameter "overhang-tolerance" of Long
        :returns: instance of type "CufflinksResult" -> structure: parameter
           "result_directory" of String, parameter "expression_obj_ref" of
           type "obj_ref" (An X/Y/Z style reference), parameter "report_name"
           of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN run_cufflinks
        #END run_cufflinks

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method run_cufflinks return value ' +
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
           "expressionset_ref" of type "obj_ref" (An X/Y/Z style reference),
           parameter "workspace_name" of String, parameter
           "diff_expression_obj_name" of String, parameter
           "filtered_expression_matrix_name" of String, parameter
           "library_norm_method" of String, parameter "multi_read_correct" of
           type "boolean" (A boolean - 0 for false, 1 for true. @range (0,
           1)), parameter "time_series" of type "boolean" (A boolean - 0 for
           false, 1 for true. @range (0, 1)), parameter "min_alignment_count"
           of Long
        :returns: instance of type "CuffdiffResult" -> structure: parameter
           "result_directory" of String, parameter "diff_expression_obj_ref"
           of type "obj_ref" (An X/Y/Z style reference), parameter
           "filtered_expression_matrix_ref" of type "obj_ref" (An X/Y/Z style
           reference), parameter "report_name" of String, parameter
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
