
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
    "workspace_name",
    "alignment_object_ref",
    "expression_set_suffix",
    "expression_suffix",
    "genome_ref",
    "num_threads",
    "min_intron_length",
    "max_intron_length",
    "overhang_tolerance"
})
public class CufflinksParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("alignment_object_ref")
    private String alignmentObjectRef;
    @JsonProperty("expression_set_suffix")
    private String expressionSetSuffix;
    @JsonProperty("expression_suffix")
    private String expressionSuffix;
    @JsonProperty("genome_ref")
    private String genomeRef;
    @JsonProperty("num_threads")
    private Long numThreads;
    @JsonProperty("min_intron_length")
    private Long minIntronLength;
    @JsonProperty("max_intron_length")
    private Long maxIntronLength;
    @JsonProperty("overhang_tolerance")
    private Long overhangTolerance;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public CufflinksParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("alignment_object_ref")
    public String getAlignmentObjectRef() {
        return alignmentObjectRef;
    }

    @JsonProperty("alignment_object_ref")
    public void setAlignmentObjectRef(String alignmentObjectRef) {
        this.alignmentObjectRef = alignmentObjectRef;
    }

    public CufflinksParams withAlignmentObjectRef(String alignmentObjectRef) {
        this.alignmentObjectRef = alignmentObjectRef;
        return this;
    }

    @JsonProperty("expression_set_suffix")
    public String getExpressionSetSuffix() {
        return expressionSetSuffix;
    }

    @JsonProperty("expression_set_suffix")
    public void setExpressionSetSuffix(String expressionSetSuffix) {
        this.expressionSetSuffix = expressionSetSuffix;
    }

    public CufflinksParams withExpressionSetSuffix(String expressionSetSuffix) {
        this.expressionSetSuffix = expressionSetSuffix;
        return this;
    }

    @JsonProperty("expression_suffix")
    public String getExpressionSuffix() {
        return expressionSuffix;
    }

    @JsonProperty("expression_suffix")
    public void setExpressionSuffix(String expressionSuffix) {
        this.expressionSuffix = expressionSuffix;
    }

    public CufflinksParams withExpressionSuffix(String expressionSuffix) {
        this.expressionSuffix = expressionSuffix;
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

    @JsonProperty("min_intron_length")
    public Long getMinIntronLength() {
        return minIntronLength;
    }

    @JsonProperty("min_intron_length")
    public void setMinIntronLength(Long minIntronLength) {
        this.minIntronLength = minIntronLength;
    }

    public CufflinksParams withMinIntronLength(Long minIntronLength) {
        this.minIntronLength = minIntronLength;
        return this;
    }

    @JsonProperty("max_intron_length")
    public Long getMaxIntronLength() {
        return maxIntronLength;
    }

    @JsonProperty("max_intron_length")
    public void setMaxIntronLength(Long maxIntronLength) {
        this.maxIntronLength = maxIntronLength;
    }

    public CufflinksParams withMaxIntronLength(Long maxIntronLength) {
        this.maxIntronLength = maxIntronLength;
        return this;
    }

    @JsonProperty("overhang_tolerance")
    public Long getOverhangTolerance() {
        return overhangTolerance;
    }

    @JsonProperty("overhang_tolerance")
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
        return ((((((((((((((((((((("CufflinksParams"+" [workspaceName=")+ workspaceName)+", alignmentObjectRef=")+ alignmentObjectRef)+", expressionSetSuffix=")+ expressionSetSuffix)+", expressionSuffix=")+ expressionSuffix)+", genomeRef=")+ genomeRef)+", numThreads=")+ numThreads)+", minIntronLength=")+ minIntronLength)+", maxIntronLength=")+ maxIntronLength)+", overhangTolerance=")+ overhangTolerance)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
