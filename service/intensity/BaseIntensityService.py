from abc import abstractmethod

class BaseIntensityService:


    @abstractmethod
    def build_workload_intensity(self):
        """
        构建按时间段划分的workload intensity
        输入：时间段t_interval（n秒、n分钟）
        输出：intensity时间序列，每个元素依次对应一个t_interval
        """
        pass

    @abstractmethod
    def build_behavior_mix(self):
        """
        构建behavior mix
        输出:各label对应的概率
        """
        pass

    @abstractmethod
    def intensity_and_mix_by_tinterval(self):
        """
        需要按时间段划分的workload intensity
        输入：时间段t_interval（n秒、n分钟）、时间段在一天中的index
        输出：对应的workload intensity以及behavior mix
        """
        pass