
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
 * <p>Original spec-file type: CuffdiffInput</p>
 * <pre>
 * Required input parameters for run_Cuffdiff.
 * expressionset_ref           -   reference for an expressionset object
 * workspace_name              -   workspace name to save the differential expression output object
 * diff_expression_obj_name    -   name of the differential expression output object
 * filtered_expression_matrix_name - name of the filtered expression matrix output object
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "expressionset_ref",
    "workspace_name",
    "diff_expression_obj_name",
    "filtered_expression_matrix_name",
    "library_norm_method",
    "multi_read_correct",
    "time_series",
    "min_alignment_count"
})
public class CuffdiffInput {

    @JsonProperty("expressionset_ref")
    private String expressionsetRef;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("diff_expression_obj_name")
    private String diffExpressionObjName;
    @JsonProperty("filtered_expression_matrix_name")
    private String filteredExpressionMatrixName;
    @JsonProperty("library_norm_method")
    private String libraryNormMethod;
    @JsonProperty("multi_read_correct")
    private Long multiReadCorrect;
    @JsonProperty("time_series")
    private Long timeSeries;
    @JsonProperty("min_alignment_count")
    private Long minAlignmentCount;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("expressionset_ref")
    public String getExpressionsetRef() {
        return expressionsetRef;
    }

    @JsonProperty("expressionset_ref")
    public void setExpressionsetRef(String expressionsetRef) {
        this.expressionsetRef = expressionsetRef;
    }

    public CuffdiffInput withExpressionsetRef(String expressionsetRef) {
        this.expressionsetRef = expressionsetRef;
        return this;
    }

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public CuffdiffInput withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("diff_expression_obj_name")
    public String getDiffExpressionObjName() {
        return diffExpressionObjName;
    }

    @JsonProperty("diff_expression_obj_name")
    public void setDiffExpressionObjName(String diffExpressionObjName) {
        this.diffExpressionObjName = diffExpressionObjName;
    }

    public CuffdiffInput withDiffExpressionObjName(String diffExpressionObjName) {
        this.diffExpressionObjName = diffExpressionObjName;
        return this;
    }

    @JsonProperty("filtered_expression_matrix_name")
    public String getFilteredExpressionMatrixName() {
        return filteredExpressionMatrixName;
    }

    @JsonProperty("filtered_expression_matrix_name")
    public void setFilteredExpressionMatrixName(String filteredExpressionMatrixName) {
        this.filteredExpressionMatrixName = filteredExpressionMatrixName;
    }

    public CuffdiffInput withFilteredExpressionMatrixName(String filteredExpressionMatrixName) {
        this.filteredExpressionMatrixName = filteredExpressionMatrixName;
        return this;
    }

    @JsonProperty("library_norm_method")
    public String getLibraryNormMethod() {
        return libraryNormMethod;
    }

    @JsonProperty("library_norm_method")
    public void setLibraryNormMethod(String libraryNormMethod) {
        this.libraryNormMethod = libraryNormMethod;
    }

    public CuffdiffInput withLibraryNormMethod(String libraryNormMethod) {
        this.libraryNormMethod = libraryNormMethod;
        return this;
    }

    @JsonProperty("multi_read_correct")
    public Long getMultiReadCorrect() {
        return multiReadCorrect;
    }

    @JsonProperty("multi_read_correct")
    public void setMultiReadCorrect(Long multiReadCorrect) {
        this.multiReadCorrect = multiReadCorrect;
    }

    public CuffdiffInput withMultiReadCorrect(Long multiReadCorrect) {
        this.multiReadCorrect = multiReadCorrect;
        return this;
    }

    @JsonProperty("time_series")
    public Long getTimeSeries() {
        return timeSeries;
    }

    @JsonProperty("time_series")
    public void setTimeSeries(Long timeSeries) {
        this.timeSeries = timeSeries;
    }

    public CuffdiffInput withTimeSeries(Long timeSeries) {
        this.timeSeries = timeSeries;
        return this;
    }

    @JsonProperty("min_alignment_count")
    public Long getMinAlignmentCount() {
        return minAlignmentCount;
    }

    @JsonProperty("min_alignment_count")
    public void setMinAlignmentCount(Long minAlignmentCount) {
        this.minAlignmentCount = minAlignmentCount;
    }

    public CuffdiffInput withMinAlignmentCount(Long minAlignmentCount) {
        this.minAlignmentCount = minAlignmentCount;
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
        return ((((((((((((((((((("CuffdiffInput"+" [expressionsetRef=")+ expressionsetRef)+", workspaceName=")+ workspaceName)+", diffExpressionObjName=")+ diffExpressionObjName)+", filteredExpressionMatrixName=")+ filteredExpressionMatrixName)+", libraryNormMethod=")+ libraryNormMethod)+", multiReadCorrect=")+ multiReadCorrect)+", timeSeries=")+ timeSeries)+", minAlignmentCount=")+ minAlignmentCount)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
