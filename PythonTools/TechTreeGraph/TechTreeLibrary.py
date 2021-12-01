from numbers import Number

import graphviz
from graphviz import nohtml
from graphviz import Digraph
from multipledispatch import dispatch
from pypinyin import pinyin, lazy_pinyin, Style


class TechNode(object):
    """
        id : 标识符
        name: 名称
        detail_arr: 效果详情
        cost_time: 花费时间
        cost_gold_arr: 消耗黄金【最小，最大】
    """

    def __init__(self, name, detail_arr, cost_time, cost_gold_arr):
        """
        :param name: 名称
        :param detail_arr: 效果详情
        :param cost_time: 花费时间
        :param cost_gold_arr: 消耗黄金【最小，最大】
        """
        # self.id = ''.join([s.capitalize() for s in lazy_pinyin(name)])
        self.id = name
        print(self.id)
        self.cost_gold_arr = cost_gold_arr
        self.cost_time = cost_time
        self.detail_arr = detail_arr
        self.name = name

    def generate_node(self, graph):
        TechTreeHelper.get_tech_node(graph, self)


class TechTreeGraph(object):
    name: str
    graph: Digraph
    node_dict = {}

    def __init__(self, name):
        self.name = name
        self.graph = graphviz.Digraph('G', filename=self.name + ".gv", encoding="utf-8")
        self.graph.attr(rankdir="LR",ranksep='1')


    def add_node(self, name, detail_arr, cost_time, cost_gold_arr, former_nodes=[]):
        node = TechNode(name,detail_arr,cost_time,cost_gold_arr)
        node.generate_node(self.graph)
        self.node_dict[node.id] = node
        for n in former_nodes:
            self.link(n,node.id)

    def link(self, *nodes):
        """
        :param graph:
        :param node0:
        :param node1:
        """
        for i in range(1, len(nodes)):
            self.graph.edge(nodes[i-1]+":e", nodes[i]+":w",len='2.00')

    def render(self):
        self.graph.render(self.name+'.dot', format='jpg',view=True)

    def view(self):
        self.graph.view(quiet=True)

    def save(self):
        self.graph.render(format='svg').replace('\\', '/')

    def __str__(self):
        return str(self.graph)




class TechTreeHelper(object):
    @staticmethod
    @dispatch(Digraph, TechNode)
    def get_tech_node(graph, tech_node):
        """
        :type tech_node: TechNode
        """
        TechTreeHelper.get_tech_node(graph, tech_node.id, tech_node.name, tech_node.detail_arr, tech_node.cost_time,
                                    tech_node.cost_gold_arr)

    @staticmethod
    @dispatch(Digraph, str, str, list, Number, list)
    def get_tech_node(graph, id, name, detail_arr, cost_time, cost_gold_arr):
        """
        :param graph:
        :param id:
        :param name:
        :param detail_arr:
        :param cost_time:
        :param cost_gold_arr:
        """
        label_str = name + "|" + "{<f0>" + str(cost_time) + "秒| <f1>" + str(cost_gold_arr) + " 黄金 }|" + TechTreeHelper.clean_label_str(("\l").join(detail_arr)) + "\l"
        graph.node(id, nohtml(label_str), shape='record', fontname="SimSun")


    @staticmethod
    def generate_nodes(graph, node_list):
        """

        :param graph:
        :param node_list:
        """
        for n in node_list:
            TechTreeHelper.get_tech_node(graph, n)\

    @staticmethod
    def clean_label_str(s):
        return s.replace('->','-\>').replace('|>','\|\>').replace('+>','\+\>').replace('X>','\X\>')
