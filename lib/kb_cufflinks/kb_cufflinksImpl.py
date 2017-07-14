# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import json
import logging
import time
import sys
from core import script_utils
from core.cuffdiff import CuffDiff



from kb_cufflinks.core.cufflinks_utils import CufflinksUtils
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
    GIT_COMMIT_HASH = "f3496194d465131a7e05a81dd48b315f4b20cf2d"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']
        if 'workspace-url' in config:
            self.__WS_URL = config['workspace-url']
        if 'shock-url' in config:
            self.__SHOCK_URL = config['shock-url']
        if 'handle-service-url' in config:
            self.__HS_URL = config['handle-service-url']
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
           parameter "workspace_name" of String, parameter
           "alignment_object_ref" of String, parameter "genome_ref" of
           String, parameter "num_threads" of Long, parameter
           "min-intron-length" of Long, parameter "max-intron-length" of
           Long, parameter "overhang-tolerance" of Long
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
           object output_obj_name             -   name of the differential
           expression matrix set output object) -> structure: parameter
           "expressionset_ref" of type "obj_ref" (An X/Y/Z style reference),
           parameter "workspace_name" of String, parameter "output_obj_name"
           of String, parameter "library_norm_method" of String, parameter
           "multi_read_correct" of type "boolean" (A boolean - 0 for false, 1
           for true. @range (0, 1)), parameter "time_series" of type
           "boolean" (A boolean - 0 for false, 1 for true. @range (0, 1)),
           parameter "min_alignment_count" of Long
        :returns: instance of type "CuffdiffResult" -> structure: parameter
           "result_directory" of String, parameter "diffExprMatrixSet_ref" of
           type "obj_ref" (An X/Y/Z style reference), parameter "report_name"
           of String, parameter "report_ref" of String
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
