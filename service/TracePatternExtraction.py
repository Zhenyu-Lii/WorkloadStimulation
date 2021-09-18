import os
import sys

sys.path.append("/workspace/code")

import json
from dao.DataHandler import DataHandler
from utils.TraceLOUDSEncoder import TraceLOUDSEncoder


class TracePatternExtraction:
    def __init__(self):
        self.data_handler = DataHandler()
        self.trace_LOUDS_encoder = TraceLOUDSEncoder()

        self.trace_pattern_time_series = dict()
        self.result_base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'result')
        if not os.path.exists(self.result_base_path):
            os.mkdir(self.result_base_path)
        self.result_base_path = os.path.join(self.result_base_path, 'trace_pattern')
        if not os.path.exists(self.result_base_path):
            os.mkdir(self.result_base_path)

    def extract_shape_pattern(self):
        trace_id_list = self.data_handler.get_trace_id_list()
        i = 0
        for trace_id in trace_id_list:
            i += 1
            if i % 1000 == 0:
                print(str(i) + '\n')
            span_list = self.data_handler.get_trace_spans_by_id(trace_id)
            if isinstance(span_list, list):
                encoding_result_dict = self.trace_LOUDS_encoder.LOUDS_encoding(span_list)
                identifier = encoding_result_dict['operation_index'] + '::' + encoding_result_dict['n_coding']
                if identifier not in self.trace_pattern_time_series.keys():
                    self.trace_pattern_time_series[identifier] = {
                        encoding_result_dict['start_time']: 1
                    }
                else:
                    if encoding_result_dict['start_time'] not in self.trace_pattern_time_series[identifier]:
                        self.trace_pattern_time_series[identifier][encoding_result_dict['start_time']] = 1
                    else:
                        self.trace_pattern_time_series[identifier][encoding_result_dict['start_time']] += 1
        with open(os.path.join(self.result_base_path, 'operation_name.json'), 'w') as f:
            json.dump({"operation_name": list(self.trace_LOUDS_encoder.operation_name_list)}, f, indent=4)
        with open(os.path.join(self.result_base_path, 'patterns.json'), 'w') as f:
            json.dump({"patterns": list(self.trace_pattern_time_series.keys())}, f, indent=4)
        with open(os.path.join(self.result_base_path, 'pattern_timeseries.json'), 'w') as f:
            json.dump(self.trace_pattern_time_series, f, indent=4)


if __name__ == '__main__':
    trace_pattern_extraction = TracePatternExtraction()
    trace_pattern_extraction.extract_shape_pattern()
