import os
import pymongo
import json
import collections


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
        self.service_frontend_log_collection = 'frontend-log'  # 本质上是service-log经提取后的子集
        self.session_log_collection = 'session'  # 每一个文档代表一个session下的所有用户行为

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

    def save_frontend_log_in_mongo(self):
        """
        存储filebeat-testbed-log-service中的前端日志（也就是包含session参数的service日志）
        """
        client = pymongo.MongoClient(self.mongo_client)
        service_log_db = client[self.log_db][self.service_log_collection]
        frontend_log_db = client[self.log_db][self.service_frontend_log_collection]
        count = iters = 0
        for doc in service_log_db.find():
            iters += 1
            if iters % 100000 == 0:
                print(int(iters // 100000))
            if "session" in doc["message"]:
                message_dict = json.loads(doc["message"])
                frontend_log_db.insert_one(message_dict)
                count += 1
        print("count:{}".format(count))
        client.close()

    def save_session_in_mongo(self):
        """
        将相同session的日志存储在同一个文档中
        """
        client = pymongo.MongoClient(self.mongo_client)
        frontend_log_db = client[self.log_db][self.service_frontend_log_collection]
        session_db = client[self.log_db][self.session_log_collection]
        d = collections.defaultdict(list)
        for doc in frontend_log_db.find():
            session = doc['session']
            doc.pop('session')
            doc.pop('_id')
            d[session].append(doc)
        session_db.remove()
        for session in d.keys():
            d[session].sort(key=lambda doc: doc['timestamp'])
            new_doc = {'session': session,
                       'user_behaviors': d[session]}
            session_db.insert_one(new_doc)
        print("count:{}".format(len(d.keys())))
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

if __name__ == "__main__":
    data_handler = DataHandler()
    data_handler.save_session_in_mongo()