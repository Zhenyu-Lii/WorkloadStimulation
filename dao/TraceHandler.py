import pymongo
from config.MongoConfig import mongo_config


class TraceHandler:
    """
    database: histershop-trace
    collection: span
    """

    def __init__(self):
        self.mongo_client = mongo_config.mongo_client
        self.trace_db = mongo_config.trace_db
        self.trace_collection = mongo_config.trace_collection

    def get_trace_id_list(self):
        """
        获取全部traceID
        :return: traceID列表
        """
        result = []
        client = pymongo.MongoClient(self.mongo_client)
        span_db = client[self.trace_db][self.trace_collection]
        for temp in span_db.aggregate([{'$group': {'_id': '$traceID'}}]):
            result.append(temp['_id'])
        client.close()
        return result

    def get_trace_spans_by_id(self, traceID):
        """
        根据traceID查找整个调用链的span信息
        :return: span列表
        """
        result = []
        client = pymongo.MongoClient(self.mongo_client)
        span_db = client[self.trace_db][self.trace_collection]
        for temp in span_db.find({"traceID": traceID}):
            result.append(temp)
        client.close()
        return result