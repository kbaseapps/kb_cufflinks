
package us.kbase.kbcufflinks;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: CuffdiffParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "ws_id",
    "rnaseq_exp_details",
    "output_obj_name",
    "time-series",
    "library-type",
    "library-norm-method",
    "multi-read-correct",
    "min-alignment-count",
    "dispersion-method",
    "no-js-tests",
    "frag-len-mean",
    "frag-len-std-dev",
    "max-mle-iterations",
    "compatible-hits-norm",
    "no-length-correction"
})
public class CuffdiffParams {

    @JsonProperty("ws_id")
    private String wsId;
    /**
     * <p>Original spec-file type: RNASeqSampleSet</p>
     * 
     * 
     */
    @JsonProperty("rnaseq_exp_details")
    private RNASeqSampleSet rnaseqExpDetails;
    @JsonProperty("output_obj_name")
    private String outputObjName;
    @JsonProperty("time-series")
    private String timeSeries;
    @JsonProperty("library-type")
    private String libraryType;
    @JsonProperty("library-norm-method")
    private String libraryNormMethod;
    @JsonProperty("multi-read-correct")
    private String multiReadCorrect;
    @JsonProperty("min-alignment-count")
    private Long minAlignmentCount;
    @JsonProperty("dispersion-method")
    private String dispersionMethod;
    @JsonProperty("no-js-tests")
    private String noJsTests;
    @JsonProperty("frag-len-mean")
    private Long fragLenMean;
    @JsonProperty("frag-len-std-dev")
    private Long fragLenStdDev;
    @JsonProperty("max-mle-iterations")
    private Long maxMleIterations;
    @JsonProperty("compatible-hits-norm")
    private String compatibleHitsNorm;
    @JsonProperty("no-length-correction")
    private String noLengthCorrection;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("ws_id")
    public String getWsId() {
        return wsId;
    }

    @JsonProperty("ws_id")
    public void setWsId(String wsId) {
        this.wsId = wsId;
    }

    public CuffdiffParams withWsId(String wsId) {
        this.wsId = wsId;
        return this;
    }

    /**
     * <p>Original spec-file type: RNASeqSampleSet</p>
     * 
     * 
     */
    @JsonProperty("rnaseq_exp_details")
    public RNASeqSampleSet getRnaseqExpDetails() {
        return rnaseqExpDetails;
    }

    /**
     * <p>Original spec-file type: RNASeqSampleSet</p>
     * 
     * 
     */
    @JsonProperty("rnaseq_exp_details")
    public void setRnaseqExpDetails(RNASeqSampleSet rnaseqExpDetails) {
        this.rnaseqExpDetails = rnaseqExpDetails;
    }

    public CuffdiffParams withRnaseqExpDetails(RNASeqSampleSet rnaseqExpDetails) {
        this.rnaseqExpDetails = rnaseqExpDetails;
        return this;
    }

    @JsonProperty("output_obj_name")
    public String getOutputObjName() {
        return outputObjName;
    }

    @JsonProperty("output_obj_name")
    public void setOutputObjName(String outputObjName) {
        this.outputObjName = outputObjName;
    }

    public CuffdiffParams withOutputObjName(String outputObjName) {
        this.outputObjName = outputObjName;
        return this;
    }

    @JsonProperty("time-series")
    public String getTimeSeries() {
        return timeSeries;
    }

    @JsonProperty("time-series")
    public void setTimeSeries(String timeSeries) {
        this.timeSeries = timeSeries;
    }

    public CuffdiffParams withTimeSeries(String timeSeries) {
        this.timeSeries = timeSeries;
        return this;
    }

    @JsonProperty("library-type")
    public String getLibraryType() {
        return libraryType;
    }

    @JsonProperty("library-type")
    public void setLibraryType(String libraryType) {
        this.libraryType = libraryType;
    }

    public CuffdiffParams withLibraryType(String libraryType) {
        this.libraryType = libraryType;
        return this;
    }

    @JsonProperty("library-norm-method")
    public String getLibraryNormMethod() {
        return libraryNormMethod;
    }

    @JsonProperty("library-norm-method")
    public void setLibraryNormMethod(String libraryNormMethod) {
        this.libraryNormMethod = libraryNormMethod;
    }

    public CuffdiffParams withLibraryNormMethod(String libraryNormMethod) {
        this.libraryNormMethod = libraryNormMethod;
        return this;
    }

    @JsonProperty("multi-read-correct")
    public String getMultiReadCorrect() {
        return multiReadCorrect;
    }

    @JsonProperty("multi-read-correct")
    public void setMultiReadCorrect(String multiReadCorrect) {
        this.multiReadCorrect = multiReadCorrect;
    }

    public CuffdiffParams withMultiReadCorrect(String multiReadCorrect) {
        this.multiReadCorrect = multiReadCorrect;
        return this;
    }

    @JsonProperty("min-alignment-count")
    public Long getMinAlignmentCount() {
        return minAlignmentCount;
    }

    @JsonProperty("min-alignment-count")
    public void setMinAlignmentCount(Long minAlignmentCount) {
        this.minAlignmentCount = minAlignmentCount;
    }

    public CuffdiffParams withMinAlignmentCount(Long minAlignmentCount) {
        this.minAlignmentCount = minAlignmentCount;
        return this;
    }

    @JsonProperty("dispersion-method")
    public String getDispersionMethod() {
        return dispersionMethod;
    }

    @JsonProperty("dispersion-method")
    public void setDispersionMethod(String dispersionMethod) {
        this.dispersionMethod = dispersionMethod;
    }

    public CuffdiffParams withDispersionMethod(String dispersionMethod) {
        this.dispersionMethod = dispersionMethod;
        return this;
    }

    @JsonProperty("no-js-tests")
    public String getNoJsTests() {
        return noJsTests;
    }

    @JsonProperty("no-js-tests")
    public void setNoJsTests(String noJsTests) {
        this.noJsTests = noJsTests;
    }

    public CuffdiffParams withNoJsTests(String noJsTests) {
        this.noJsTests = noJsTests;
        return this;
    }

    @JsonProperty("frag-len-mean")
    public Long getFragLenMean() {
        return fragLenMean;
    }

    @JsonProperty("frag-len-mean")
    public void setFragLenMean(Long fragLenMean) {
        this.fragLenMean = fragLenMean;
    }

    public CuffdiffParams withFragLenMean(Long fragLenMean) {
        this.fragLenMean = fragLenMean;
        return this;
    }

    @JsonProperty("frag-len-std-dev")
    public Long getFragLenStdDev() {
        return fragLenStdDev;
    }

    @JsonProperty("frag-len-std-dev")
    public void setFragLenStdDev(Long fragLenStdDev) {
        this.fragLenStdDev = fragLenStdDev;
    }

    public CuffdiffParams withFragLenStdDev(Long fragLenStdDev) {
        this.fragLenStdDev = fragLenStdDev;
        return this;
    }

    @JsonProperty("max-mle-iterations")
    public Long getMaxMleIterations() {
        return maxMleIterations;
    }

    @JsonProperty("max-mle-iterations")
    public void setMaxMleIterations(Long maxMleIterations) {
        this.maxMleIterations = maxMleIterations;
    }

    public CuffdiffParams withMaxMleIterations(Long maxMleIterations) {
        this.maxMleIterations = maxMleIterations;
        return this;
    }

    @JsonProperty("compatible-hits-norm")
    public String getCompatibleHitsNorm() {
        return compatibleHitsNorm;
    }

    @JsonProperty("compatible-hits-norm")
    public void setCompatibleHitsNorm(String compatibleHitsNorm) {
        this.compatibleHitsNorm = compatibleHitsNorm;
    }

    public CuffdiffParams withCompatibleHitsNorm(String compatibleHitsNorm) {
        this.compatibleHitsNorm = compatibleHitsNorm;
        return this;
    }

    @JsonProperty("no-length-correction")
    public String getNoLengthCorrection() {
        return noLengthCorrection;
    }

    @JsonProperty("no-length-correction")
    public void setNoLengthCorrection(String noLengthCorrection) {
        this.noLengthCorrection = noLengthCorrection;
    }

    public CuffdiffParams withNoLengthCorrection(String noLengthCorrection) {
        this.noLengthCorrection = noLengthCorrection;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((((((((((((((((((((("CuffdiffParams"+" [wsId=")+ wsId)+", rnaseqExpDetails=")+ rnaseqExpDetails)+", outputObjName=")+ outputObjName)+", timeSeries=")+ timeSeries)+", libraryType=")+ libraryType)+", libraryNormMethod=")+ libraryNormMethod)+", multiReadCorrect=")+ multiReadCorrect)+", minAlignmentCount=")+ minAlignmentCount)+", dispersionMethod=")+ dispersionMethod)+", noJsTests=")+ noJsTests)+", fragLenMean=")+ fragLenMean)+", fragLenStdDev=")+ fragLenStdDev)+", maxMleIterations=")+ maxMleIterations)+", compatibleHitsNorm=")+ compatibleHitsNorm)+", noLengthCorrection=")+ noLengthCorrection)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
