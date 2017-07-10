# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import time

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except BaseException:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from DataFileUtil.DataFileUtilClient import DataFileUtil
from kb_cufflinks.kb_cufflinksImpl import kb_cufflinks
from kb_cufflinks.kb_cufflinksServer import MethodContext
from kb_cufflinks.authclient import KBaseAuth as _KBaseAuth


class kb_cufflinksTest(unittest.TestCase):

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
        # authServiceUrlAllowInsecure = cls.cfg['auth_service_url_allow_insecure']
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
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = kb_cufflinks(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        cls.dfu = DataFileUtil(cls.callback_url)

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
    def test_cuffdiff_success(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods

        params = {'expressionset_ref': '22254/32/1',
                  'workspace_name': self.getWsName(),
                  'diff_expression_obj_name': 'test_output_diffexp',
                  'filtered_expression_matrix_name': 'test_output_expmatrix',
                  'library_norm_method': 'geometric'
                  }

        retVal = self.getImpl().run_Cuffdiff(self.ctx, params)[0]

        inputObj = self.dfu.get_objects(
            {'object_refs': [retVal.get('diff_expression_obj_ref')]})['data'][0]

        obj = self.dfu.get_objects(
            {'object_refs': [retVal.get('diff_expression_obj_ref')]})['data'][0]

        print("============ DIFFERENTIAL EXPRESSION OUTPUT ==============")
        pprint(obj)
        print("==========================================================")

        self.assertEqual(obj['info'][2].startswith(
            'KBaseRNASeq.RNASeqDifferentialExpression'), True)
        d = obj['data']
        self.assertEqual(d['genome_id'], inputObj['data']['genome_id'])
        self.assertEqual(d['expressionSet_id'], inputObj['data']['expressionSet_id'])
        self.assertEqual(d['alignmentSet_id'], inputObj['data']['alignmentSet_id'])
        self.assertEqual(d['sampleset_id'], inputObj['data']['sampleset_id'])

        f = d['file']
        result_dir = retVal['result_directory']
        result_file = os.path.split(result_dir)[1] + '.zip'
        self.assertEqual(f['file_name'], result_file)
