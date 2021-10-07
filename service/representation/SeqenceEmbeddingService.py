import pandas as pd
import collections
from sgt import SGT
from dao.SessionHandler import SessionHandler
from config.SessionConfig import session_config
from service.representation.BaseRepresentationService import BaseRepresentationService


class SequenceEmbeddingService(BaseRepresentationService):
    def __init__(self, sessions):
        self.sessions = sessions
        self.message_texts = session_config.message_texts
        self.message_dict = session_config.message_dict

    def represent(self):
        n = len(self.message_texts)
        id = []
        behaviors = []
        for session_id, user_behaviors in self.sessions.items():
            id.append(session_id)
            session_behavior = []
            for user_behavior in user_behaviors:
                cur = self.message_dict[user_behavior.message]
                session_behavior.append(cur)
            behaviors.append(session_behavior)
        corpus = pd.DataFrame({'id': id, 'sequence': behaviors})
        sgt = SGT(kappa=1,
                  flatten=True,
                  lengthsensitive=False,
                  mode='default')
        embedding = sgt.fit_transform(corpus)
        # print(embedding)
        sessionid2vec = collections.OrderedDict()
        for index, row in embedding.iterrows():
            # behavior_vec = []
            # for column in embedding.columns[1:]:
            #     behavior_vec.append(row[column])
            sessionid2vec[row['id']] = row.values[1:]
        return sessionid2vec


if __name__ == "__main__":
    # session读取
    session_handler = SessionHandler()
    session_collection = session_handler.get_test_session_collection()
    session_collection.shrink()
    sessions = session_collection.sessions

    # session表征
    represent_service = SequenceEmbeddingService(sessions)
    sessionid2vec = represent_service.represent()
    print(sessionid2vec)