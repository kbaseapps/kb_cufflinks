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
};

