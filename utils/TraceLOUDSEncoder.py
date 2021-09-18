from queue import Queue


class TraceLOUDSEncoder:
    def __init__(self):
        self.operation_name_list = []

    def LOUDS_encoding(self, span_list):
        encoding_result_dict = {
            'operation_index': '',
            'n_coding': '10',
            'start_time': ''
        }

        span_list = sorted(span_list, key=lambda x: x['startTime'])
        root_span_id = ""

        span_set = set()
        span_id_dict = dict()
        for i in range(len(span_list)):
            if span_list[i]['spanID'] not in span_set:
                span_set.add(span_list[i]['spanID'])  # 去重
                span_id_dict[span_list[i]['spanID']] = i  # 提取出spanID所在的位置

        relation_list = []
        for span in span_list:
            if span['operationName'] not in self.operation_name_list:
                self.operation_name_list.append(span['operationName'])

            if len(span['references']) == 0:
                root_span_id = span['spanID']
                encoding_result_dict['start_time'] = span['startTime']
            else:
                parent_span_id = span['references'][0]['spanID']
                relation_list.append((parent_span_id, span['spanID']))

        span_queue = Queue()
        span_queue.put(root_span_id)
        while span_queue.qsize() > 0:
            span_id = span_queue.get()
            if encoding_result_dict['operation_index'] != '':
                encoding_result_dict['operation_index'] += '-'
            encoding_result_dict['operation_index'] += str(self.operation_name_list.index(span_list[span_id_dict[span_id]]['operationName']))

            for relation in relation_list:
                if relation[0] == span_id:
                    span_queue.put(relation[1])
                    encoding_result_dict['n_coding'] += '1'
            encoding_result_dict['n_coding'] += '0'

        return encoding_result_dict
