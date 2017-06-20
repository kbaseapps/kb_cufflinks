# -*- coding: utf-8 -*-
# BEGIN_HEADER
import os
import logging
import time
import sys
from core import script_utils
from core import handler_utils
from biokbase.workspace.client import Workspace
try:
    from biokbase.HandleService.Client import HandleService
except BaseException:
    from biokbase.AbstractHandle.Client import AbstractHandle as HandleService
# END_HEADER


class kb_cufflinks:
    '''
    Module Name:
    kb_cufflinks

    Module Description:
    A KBase module: kb_cufflinks
    '''

    # WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    # noqa
    VERSION = "0.0.1"
    GIT_URL = "git@github.com:arfathpasha/kb_cufflinks.git"
    GIT_COMMIT_HASH = "b7c78214da9b2fc65d7f6830b9180c9204c4dc9f"

    # BEGIN_CLASS_HEADER
    # END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        # BEGIN_CONSTRUCTOR
        print('>>>>>>>>>>>>>' + str(config))
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
        # END_CONSTRUCTOR
        pass

    def CufflinksCall(self, ctx, params):
        """
        :param params: instance of type "CufflinksParams" -> structure:
           parameter "ws_id" of String, parameter "sample_alignment" of
           String, parameter "num_threads" of Long, parameter
           "min-intron-length" of Long, parameter "max-intron-length" of
           Long, parameter "overhang-tolerance" of Long
        :returns: instance of type "ResultsToReport" (Object for Report type)
           -> structure: parameter "report_name" of String, parameter
           "report_ref" of String
        """
        if not os.path.exists(self.__SCRATCH):
            os.makedirs(self.__SCRATCH)
        cufflinks_dir = os.path.join(self.__SCRATCH, "tmp")
        handler_utils.setupWorkingDir(self.__LOGGER, cufflinks_dir)
        # Set the common Params
        common_params = {'ws_client': Workspace(url=self.__WS_URL, token=ctx['token']),
                         'hs_client': HandleService(url=self.__HS_URL, token=ctx['token']),
                         'user_token': ctx['token']
                         }
        # Set the Number of threads if specified
        if 'num_threads' in params and params['num_threads'] is not None:
            common_params['num_threads'] = params['num_threads']

        # Check to Call Cufflinks in Set mode or Single mode
        wsc = common_params['ws_client']
        obj_info = script_util.ws_get_obj_info(self.__LOGGER, wsc, params['ws_id'],
                                               params['alignmentset_id'])
        obj_type = obj_info[0][2].split('-')[0]
        if obj_type == 'KBaseRNASeq.RNASeqAlignmentSet':
            self.__LOGGER.info("Cufflinks AlignmentSet Case")
            sts = CufflinksSampleSet(self.__LOGGER, cufflinks_dir, self.__SERVICES,
                                     self.__MAX_CORES)
            returnVal = sts.run(common_params, params)
        else:
            sts = CufflinksSample(self.__LOGGER, cufflinks_dir, self.__SERVICES,
                                  self.__MAX_CORES)
            returnVal = sts.run(common_params, params)
        handler_util.cleanup(self.__LOGGER, cufflinks_dir)
        # END CufflinksCall

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method CufflinksCall return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def status(self, ctx):
        # BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        # END_STATUS
        return [returnVal]
