import time
import os
import uuid
import errno
import traceback
import script_utils

class CuffMerge:

    def __init__(self, config, logger=None):
        self.config = config
        self.logger = logger

    def run_cuffmerge(self, directory, num_threads, gtf_file, list_file):
        self.logger.info("Running cuffmerge")
        print "Args passed {0},{1},{2},{3}".format(directory,
                                                   num_threads,
                                                   gtf_file,
                                                   list_file)
        cuffmerge_command = " -p {0} -o {1} -g {2} {3}".format(str(num_threads),
                                                               directory,
                                                               gtf_file,
                                                               list_file)
        merged_gtf = None
        try:
            # logger.info("Executing: cuffmerge {0}".format(cuffmerge_command))
            print  "Executing: cuffmerge {0}".format(cuffmerge_command)
            r, e = script_utils.runProgram(self.logger,
                                          "cuffmerge",
                                          cuffmerge_command,
                                          None)
            print r + "\n" + e
            if os.path.exists(directory + "/merged.gtf"):
                merged_gtf = os.path.join(directory, "merged.gtf")
        except Exception, e:
            print "".join(traceback.format_exc())
            raise Exception(
                "Error executing cuffmerge {0},{1}".format(cuffmerge_command,
                                                           "".join(traceback.format_exc())))
        return merged_gtf
