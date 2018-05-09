# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import time
import hashlib
import inspect
import requests
import shutil
import zipfile
import glob
from datetime import datetime
from string import Template

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except BaseException:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil
from ReadsUtils.ReadsUtilsClient import ReadsUtils
from ReadsAlignmentUtils.ReadsAlignmentUtilsClient import ReadsAlignmentUtils
from DataFileUtil.DataFileUtilClient import DataFileUtil
from DifferentialExpressionUtils.DifferentialExpressionUtilsClient import DifferentialExpressionUtils
from kb_cufflinks.kb_cufflinksImpl import kb_cufflinks
from kb_cufflinks.kb_cufflinksServer import MethodContext
from kb_cufflinks.authclient import KBaseAuth as _KBaseAuth

class CuffdiffTest(unittest.TestCase):

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
        cls.gfu = GenomeFileUtil(cls.callback_url)
        cls.dfu = DataFileUtil(cls.callback_url)
        cls.ru = ReadsUtils(cls.callback_url)
        cls.rau = ReadsAlignmentUtils(cls.callback_url)
        cls.deu = DifferentialExpressionUtils(cls.callback_url, service_ver='beta')
        suffix = int(time.time() * 1000)
        cls.wsName = "test_cuffdiff_" + str(suffix)
        cls.wsClient.create_workspace({'workspace': cls.wsName})
        cls.upload_genome()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        return self.__class__.wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    @classmethod
    def upload_genome(cls):
        # upload genome object

        genbank_file_name = 'minimal.gbff'
        genbank_file_path = os.path.join(cls.scratch, genbank_file_name)
        shutil.copy(os.path.join('data', genbank_file_name), genbank_file_path)

        genome_object_name = 'test_Genome'
        cls.genome_ref = cls.gfu.genbank_to_genome({'file': {'path': genbank_file_path},
                                                    'workspace_name': cls.wsName,
                                                    'genome_name': genome_object_name,
                                                    'generate_missing_genes': 1,
                                                    'generate_ids_if_needed': 1,
                                                    })['genome_ref']
    @classmethod
    def prepare_data(cls):

        # upload reads object
        reads_file_name = 'Sample1.fastq'
        reads_file_path = os.path.join(cls.scratch, reads_file_name)
        shutil.copy(os.path.join('data', reads_file_name), reads_file_path)

        reads_object_name_1 = 'test_Reads_1'
        cls.reads_ref_1 = cls.ru.upload_reads({'fwd_file': reads_file_path,
                                               'wsname': cls.wsName,
                                               'sequencing_tech': 'Unknown',
                                               'interleaved': 0,
                                               'name': reads_object_name_1
                                               })['obj_ref']

        reads_object_name_2 = 'test_Reads_2'
        cls.reads_ref_2 = cls.ru.upload_reads({'fwd_file': reads_file_path,
                                               'wsname': cls.wsName,
                                               'sequencing_tech': 'Unknown',
                                               'interleaved': 0,
                                               'name': reads_object_name_2
                                               })['obj_ref']

        reads_object_name_3 = 'test_Reads_3'
        cls.reads_ref_3 = cls.ru.upload_reads({'fwd_file': reads_file_path,
                                               'wsname': cls.wsName,
                                               'sequencing_tech': 'Unknown',
                                               'interleaved': 0,
                                               'name': reads_object_name_3
                                               })['obj_ref']
        # upload alignment object
        alignment_file_name = 'accepted_hits.bam'
        # alignment_file_name = 'Ath_WT_R1.fastq.sorted.bam'
        alignment_file_path = os.path.join(cls.scratch, alignment_file_name)
        shutil.copy(os.path.join('data', alignment_file_name), alignment_file_path)

        alignment_object_name_1 = 'test_Alignment_1'
        cls.condition_1 = 'test_condition_1'
        cls.alignment_ref_1 = cls.rau.upload_alignment(
            {'file_path': alignment_file_path,
             'destination_ref': cls.wsName + '/' + alignment_object_name_1,
             'read_library_ref': cls.reads_ref_1,
             'condition': cls.condition_1,
             'library_type': 'single_end',
             'assembly_or_genome_ref': cls.genome_ref
             })['obj_ref']

        alignment_object_name_2 = 'test_Alignment_2'
        cls.condition_2 = 'test_condition_2'
        cls.alignment_ref_2 = cls.rau.upload_alignment(
            {'file_path': alignment_file_path,
             'destination_ref': cls.wsName + '/' + alignment_object_name_2,
             'read_library_ref': cls.reads_ref_2,
             'condition': cls.condition_2,
             'library_type': 'single_end',
             'assembly_or_genome_ref': cls.genome_ref
             })['obj_ref']

        alignment_object_name_3 = 'test_Alignment_3'
        cls.condition_3 = 'test_condition_3'
        cls.alignment_ref_3 = cls.rau.upload_alignment(
            {'file_path': alignment_file_path,
             'destination_ref': cls.wsName + '/' + alignment_object_name_3,
             'read_library_ref': cls.reads_ref_3,
             'condition': cls.condition_3,
             'library_type': 'single_end',
             'assembly_or_genome_ref': cls.genome_ref,
             'library_type': 'single_end'
             })['obj_ref']

        # upload sample_set object
        workspace_id = cls.dfu.ws_name_to_id(cls.wsName)
        sample_set_object_name = 'test_Sample_Set'
        sample_set_data = {
            'sampleset_id': sample_set_object_name,
            'sampleset_desc': 'test sampleset object',
            'Library_type': 'SingleEnd',
            'condition': [cls.condition_1, cls.condition_2, cls.condition_3],
            'sample_ids': [cls.reads_ref_1, cls.reads_ref_2, cls.reads_ref_3],
            'domain': 'Unknown',
            'num_samples': 3,
            'platform': 'Unknown'}
        save_object_params = {
            'id': workspace_id,
            'objects': [{
                'type': 'KBaseRNASeq.RNASeqSampleSet',
                'data': sample_set_data,
                'name': sample_set_object_name
            }]
        }

        dfu_oi = cls.dfu.save_objects(save_object_params)[0]
        cls.sample_set_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

        # upload alignment_set object
        object_type = 'KBaseRNASeq.RNASeqAlignmentSet'
        alignment_set_object_name = 'test_Alignment_Set'
        alignment_set_data = {
            'genome_id': cls.genome_ref,
            'read_sample_ids': [reads_object_name_1,
                                reads_object_name_2,
                                reads_object_name_3],
            'mapped_rnaseq_alignments': [{reads_object_name_1: alignment_object_name_1},
                                         {reads_object_name_2: alignment_object_name_2},
                                         {reads_object_name_3: alignment_object_name_3}],
            'mapped_alignments_ids': [{reads_object_name_1: cls.alignment_ref_1},
                                      {reads_object_name_2: cls.alignment_ref_2},
                                      {reads_object_name_3: cls.alignment_ref_3}],
            'sample_alignments': [cls.alignment_ref_1,
                                  cls.alignment_ref_2,
                                  cls.alignment_ref_3],
            'sampleset_id': cls.sample_set_ref}
        save_object_params = {
            'id': workspace_id,
            'objects': [{
                'type': object_type,
                'data': alignment_set_data,
                'name': alignment_set_object_name
            }]
        }

        dfu_oi = cls.dfu.save_objects(save_object_params)[0]
        cls.alignment_rnaseq_set_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

    @classmethod
    def getSize(cls, filename):
        return os.path.getsize(filename)

    @classmethod
    def md5(cls, filename):
        with open(filename, 'rb') as file_:
            hash_md5 = hashlib.md5()
            buf = file_.read(65536)
            while len(buf) > 0:
                hash_md5.update(buf)
                buf = file_.read(65536)
            return hash_md5.hexdigest()

    def check_files(self, new_dir, orig_dir):

        self.assertEqual(len(os.listdir(new_dir)),
                         len(os.listdir(orig_dir)))

        for new_file in os.listdir(new_dir):

            new_file_path = os.path.join(new_dir, new_file)
            orig_file_path = os.path.join(orig_dir, new_file)

            if not zipfile.is_zipfile(new_file_path):
                print
                print("%%%%%%%%%%%%%%%%%%%% new_file_path: ", new_file_path)
                print("%%%%%%%%%%%%%%%%%%% orig_file_path: ", orig_file_path)

                if self.getSize(new_file_path) != self.getSize(orig_file_path):
                    print('************** sizes differ ************')
                if self.md5(new_file_path) != self.md5(orig_file_path):
                    print('************** md5s differ **************')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def cuffdiff_success(self, input_exprset_ref, output_obj_name, expected_obj_ref=None, expected_dir=None):

        test_name = inspect.stack()[1][3]
        print('\n*** starting expected cuffdiff success test: ' + test_name + ' **********************')

        params = {'expressionset_ref': input_exprset_ref,
                  'workspace_name': self.getWsName(),
                  'output_obj_name': output_obj_name,
                  'library_norm_method': 'classic-fpkm',
                  'library_type': 'fr-unstranded'
                  }

        cuffdiff_retVal = self.getImpl().run_Cuffdiff(self.ctx, params)[0]

        inputObj = self.dfu.get_objects(
            {'object_refs': [input_exprset_ref]})['data'][0]

        output_dir = cuffdiff_retVal.get('destination_dir')

        print("============ INPUT EXPRESSION SET OBJECT ==============")
        pprint(inputObj)
        print("==========================================================")

        outputObj = self.dfu.get_objects(
            {'object_refs': [cuffdiff_retVal.get('diffExprMatrixSet_ref')]})['data'][0]

        print("============ OUTPUT FROM CUFFDIFF ==============")
        pprint(cuffdiff_retVal)
        print("============ DIFFERENTIAL EXPRESSION MATRIX SET OUTPUT ==============")
        pprint(outputObj)
        print("==========================================================")

        """
        Get files from expected object ref
        """
        if expected_obj_ref is not None:
            timestamp = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * 1000)
            expected_dir = os.path.join(self.scratch, 'expected_' + str(timestamp))
            os.mkdir(expected_dir)

            expected_obj = self.dfu.get_objects(
                {'object_refs': [expected_obj_ref]})['data'][0]
            expected_file = expected_obj['data']['file']
            expected_file_ret = self.dfu.shock_to_file({
                'shock_id': expected_file['id'],
                'file_path': expected_dir,
                'unpack': 'unpack'
            })
            for f in glob.glob(expected_dir + '/*.zip'):
                os.remove(f)

        if expected_dir is not None:
            self.check_files(output_dir, expected_dir)

    # Following test uses object refs from a narrative. Comment the next line to run the test
    @unittest.skip("skipped test_cuffdiff_RNASeq_exprset_success")
    def test_cuffdiff_narrative_rnaseq_exprset_success(self):
        """
        Input object: downsized_AT_reads_tophat_AlignmentSet_cufflinks_ExpressionSet (4389/45/1)
        Expected output object: downsized_AT_tophat_cufflinks_cuffdiff_output (4389/58/1)
        Files in output object should be the same as in expected output object
        """
        narrative_rnaseq_exprset_ref = '4389/45/1'
        narrative_expected_obj_ref = '4389/58/1'
        #narrative_rnaseq_exprset_ref = '6743/48/2'

        appdev_three_by_two_diffexpr_matrixset_obj_ref = '5264/17/1'
        appdev_three_by_two_diffexpr_matrixset_obj_name = 'three_by_two_diffexp_output'

        self.cuffdiff_success(narrative_rnaseq_exprset_ref,
                              'narrative_rnaseq_exprset_cuffdiff_output',
                              expected_obj_ref=narrative_expected_obj_ref)


    @unittest.skip("skipped test_cuffdiff_narrative_setapi_exprset_success")
    def test_cuffdiff_narrative_setapi_exprset_success(self):

        narrarive_setapi_exprset_ref = '2409/348/1'

        self.cuffdiff_success(narrarive_setapi_exprset_ref,
                              'narrative_setapi_exprset_cuffdiff_output')

    @unittest.skip("skipped test_cuffdiff_created_setapi_exprset_success")
    def test_cuffdiff_created_setapi_exprset_success(self):

        self.prepare_data()
        # upload expression_set object
        params = {
            "workspace_name": self.wsName,
            "alignment_object_ref": self.alignment_rnaseq_set_ref,
            "genome_ref": self.genome_ref,
            "min-intron-length": 50,
            "max-intron-length": 300000,
            "overhang-tolerance": 8,
            "num_threads": 2
        }
        cufflinks_retval = self.getImpl().run_cufflinks(self.ctx, params)[0]

        self.cuffdiff_success(cufflinks_retval.get('expression_obj_ref'),
                              'created_setapi_exprset_cuffdiff_output')

    def cuffdiff_fail(self, params, error, exception=ValueError, do_startswith=False):

        test_name = inspect.stack()[1][3]
        print('\n*** starting expected cuffdiff fail test: ' + test_name + ' **********************')

        with self.assertRaises(exception) as context:
            self.getImpl().run_Cuffdiff(self.ctx, params)
        if do_startswith:
            self.assertTrue(str(context.exception.message).startswith(error),
                            "Error message {} does not start with {}".format(
                                str(context.exception.message),
                                error))
        else:
            self.assertEqual(error, str(context.exception.message))

    def test_cuffdiff_fail_no_ws_name(self):
        self.cuffdiff_fail(
                        {
                         'expressionset_ref': '1/1/1',
                         'output_obj_name': 'test_createdExprSet'
                         },
            '"workspace_name" parameter is required, but missing')

    def test_cuffdiff_fail_no_obj_name(self):
        self.cuffdiff_fail(
                        {
                         'workspace_name': self.getWsName(),
                         'expressionset_ref': '1/1/1'
                         },
            '"output_obj_name" parameter is required, but missing')

    def test_cuffdiff_fail_no_exprset_ref(self):
        self.cuffdiff_fail(
                        {
                         'workspace_name': self.getWsName(),
                         'output_obj_name': 'test_createdExprSet'
                         },
            '"expressionset_ref" parameter is required, but missing')

    def test_cuffdiff_fail_bad_wsname(self):
        self.cuffdiff_fail(
                        {
                         'workspace_name': '&bad',
                         'expressionset_ref': '1/1/1',
                         'output_obj_name': 'test_createdExprSet'
                         },
            'Illegal character in workspace name &bad: &')

    def test_cuffdiff_fail_non_existant_wsname(self):
        self.cuffdiff_fail(
                        {
                         'workspace_name': '1s',
                         'expressionset_ref': '1/1/1',
                         'output_obj_name': 'test_createdExprSet'
                         },
            'No workspace with name 1s exists')

    def test_cuffdiff_fail_non_expset_ref(self):
        self.cuffdiff_fail(
                        {
                         'workspace_name': self.getWsName(),
                         'expressionset_ref': self.genome_ref,
                         'output_obj_name': 'test_createdExprSet'
                         },
            'expressionset_ref should be of type KBaseRNASeq.RNASeqExpressionSet ' +
            'or KBaseSets.ExpressionSet', exception=TypeError)






