package us.kbase.genomeannotationapi;

import com.fasterxml.jackson.core.type.TypeReference;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import us.kbase.auth.AuthToken;
import us.kbase.common.service.JsonClientCaller;
import us.kbase.common.service.JsonClientException;
import us.kbase.common.service.RpcContext;
import us.kbase.common.service.UnauthorizedException;

/**
 * <p>Original spec-file module name: GenomeAnnotationAPI</p>
 * <pre>
 * A KBase module: GenomeAnnotationAPI
 * </pre>
 */
public class GenomeAnnotationAPIClient {
    private JsonClientCaller caller;
    private String serviceVersion = null;


    /** Constructs a client with a custom URL and no user credentials.
     * @param url the URL of the service.
     */
    public GenomeAnnotationAPIClient(URL url) {
        caller = new JsonClientCaller(url);
    }
    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param token the user's authorization token.
     * @throws UnauthorizedException if the token is not valid.
     * @throws IOException if an IOException occurs when checking the token's
     * validity.
     */
    public GenomeAnnotationAPIClient(URL url, AuthToken token) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, token);
    }

    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public GenomeAnnotationAPIClient(URL url, String user, String password) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password);
    }

    /** Constructs a client with a custom URL
     * and a custom authorization service URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @param auth the URL of the authorization server.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public GenomeAnnotationAPIClient(URL url, String user, String password, URL auth) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password, auth);
    }

    /** Get the token this client uses to communicate with the server.
     * @return the authorization token.
     */
    public AuthToken getToken() {
        return caller.getToken();
    }

    /** Get the URL of the service with which this client communicates.
     * @return the service URL.
     */
    public URL getURL() {
        return caller.getURL();
    }

    /** Set the timeout between establishing a connection to a server and
     * receiving a response. A value of zero or null implies no timeout.
     * @param milliseconds the milliseconds to wait before timing out when
     * attempting to read from a server.
     */
    public void setConnectionReadTimeOut(Integer milliseconds) {
        this.caller.setConnectionReadTimeOut(milliseconds);
    }

    /** Check if this client allows insecure http (vs https) connections.
     * @return true if insecure connections are allowed.
     */
    public boolean isInsecureHttpConnectionAllowed() {
        return caller.isInsecureHttpConnectionAllowed();
    }

    /** Deprecated. Use isInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public boolean isAuthAllowedForHttp() {
        return caller.isAuthAllowedForHttp();
    }

    /** Set whether insecure http (vs https) connections should be allowed by
     * this client.
     * @param allowed true to allow insecure connections. Default false
     */
    public void setIsInsecureHttpConnectionAllowed(boolean allowed) {
        caller.setInsecureHttpConnectionAllowed(allowed);
    }

    /** Deprecated. Use setIsInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public void setAuthAllowedForHttp(boolean isAuthAllowedForHttp) {
        caller.setAuthAllowedForHttp(isAuthAllowedForHttp);
    }

    /** Set whether all SSL certificates, including self-signed certificates,
     * should be trusted.
     * @param trustAll true to trust all certificates. Default false.
     */
    public void setAllSSLCertificatesTrusted(final boolean trustAll) {
        caller.setAllSSLCertificatesTrusted(trustAll);
    }
    
    /** Check if this client trusts all SSL certificates, including
     * self-signed certificates.
     * @return true if all certificates are trusted.
     */
    public boolean isAllSSLCertificatesTrusted() {
        return caller.isAllSSLCertificatesTrusted();
    }
    /** Sets streaming mode on. In this case, the data will be streamed to
     * the server in chunks as it is read from disk rather than buffered in
     * memory. Many servers are not compatible with this feature.
     * @param streamRequest true to set streaming mode on, false otherwise.
     */
    public void setStreamingModeOn(boolean streamRequest) {
        caller.setStreamingModeOn(streamRequest);
    }

    /** Returns true if streaming mode is on.
     * @return true if streaming mode is on.
     */
    public boolean isStreamingModeOn() {
        return caller.isStreamingModeOn();
    }

    public void _setFileForNextRpcResponse(File f) {
        caller.setFileForNextRpcResponse(f);
    }

    public String getServiceVersion() {
        return this.serviceVersion;
    }

    public void setServiceVersion(String newValue) {
        this.serviceVersion = newValue;
    }

    /**
     * <p>Original spec-file function name: get_taxon</p>
     * <pre>
     * *
     * * Retrieve the Taxon associated with this GenomeAnnotation.
     * *
     * * @return Reference to TaxonAPI object
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @return   instance of original type "ObjectReference"
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public String getTaxon(String ref, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        TypeReference<List<String>> retType = new TypeReference<List<String>>() {};
        List<String> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_taxon", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_assembly</p>
     * <pre>
     * *
     * * Retrieve the Assembly associated with this GenomeAnnotation.
     * *
     * * @return Reference to AssemblyAPI object
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @return   instance of original type "ObjectReference"
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public String getAssembly(String ref, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        TypeReference<List<String>> retType = new TypeReference<List<String>>() {};
        List<String> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_assembly", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_feature_types</p>
     * <pre>
     * *
     * * Retrieve the list of Feature types.
     * *
     * * @return List of feature type identifiers (strings)
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @return   instance of list of String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public List<String> getFeatureTypes(String ref, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        TypeReference<List<List<String>>> retType = new TypeReference<List<List<String>>>() {};
        List<List<String>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_feature_types", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_feature_type_descriptions</p>
     * <pre>
     * *
     * * Retrieve the descriptions for each Feature type in
     * * this GenomeAnnotation.
     * *
     * * @param feature_type_list List of Feature types. If this list
     * *  is empty or None,
     * *  the whole mapping will be returned.
     * * @return Name and description for each requested Feature Type
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @param   featureTypeList   instance of list of String
     * @return   instance of mapping from String to String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,String> getFeatureTypeDescriptions(String ref, List<String> featureTypeList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(featureTypeList);
        TypeReference<List<Map<String,String>>> retType = new TypeReference<List<Map<String,String>>>() {};
        List<Map<String,String>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_feature_type_descriptions", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_feature_type_counts</p>
     * <pre>
     * *
     * * Retrieve the count of each Feature type.
     * *
     * * @param feature_type_list  List of Feature Types. If empty,
     * *   this will retrieve  counts for all Feature Types.
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @param   featureTypeList   instance of list of String
     * @return   instance of mapping from String to Long
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,Long> getFeatureTypeCounts(String ref, List<String> featureTypeList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(featureTypeList);
        TypeReference<List<Map<String,Long>>> retType = new TypeReference<List<Map<String,Long>>>() {};
        List<Map<String,Long>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_feature_type_counts", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_feature_ids</p>
     * <pre>
     * *
     * * Retrieve Feature IDs, optionally filtered by type, region, function, alias.
     * *
     * * @param filters Dictionary of filters that can be applied to contents.
     * *   If this is empty or missing, all Feature IDs will be returned.
     * * @param group_type How to group results, which is a single string matching one
     * *   of the values for the ``filters`` parameter.
     * * @return Grouped mapping of features.
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @param   filters   instance of type {@link us.kbase.genomeannotationapi.FeatureIdFilters FeatureIdFilters} (original type "Feature_id_filters")
     * @param   groupType   instance of String
     * @return   instance of type {@link us.kbase.genomeannotationapi.FeatureIdMapping FeatureIdMapping} (original type "Feature_id_mapping")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public FeatureIdMapping getFeatureIds(String ref, FeatureIdFilters filters, String groupType, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(filters);
        args.add(groupType);
        TypeReference<List<FeatureIdMapping>> retType = new TypeReference<List<FeatureIdMapping>>() {};
        List<FeatureIdMapping> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_feature_ids", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_features</p>
     * <pre>
     * *
     * * Retrieve Feature data.
     * *
     * * @param feature_id_list List of Features to retrieve.
     * *   If None, returns all Feature data.
     * * @return Mapping from Feature IDs to dicts of available data.
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @param   featureIdList   instance of list of String
     * @return   instance of mapping from String to type {@link us.kbase.genomeannotationapi.FeatureData FeatureData} (original type "Feature_data")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,FeatureData> getFeatures(String ref, List<String> featureIdList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(featureIdList);
        TypeReference<List<Map<String,FeatureData>>> retType = new TypeReference<List<Map<String,FeatureData>>>() {};
        List<Map<String,FeatureData>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_features", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_features2</p>
     * <pre>
     * *
     * * Retrieve Feature data, v2.
     * *
     * * @param feature_id_list List of Features to retrieve.
     * *   If None, returns all Feature data.
     * * @return Mapping from Feature IDs to dicts of available data.
     * </pre>
     * @param   params   instance of type {@link us.kbase.genomeannotationapi.GetFeatures2Params GetFeatures2Params}
     * @return   instance of mapping from String to type {@link us.kbase.genomeannotationapi.FeatureData FeatureData} (original type "Feature_data")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,FeatureData> getFeatures2(GetFeatures2Params params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<Map<String,FeatureData>>> retType = new TypeReference<List<Map<String,FeatureData>>>() {};
        List<Map<String,FeatureData>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_features2", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_proteins</p>
     * <pre>
     * *
     * * Retrieve Protein data.
     * *
     * * @return Mapping from protein ID to data about the protein.
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @return   instance of mapping from String to type {@link us.kbase.genomeannotationapi.ProteinData ProteinData} (original type "Protein_data")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,ProteinData> getProteins(String ref, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        TypeReference<List<Map<String,ProteinData>>> retType = new TypeReference<List<Map<String,ProteinData>>>() {};
        List<Map<String,ProteinData>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_proteins", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_feature_locations</p>
     * <pre>
     * *
     * * Retrieve Feature locations.
     * *
     * * @param feature_id_list List of Feature IDs for which to retrieve locations.
     * *     If empty, returns data for all features.
     * * @return Mapping from Feature IDs to location information for each.
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @param   featureIdList   instance of list of String
     * @return   instance of mapping from String to list of type {@link us.kbase.genomeannotationapi.Region Region}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,List<Region>> getFeatureLocations(String ref, List<String> featureIdList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(featureIdList);
        TypeReference<List<Map<String,List<Region>>>> retType = new TypeReference<List<Map<String,List<Region>>>>() {};
        List<Map<String,List<Region>>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_feature_locations", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_feature_publications</p>
     * <pre>
     * *
     * * Retrieve Feature publications.
     * *
     * * @param feature_id_list List of Feature IDs for which to retrieve publications.
     * *     If empty, returns data for all features.
     * * @return Mapping from Feature IDs to publication info for each.
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @param   featureIdList   instance of list of String
     * @return   instance of mapping from String to list of String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,List<String>> getFeaturePublications(String ref, List<String> featureIdList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(featureIdList);
        TypeReference<List<Map<String,List<String>>>> retType = new TypeReference<List<Map<String,List<String>>>>() {};
        List<Map<String,List<String>>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_feature_publications", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_feature_dna</p>
     * <pre>
     * *
     * * Retrieve Feature DNA sequences.
     * *
     * * @param feature_id_list List of Feature IDs for which to retrieve sequences.
     * *     If empty, returns data for all features.
     * * @return Mapping of Feature IDs to their DNA sequence.
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @param   featureIdList   instance of list of String
     * @return   instance of mapping from String to String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,String> getFeatureDna(String ref, List<String> featureIdList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(featureIdList);
        TypeReference<List<Map<String,String>>> retType = new TypeReference<List<Map<String,String>>>() {};
        List<Map<String,String>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_feature_dna", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_feature_functions</p>
     * <pre>
     * *
     * * Retrieve Feature functions.
     * *
     * * @param feature_id_list List of Feature IDs for which to retrieve functions.
     * *     If empty, returns data for all features.
     * * @return Mapping of Feature IDs to their functions.
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @param   featureIdList   instance of list of String
     * @return   instance of mapping from String to String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,String> getFeatureFunctions(String ref, List<String> featureIdList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(featureIdList);
        TypeReference<List<Map<String,String>>> retType = new TypeReference<List<Map<String,String>>>() {};
        List<Map<String,String>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_feature_functions", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_feature_aliases</p>
     * <pre>
     * *
     * * Retrieve Feature aliases.
     * *
     * * @param feature_id_list List of Feature IDS for which to retrieve aliases.
     * *     If empty, returns data for all features.
     * * @return Mapping of Feature IDs to a list of aliases.
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @param   featureIdList   instance of list of String
     * @return   instance of mapping from String to list of String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,List<String>> getFeatureAliases(String ref, List<String> featureIdList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(featureIdList);
        TypeReference<List<Map<String,List<String>>>> retType = new TypeReference<List<Map<String,List<String>>>>() {};
        List<Map<String,List<String>>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_feature_aliases", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_cds_by_gene</p>
     * <pre>
     * *
     * * Retrieves coding sequence Features (cds) for given gene Feature IDs.
     * *
     * * @param gene_id_list List of gene Feature IDS for which to retrieve CDS.
     * *     If empty, returns data for all features.
     * * @return Mapping of gene Feature IDs to a list of CDS Feature IDs.
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @param   geneIdList   instance of list of String
     * @return   instance of mapping from String to list of String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,List<String>> getCdsByGene(String ref, List<String> geneIdList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(geneIdList);
        TypeReference<List<Map<String,List<String>>>> retType = new TypeReference<List<Map<String,List<String>>>>() {};
        List<Map<String,List<String>>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_cds_by_gene", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_cds_by_mrna</p>
     * <pre>
     * *
     * * Retrieves coding sequence (cds) Feature IDs for given mRNA Feature IDs.
     * *
     * * @param mrna_id_list List of mRNA Feature IDS for which to retrieve CDS.
     * *     If empty, returns data for all features.
     * * @return Mapping of mRNA Feature IDs to a list of CDS Feature IDs.
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @param   mrnaIdList   instance of list of String
     * @return   instance of mapping from String to String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,String> getCdsByMrna(String ref, List<String> mrnaIdList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(mrnaIdList);
        TypeReference<List<Map<String,String>>> retType = new TypeReference<List<Map<String,String>>>() {};
        List<Map<String,String>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_cds_by_mrna", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_gene_by_cds</p>
     * <pre>
     * *
     * * Retrieves gene Feature IDs for given coding sequence (cds) Feature IDs.
     * *
     * * @param cds_id_list List of cds Feature IDS for which to retrieve gene IDs.
     * *     If empty, returns all cds/gene mappings.
     * * @return Mapping of cds Feature IDs to gene Feature IDs.
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @param   cdsIdList   instance of list of String
     * @return   instance of mapping from String to String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,String> getGeneByCds(String ref, List<String> cdsIdList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(cdsIdList);
        TypeReference<List<Map<String,String>>> retType = new TypeReference<List<Map<String,String>>>() {};
        List<Map<String,String>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_gene_by_cds", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_gene_by_mrna</p>
     * <pre>
     * *
     * * Retrieves gene Feature IDs for given mRNA Feature IDs.
     * *
     * * @param mrna_id_list List of mRNA Feature IDS for which to retrieve gene IDs.
     * *     If empty, returns all mRNA/gene mappings.
     * * @return Mapping of mRNA Feature IDs to gene Feature IDs.
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @param   mrnaIdList   instance of list of String
     * @return   instance of mapping from String to String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,String> getGeneByMrna(String ref, List<String> mrnaIdList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(mrnaIdList);
        TypeReference<List<Map<String,String>>> retType = new TypeReference<List<Map<String,String>>>() {};
        List<Map<String,String>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_gene_by_mrna", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_mrna_by_cds</p>
     * <pre>
     * *
     * * Retrieves mRNA Features for given coding sequences (cds) Feature IDs.
     * *
     * * @param cds_id_list List of cds Feature IDS for which to retrieve mRNA IDs.
     * *     If empty, returns all cds/mRNA mappings.
     * * @return Mapping of cds Feature IDs to mRNA Feature IDs.
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @param   cdsIdList   instance of list of String
     * @return   instance of mapping from String to String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,String> getMrnaByCds(String ref, List<String> cdsIdList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(cdsIdList);
        TypeReference<List<Map<String,String>>> retType = new TypeReference<List<Map<String,String>>>() {};
        List<Map<String,String>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_mrna_by_cds", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_mrna_by_gene</p>
     * <pre>
     * *
     * * Retrieve the mRNA IDs for given gene IDs.
     * *
     * * @param gene_id_list List of gene Feature IDS for which to retrieve mRNA IDs.
     * *     If empty, returns all gene/mRNA mappings.
     * * @return Mapping of gene Feature IDs to a list of mRNA Feature IDs.
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @param   geneIdList   instance of list of String
     * @return   instance of mapping from String to list of String
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,List<String>> getMrnaByGene(String ref, List<String> geneIdList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(geneIdList);
        TypeReference<List<Map<String,List<String>>>> retType = new TypeReference<List<Map<String,List<String>>>>() {};
        List<Map<String,List<String>>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_mrna_by_gene", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_mrna_exons</p>
     * <pre>
     * *
     * * Retrieve Exon information for each mRNA ID.
     * *
     * * @param mrna_id_list List of mRNA Feature IDS for which to retrieve exons.
     * *     If empty, returns data for all exons.
     * * @return Mapping of mRNA Feature IDs to a list of exons (:js:data:`Exon_data`).
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @param   mrnaIdList   instance of list of String
     * @return   instance of mapping from String to list of type {@link us.kbase.genomeannotationapi.ExonData ExonData} (original type "Exon_data")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,List<ExonData>> getMrnaExons(String ref, List<String> mrnaIdList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(mrnaIdList);
        TypeReference<List<Map<String,List<ExonData>>>> retType = new TypeReference<List<Map<String,List<ExonData>>>>() {};
        List<Map<String,List<ExonData>>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_mrna_exons", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_mrna_utrs</p>
     * <pre>
     * *
     * * Retrieve UTR information for each mRNA Feature ID.
     * *
     * *  UTRs are calculated between mRNA features and corresponding CDS features.
     * *  The return value for each mRNA can contain either:
     * *     - no UTRs found (empty dict)
     * *     -  5' UTR only
     * *     -  3' UTR only
     * *     -  5' and 3' UTRs
     * *
     * *  Note: The Genome data type does not contain interfeature
     * *  relationship information. Calling this method for Genome objects
     * *  will raise a :js:throws:`exc.TypeException`.
     * *
     * * @param feature_id_list List of mRNA Feature IDS for which to retrieve UTRs.
     * * If empty, returns data for all UTRs.
     * * @return Mapping of mRNA Feature IDs to a mapping that contains
     * * both 5' and 3' UTRs::
     * *     { "5'UTR": :js:data:`UTR_data`, "3'UTR": :js:data:`UTR_data` }
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @param   mrnaIdList   instance of list of String
     * @return   instance of mapping from String to mapping from String to type {@link us.kbase.genomeannotationapi.UTRData UTRData} (original type "UTR_data")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Map<String,Map<String,UTRData>> getMrnaUtrs(String ref, List<String> mrnaIdList, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        args.add(mrnaIdList);
        TypeReference<List<Map<String,Map<String,UTRData>>>> retType = new TypeReference<List<Map<String,Map<String,UTRData>>>>() {};
        List<Map<String,Map<String,UTRData>>> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_mrna_utrs", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_summary</p>
     * <pre>
     * *
     * * Retrieve a summary representation of this GenomeAnnotation.
     * *
     * * @return summary data
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @return   instance of type {@link us.kbase.genomeannotationapi.SummaryData SummaryData} (original type "Summary_data")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public SummaryData getSummary(String ref, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        TypeReference<List<SummaryData>> retType = new TypeReference<List<SummaryData>>() {};
        List<SummaryData> res = caller.jsonrpcCall("GenomeAnnotationAPI.get_summary", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: save_summary</p>
     * <pre>
     * *
     * * Retrieve a summary representation of this GenomeAnnotation.
     * *
     * * @return summary data
     * </pre>
     * @param   ref   instance of original type "ObjectReference"
     * @return   instance of Long
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public Long saveSummary(String ref, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(ref);
        TypeReference<List<Long>> retType = new TypeReference<List<Long>>() {};
        List<Long> res = caller.jsonrpcCall("GenomeAnnotationAPI.save_summary", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    public Map<String, Object> status(RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        TypeReference<List<Map<String, Object>>> retType = new TypeReference<List<Map<String, Object>>>() {};
        List<Map<String, Object>> res = caller.jsonrpcCall("GenomeAnnotationAPI.status", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }
}
