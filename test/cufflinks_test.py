# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import shutil

from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil
from ReadsUtils.ReadsUtilsClient import ReadsUtils
from ReadsAlignmentUtils.ReadsAlignmentUtilsClient import ReadsAlignmentUtils
from DataFileUtil.DataFileUtilClient import DataFileUtil

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from kb_cufflinks.core.cufflinks_utils import CufflinksUtils
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
        cls.wsClient = Workspace(url=cls.wsURL, token=token)
        cls.serviceImpl = kb_cufflinks(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

        cls.gfu = GenomeFileUtil(cls.callback_url)
        cls.dfu = DataFileUtil(cls.callback_url)
        cls.ru = ReadsUtils(cls.callback_url)
        cls.rau = ReadsAlignmentUtils(cls.callback_url, service_ver='dev')

        cls.cufflinks_runner = CufflinksUtils(cls.cfg)

        #suffix = int(time.time() * 1000)
        suffix = 1001
        cls.wsName = "test_kb_cufflinks_" + str(suffix)

        try:
            # reuse existing (previously torn down) workspace
            cls.wsClient.undelete_workspace({'workspace': cls.wsName})
            print('reusing old workspace...')
        except:
            try:
                # create if workspace does not exist
                cls.wsClient.create_workspace({'workspace': cls.wsName})
            except:
                # get workspace if it exists and was not previously deleted (previously not torn down)
                ws_info = cls.wsClient.get_workspace_info({'workspace': cls.wsName})
                print("creating new workspace: " + str(ws_info))

        cls.prepare_data()

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

        
        # upload genbank file
        print('uploading genbank file to workspace...')
        INPUT_DATA_DIR = "/kb/module/test/data/"
        TMP_INPUT_DATA_DIR = "/kb/module/work/tmp/"
        genbank_file_name = 'Atmt.gbk'
        genbank_data_path = os.path.join(INPUT_DATA_DIR, genbank_file_name)

        print('input data path: ' + genbank_data_path)
        
        # data has to be copied to tmp dir so it can be seen by
        # GenomeFileUtil subjob running in a separate docker container
        tmp_genbank_data_path = os.path.join(TMP_INPUT_DATA_DIR, genbank_file_name)
        shutil.copy(genbank_data_path, tmp_genbank_data_path)

        genbankToGenomeParams = {"file": {"path": tmp_genbank_data_path},
                                 "genome_name": "KBase_derived_Athaliana_PhytozomeV11_TAIR10",
                                 "workspace_name": cls.wsName,
                                 "source": "thale-cress",
                                 "release": "1TAIR10",
                                 "generate_ids_if_needed": True,
                                 "type": "User upload"
                                 }
        gfu = GenomeFileUtil(os.environ['SDK_CALLBACK_URL'], token=token)
        save_result = gfu.genbank_to_genome(genbankToGenomeParams)
        print('genbank_to_genome save result: ' + str(save_result))
        

        # upload downsized single reads
        ru = ReadsUtils(os.environ['SDK_CALLBACK_URL'], token=token)
        reads_file_name = 'Ath_hy5_rep1.fastq'

        reads_data_path = os.path.join(INPUT_DATA_DIR, reads_file_name)
        tmp_reads_data_path = os.path.join(TMP_INPUT_DATA_DIR, reads_file_name)
        shutil.copy(reads_data_path, tmp_reads_data_path)
        print('input data path: ' + reads_data_path)
        result = ru.upload_reads({"fwd_file": tmp_reads_data_path,
                                  "sequencing_tech": "Illumina",
                                  "wsname": cls.wsName,
                                  "name": reads_file_name})
        print('reads upload save result: ' + str(result))


        # data has to be copied to tmp dir so it can be seen by
        # ReadsAlignmentUtils subjob running in a separate docker container
        shutil.copy('/kb/module/test/data/accepted_hits.bam', '/kb/module/work/tmp')
        '''



    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    @classmethod
    def prepare_data(cls):
        # upload genome object
        genbank_file_name = 'minimal.gbff'
        #genbank_file_name = 'Atmt.gbk'
        genbank_file_path = os.path.join(cls.scratch, genbank_file_name)
        shutil.copy(os.path.join('data', genbank_file_name), genbank_file_path)

        genome_object_name = 'test_Genome'
        cls.genome_ref = cls.gfu.genbank_to_genome({'file': {'path': genbank_file_path},
                                                    'workspace_name': cls.wsName,
                                                    'genome_name': genome_object_name
                                                    })['genome_ref']

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

        # upload alignment object
        alignment_file_name = 'accepted_hits.bam'
        #alignment_file_name = 'at_accepted_hits.bam'
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

        # upload sample_set object
        workspace_id = cls.dfu.ws_name_to_id(cls.wsName)
        sample_set_object_name = 'test_Sample_Set'
        sample_set_data = {
            'sampleset_id': sample_set_object_name,
            'sampleset_desc': 'test sampleset object',
            'Library_type': 'SingleEnd',
            'condition': [cls.condition_1, cls.condition_2],
            'domain': 'Unknown',
            'num_samples': 2,
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
            'read_sample_ids': [reads_object_name_1, reads_object_name_2],
            'mapped_rnaseq_alignments': [{reads_object_name_1: alignment_object_name_1},
                                         {reads_object_name_2: alignment_object_name_2}],
            'mapped_alignments_ids': [{reads_object_name_1: cls.alignment_ref_1},
                                      {reads_object_name_2: cls.alignment_ref_2}],
            'sample_alignments': [cls.alignment_ref_1, cls.alignment_ref_2],
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
        cls.alignment_set_ref = str(dfu_oi[6]) + '/' + str(dfu_oi[0]) + '/' + str(dfu_oi[4])

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
        params = {
            "workspace_name": self.getWsName(),
            "alignment_object_ref" : self.alignment_ref_1,
            "genome_ref" : self.__class__.genome_ref,
            "min-intron-length" : 50,
            "max-intron-length" : 300000,
            "overhang-tolerance" : 8,
            "num_threads": 1
	    }

        result = self.getImpl().run_cufflinks(self.ctx, params)[0]

        self.assertTrue('result_directory' in result)
        result_files = os.listdir(result['result_directory'])
        print result_files
        expect_result_files = ['genes.fpkm_tracking', 'transcripts.gtf',
                               'isoforms.fpkm_tracking', 'skipped.gtf']
        self.assertTrue(all(x in result_files for x in expect_result_files))
        self.assertTrue('expression_obj_ref' in result)
        self.assertTrue('report_name' in result)
        self.assertTrue('report_ref' in result)
        print('>>>>expr_obj_ref: '+str(result.get('expression_obj_ref')))
        #expression_data = self.getWsClient().get_objects([{'objid': int(result.get('expression_obj_ref').split('/')[1]), 'workspace': self.__class__.wsName}])['data'][0]['data']
        #self.assertEqual(expression_data.get('genome_id'), self.genome_ref)
        #self.assertEqual(expression_data.get('condition'), self.condition_1)
        #self.assertEqual(expression_data.get('id'), 'test_cufflinks_expression_1')
