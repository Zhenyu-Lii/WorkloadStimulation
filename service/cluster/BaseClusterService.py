from abc import abstractmethod

class BaseClusterService:
    """
    基类，用于完成用户行为的聚类
    """

    @abstractmethod
    def cluster(self):
        pass
