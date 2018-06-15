import csv
import os
from collections import namedtuple
from datetime import datetime
from pprint import pprint

new_col_names = ['gene_id', 'log2_fold_change', 'p_value', 'q_value']
delimiter = '\t'


def get_max_fold_change_to_handle_inf(infile):
    maxvalue = 0
    with open(infile) as source:
        rdr = csv.DictReader(source, dialect='excel-tab')
        for line in rdr:
            log2fc_val = line.get('log2_fold_change')
            if not 'inf' in str(log2fc_val):
                log2fc = abs(float(log2fc_val))
                if log2fc > maxvalue:
                    maxvalue = log2fc

        print('maxvalue: ', maxvalue)
        return maxvalue


def handle_max_fold_change(infile):
    outfile = infile + '_fc'
    outfile_obj = open(outfile, 'wb')

    max_value = get_max_fold_change_to_handle_inf(infile)
    with open(infile, 'rb') as source:
        rdr = csv.DictReader(source, delimiter=delimiter)
        csv_wtr = csv.DictWriter(outfile_obj, delimiter='\t', fieldnames=new_col_names)
        csv_wtr.writerow(dict((cn, cn) for cn in new_col_names))

        for row in rdr:

            log2fc_val = row.get('log2_fold_change')
            # print 'FC_VAL: ', log2fc_val
            if '-inf' in str(log2fc_val):
                row['log2_fold_change'] = -float(max_value)
            elif 'inf' in str(log2fc_val):
                row['log2_fold_change'] = float(max_value)
            elif 'nan' in str(log2fc_val):
                row['log2_fold_change'] = 'None'

            csv_wtr.writerow(row)

    outfile_obj.close()
    return outfile


def process_cuffdiff_file(diffexpr_filepath, scratch, transcripts=False):
    cuffdiff_col_names = ['gene',
                          'log2(fold_change)',
                          'p_value',
                          'q_value']

    ConditionPair = namedtuple("ConditionPair", ["condition1", "condition2"])
    FileInfo = namedtuple('FileInfo', ['file_path', 'file_obj'])

    condPair_fileInfo = {}

    timestamp = str(int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * 1000))
    with open(diffexpr_filepath, 'rb') as source:
        rdr = csv.DictReader(source, dialect='excel-tab')
        """
        save the files opened for writing in outfiles list, so they can be closed later
        """
        outfiles = list()
        if transcripts:
            reader = csv.DictReader(open(transcripts), dialect='excel-tab')
            trans_ids = {r['tracking_id']: r['nearest_ref_id'] for r in reader}

        for r in rdr:
            c1 = r['sample_1']
            c2 = r['sample_2']
            if transcripts:
                r['gene'] = trans_ids[r['test_id']]
                # strip out transcripts w/o a transcript
                if r['gene'] == "-":
                    continue

            cond_pair = ConditionPair(condition1=c1,
                                      condition2=c2)
            tsv_file_info = condPair_fileInfo.get(cond_pair, None)
            if tsv_file_info is None:
                tsv_file_name = timestamp + '_' + c1 + '~~' + c2
                tsv_file_path = os.path.join(scratch, tsv_file_name)
                outfile = open(tsv_file_path, 'wb')
                outfiles.append(outfile)
                csv_wtr = csv.DictWriter(outfile, delimiter='\t', fieldnames=new_col_names)
                csv_wtr.writerow(dict((cn, cn) for cn in new_col_names))
                tsv_file_info = FileInfo(file_path=tsv_file_path,
                                         file_obj=csv_wtr)
                condPair_fileInfo[cond_pair] = tsv_file_info

            wtr = tsv_file_info.file_obj
            col_vals = [r[v] for v in cuffdiff_col_names]
            wtr.writerow(dict(zip(new_col_names, col_vals)))

        for ofile in outfiles:
            ofile.close()

        diff_expr_files = list()

        for cond_pair, file_info in condPair_fileInfo.iteritems():
            print('Cond_pair: ', cond_pair)
            print('File: ', file_info.file_path)
            tsv_file = file_info.file_path

            new_tsv_file = handle_max_fold_change(tsv_file)

            file_entry = dict()
            file_entry['condition_mapping'] = {cond_pair.condition1: cond_pair.condition2}
            file_entry['diffexpr_filepath'] = new_tsv_file

            diff_expr_files.append(file_entry)

        print('===================  DIFF EXPR FILES ======================================')
        pprint(diff_expr_files)
        print('===================  END DIFF EXPR FILES ==================================')

        return diff_expr_files
