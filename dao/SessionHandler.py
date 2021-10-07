import pymongo
from config.MongoConfig import mongo_config
from entity.SessionCollection import SessionCollection


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
        """
        获取全部session
        :return:
        """
        session_collection = SessionCollection()
        client = pymongo.MongoClient(self.mongo_client)
        span_db = client[self.log_db][self.session_log_collection]
        for i, doc in enumerate(span_db.find(), start=1):
            session_collection.add_session(doc)
            if i % 10000 == 0:
                print("{} sessions has been loaded".format(i))
        client.close()
        return session_collection

    def get_test_session_collection(self):
        """
        获取部分用于测试的session
        """
        session_collection = SessionCollection()
        client = pymongo.MongoClient(self.mongo_client)
        span_db = client[self.log_db][self.session_log_collection]
        for i, doc in enumerate(span_db.find(), start=1):
            session_collection.add_session(doc)
            if i % 1000 == 0:
                print("1000 sessions has been loaded.")
                break
        client.close()
        return session_collection

