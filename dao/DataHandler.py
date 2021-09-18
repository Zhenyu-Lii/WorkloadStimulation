import os
import pymongo
import json


class DataHandler:
    def __init__(self):
        temp_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        self.log_base_path = os.path.join(temp_path, 'dataset', '2021-Bizseer', '2021-07-09', 'log')
        self.trace_base_path = os.path.join(temp_path, 'dataset', '2021-Bizseer', '2021-07-09', 'trace')

        self.mongo_client = 'mongodb://mongoadmin:mongoadmin@172.17.0.1:27017'
        self.trace_db = 'hipstershop-trace'
        self.trace_collection = 'span'
        self.log_db = 'hipstershop-log'
        self.service_log_collection = 'service-log'


    def save_trace_log_in_mongo(self):
        client = pymongo.MongoClient(self.mongo_client)
        span_db = client[self.trace_db][self.trace_collection]
        with open(os.path.join(self.trace_base_path, 'jaeger-span_2021-07-09.tar'), 'r') as f:
            while 1:
                line = f.readline()
                if not line:
                    break
                else:
                    message_dict = json.loads(line)['_source']
                    span_db.insert_one(message_dict)
        client.close()

    def save_service_log_in_mongo(self):
        client = pymongo.MongoClient(self.mongo_client)
        service_log_db = client[self.log_db][self.service_log_collection]
        with open(os.path.join(self.log_base_path, 'filebeat-testbed-log-service_2021.07.09.tar'), 'r') as f:
            while 1:
                line = f.readline()
                if not line:
                    break
                else:
                    message_dict = json.loads(json.loads(line)['_source']['message'])
                    service_log_db.insert_one(message_dict)
                    pass
        client.close()


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

