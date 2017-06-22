import logging
import os
import subprocess
import traceback
from zipfile import ZipFile
from os import listdir
from os.path import isfile, join
from DataFileUtil.DataFileUtilClient import DataFileUtil
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil
import contig_id_mapping as c_mapping


'''
A utility python module containing a set of methods necessary for this kbase
module.
'''

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}


def create_logger(log_dir,name):
    """Create a logger

    args: name (str): name of logger

    returns: logger (obj): logging.Logger instance
    """
    logger = logging.getLogger(name)
    fmt = logging.Formatter('%(asctime)s - %(process)d - %(name)s - '
                            ' %(levelname)s -%(message)s')
    hdl = logging.FileHandler(os.path.join(log_dir,name+'.log'))
    hdl.setFormatter(fmt)

    logger.addHandler(hdl)

    return logger

def if_obj_exists(logger,ws_client,ws_id,o_type,obj_l):
    obj_list = ws_client.list_objects( {"workspaces" : [ws_id ] ,"type" : o_type,'showHidden' : 1})
    obj_names = [i[1] for i in obj_list]
    existing_names = [i for i in obj_l if i in obj_names]
    obj_ids = None
    if len(existing_names) != 0:
        e_queries = [{'name' : j , 'workspace' : ws_id } for j in existing_names]
        e_infos = ws_client.get_object_info_new({"objects": e_queries })
	obj_ids =[ (str(k[1]) , (str(k[6]) + '/' + str(k[0]) + '/' + str(k[4])) ) for k in e_infos]
    return obj_ids

def log(message, level=logging.INFO, logger=None):
    if logger is None:
        if level == logging.DEBUG:
            print('\nDEBUG: ' + message + '\n')
        elif level == logging.INFO:
            print('\nINFO: ' + message + '\n')
        elif level == logging.WARNING:
            print('\nWARNING: ' + message + '\n')
        elif level == logging.ERROR:
            print('\nERROR: ' + message + '\n')
        elif level == logging.CRITICAL:
            print('\nCRITICAL: ' + message + '\n')
    else:
        logger.log(level, '\n' + message + '\n')

def zip_files(logger, src_path, output_fn):
    """
    Compress all index files (not directory) into an output zip file on disk.
    """

    files = [ f for f in listdir(src_path) if isfile(join(src_path,f)) ]
    with ZipFile(output_fn, 'w', allowZip64=True) as izip:
        for f in files:
            izip.write(join(src_path,f),f)

def unzip_files(logger, src_fn, dst_path):
    """
    Extract all index files into an output zip file on disk.
    """

    with ZipFile(src_fn, 'r') as ozip:
        ozip.extractall(dst_path)


def whereis(program):
    """
    returns path of program if it exists in your ``$PATH`` variable or `
    `None`` otherwise
    """
    for path in os.environ.get('PATH', '').split(':'):
        if os.path.exists(os.path.join(path, program)) and not os.path.isdir(
                os.path.join(path, program)):
            return os.path.join(path, program)
    return None


def runProgram(logger=None,
               progName=None,
               argStr=None,
               script_dir=None,
               working_dir=None):
    """
    Convenience func to handle calling and monitoring output of external programs.

    :param progName: name of system program command
    :param argStr: string containing command line options for ``progName``

    :returns: subprocess.communicate object
    """

    # Ensure program is callable.
    if script_dir is not None:
        progPath = os.path.join(script_dir, progName)
    else:
        progPath = progName
    progPath = whereis(progName)
    if not progPath:
        raise RuntimeError(
            None,
            '{0} command not found in your PATH environmental variable. {1}'.format(
                progName,
                os.environ.get(
                    'PATH',
                    '')))

    # Construct shell command
    cmdStr = "%s %s" % (progPath, argStr)
    print "Executing : " + cmdStr
    if logger is not None:
        logger.info("Executing : " + cmdStr)
    # if working_dir is None:
        logger.info("Executing: " + cmdStr + " on cwd")
    else:
        logger.info("Executing: " + cmdStr + " on " + working_dir)

    # Set up process obj
    process = subprocess.Popen(cmdStr,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               cwd=working_dir)
    # Get results
    result, stderr = process.communicate()
    # print result
    # print stderr
    # keep this until your code is stable for easier debugging
    if logger is not None and result is not None and len(result) > 0:
        logger.info(result)
    else:
        print result
    if logger is not None and stderr is not None and len(stderr) > 0:
        logger.info(stderr)
    else:
        print stderr

    # Check returncode for success/failure
    if process.returncode != 0:
        raise Exception("Command execution failed  {0}".format(
            "".join(traceback.format_exc())))
        raise RuntimeError(
            'Return Code : {0} , result {1} , progName {2}'.format(
                process.returncode, result, progName))

    # Return result
    return {"result": result, "stderr": stderr}


def check_sys_stat(logger):
    check_disk_space(logger)
    check_memory_usage(logger)
    check_cpu_usage(logger)


def check_disk_space(logger):
    runProgram(logger=logger, progName="df", argStr="-h")


def check_memory_usage(logger):
    runProgram(logger=logger, progName="vmstat", argStr="-s")


def check_cpu_usage(logger):
    runProgram(logger=logger, progName="mpstat", argStr="-P ALL")

def download_file_from_shock(logger,
                             shock_service_url = None,
                             shock_id = None,
                             filename = None,
                             directory = None,
			     filesize= None,
                             token = None):
    """
    Given a SHOCK instance URL and a SHOCK node id, download the contents of that node
    to a file on disk.
    """

    if filename is not None:
        shockFileName = filename

    if directory is not None:
        filePath = os.path.join(directory, shockFileName)
    else:
        filePath = shockFileName

    #shock_service_url is from config
    dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'], token=token)
    return dfu.shock_to_file({"shock_id" : shock_id, "file_path":filePath, "unpack" : None})


def ws_get_ref(logger, ws_client, ws_id, obj_id):
    if '/' in obj_id:
        return obj_id
    else:
        info = ws_client.get_object_info_new({"objects": [{'name': obj_id, 'workspace': ws_id}]})[0]
        return "{0}/{1}/{2}".format(info[6],info[0],info[4])


def check_and_download_existing_handle_obj(logger, ws_client, urls, ws_id, ws_object_name,
                                           ws_obj_type, directory, token):
    try:
        obj_id = ws_get_ref(logger, ws_client, ws_id, ws_object_name)
    except Exception, e:
        return None

    logger.info("Object {0} exists".format(obj_id))
    obj_info = ws_client.get_objects([{'ref': obj_id}])[0]
    handle_id = obj_info['data']['handle']['id']
    handle_name = obj_info['data']['handle']['file_name']
    try:
        download_file_from_shock(logger, shock_service_url=urls['shock_service_url'],
                                 shock_id=handle_id, filename=handle_name, directory=directory,
                                 token=token)
        file_path = os.path.join(directory, handle_name)
    except Exception, e:
        raise Exception("Unable to download shock file, {0}".format(handle_name))
    return file_path

def create_gtf_annotation_from_genome(logger,ws_client,hs_client,urls,ws_id,genome_ref,genome_name,directory,token):
    ref = ws_client.get_object_subset(
                                     [{ 'ref' : genome_ref ,'included': ['contigset_ref', 'assembly_ref']}])
    if 'contigset_ref' in ref[0]['data']:
        contig_id = ref[0]['data']['contigset_ref']
    elif 'assembly_ref' in ref[0]['data']:
        contig_id = ref[0]['data']['assembly_ref']
    if contig_id is None:
        raise ValueError("Genome {0} object does not have reference to the assembly object".format(genome_name))
    print contig_id
    logger.info( "Generating GFF file from Genome")
    try:
                assembly = AssemblyUtil(urls['callback_url'])
                ret = assembly.get_assembly_as_fasta({'ref':contig_id})
                output_file = ret['path']
                mapping_filename = c_mapping.create_sanitized_contig_ids(output_file)
                os.remove(output_file)
                ## get the GFF
                genome = GenomeFileUtil(urls['callback_url'])
                ret = genome.genome_to_gff({'genome_ref':genome_ref})
                file_path = ret['file_path']
                c_mapping.replace_gff_contig_ids(file_path, mapping_filename, to_modified=True)
                gtf_ext = ".gtf"
                if not file_path.endswith(gtf_ext):
                        gtf_path = os.path.join(directory,genome_name+".gtf")
                        gtf_cmd = " -E {0} -T -o {1}".format(file_path,gtf_path)
                        try:
                                   logger.info("Executing: gffread {0}".format(gtf_cmd))
                                   cmdline_output = runProgram(logger,"/opt/cufflinks/gffread",gtf_cmd,None,directory)
                        except Exception as e:
                                   raise Exception("Error Converting the GFF file to GTF using gffread {0},{1}".format(gtf_cmd,"".join(traceback.format_exc())))
                else:
                        logger.info("GTF handled by GAU")
                        gtf_path = file_path
                logger.info("gtf file : " + gtf_path)
                if os.path.exists(gtf_path):
                               annotation_handle = hs_client.upload(gtf_path)
                               a_handle = { "handle" : annotation_handle ,"size" : os.path.getsize(gtf_path), 'genome_id' : genome_ref}
                ##Saving GFF/GTF annotation to the workspace
                res= ws_client.save_objects(
                                        {"workspace":ws_id,
                                         "objects": [{
                                         "type":"KBaseRNASeq.GFFAnnotation",
                                         "data":a_handle,
                                         "name":genome_name+"_GTF_Annotation",
                                         "hidden":1}
                                        ]})
    except Exception as e:
                raise ValueError("Generating GTF file from Genome Annotation object Failed :  {}".format("".join(traceback.format_exc())))
    return gtf_path


def upload_file_to_shock(logger,
                         filePath,
                         make_handle=True,
                         shock_service_url=None,
                         # attributes = '{}',
                         ssl_verify=True,
                         token=None):
    """
    Use HTTP multi-part POST to save a file to a SHOCK instance.
    """

    # shock_service_url is from config
    dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'], token=token)
    # return dfu.file_to_shock({"file_path":filePath, "attributes": json.dumps(attributes), "make_handle" : make_handle})
    return dfu.file_to_shock({"file_path": filePath, "make_handle": make_handle})