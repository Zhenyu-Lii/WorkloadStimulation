from dao.SessionHandler import SessionHandler
from config.SessionConfig import session_config
from service.transition.BaseTransitionService import BaseTransitionService

class SimpleTransitionService(BaseTransitionService):
    """
    最直观的transition方法
    """

    def __init__(self, sessions):
        self.sessions = sessions
        self.message_texts = session_config.message_texts
        self.message_dict = session_config.message_dict

    def build(self):
        self.start_prob = self.calc_start_prob()
        self.transition_prob = self.calc_transition_prob()
        self.end_prob = self.calc_end_prob()

    # todo: sample a sequence from the transition model
    def sample(self):

        pass


    def calc_start_prob(self):
        """
        计算初始概率
        :return:
        """
        n = len(self.message_texts)
        start_count = [0] * n
        for session_id, user_behaviors in self.sessions.items():
            for user_behavior in user_behaviors:
                cur = self.message_dict[user_behavior.message]
                start_count[cur] += 1
                break
        start_prob = [round(v / sum(start_count), 4) for v in start_count]
        print("start prob:\n {}".format(start_prob))
        return start_prob

    def calc_transition_prob(self):
        """
        计算转移概率
        :return:
        """
        n = len(self.message_texts)
        transition_count = [[0] * n for _ in range(n)]
        for session_id, user_behaviors in self.sessions.items():
            last = None
            for user_behavior in user_behaviors:
                cur = self.message_dict[user_behavior.message]
                if last:
                    transition_count[last][cur] += 1
                last = cur
        transition_prob = [[round(v / sum(row), 4) if sum(row) else 0 for v in row] for row in transition_count]
        print("transition prob:\n {}".format(transition_prob))
        return transition_prob

    def calc_end_prob(self):
        """
        计算终止概率
        :return:
        """
        n = len(self.message_texts)
        end_count = [0] * n
        for session_id, user_behaviors in self.sessions.items():
            for user_behavior in user_behaviors[::-1]:
                cur = self.message_dict[user_behavior.message]
                end_count[cur] += 1
                break
        end_prob = [round(v / sum(end_count), 4) for v in end_count]
        print("end prob:\n {}".format(end_prob))
        return end_prob

if __name__ == "__main__":
    # session读取
    session_handler = SessionHandler()
    session_collection = session_handler.get_session_collection()
    session_collection.shrink()
    sessions = session_collection.sessions


    simple_transition = SimpleTransitionService(session)
    simple_transition.calc_start_prob()
    simple_transition.calc_transition_prob()
    simple_transition.calc_end_prob()