from abc import abstractmethod, ABCMeta

class BaseRepresentationService:
    """
    基类，用于完成用户行为的向量化
    """

    @abstractmethod
    def represent(self):
        pass
