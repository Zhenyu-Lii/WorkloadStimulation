from abc import abstractmethod

class BaseIntensityService:


    @abstractmethod
    def build_workload_intensity(self):
        """
        构建workload intensity
        :return:
        """
        pass

    @abstractmethod
    def build_behavior_mix(self):
        """
        构建behavior mix
        :return:
        """
        pass

    @abstractmethod
    def get_both(self):
        """
        输入时间戳或时间段，返回对应的workload intensity以及behavior mix
        :return:
        """
        pass