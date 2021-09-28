from itertools import chain
import collections
from dao.SessionHandler import SessionHandler
from config.SessionConfig import session_config
from service.representation.BaseRepresentationService import BaseRepresentationService


class WESSBASRepresentationService(BaseRepresentationService):
    """
    论文WESSBAS提出用户行为向量化方法
    """

    def __init__(self, sessions):
        self.sessions = sessions
        self.message_texts = session_config.message_texts
        self.message_dict = session_config.message_dict

    def represent(self):
        n = len(self.message_texts)
        sessionid2vec = collections.OrderedDict()
        for session_id, user_behaviors in self.sessions.items():
            last = None
            matrix = [[0] * n for _ in range(n)]
            for user_behavior in user_behaviors:
                cur = self.message_dict[user_behavior.message]
                if last:
                    matrix[last][cur] += 1
                last = cur
            vector = list(chain.from_iterable(matrix))
            sessionid2vec[session_id] = vector
        return sessionid2vec

if __name__ == "__main__":
    # session读取
    session_handler = SessionHandler()
    session_collection = session_handler.get_session_collection()
    session_collection.shrink()
    sessions = session_collection.sessions

    # session表征
    represent_service = WESSBASRepresentationService(sessions)
    sessionid2vec = represent_service.represent()