from abc import abstractmethod

class BaseTransitionService:


    @abstractmethod
    def build(self):
        """
        构建模型
        :return:
        """
        pass

    @abstractmethod
    def sample(self):
        """
        从构建的模型中采样
        :return: [list of UserBehavior]
        """
        pass