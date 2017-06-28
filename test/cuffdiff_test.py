# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import inspect
import requests
import shutil
from datetime import datetime
from string import Template

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
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
        #authServiceUrlAllowInsecure = cls.cfg['auth_service_url_allow_insecure']
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

    def check_files(self, new_dir, orig_dir):

        self.assertEqual(len(os.listdir(new_dir)),
                         len(os.listdir(orig_dir)))

        for new_file in os.listdir(new_dir):
            new_file_path = os.path.join(new_dir, new_file)
            orig_file_path = os.path.join(orig_dir, new_file)

            self.assertEqual(self.getSize(new_file_path), self.getSize(orig_file_path))
            self.assertEqual(self.md5(new_file_path), self.md5(orig_file_path))

            print("Files checked: " + new_file_path + ', ' + orig_file_path)

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_cuffdiff_success(self):
        """
        Input object: downsized_AT_reads_tophat_AlignmentSet_cufflinks_ExpressionSet (4389/46/1)
        Expected output object: downsized_AT_reads_cuffdiff_output (4389/48/1)
        Files in output object should be the same as in expected output object
        """
        input_obj_ref = '4389/18/2'
        expected_obj_ref = '4389/48/1'

        params = {'expressionset_ref': input_obj_ref,
                  'workspace_name': self.getWsName(),
                  'diff_expression_obj_name': 'test_output_diffexp',
                  'filtered_expression_matrix_name': 'test_output_expmatrix',
                  'library_norm_method': 'geometric'
                  }

        retVal = self.getImpl().run_Cuffdiff(self.ctx, params)[0]

        inputObj = self.dfu.get_objects(
            {'object_refs': [input_obj_ref]})['data'][0]

        print("============ INPUT EXPRESSION SET OBJECT ==============")
        pprint(inputObj)
        print("==========================================================")

        outputObj = self.dfu.get_objects(
            {'object_refs': [retVal.get('diff_expression_obj_ref')]})['data'][0]

        print("============ DIFFERENTIAL EXPRESSION OUTPUT ==============")
        pprint(outputObj)
        print("==========================================================")

        self.assertEqual(outputObj['info'][2].startswith('KBaseRNASeq.RNASeqDifferentialExpression'), True)
        inputData = inputObj['data']
        outputData = outputObj['data']
        self.assertEqual(outputData['genome_id'], inputData['genome_id'])
        self.assertEqual(outputData['expressionSet_id'], input_obj_ref)
        self.assertEqual(outputData['alignmentSet_id'], inputData['alignmentSet_id'])
        self.assertEqual(outputData['sampleset_id'], inputData['sampleset_id'])

        outputFile = outputData['file']
        output_dir = retVal['result_directory']
        output_zipfile = os.path.split(output_dir)[1] + '.zip'
        self.assertEqual(outputFile['file_name'], output_zipfile)

        """
        Get files from expected object ref
        """
        '''
        timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * 1000)
        expected_dir = os.path.join(self.scratch, 'expected_' + str(timestamp))
        os.mkdir(expected_dir)

        expectedObj = self.dfu.get_objects(
            {'object_refs': [expected_obj_ref]})['data'][0]
        expectedFile = expectedObj['data']['file']
        expectedFile_ret = self.dfu.shock_to_file({
                                                   'shock_id': expectedFile['id'],
                                                   'file_path': expected_dir,
                                                   'unpack': 'unpack'
                                                   })
        self.check_files(output_dir, expected_dir)
        '''

    '''
    def test_no_workspace_param(self):

        self.run_error(
            [{'expressionset_ref': '5264/2/2'}], 'workspace_name parameter is required')

    def test_no_workspace_name(self):

        self.run_error(
            [{'libfile_library': 'foo'}], 'workspace_name parameter is required', wsname='None')

    def test_bad_workspace_name(self):

        self.run_error([{'libfile_library': 'foo'}], 'Invalid workspace name bad|name',
                       wsname='bad|name')

    def test_non_extant_workspace(self):

        self.run_error(
            [{'libfile_library': 'foo'}], 'Object foo cannot be accessed: No workspace with name ' +
                                          'Ireallyhopethisworkspacedoesntexistorthistestwillfail exists',
            wsname='Ireallyhopethisworkspacedoesntexistorthistestwillfail',
            exception=WorkspaceError)

    def test_no_libs_param(self):

        self.run_error(None, 'libfile_args parameter is required')

    def test_non_extant_lib(self):

        self.run_error(
            [{'libfile_library': 'foo'}],
            ('No object with name foo exists in workspace {} ' +
             '(name {})').format(str(self.wsinfo[0]), self.wsinfo[1]),
            exception=WorkspaceError)

    def test_no_libs(self):

        self.run_error([], 'At least one reads library must be provided')

    def test_no_output_param(self):

        self.run_error(
            [{'libfile_library': 'foo'}], 'output_contigset_name parameter is required',
            output_name=None)

    def test_invalid_min_contig(self):

        self.run_error(
            [{'libfile_library': 'foo'}], 'min_contig must be of type int', wsname='fake', output_name='test-output',
            min_contig_len='not an int!')

    def run_error(self, params, error, exception=ValueError):

        test_name = inspect.stack()[1][3]
        print('\n***** starting expected fail test: ' + test_name + ' *****')

        with self.assertRaises(exception) as context:
            self.getImpl().run_cuffdiff(self.ctx, params[0])
        self.assertEqual(error, str(context.exception.message))
    '''

