from sklearn.cluster import KMeans
import numpy as np
import collections
from config.SessionConfig import session_config
from service.representation.WESSBASRepresentationService import WESSBASRepresentationService

class KMeansClusterService:
    """
    对向量化后的用户行为进行KMeans聚类
    """

    def __init__(self):
        represent_service = WESSBASRepresentationService()
        sessionid2vec = represent_service.represent()
        self.data = np.array(list(sessionid2vec.values()))

    def cluster(self):
        results = collections.defaultdict(list)
        estimator = KMeans(n_clusters=3)
        estimator.fit(self.data)
        labels = estimator.labels_
        centroids = estimator.cluster_centers_
        for i in range(len(labels)):
            results[labels[i]].append(self.data[i])
        return results

if __name__ == "__main__":
    kmeans_cluster = KMeansClusterService()
    kmeans_cluster.cluster()