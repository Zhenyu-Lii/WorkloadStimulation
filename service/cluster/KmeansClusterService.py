from sklearn.cluster import KMeans
import numpy as np
import collections

from dao.SessionHandler import SessionHandler
from service.representation.WESSBASRepresentationService import WESSBASRepresentationService
from service.representation.SeqenceEmbeddingService import SequenceEmbeddingService
from service.cluster.BaseClusterService import BaseClusterService


class KMeansClusterService(BaseClusterService):
    """
    对向量化后的用户行为进行KMeans聚类
    """

    def __init__(self, sessionid2vec):
        self.sessionid = np.array(list(sessionid2vec.keys()))
        self.data = np.array(list(sessionid2vec.values()))

    def cluster(self):
        class_num = 3
        estimator = KMeans(n_clusters=class_num)
        estimator.fit(self.data)
        labels = estimator.labels_
        centroids = estimator.cluster_centers_
        LABELS = list(range(class_num))
        label_num ={}
        for label in labels:
            if label not in label_num.keys():
                label_num[label] = 1
            else:
                label_num[label] += 1
        return labels, centroids, LABELS, label_num


if __name__ == "__main__":
    # session读取
    session_handler = SessionHandler()
    session_collection = session_handler.get_session_collection()
    session_collection.shrink()
    sessions = session_collection.sessions

    # session表征
    represent_service = WESSBASRepresentationService(sessions)
    # represent_service = SequenceEmbeddingService(sessions)
    sessionid2vec = represent_service.represent()

    # session聚类
    kmeans_cluster = KMeansClusterService(sessionid2vec)
    labels, centroids, LABELS, label_num = kmeans_cluster.cluster()
    print(label_num)