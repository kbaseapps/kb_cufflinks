# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import logging
import time
import sys
import json
from core import script_utils
from core.cuffdiff import CuffDiff
from core.cufflinks_utils import CufflinksUtils

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
    GIT_COMMIT_HASH = "f7497b4d27a60a806f3ea60c55c783fb0e21c934"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']
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
        print '--->\nRunning kb_cufflinks.run_cufflinks\nparams:'
        print json.dumps(params, indent=1)

        for key, value in params.iteritems():
            if isinstance(value, basestring):
                params[key] = value.strip()

        cufflinks_runner = CufflinksUtils(self.config)
        returnVal = cufflinks_runner.run_cufflinks_app(params)

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method run_cufflinks return value ' +
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
