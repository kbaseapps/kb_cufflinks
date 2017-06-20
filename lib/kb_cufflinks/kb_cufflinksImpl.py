# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import logging
import time
import sys
from core import script_utils
from core import handler_utils
from biokbase.workspace.client import Workspace
try:
    from biokbase.HandleService.Client import HandleService
except:
    from biokbase.AbstractHandle.Client import AbstractHandle as HandleService
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
    GIT_COMMIT_HASH = "496b9f2c05220bb9625db21ee8914f1106205713"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        print('>>>>>>>>>>>>>'+str(config))
        if 'auth-service-url' in config:
              self.__AUTH_SERVICE_URL = config['auth-service-url']
        if 'max_cores' in config:
              self.__MAX_CORES= int(config['max_cores'])
        if 'workspace-url' in config:
              self.__WS_URL = config['workspace-url']
        if 'shock-url' in config:
              self.__SHOCK_URL = config['shock-url']
        if 'handle-service-url' in config:
              self.__HS_URL = config['handle-service-url']
        if 'temp_dir' in config:
              self.__TEMP_DIR = config['temp_dir']
        if 'scratch' in config:
              self.__SCRATCH= config['scratch']
              #print self.__SCRATCH
        if 'svc_user' in config:
              self.__SVC_USER = config['svc_user']
        if 'svc_pass' in config:
              self.__SVC_PASS = config['svc_pass']
        if 'scripts_dir' in config:
              self.__SCRIPTS_DIR = config['scripts_dir']
        #if 'rscripts' in config:
        #      self.__RSCRIPTS_DIR = config['rscripts_dir']
        if 'force_shock_node_2b_public' in config: # expect 'true' or 'false' string
              self.__PUBLIC_SHOCK_NODE = config['force_shock_node_2b_public']
        self.__CALLBACK_URL = os.environ['SDK_CALLBACK_URL']

        self.__SERVICES = { 'workspace_service_url' : self.__WS_URL,
                            'shock_service_url'     : self.__SHOCK_URL,
                            'handle_service_url'    : self.__HS_URL,
                            'callback_url'          : self.__CALLBACK_URL }
        # logging
        self.__LOGGER = logging.getLogger('KBaseRNASeq')
        if 'log_level' in config:
              self.__LOGGER.setLevel(config['log_level'])
        else:
              self.__LOGGER.setLevel(logging.INFO)
        streamHandler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s")
        formatter.converter = time.gmtime
        streamHandler.setFormatter(formatter)
        self.__LOGGER.addHandler(streamHandler)
        self.__LOGGER.info("Logger was set")

        script_utils.check_sys_stat(self.__LOGGER)
        #END_CONSTRUCTOR
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
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN CufflinksCall
        #END CufflinksCall

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method CufflinksCall return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def run_Cuffdiff(self, ctx, params):
        """
        :param params: instance of type "CuffdiffParams" -> structure:
           parameter "ws_id" of String, parameter "rnaseq_exp_details" of
           type "RNASeqSampleSet" -> structure: parameter "sampleset_id" of
           String, parameter "sampleset_desc" of String, parameter "domain"
           of String, parameter "platform" of String, parameter "num_samples"
           of Long, parameter "num_replicates" of Long, parameter
           "sample_ids" of list of String, parameter "condition" of list of
           String, parameter "source" of String, parameter "Library_type" of
           String, parameter "publication_Id" of String, parameter
           "external_source_date" of String, parameter "output_obj_name" of
           String, parameter "time-series" of String, parameter
           "library-type" of String, parameter "library-norm-method" of
           String, parameter "multi-read-correct" of String, parameter
           "min-alignment-count" of Long, parameter "dispersion-method" of
           String, parameter "no-js-tests" of String, parameter
           "frag-len-mean" of Long, parameter "frag-len-std-dev" of Long,
           parameter "max-mle-iterations" of Long, parameter
           "compatible-hits-norm" of String, parameter "no-length-correction"
           of String
        :returns: instance of type "RNASeqDifferentialExpression" (Result of
           run_CuffDiff Object RNASeqDifferentialExpression file structure
           @optional tool_opts tool_version sample_ids comments) ->
           structure: parameter "tool_used" of String, parameter
           "tool_version" of String, parameter "tool_opts" of list of mapping
           from String to String, parameter "file" of type "Handle"
           (@optional hid file_name type url remote_md5 remote_sha1) ->
           structure: parameter "hid" of type "HandleId" (Input parameters
           and output for run_cuffdiff), parameter "file_name" of String,
           parameter "id" of String, parameter "type" of String, parameter
           "url" of String, parameter "remote_md5" of String, parameter
           "remote_sha1" of String, parameter "sample_ids" of list of String,
           parameter "condition" of list of String, parameter "genome_id" of
           String, parameter "expressionSet_id" of type
           "ws_expressionSet_id", parameter "alignmentSet_id" of type
           "ws_alignmentSet_id", parameter "sampleset_id" of type
           "ws_Sampleset_id", parameter "comments" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN run_Cuffdiff
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
