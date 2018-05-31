__author__ = 'Alipour'
import numpy as np
from sklearn.cluster import SpectralClustering,KMeans,AffinityPropagation

class DPWC():
    def __init__(self,dpw,snippets):
        self.co_occurrence_matrix={}
        self.snippets=snippets
        self.dpw=dpw
        self.matrix=[]
        self.raw_clusters=[]
        self.clusters={}
        self.profile={}
    def calc_co_occurrence(self):
        raw_matrix=[]
        for key1 in sorted(self.dpw.keys()):
            row=[]
            for key2 in sorted(self.dpw.keys()):
                count=0
                for item in self.snippets:
                    if key1 in item and key2 in item:
                        count+=1
                row.append(count)
            raw_matrix.append(row)
        self.matrix=np.matrix(raw_matrix)
        return self.matrix
    def spectral_clustering(self):
        self.raw_clusters=SpectralClustering(2).fit_predict(self.matrix)
        return self.raw_clusters
    def kmeans(self):
        self.raw_clusters = KMeans(n_clusters=10, random_state=0).fit(self.matrix).labels_
        return self.raw_clusters
    def affinity_propagation(self):
        af = AffinityPropagation(preference=-50,affinity="precomputed").fit(self.matrix)
        cluster_centers_indices = af.cluster_centers_indices_
        self.raw_clusters = af.labels_
        n_clusters_ = len(cluster_centers_indices)
        return self.raw_clusters
    def calculate_profile(self):
        sorted_keys=sorted(self.dpw.keys())
        for i in range(len(self.raw_clusters)):
            if not self.raw_clusters[i] in self.clusters:
                self.clusters.update({
                    self.raw_clusters[i]:{}
                })
            self.clusters[self.raw_clusters[i]].update({
                    sorted_keys[i]:self.dpw[sorted_keys[i]]
                })
        return self.clusters

