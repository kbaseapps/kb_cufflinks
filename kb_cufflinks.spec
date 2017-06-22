/*
A KBase module: kb_cufflinks
*/

module kb_cufflinks {

    /* A boolean - 0 for false, 1 for true.
	  @range (0, 1)
	*/
	typedef int boolean;

	/*
		 Object for Report type
	*/
	typedef structure {
		string report_name;
		string report_ref;
	} ResultsToReport;

	typedef structure{
		string ws_id;
		string sample_alignment;
		int num_threads;
		/*string library-type; */
		/*string library-norm-method; */
		int min-intron-length;
		int max-intron-length;
		int overhang-tolerance;
	} CufflinksParams;

    async funcdef CufflinksCall(CufflinksParams params)
		returns (ResultsToReport) authentication required;


    typedef string obj_ref;

    /*
        Required input parameters for run_Cuffdiff.

        expressionset_ref           -   reference for an expressionset object
        workspace_name              -   workspace name to save the differential expression output object
        diff_expression_obj_name    -   name of the differential expression output object
        filtered_expression_matrix_name - name of the filtered expression matrix output object
    */

	typedef structure{
        obj_ref     expressionset_ref;
        string      workspace_name;
        string      diff_expression_obj_name;
        string      filtered_expression_matrix_name;

        string      library_norm_method;    /* Optional */
        boolean     multi_read_correct;     /* Optional */
        boolean     time_series;
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

