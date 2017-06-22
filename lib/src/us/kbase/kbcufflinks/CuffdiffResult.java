
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
 * <p>Original spec-file type: CuffdiffResult</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "result_directory",
    "diff_expression_obj_ref",
    "filtered_expression_matrix_ref",
    "report_name",
    "report_ref"
})
public class CuffdiffResult {

    @JsonProperty("result_directory")
    private String resultDirectory;
    @JsonProperty("diff_expression_obj_ref")
    private String diffExpressionObjRef;
    @JsonProperty("filtered_expression_matrix_ref")
    private String filteredExpressionMatrixRef;
    @JsonProperty("report_name")
    private String reportName;
    @JsonProperty("report_ref")
    private String reportRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("result_directory")
    public String getResultDirectory() {
        return resultDirectory;
    }

    @JsonProperty("result_directory")
    public void setResultDirectory(String resultDirectory) {
        this.resultDirectory = resultDirectory;
    }

    public CuffdiffResult withResultDirectory(String resultDirectory) {
        this.resultDirectory = resultDirectory;
        return this;
    }

    @JsonProperty("diff_expression_obj_ref")
    public String getDiffExpressionObjRef() {
        return diffExpressionObjRef;
    }

    @JsonProperty("diff_expression_obj_ref")
    public void setDiffExpressionObjRef(String diffExpressionObjRef) {
        this.diffExpressionObjRef = diffExpressionObjRef;
    }

    public CuffdiffResult withDiffExpressionObjRef(String diffExpressionObjRef) {
        this.diffExpressionObjRef = diffExpressionObjRef;
        return this;
    }

    @JsonProperty("filtered_expression_matrix_ref")
    public String getFilteredExpressionMatrixRef() {
        return filteredExpressionMatrixRef;
    }

    @JsonProperty("filtered_expression_matrix_ref")
    public void setFilteredExpressionMatrixRef(String filteredExpressionMatrixRef) {
        this.filteredExpressionMatrixRef = filteredExpressionMatrixRef;
    }

    public CuffdiffResult withFilteredExpressionMatrixRef(String filteredExpressionMatrixRef) {
        this.filteredExpressionMatrixRef = filteredExpressionMatrixRef;
        return this;
    }

    @JsonProperty("report_name")
    public String getReportName() {
        return reportName;
    }

    @JsonProperty("report_name")
    public void setReportName(String reportName) {
        this.reportName = reportName;
    }

    public CuffdiffResult withReportName(String reportName) {
        this.reportName = reportName;
        return this;
    }

    @JsonProperty("report_ref")
    public String getReportRef() {
        return reportRef;
    }

    @JsonProperty("report_ref")
    public void setReportRef(String reportRef) {
        this.reportRef = reportRef;
    }

    public CuffdiffResult withReportRef(String reportRef) {
        this.reportRef = reportRef;
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
        return ((((((((((((("CuffdiffResult"+" [resultDirectory=")+ resultDirectory)+", diffExpressionObjRef=")+ diffExpressionObjRef)+", filteredExpressionMatrixRef=")+ filteredExpressionMatrixRef)+", reportName=")+ reportName)+", reportRef=")+ reportRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
