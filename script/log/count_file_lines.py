import json
import os

workspace_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
date_dir_path = os.path.join(workspace_dir_path, 'dataset', '2021-Bizseer', '2021-07-09')
trace_file_path = os.path.join(date_dir_path, 'trace', 'jaeger-span_2021-07-09.tar')
service_file_path = os.path.join(date_dir_path, 'log', 'filebeat-testbed-log-service_2021.07.09.tar')

# 统计字段信息
def ref_count(file_path):
    refType_set = set()
    references_num = set()
    operationName_set = set()
    count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i > 500000:
                break
            data = json.loads(line)
            references = data["_source"]["references"]
            references_num.add(len(references))
            if len(references) == 0:
                count += 1
                operationName_set.add(data["_source"]["operationName"])
            for r in references:
                refType_set.add(r["refType"])
    print(refType_set)
    print(references_num)
    print(count)
    print(operationName_set)


# 统计文件行数
def buff_count(file_path):
    with open(file_path, 'rb') as f:
        count = 0
        buf_size = 1024 * 1024 # 1 MB
        buf = f.read(buf_size)
        iter_count = 0
        while buf:
            count += buf.count(b'\n')
            buf = f.read(buf_size)
            iter_count += 1
            if iter_count == 100:
                break
        print("{} lines for {} MB".format(count // 100, buf_size / (1024 ** 2)))

ref_count(trace_file_path)