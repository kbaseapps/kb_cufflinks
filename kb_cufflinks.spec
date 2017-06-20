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

	/*
	    Input parameters and output for run_cuffdiff
	*/

	typedef string HandleId;

    typedef string ws_Sampleset_id;
	typedef string ws_alignmentSet_id;
    typedef string ws_expressionSet_id;

    /*
      @optional hid file_name type url remote_md5 remote_sha1
    */

   	typedef structure {
       		HandleId hid;
       		string file_name;
       		string id;
       		string type;
       		string url;
       		string remote_md5;
       		string remote_sha1;
   	} Handle;

    typedef structure {
        string sampleset_id;
        string sampleset_desc;
	    string domain;
        string platform;
        int num_samples;
        int num_replicates;
        list<string> sample_ids;
        list<string> condition;
        string source;
        string Library_type;
        string publication_Id;
        string external_source_date;
    } RNASeqSampleSet;

    typedef structure {
        string ws_id;
        RNASeqSampleSet rnaseq_exp_details;
        string output_obj_name;
        string time-series;
        string library-type;
        string library-norm-method;
        string multi-read-correct;
        int  min-alignment-count;
        string dispersion-method;
        string no-js-tests;
        int frag-len-mean;
        int frag-len-std-dev;
        int max-mle-iterations;
        string compatible-hits-norm;
        string no-length-correction;
    } CuffdiffParams;

    /*
    Result of run_CuffDiff
    Object RNASeqDifferentialExpression file structure
    @optional tool_opts tool_version sample_ids comments
    */
    typedef structure {
        string tool_used;
        string tool_version;
        list<mapping<string opt_name, string opt_value>> tool_opts;
        Handle file;
        list<string> sample_ids;
        list<string> condition;
        string genome_id;
        ws_expressionSet_id expressionSet_id;
        ws_alignmentSet_id alignmentSet_id;
        ws_Sampleset_id sampleset_id;
        string comments;
    } RNASeqDifferentialExpression;

    async funcdef run_Cuffdiff(CuffdiffParams params)
                      returns (RNASeqDifferentialExpression)
                      authentication required;
};

