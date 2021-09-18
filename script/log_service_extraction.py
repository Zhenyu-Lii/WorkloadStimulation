import os
import json

"""
提取2w行filebeat-testbed-log-service下的日志
"""
class UserBehaviourExtraction:
    def __init__(self):
        temp_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        self.log_base_path = os.path.join(temp_path, 'dataset', '2021-Bizseer', '2021-07-09', 'log')
        pass

    def service_userid_extract(self):
        result_list = []
        with open(os.path.join(self.log_base_path, 'filebeat-testbed-log-service_2021.07.09.tar'), 'r') as f:
            i = 0
            while i < 20000:
                line = f.readline()
                if not line:
                    break
                else:
                    message_dict = json.loads(json.loads(line)['_source']['message'])
                    if "session" or "userId" in message_dict['message']:
                        result_list.append(message_dict['message'])
                        i += 1
                        pass

        with open('log-service-2w-lines.txt', 'w') as f:
            for result in result_list:
                f.write(result + '\n')
        f.close()

        # with open('template_log_service.json', 'w') as f:
        #     json.dump(result_list, f, indent=4)


if __name__ == '__main__':
    user_behaviour_extraction = UserBehaviourExtraction()
    user_behaviour_extraction.service_userid_extract()

