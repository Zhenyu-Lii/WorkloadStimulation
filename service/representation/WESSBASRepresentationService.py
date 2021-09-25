from itertools import chain
from dao.SessionHandler import SessionHandler
from config.SessionConfig import session_config
from service.representation.BaseRepresentationService import BaseRepresentationService


class WESSBASRepresentationService(BaseRepresentationService):
    """
    论文WESSBAS提出用户行为向量化方法
    """

    def __init__(self):
        session_handler = SessionHandler()
        session_group = session_handler.get_session_collection()
        session_group.shrink()
        self.sessions = session_group.sessions
        self.message_texts = session_config.message_texts
        self.message_dict = session_config.message_dict

    def represent(self):
        n = len(self.message_texts)
        sessionid2vec = {}
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
