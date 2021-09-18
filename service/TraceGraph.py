import collections
import networkx as nx
import matplotlib.pyplot as plt
from dao.DataHandler import DataHandler
from entity.Span import Span
from entity.Trace import Trace

"""常见mongodb查询语句
{'operationName':{$regex:/Empty/}}
"""

class TraceGraph:
    def __init__(self):
        self.data_handler = DataHandler()

    def create_graph(self, trace):
        g = nx.DiGraph()
        create_success = True
        edge2weight = collections.defaultdict(int)
        parent_num = 0
        for id in trace.id2span.keys():
            child = trace.id2span[id]
            if child.parentSpanID == None:
                parent_num += 1
                continue
            else:
                if child.parentSpanID in trace.id2span:
                    parent = trace.id2span[child.parentSpanID]
                    c = child.operationName.split('/')[-1]
                    p = parent.operationName.split('/')[-1]
                    edge2weight[(c, p)] += 1

                else:
                    create_success = False
        assert parent_num == 1
        cycles = 0
        for (c, p), w in edge2weight.items():
            g.add_edge(p, c, weight=w)
            if c == p:
                cycles += w
                print("{}--->{} : {}".format(p, c, w))
        self.g = g
        print("******\ncreate_success: {}".format(create_success))
        print("total span num ({}) = parent (1) + cycles ({}) + draw ({})".
              format(len(trace.id2span), cycles, sum(edge2weight.values())-cycles))
        print("parent: {}".format(trace.root_span.operationName))
        return g

    def draw(self, g):
        plt.figure(figsize=(10, 10))
        edge_labels = {(i, j): w['weight'] for i, j, w in self.g.edges(data=True)}
        pos = nx.spring_layout(g, k = 0.2)
        nx.draw_networkx_nodes(g, pos, node_size=300, alpha=0.8)
        nx.draw_networkx_labels(g, pos, font_size=10, font_color='purple')
        nx.draw_networkx_edges(g, pos, edge_labels.keys(), arrowsize=14)
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=10, font_color="red")
        plt.savefig("trace.png")

    def draw_trace(self, traceID):
        trace = Trace(traceID=traceID)
        span_list = self.data_handler.get_trace_spans_by_id(traceID)
        for span in span_list:
            traceID = span["traceID"]
            spanID = span["spanID"]
            operationName = span["operationName"]
            startTime = span["startTime"]
            duration = span["duration"]
            references = span["references"]
            if len(references) == 0:
                parentSpanID = None
            else:
                parentSpanID = references[0]["spanID"]
            span = Span(traceID, spanID, operationName, parentSpanID, startTime, duration)
            trace.add_span(span)
        g = self.create_graph(trace)
        self.draw(g)

if __name__ == '__main__':
    trace_graph = TraceGraph()
    trace_graph.draw_trace('8ead3831c21ed055a29295ea6776d62c')

