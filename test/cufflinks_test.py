# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import shutil
from string import Template
from readsAlignmentUtils.readsAlignmentUtilsClient import ReadsAlignmentUtils
from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil
from ReadsUtils.ReadsUtilsClient import ReadsUtils

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

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

        # upload genbank file
        print('uploading genbank file to workspace...')
        INPUT_DATA_DIR = "/kb/module/test/data/"
        TMP_INPUT_DATA_DIR = "/kb/module/work/tmp/"
        genbank_file_name = 'at_chrom1_section.gbk'
        genbank_data_path = os.path.join(INPUT_DATA_DIR, genbank_file_name)

        print('input data path: ' + genbank_data_path)
        
        # data has to be copied to tmp dir so it can be seen by
        # GenomeFileUtil subjob running in a separate docker container
        tmp_genbank_data_path = os.path.join(TMP_INPUT_DATA_DIR, genbank_file_name)
        shutil.copy(genbank_data_path, tmp_genbank_data_path)

        genbankToGenomeParams = {"file": {"path": tmp_genbank_data_path},
                                 "genome_name": "at_chrom1_section",
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
        reads_file_name = 'extracted_hy5_rep1.fastq'

        reads_data_path = os.path.join(INPUT_DATA_DIR, reads_file_name)
        tmp_reads_data_path = os.path.join(TMP_INPUT_DATA_DIR, reads_file_name)
        shutil.copy(reads_data_path, tmp_reads_data_path)
        print('input data path: ' + reads_data_path)
        result = ru.upload_reads({"fwd_file": tmp_reads_data_path,
                                  "sequencing_tech": "Illumina",
                                  "wsname": cls.wsName,
                                  "name": reads_file_name})
        print('reads upload save result: ' + str(result))

        '''
        # data has to be copied to tmp dir so it can be seen by
        # ReadsAlignmentUtils subjob running in a separate docker container
        shutil.copy('/kb/module/test/data/WT1_alignment.bam', '/kb/module/work/tmp')



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

        # upload alignment file
        params = {
                  'destination_ref': self.getWsName() + '/WT1_alignment.bam',
                  'file_path': '/kb/module/work/tmp/WT1_alignment.bam',
                  'validate': 'True',
                  'read_library_ref': self.getWsName() + '/extracted_hy5_rep1.fastq',
                  'assembly_or_genome_ref': self.getWsName() + '/at_chrom1_section',
                  'condition': 'test_condition'
                 }

        rau = ReadsAlignmentUtils(url=self.__class__.callback_url, token=self.getContext()['token'], service_ver='dev')
        ref = rau.upload_alignment(params=params)

        params = {
            "ws_id": "Cufflinks_test_arfath",
            "sample_alignment_ref" : "WT1_alignment.bam",
            "genome_ref" : "at_chrom1_section",
            "min-intron-length" : 50,
            "max-intron-length" : 300000,
            "overhang-tolerance" : 8,
            "num_threads": 1
	    }

        out = self.getImpl().CufflinksCall(self.ctx, params)[0]

        print('>>>>>>>>>>>>>>>>out: '+str(out))

        expression_set = self.__class__.wsClient.get_objects([
            {'workspace': params['ws_id'],
             'name': out['expression_ref']}])

        self.assertEqual('KBaseRNASeq.RNASeqExpression-6.0',
                         expression_set[0]['info'][2],
                         "output expression set object type did not match")
