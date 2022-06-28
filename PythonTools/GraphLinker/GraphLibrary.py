import math

import matplotlib.pyplot as plt
import networkx as nx


class Path(object):
    def __init__(self, a, b, distance):
        self.a = a
        self.b = b
        self.distance = distance


class PathGraph(object):

    def __init__(self, scale=50.0):
        self.nodes = []
        self.paths = []
        self.graph = nx.Graph()
        self.scale = scale

    def add_node(self, node_name):
        self.nodes.append(node_name)

    def add_path(self, a, b, distance):
        if not a in self.nodes:
            self.add_node(a)
        if not b in self.nodes:
            self.add_node(b)
        self.paths.append(Path(a, b, distance))

    def render(self):
        self.graph.add_nodes_from(self.nodes)
        min_path_length = min(self.paths, key=lambda e: e.distance).distance
        for edge in self.paths:
            self.graph.add_edge(edge.a, edge.b, length=int((edge.distance / min_path_length) * self.scale))
        pos = nx.spring_layout(self.graph, scale=3)

        tmp_dis = 99999
        center_node = 0
        for (k, p) in pos.items():
            if (p[0] ** 2 + p[1] ** 2) < tmp_dis:
                center_node = k
                tmp_dis = p[0] ** 2 + p[1] ** 2

        pos_dict = {}
        for (k, p) in pos.items():
            if k != center_node:
                if len(list(filter(lambda n: n.a == k or n.b == k, self.paths))) != 0:
                    l = list(filter(lambda n: n.a == k or n.b == k, self.paths))
                    l_c = list(filter(lambda n: n.a == center_node or n.b == center_node, l))
                    if len(l_c) != 0:
                        d = l_c[0].distance
                        pos_dict[k] = p * (math.log2(d / min_path_length) + 1)
                    else:
                        pos_dict[k] = p
            else:
                pos_dict[k] = p

        options = {
            "font_size": 8,
            "node_size": 200,
            "node_color": "white",
            "font_color": "black",
            "edgecolors": "black",
            "linewidths": 2.5,
            "width": 2.5,
        }
        nx.draw_networkx(self.graph, pos_dict, **options)
        edge_labels = dict([((p.a, p.b), f'{int(p.distance)}')
                            for p in self.paths])
        nx.draw_networkx_edge_labels(
            self.graph, pos_dict,
            edge_labels=edge_labels,
            font_color='red',
            font_size=8,
            label_pos=0.5
        )
        ax = plt.gca()
        ax.margins(0.20)
        plt.axis("off")
        plt.show()
