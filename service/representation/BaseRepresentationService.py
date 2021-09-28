from abc import abstractmethod, ABCMeta

class BaseRepresentationService:
    """
    基类，用于完成用户行为的向量化
    """

    @abstractmethod
    def represent(self):
        """
        return:
            A dict mapping session IDs to the corresponding session representations.
            For example:

             {'8ead3831c21ed055a29295ea6776d62c': [0, 1, 3, 0],
              'b6e69f8f834d7aa1647bdd3d60072368': [1, 0, 0, 2]}
        """
        pass
