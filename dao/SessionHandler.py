import pymongo
from config.MongoConfig import mongo_config
from entity.SessionGroup import SessionGroup


class SessionHandler:
    """
    database: histershop-log
    collection: session
    """

    def __init__(self):
        self.mongo_client = mongo_config.mongo_client
        self.log_db = mongo_config.log_db
        self.session_log_collection = mongo_config.session_log_collection

    def get_session_collection(self):
        session_list = SessionGroup()
        client = pymongo.MongoClient(self.mongo_client)
        span_db = client[self.log_db][self.session_log_collection]
        for i, doc in enumerate(span_db.find(), start=1):
            session_list.add_session(doc)
            if i % 10000 == 0:
                print("{} sessions has been loaded".format(i))
        client.close()
        return session_list
