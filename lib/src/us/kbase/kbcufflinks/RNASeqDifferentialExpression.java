
package us.kbase.kbcufflinks;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: RNASeqDifferentialExpression</p>
 * <pre>
 * Result of run_CuffDiff
 * Object RNASeqDifferentialExpression file structure
 * @optional tool_opts tool_version sample_ids comments
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "tool_used",
    "tool_version",
    "tool_opts",
    "file",
    "sample_ids",
    "condition",
    "genome_id",
    "expressionSet_id",
    "alignmentSet_id",
    "sampleset_id",
    "comments"
})
public class RNASeqDifferentialExpression {

    @JsonProperty("tool_used")
    private java.lang.String toolUsed;
    @JsonProperty("tool_version")
    private java.lang.String toolVersion;
    @JsonProperty("tool_opts")
    private List<Map<String, String>> toolOpts;
    /**
     * <p>Original spec-file type: Handle</p>
     * <pre>
     * @optional hid file_name type url remote_md5 remote_sha1
     * </pre>
     * 
     */
    @JsonProperty("file")
    private Handle file;
    @JsonProperty("sample_ids")
    private List<String> sampleIds;
    @JsonProperty("condition")
    private List<String> condition;
    @JsonProperty("genome_id")
    private java.lang.String genomeId;
    @JsonProperty("expressionSet_id")
    private java.lang.String expressionSetId;
    @JsonProperty("alignmentSet_id")
    private java.lang.String alignmentSetId;
    @JsonProperty("sampleset_id")
    private java.lang.String samplesetId;
    @JsonProperty("comments")
    private java.lang.String comments;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("tool_used")
    public java.lang.String getToolUsed() {
        return toolUsed;
    }

    @JsonProperty("tool_used")
    public void setToolUsed(java.lang.String toolUsed) {
        this.toolUsed = toolUsed;
    }

    public RNASeqDifferentialExpression withToolUsed(java.lang.String toolUsed) {
        this.toolUsed = toolUsed;
        return this;
    }

    @JsonProperty("tool_version")
    public java.lang.String getToolVersion() {
        return toolVersion;
    }

    @JsonProperty("tool_version")
    public void setToolVersion(java.lang.String toolVersion) {
        this.toolVersion = toolVersion;
    }

    public RNASeqDifferentialExpression withToolVersion(java.lang.String toolVersion) {
        this.toolVersion = toolVersion;
        return this;
    }

    @JsonProperty("tool_opts")
    public List<Map<String, String>> getToolOpts() {
        return toolOpts;
    }

    @JsonProperty("tool_opts")
    public void setToolOpts(List<Map<String, String>> toolOpts) {
        this.toolOpts = toolOpts;
    }

    public RNASeqDifferentialExpression withToolOpts(List<Map<String, String>> toolOpts) {
        this.toolOpts = toolOpts;
        return this;
    }

    /**
     * <p>Original spec-file type: Handle</p>
     * <pre>
     * @optional hid file_name type url remote_md5 remote_sha1
     * </pre>
     * 
     */
    @JsonProperty("file")
    public Handle getFile() {
        return file;
    }

    /**
     * <p>Original spec-file type: Handle</p>
     * <pre>
     * @optional hid file_name type url remote_md5 remote_sha1
     * </pre>
     * 
     */
    @JsonProperty("file")
    public void setFile(Handle file) {
        this.file = file;
    }

    public RNASeqDifferentialExpression withFile(Handle file) {
        this.file = file;
        return this;
    }

    @JsonProperty("sample_ids")
    public List<String> getSampleIds() {
        return sampleIds;
    }

    @JsonProperty("sample_ids")
    public void setSampleIds(List<String> sampleIds) {
        this.sampleIds = sampleIds;
    }

    public RNASeqDifferentialExpression withSampleIds(List<String> sampleIds) {
        this.sampleIds = sampleIds;
        return this;
    }

    @JsonProperty("condition")
    public List<String> getCondition() {
        return condition;
    }

    @JsonProperty("condition")
    public void setCondition(List<String> condition) {
        this.condition = condition;
    }

    public RNASeqDifferentialExpression withCondition(List<String> condition) {
        this.condition = condition;
        return this;
    }

    @JsonProperty("genome_id")
    public java.lang.String getGenomeId() {
        return genomeId;
    }

    @JsonProperty("genome_id")
    public void setGenomeId(java.lang.String genomeId) {
        this.genomeId = genomeId;
    }

    public RNASeqDifferentialExpression withGenomeId(java.lang.String genomeId) {
        this.genomeId = genomeId;
        return this;
    }

    @JsonProperty("expressionSet_id")
    public java.lang.String getExpressionSetId() {
        return expressionSetId;
    }

    @JsonProperty("expressionSet_id")
    public void setExpressionSetId(java.lang.String expressionSetId) {
        this.expressionSetId = expressionSetId;
    }

    public RNASeqDifferentialExpression withExpressionSetId(java.lang.String expressionSetId) {
        this.expressionSetId = expressionSetId;
        return this;
    }

    @JsonProperty("alignmentSet_id")
    public java.lang.String getAlignmentSetId() {
        return alignmentSetId;
    }

    @JsonProperty("alignmentSet_id")
    public void setAlignmentSetId(java.lang.String alignmentSetId) {
        this.alignmentSetId = alignmentSetId;
    }

    public RNASeqDifferentialExpression withAlignmentSetId(java.lang.String alignmentSetId) {
        this.alignmentSetId = alignmentSetId;
        return this;
    }

    @JsonProperty("sampleset_id")
    public java.lang.String getSamplesetId() {
        return samplesetId;
    }

    @JsonProperty("sampleset_id")
    public void setSamplesetId(java.lang.String samplesetId) {
        this.samplesetId = samplesetId;
    }

    public RNASeqDifferentialExpression withSamplesetId(java.lang.String samplesetId) {
        this.samplesetId = samplesetId;
        return this;
    }

    @JsonProperty("comments")
    public java.lang.String getComments() {
        return comments;
    }

    @JsonProperty("comments")
    public void setComments(java.lang.String comments) {
        this.comments = comments;
    }

    public RNASeqDifferentialExpression withComments(java.lang.String comments) {
        this.comments = comments;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((((((((((((((((("RNASeqDifferentialExpression"+" [toolUsed=")+ toolUsed)+", toolVersion=")+ toolVersion)+", toolOpts=")+ toolOpts)+", file=")+ file)+", sampleIds=")+ sampleIds)+", condition=")+ condition)+", genomeId=")+ genomeId)+", expressionSetId=")+ expressionSetId)+", alignmentSetId=")+ alignmentSetId)+", samplesetId=")+ samplesetId)+", comments=")+ comments)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
