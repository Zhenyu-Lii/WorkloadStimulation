import numpy as np
import collections
import time
import matplotlib.pyplot as plt
from dao.SessionHandler import SessionHandler
from config.SessionConfig import session_config
from service.cluster.KmeansClusterService import KMeansClusterService


class WESSBASIntensityService:
    """
    在这个类完成workload intensity与behavior mix
    """

    def __init__(self):
        self.message_texts = session_config.message_texts
        self.message_dict = session_config.message_dict

    def workload_intensity(self):
        session_handler = SessionHandler()
        session_group = session_handler.get_session_collection()
        self.sessions = session_group.sessions
        session_start = collections.defaultdict(list)
        for session_id, user_behaviors in self.sessions.items():
            for user_behavior in user_behaviors:
                a = user_behavior.timestamp  # '2021-07-09T10:16:49.338460317Z'
                timestamp = time.strptime(a.split(".")[0], '%Y-%m-%dT%H:%M:%S')
                h = timestamp.tm_hour
                m = timestamp.tm_min
                s = timestamp.tm_sec
                total_s = h * 3600 + m * 60 + s
                session_start[total_s].append(session_id)
        start = np.zeros(24 * 3600, dtype=int)
        for k, v in session_start.items():
            start[k] = len(v)
        plt.plot(start, label="session start")
        plt.legend()
        plt.savefig("intensity.png")

    def behavior_mix(self):
        kmeans_cluster = KMeansClusterService()
        results = kmeans_cluster.cluster()
        count = [len(v) for v in results.values()]
        prob = [round(v / sum(count), 4) for v in count]
        print("behavior mix for one day:\n{}".format(prob))



if __name__ == "__main__":
    wessbas_intensity = WESSBASIntensityService()
    # wessbas_intensity.workload_intensity()
    wessbas_intensity.behavior_mix()