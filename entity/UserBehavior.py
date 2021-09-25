from config.SessionConfig import session_config

class UserBehavior:
    """
    database: histershop-log
    collection: session
    column: user_behaviors
    """

    def __init__(self, doc):
        """
        :param doc: user_behaviors字段下的一个元素
        """
        self.user_behavior = doc
        self.http_req_method = doc["http.req.method"]
        self.http_req_path = doc["http.req.path"]
        self.message = doc["message"]
        self.timestamp = doc["timestamp"]

        self.params = {}
        for k, v in doc.items():
            if k in session_config.param_set:
                self.params[k] = v


