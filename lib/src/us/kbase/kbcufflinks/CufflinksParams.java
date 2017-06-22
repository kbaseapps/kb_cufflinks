
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
 * <p>Original spec-file type: CufflinksParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "ws_id",
    "sample_alignment_ref",
    "genome_ref",
    "num_threads",
    "min-intron-length",
    "max-intron-length",
    "overhang-tolerance"
})
public class CufflinksParams {

    @JsonProperty("ws_id")
    private String wsId;
    @JsonProperty("sample_alignment_ref")
    private String sampleAlignmentRef;
    @JsonProperty("genome_ref")
    private String genomeRef;
    @JsonProperty("num_threads")
    private Long numThreads;
    @JsonProperty("min-intron-length")
    private Long minIntronLength;
    @JsonProperty("max-intron-length")
    private Long maxIntronLength;
    @JsonProperty("overhang-tolerance")
    private Long overhangTolerance;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("ws_id")
    public String getWsId() {
        return wsId;
    }

    @JsonProperty("ws_id")
    public void setWsId(String wsId) {
        this.wsId = wsId;
    }

    public CufflinksParams withWsId(String wsId) {
        this.wsId = wsId;
        return this;
    }

    @JsonProperty("sample_alignment_ref")
    public String getSampleAlignmentRef() {
        return sampleAlignmentRef;
    }

    @JsonProperty("sample_alignment_ref")
    public void setSampleAlignmentRef(String sampleAlignmentRef) {
        this.sampleAlignmentRef = sampleAlignmentRef;
    }

    public CufflinksParams withSampleAlignmentRef(String sampleAlignmentRef) {
        this.sampleAlignmentRef = sampleAlignmentRef;
        return this;
    }

    @JsonProperty("genome_ref")
    public String getGenomeRef() {
        return genomeRef;
    }

    @JsonProperty("genome_ref")
    public void setGenomeRef(String genomeRef) {
        this.genomeRef = genomeRef;
    }

    public CufflinksParams withGenomeRef(String genomeRef) {
        this.genomeRef = genomeRef;
        return this;
    }

    @JsonProperty("num_threads")
    public Long getNumThreads() {
        return numThreads;
    }

    @JsonProperty("num_threads")
    public void setNumThreads(Long numThreads) {
        this.numThreads = numThreads;
    }

    public CufflinksParams withNumThreads(Long numThreads) {
        this.numThreads = numThreads;
        return this;
    }

    @JsonProperty("min-intron-length")
    public Long getMinIntronLength() {
        return minIntronLength;
    }

    @JsonProperty("min-intron-length")
    public void setMinIntronLength(Long minIntronLength) {
        this.minIntronLength = minIntronLength;
    }

    public CufflinksParams withMinIntronLength(Long minIntronLength) {
        this.minIntronLength = minIntronLength;
        return this;
    }

    @JsonProperty("max-intron-length")
    public Long getMaxIntronLength() {
        return maxIntronLength;
    }

    @JsonProperty("max-intron-length")
    public void setMaxIntronLength(Long maxIntronLength) {
        this.maxIntronLength = maxIntronLength;
    }

    public CufflinksParams withMaxIntronLength(Long maxIntronLength) {
        this.maxIntronLength = maxIntronLength;
        return this;
    }

    @JsonProperty("overhang-tolerance")
    public Long getOverhangTolerance() {
        return overhangTolerance;
    }

    @JsonProperty("overhang-tolerance")
    public void setOverhangTolerance(Long overhangTolerance) {
        this.overhangTolerance = overhangTolerance;
    }

    public CufflinksParams withOverhangTolerance(Long overhangTolerance) {
        this.overhangTolerance = overhangTolerance;
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
        return ((((((((((((((((("CufflinksParams"+" [wsId=")+ wsId)+", sampleAlignmentRef=")+ sampleAlignmentRef)+", genomeRef=")+ genomeRef)+", numThreads=")+ numThreads)+", minIntronLength=")+ minIntronLength)+", maxIntronLength=")+ maxIntronLength)+", overhangTolerance=")+ overhangTolerance)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
