import numpy as np
import collections
import time
import matplotlib.pyplot as plt
from dao.SessionHandler import SessionHandler
from config.SessionConfig import session_config
from service.cluster.KmeansClusterService import KMeansClusterService
from service.representation.WESSBASRepresentationService import WESSBASRepresentationService
from service.cluster.BaseClusterService import BaseClusterService


class WESSBASIntensityService:
    """
    在这个类完成workload intensity与behavior mix
    """

    def __init__(self, sessions, sessionid2vec, labels):
        self.sessions = sessions
        self.sessionid2vec = sessionid2vec
        self.labels = labels
        self.message_texts = session_config.message_texts
        self.message_dict = session_config.message_dict

    def build_workload_intensity(self):
        # 目前用了shrink()后的sessions而非shrink()前的，需要分析一下是否合理
        session_intensity = collections.defaultdict(list)
        for session_id, user_behaviors in self.sessions.items():
            for user_behavior in user_behaviors:
                a = user_behavior.timestamp  # '2021-07-09T10:16:49.338460317Z'
                timestamp = time.strptime(a.split(".")[0], '%Y-%m-%dT%H:%M:%S')
                h = timestamp.tm_hour
                m = timestamp.tm_min
                s = timestamp.tm_sec
                total_s = h * 3600 + m * 60 + s
                session_intensity[total_s].append(session_id)
        intensity = np.zeros(24 * 3600, dtype=int)
        for k, v in session_intensity.items():
            intensity[k] = len(v)
        plt.plot(intensity, label="session start")
        plt.legend()
        plt.savefig("intensity.png")
        return intensity

    def build_behavior_mix(self):
        counter = collections.Counter(self.labels)
        label2prob = {}
        for key in sorted(counter.keys()):
            prob = round(counter[key] / len(self.labels), 4)
            label2prob[key] = prob
        print("behavior mix for one day:\n{}".format(label2prob))
        return label2prob

    # todo
    def get_both(self):
        pass


if __name__ == "__main__":
    # session读取
    session_handler = SessionHandler()
    session_collection = session_handler.get_session_collection()
    session_collection.shrink()
    sessions = session_collection.sessions

    # session表征
    represent_service = WESSBASRepresentationService(sessions)
    sessionid2vec = represent_service.represent()

    # session聚类
    kmeans_cluster = KMeansClusterService(sessionid2vec)
    labels, centroids, LABELS = kmeans_cluster.cluster()

    # intensity & mix
    wessbas_intensity = WESSBASIntensityService(sessions, sessionid2vec, labels)
    wessbas_intensity.build_workload_intensity()
    wessbas_intensity.build_behavior_mix()