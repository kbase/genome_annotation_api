import os
import hashlib
from collections import defaultdict
from repoze.lru import lru_cache

from Workspace.WorkspaceClient import Workspace
from DataFileUtil.DataFileUtilClient import DataFileUtil


class GenomeIAnnotationUtil:
    def __init__(self, services):
        self.ws = Workspace(services['workspace_service_url'])
        self.handle_url = services['handle_service_url']
        self.shock_url = services['shock_service_url']
        self.sw_url = services['service_wizard_url']
        self.dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'])
        self.taxon_wsname = 'ReferenceTaxons'
        self._valid_filters = ["type_list", "region_list", "function_list",
                               "alias_list"]
        self._valid_groups = ["type", "region", "function", "alias"]

    @lru_cache(maxsize=8)
    def get_genome(self, genome_ref):
        return self.dfu.get_objects(
            {'object_refs': [genome_ref]}
        )['data'][0]['data']

    def get_taxon_ref(self, genome_ref):
        return self.ws.get_objects2({'objects': [
            {'ref': genome_ref, 'included': ['/taxon_ref']}
        ]})['data'][0]['data']['taxon_ref']

    def get_assembly_ref(self, genome_ref):
        return self.ws.get_objects2({'objects': [
            {'ref': genome_ref, 'included': ['/assembly_ref']}
        ]})['data'][0]['data']['assembly_ref']

    @staticmethod
    def _make_feature_list(genome, limited_keys=()):
        feature_list = []
        for feat_array in (('features', 'gene'), ('mrnas', 'mRNA'),
                           ('cdss', 'CDS'), ('non_coding_features', 'gene')):
            for feat in genome.get(feat_array[0], []):
                if 'type' not in feat:
                    feat['type'] = feat_array[1]
                if feat.get("aliases") and isinstance(feat['aliases'][0], list):
                    feat['aliases'] = [x[1] for x in feat['aliases']]
                if isinstance(feat.get("function"), basestring):
                    feat["functions"] = feat["function"].split("; ")
                if limited_keys:
                    limited_keys = set(limited_keys)
                    feature_list.append({k: v for k, v in feat.items()
                                         if k in limited_keys})
                else:
                    feature_list.append(feat)
        return feature_list

    def get_feature_ids(self, genome_ref, filters=None, group_by="type"):
        if filters is None:
            filters = {}

        for k in filters:
            if k not in self._valid_filters:
                raise KeyError(
                    "Invalid filter key {}, valid filters are {}".format(
                        k, self._valid_filters))

        if group_by not in self._valid_groups:
            raise ValueError(
                "Invalid group_by {}, valid group_by values are {}".format(
                    group_by, self._valid_groups))

        limited_keys = ['id']

        if group_by == "type" or "type_list" in filters:
            limited_keys.append('type')
        elif group_by == "region" or "region_list" in filters:
            limited_keys.append("location")
        elif group_by == "function" or "function_list" in filters:
            limited_keys.append("functions")
        elif group_by == "alias" or "alias_list" in filters:
            limited_keys.append("aliases")

        genome = self.get_genome(genome_ref)
        features = self._make_feature_list(genome, limited_keys)

        # now process all filters and reduce the data
        remove_features = set()

        if "type_list" in filters and filters["type_list"] is not None:
            if not isinstance(filters["type_list"], list):
                raise TypeError(
                    "A list of strings indicating Feature types is required.")
            elif len(filters["type_list"]) == 0:
                raise TypeError(
                    "A list of strings indicating Feature types is required, received an empty list.")

            for i in xrange(len(features)):
                if features[i]["type"] not in filters["type_list"]:
                    remove_features.add(i)

        if "region_list" in filters and filters["region_list"] is not None:
            if not isinstance(filters["region_list"], list):
                raise TypeError("A list of region dictionaries is required.")
            elif len(filters["region_list"]) == 0:
                raise TypeError(
                    "A list of region dictionaries is required, received an empty list.")

            def is_feature_in_regions(f, regions):
                if "location" not in f:
                    return False

                for loc in f["location"]:
                    for r in regions:
                        if r["contig_id"] == loc[0] and loc[2] == r["strand"]:
                            if loc[2] == "+" and \
                                            max(loc[1], r["start"]) <= min(
                                                loc[1] + loc[3],
                                                r["start"] + r["length"]):
                                return True
                            elif loc[2] == "-" and \
                                            max(loc[1] - loc[3],
                                                r["start"] - r[
                                                    "length"]) <= min(
                                        loc[1], r["start"]):
                                return True
                return False

            for i in xrange(len(features)):
                if not is_feature_in_regions(features[i],
                                             filters["region_list"]):
                    remove_features.add(i)

        if "function_list" in filters and filters["function_list"] is not None:
            if not isinstance(filters["function_list"], list):
                raise TypeError(
                    "A list of Feature function strings is required.")
            elif len(filters["function_list"]) == 0:
                raise TypeError(
                    "A list of Feature function strings is required, received an empty list.")

            function_set = set(filters["function_list"])
            for i in xrange(len(features)):
                if "functions" not in features[i]:
                    remove_features.add(i)
                else:
                    found = False
                    for f in features[i]["functions"]:
                        if f in function_set:
                            found = True
                            break

                    if not found:
                        remove_features.add(i)

        if "alias_list" in filters and filters["alias_list"] is not None:
            if not isinstance(filters["alias_list"], list):
                raise TypeError("A list of Feature alias strings is required.")
            elif len(filters["alias_list"]) == 0:
                raise TypeError(
                    "A list of Feature alias strings is required, received an empty list.")
            alias_set = set(filters["alias_list"])
            for i in xrange(len(features)):
                if "aliases" not in features[i]:
                    remove_features.add(i)
                else:
                    found = False
                    for alias in features[i]["aliases"]:
                        if alias in alias_set:
                            found = True
                            break

                    if not found:
                        remove_features.add(i)

        keep_features = [i for i in xrange(len(features)) if
                         i not in remove_features]

        # now that filtering has been completed, attempt to group the data as requested
        results = {}

        if group_by == "type":
            results["by_type"] = defaultdict(list)
            for i in keep_features:
                results["by_type"][features[i]["type"]].append(
                    features[i]["id"])
        elif group_by == "region":
            results["by_region"] = {}
            for i in keep_features:
                for r in features[i]["location"]:
                    contig_id = r[0]
                    strand = r[2]
                    start = r[1]
                    length = r[3]
                    range = "{}-{}".format(start, start + length)

                    if contig_id not in results["by_region"]:
                        results["by_region"][contig_id] = {}

                    if strand not in results["by_region"][contig_id]:
                        results["by_region"][contig_id][strand] = {}

                    if range not in results["by_region"][contig_id][strand]:
                        results["by_region"][contig_id][strand][range] = []

                    results["by_region"][contig_id][strand][range].append(
                        features[i]["id"])
        elif group_by == "function":
            results["by_function"] = defaultdict(list)
            for i in keep_features:
                for func in features[i]["functions"]:
                    results["by_function"][func].append(features[i]["id"])
        elif group_by == "alias":
            results["by_alias"] = defaultdict(list)
            for i in keep_features:
                for alias in features[i]["aliases"]:
                    results["by_alias"][alias].append(features[i]["id"])

        return results

    def get_features(self, genome_ref, feature_id_list=None, exclude_sequence=False):
        out_features = {}
        genome = self.get_genome(genome_ref)

        if exclude_sequence:
            limited_keys = ["function", "location", "md5", "type", "id", "aliases", "dna_sequence_length"]
            features = self._make_feature_list(genome, limited_keys)
        else:
            features = self._make_feature_list(genome)

        def fill_out_feature(x):
            f = {
                "feature_id": x['id'],
                "feature_type": x['type'],
                "feature_function": x.get('function', ''),
                "feature_publications": [],
                "feature_notes": "",
                "feature_inference": "",
                "feature_quality_warnings": []
            }
            if 'functions' in x:
                f['feature_function'] = "; ".join(x.get('functions', [])),

            if "location" in x:
                f["feature_locations"] = [{"contig_id": loc[0],
                                           "start": loc[1],
                                           "strand": loc[2],
                                           "length": loc[3]} for loc in x['location']]
            else:
                f["feature_locations"] = []

            if 'dna_sequence' in x:
                f["feature_dna_sequence"] = x['dna_sequence']

                if 'md5' in x:
                    f["feature_md5"] = x['md5']
                else:
                    f["feature_md5"] = hashlib.md5(x["dna_sequence"].upper()).hexdigest()
            else:
                f["feature_dna_sequence"] = ""
                f["feature_md5"] = ""

            if 'dna_sequence_length' in x:
                f["feature_dna_sequence_length"] = x['dna_sequence_length']
            else:
                f["feature_dna_sequence_length"] = -1

            f["feature_aliases"] = {}
            if 'aliases' in x:
                for key in x['aliases']:
                    if isinstance(key, list):
                        key = ':'.join(key)
                    f["feature_aliases"][key] = []

            if "feature_quality_score" in x:
                f["feature_quality_score"] = str(x['quality'])
            else:
                f["feature_quality_score"] = ""

            return f

        if feature_id_list is None:
            for x in features:
                out_features[x['id']] = fill_out_feature(x)
        else:
            if not isinstance(feature_id_list, list):
                raise TypeError("A list of strings indicating Feature identifiers is required.")
            try:
                feature_refs = ["features/" + x for x in feature_id_list]
                assert len(feature_refs) > 0
            except TypeError:
                raise TypeError("A list of strings indicating Feature identifiers is required.")
            except AssertionError:
                raise TypeError("A list of strings indicating Feature identifiers is required, received an empty list.")

            for x in features:
                if x['id'] in feature_id_list:
                    out_features[x['id']] = fill_out_feature(x)

        return out_features

    def get_cds_by_gene(self, genome_ref, gene_id_list=None):
        cds_by_gene = {}
        genome = self.get_genome(genome_ref)
        id_set = set(gene_id_list)
        for gene in genome.get('features', []):
            if id_set and gene['id'] not in id_set:
                continue
            if 'cdss' in gene:
                cds_by_gene[gene['id']] = gene['cdss']
        return cds_by_gene
