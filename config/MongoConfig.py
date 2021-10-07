class MongoConfig:

    def __init__(self):
        self.mongo_client = 'mongodb://mongoadmin:mongoadmin@10.60.38.173:27017'
        self.trace_db = 'hipstershop-trace'
        self.trace_collection = 'span'
        self.log_db = 'hipstershop-log'
        self.service_log_collection = 'service-log'
        self.service_frontend_log_collection = 'frontend-log'  # 本质上是service-log经提取后的子集
        self.session_log_collection = 'session'  # 每一个文档代表一个session下的所有用户行为

mongo_config = MongoConfig()