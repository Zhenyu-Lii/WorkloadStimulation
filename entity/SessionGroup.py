from entity.UserBehavior import UserBehavior
from config.SessionConfig import session_config

class SessionGroup:
    """
    database: histershop-log
    collection: session
    """

    def __init__(self):
        """
        :param doc: mongo session中的doc
        """
        self.sessions = {}  # key: session_id, value: user_behaviors

    def add_session(self, doc):
        session_id = doc["session"]
        user_behaviors = []
        for d in doc["user_behaviors"]:
            user_behaviors.append(UserBehavior(d))
        self.sessions[session_id] = user_behaviors

    def shrink(self):
        """
        由于每个用户行为在日志中均对应3～4条user behavior，此处去除冗余的user behavior
        :return:
        """
        _sessions = {}
        for session_id, user_behaviors in self.sessions.items():
            arr = []
            for user_behavior in user_behaviors:
                if user_behavior.message in session_config.message_dict:
                    arr.append(user_behavior)
            _sessions[session_id] = arr
        self.sessions = _sessions
