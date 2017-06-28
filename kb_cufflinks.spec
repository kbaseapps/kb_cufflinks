/*
A KBase module: kb_cufflinks
*/

module kb_cufflinks {

    /* A boolean - 0 for false, 1 for true.
	  @range (0, 1)
	*/
	typedef int boolean;

	/* An X/Y/Z style reference
    */
    typedef string obj_ref;

	typedef structure{
        string      result_directory;
        obj_ref     expression_obj_ref;
        string      report_name;
        string      report_ref;
    } CufflinksResult;

	typedef structure{
		string workspace_name;
		string alignment_object_ref;
		string genome_ref;
		int num_threads;
		/*string library-type; */
		/*string library-norm-method; */
		int min-intron-length;
		int max-intron-length;
		int overhang-tolerance;
	} CufflinksParams;

    async funcdef run_cufflinks(CufflinksParams params)
		returns (CufflinksResult) authentication required;

    /*
        Required input parameters for run_Cuffdiff.

        expressionset_ref           -   reference for an expressionset object
        workspace_name              -   workspace name to save the differential expression output object
        diff_expression_obj_name    -   name of the differential expression output object
    */

	typedef structure{
        obj_ref     expressionset_ref;
        string      workspace_name;
        string      diff_expression_obj_name;

        string      filtered_expression_matrix_name; /* Optional - name of the filtered
                                                        expression matrix output object  */
        string      library_norm_method;    /* Optional */
        boolean     multi_read_correct;     /* Optional */
        boolean     time_series;            /* Optional */
        int         min_alignment_count;    /* Optional */

    } CuffdiffInput;

    typedef structure{
        string      result_directory;
        obj_ref     diff_expression_obj_ref;
        obj_ref     filtered_expression_matrix_ref;
        string      report_name;
        string      report_ref;
    } CuffdiffResult;

    funcdef run_Cuffdiff(CuffdiffInput params)
        returns (CuffdiffResult returnVal) authentication required;
};

