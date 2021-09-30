from abc import abstractmethod

class BaseTransitionService:


    @abstractmethod
    def build(self):
        """
        构建概率图形式的behavior model
        """
        pass

    @abstractmethod
    def sample(self):
        """
        从构建的behavior model中采样
        输出：[list of UserBehavior]
        """
        pass