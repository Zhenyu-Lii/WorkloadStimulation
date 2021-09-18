"""
本脚本根据关键词过滤'log-service-2w-lines.txt'中的service日志，
从而将日志划分至不同的前端路由以及后端service下。
"""
import os

workspace_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
file_path = os.path.join(workspace_dir_path, 'WS-log-analysis', 'log-service-2w-lines.txt')

write_file_path = os.path.join(workspace_dir_path, 'WS-log-analysis', 'log_classification', 'filter.txt')
lines = []
with open(file_path, 'r') as f:
    keywords = ["Microsoft", "session", "Async",
                "currencyservice", "payment", "recommendationservice", "emailservice",
                "GetQuote", "ShipOrder", "PlaceOrder", "ad request", "email"]
    for line in f:
        if any(word in line for word in keywords):
            continue
        if line.startswith("      "):
            continue
        lines.append(line)
with open(write_file_path, 'w') as f:
    for line in lines:
        f.write(line)
print(len(lines))
