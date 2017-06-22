# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests
import shutil
from string import Template
from datetime import datetime
from readsAlignmentUtils.readsAlignmentUtilsClient import ReadsAlignmentUtils
from subprocess import call

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from kb_cufflinks.kb_cufflinksImpl import kb_cufflinks
from kb_cufflinks.kb_cufflinksServer import MethodContext
from kb_cufflinks.authclient import KBaseAuth as _KBaseAuth
from biokbase.workspace.client import Workspace as Workspace


class CufflinksTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)

        for nameval in config.items('kb_cufflinks'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        authServiceUrlAllowInsecure = cls.cfg['auth-service-url-allow-insecure']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_cufflinks',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(url=cls.wsURL, token=token)
        cls.serviceImpl = kb_cufflinks(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

        '''
        input_meta_data_filename = '/kb/module/test/metadata/cufflinks_input.json'

        with open(input_meta_data_filename,'r') as infile:
            input_meta_data = json.load(infile)

        # update workspace name in input.json files and write to work dir
        ws_id_t = Template(input_meta_data['params'][0]['ws_id'])
        cls.wsName = ws_id_t.substitute(user_id=user_id)

        print('workspace_name: ' + cls.wsName)

        # create workspace that is local to the user if it does not exist
        cls.ws = Workspace(url=cls.wsURL, token=token)

        try:
            cls.ws.undelete_workspace({'workspace': cls.wsName})
            print('reusing old workspace...')
        except:
            ws_info = cls.ws.get_workspace_info({'workspace': cls.wsName})
            print("creating new workspace: " + str(ws_info))
        '''
        #except:
        #    ws_info = cls.ws.create_workspace(
        #        {'workspace': cls.wsName, 'description': 'Workspace for ' + str(
        #            input_meta_data['method'])})
        #    print("Created new workspace: " + str(ws_info))



    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')



    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_kb_cufflinks_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx


    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_cufflinks(self):
        '''
        params = {'destination_ref': self.getWsName() + '/test_alignment',
                  'file_path': '/kb/module/test/data/accepted_hits.bam',
                  'validate': 'True',
                  'read_library_ref': self.getWsName() + '/intbasic', # a dummy value that is not being used by cufflinks
                  'assembly_or_genome_ref': self.getWsName() + '/test_assembly', # a dummy value that is not being used by cufflinks
                  'condition': 'test_condition'
                 }

        print('>>>>>>>>>>>>>>>>>>>>>>params: ' + str(params))

        rau = ReadsAlignmentUtils(self.__class__.callback_url, token=self.getContext()['token'], service_ver='dev')
        ref = rau.upload_alignment(self.getContext(), params)[0]

        print('>>>>>>>>>>>>>>>>>>>>>>ref: '+str(ref))
        '''
        

        params = {
  	"ws_id": "KBaseRNASeq_test_arfath",
	"alignmentset_id" : "downsized_AT_reads_hisat2_AlignmentSet",
    "min-intron-length" : 50,
	"max-intron-length" : 300000,
    "overhang-tolerance" : 8,
    "num_threads": 1
	}

        out = self.getImpl().CufflinksCall(self.ctx, params)[0]


        # print error code of Implementation

        expression_set = self.__class__.wsClient.get_objects([
            {'workspace': params['ws_id'],
             'name': out[1]}])

        self.assertEqual('KBaseRNASeq.RNASeqExpression-6.0',
                         expression_set[0]['info'][2],
                         "output expression set object type did not match")



        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        pass
