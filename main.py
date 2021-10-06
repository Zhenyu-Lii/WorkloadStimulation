import collections
from dao.SessionHandler import SessionHandler
from service.representation.WESSBASRepresentationService import WESSBASRepresentationService
from service.cluster.KmeansClusterService import KMeansClusterService
from service.intensity.WESSBASIntensityService import WESSBASIntensityService
from service.transition.SimpleTransitionService import SimpleTransitionService

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

# workload intensity & behavior mix
wessbas_intensity = WESSBASIntensityService(sessions, sessionid2vec, labels)
intensity = wessbas_intensity.build_workload_intensity()
label2prob = wessbas_intensity.build_behavior_mix()

# behavior model
label2sessions = collections.defaultdict(lambda: {})
for i, (session_id, user_behaviors) in enumerate(sessions.items()):
    label2sessions[labels[i]][session_id] = user_behaviors
label2transition = {}
for label in LABELS:
    sessions_for_one_label = label2sessions[label]
    simple_transition = SimpleTransitionService(sessions_for_one_label)
    simple_transition.build()
    label2transition[label] = simple_transition
# todo:根据intensity、label2prob、label2transition采样，生成待执行的session

