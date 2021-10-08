import numpy as np
import collections
import time
import matplotlib.pyplot as plt
from dao.SessionHandler import SessionHandler
from config.SessionConfig import session_config
from service.cluster.KmeansClusterService import KMeansClusterService
from service.representation.WESSBASRepresentationService import WESSBASRepresentationService
from service.cluster.BaseClusterService import BaseClusterService
import arrow


class WESSBASIntensityService:
    """
    在这个类完成workload intensity与behavior mix
    """

    def __init__(self, sessions, sessionid2vec, labels, interval_type, t_interval):
        """
        interval_type: 时间间隔类型，可为：
        year(s), month(s), day(s), hour(s), minute(s),
        second(s), microsecond(s), week(s), quarter(s)
        其中的一种

        t_interval: 时间间隔大小
        """
        self.sessions = sessions
        self.sessionid2vec = sessionid2vec
        self.labels = labels
        self.message_texts = session_config.message_texts
        self.message_dict = session_config.message_dict
        self.interval_type = interval_type
        self.t_interval = t_interval
        self.intensities = self.build_workload_intensity()

    def build_workload_intensity(self):
        # 目前用了shrink()后的sessions而非shrink()前的，需要分析一下是否合理
        session_intensity = collections.defaultdict(list)
        first_timestamp = (list(sessions.values()))[0][0].timestamp  # '2021-07-09T10:16:49.338460317Z'
        first_timestamp = arrow.get(first_timestamp)
        start_timestamp = first_timestamp.floor('day')
        end_timestamp = first_timestamp.ceil('day')
        for timespan in arrow.Arrow.interval(self.interval_type, start_timestamp, end_timestamp, self.t_interval):
            session_intensity[timespan] = []

        for session_id, user_behaviors in self.sessions.items():
            start_user_behavior = user_behaviors[0]
            a = start_user_behavior.timestamp  # '2021-07-09T10:16:49.338460317Z'
            timestamp = arrow.get(a)
            for timespan, session_ids in session_intensity.items():
                if timespan[0] <= timestamp <= timespan[1]:
                    session_ids.append(session_id)

        intensity = np.zeros(24 * 3600, dtype=int)
        for k, v in session_intensity.items():
            hour = k[0].hour
            minutes = k[0].minute
            second = k[0].second
            intensity[hour * 3600 + minutes * 60 + second] = len(v)
            session_intensity[k] = len(v)
        plt.plot(intensity, label="session start")
        plt.legend()
        plt.savefig("intensity.png")
        return session_intensity

    def build_behavior_mix(self):
        counter = collections.Counter(self.labels)
        label2prob = {}
        for key in sorted(counter.keys()):
            prob = round(counter[key] / len(self.labels), 4)
            label2prob[key] = prob
        print("behavior mix for one day:\n{}".format(label2prob))
        return label2prob

    def get_intensity_by_timestamp(self, timestamp):
        for key, intensity in self.intensities.items():
            if key[0] <= timestamp <= key[1]:
                return intensity
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
    wessbas_intensity = WESSBASIntensityService(sessions, sessionid2vec, labels, 'hours', 1)
    # print(wessbas_intensity.get_intensity_by_timestamp(arrow.get('2021-07-09T11:16:49.338460317Z')))
    wessbas_intensity.build_behavior_mix()
