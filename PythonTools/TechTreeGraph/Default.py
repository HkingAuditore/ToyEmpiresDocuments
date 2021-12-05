import graphviz

from TechTreeGraph.TechTreeLibrary import TechNode, TechTreeHelper, TechTreeGraph

tech_tree_name = "default"
g = TechTreeGraph(tech_tree_name)
g.add_node("手推车", ["提高工人速度", "减少卸货时间"], 20, [10, 20], node_type="ECO")
g.add_node("水利", ["提高食物采集量", "降低食物采集时间"], 20, [10, 20],former_nodes=["手推车"], node_type="ECO")
g.add_node("采矿", ["提高矿物采集量", "降低矿物采集时间"], 10, [10, 20],former_nodes=["手推车"])
g.add_node("行政机构", ["提高工人人口上限", "提高工人生产速度","+>【仓库】"], 10, [10, 20],former_nodes=["手推车"], node_type="ECO")
g.add_node("农学", ["提高食物采集量","+>【农庄】"], 10, [10, 20],former_nodes=["水利","行政机构"], node_type="ECO")
g.add_node("历法", ["提高食物采集量"], 10, [10, 20],former_nodes=["农学"], node_type="ECO")
g.add_node("矿井勘探", ["提高矿物采集量","+>【矿场】"], 10, [10, 20],former_nodes=["采矿","行政机构"], node_type="ECO")
g.add_node("化学", ["提高矿物采集量"], 10, [10, 20],former_nodes=["矿井勘探"], node_type="ECO")
g.add_node("教育", ["提高科研速度","提高单位生产力","提高工人人口上限","提高军事人口上限"], 10, [10, 20],former_nodes=["行政机构"], node_type="ECO")
g.add_node("经济", ["提高工人人口上限","提高军事人口上限","提高单位生产力","+>【市场】"], 10, [10, 20],former_nodes=["教育"], node_type="ECO")
g.add_node("工程技术", ["提高建筑速度","提高单位生产力","提高工人人口上限","提高军事人口上限"], 10, [10, 20],former_nodes=["经济"], node_type="ECO")
g.add_node("交通运输", ["提高工人人口上限","提高军事人口上限","提高单位生产力","+>【补给站】"], 10, [10, 20],former_nodes=["经济"], node_type="ECO")

g.add_node("军事训练", ["X>【民兵】", "+>【剑士】", "+>【长矛兵】"], 20, [10, 20], node_type="MIL")
g.add_node("战术", ["+>【弓箭手】"], 20, [10, 20],former_nodes=["军事训练"], node_type="MIL")
g.add_node("马镫", ["+>【骑手】"], 20, [10, 20],former_nodes=["战术"], node_type="MIL")
g.add_node("医药", ["+>【军医】"], 20, [10, 20], former_nodes=["战术"], node_type="MIL")
g.add_node("军事工程", ["+>【拒马】","+>【堡垒】"], 30, [10, 20], former_nodes=["马镫"], node_type="MIL")
g.add_node("攻城器械", ["+>【冲车】","+>【投石机】"], 30, [10, 20], former_nodes=["军事工程"], node_type="MIL")
g.add_node("火药", ["+>【火门枪手】"], 20, [10, 20], former_nodes=["攻城器械"], node_type="MIL")
g.add_node("火炮", ["+>【火炮】"], 20, [10, 20], former_nodes=["火药"], node_type="MIL")


g.add_node("军功制", ["提高步兵攻击力","提高步兵防御力","+>【兵营】"], 30, [10, 20], former_nodes=["军事训练"], node_type="MIL")
g.add_node("复合弓", ["提高远程单位攻击力","提高射击距离","+>【靶场】"], 30, [10, 20], former_nodes=["战术"], node_type="MIL")
g.add_node("马匹育种", ["提高骑兵速度","降低骑兵价格","+>【马厩】"], 30, [10, 20], former_nodes=["马镫"], node_type="MIL")
g.add_node("军事技术", ["提高攻城器械生产速度","降低攻城器械价格","+>【兵工厂】"], 30, [10, 20], former_nodes=["攻城器械"], node_type="MIL")

g.add_node("手工业", ["提高攻击力","提高防御力","+>【铁匠铺】"], 30, [10, 20], node_type="SCI")
g.add_node("铸造", ["提高攻击力","提高攻击速度"], 30, [10, 20], former_nodes=["手工业"], node_type="SCI")
g.add_node("冶金", ["提高攻击力"], 30, [10, 20], former_nodes=["铸造"], node_type="SCI")
g.add_node("锁子甲", ["提高防御力","提高速度"], 30, [10, 20], former_nodes=["手工业"], node_type="SCI")
g.add_node("板甲", ["提高防御力"], 30, [10, 20], former_nodes=["锁子甲"], node_type="SCI")



print(g)
g.save()