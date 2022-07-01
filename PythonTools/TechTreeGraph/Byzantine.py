import graphviz

from TechTreeLibrary import TechNode, TechTreeHelper, TechTreeGraph

tech_tree_name = "Byzantine"

g = TechTreeGraph(tech_tree_name)
g.add_node("0016.手推车", ["提高工人速度", "减少卸货时间"], 20, [10, 20], node_type="ECO")
g.add_node("0017.水利", ["提高食物采集量", "降低食物采集时间"], 20, [10, 20],former_nodes=["0016.手推车"], node_type="ECO")
g.add_node("0018.行政机构", ["提高工人人口上限", "提高工人生产速度","+>【仓库】"], 10, [10, 20],former_nodes=["0016.手推车"], node_type="ECO")
g.add_node("0019.采矿", ["提高矿物采集量", "降低矿物采集时间"], 10, [10, 20],former_nodes=["0016.手推车"])
g.add_node("0020.农学", ["提高食物采集量","+>【农庄】"], 10, [10, 20],former_nodes=["0017.水利","0018.行政机构"], node_type="ECO")
g.add_node("0024.经济", ["提高工人人口上限","提高军事人口上限","提高单位生产力","+>【市场】"], 10, [10, 20],former_nodes=["0018.行政机构"], node_type="ECO")
g.add_node("0026.工程技术", ["提高建筑速度","提高单位生产力","提高工人人口上限","提高军事人口上限"], 10, [10, 20],former_nodes=["0024.经济"], node_type="ECO")
g.add_node("世界渴望之城", ["提高建筑速度","提高单位生产力","提高工人人口上限","提高军事人口上限","+>【圣索菲亚大教堂】"], 10, [10, 20],former_nodes=["0026.工程技术"], node_type="ECO")

g.add_node("军事训练", ["X>【民兵】", "+>【盾牌手】", "+>【长矛兵】"], 20, [10, 20], node_type="MIL")
g.add_node("0006.战术", ["+>【弓箭手】"], 20, [10, 20],former_nodes=["军事训练"], node_type="MIL")
g.add_node("希腊火", ["+>【希腊火喷射手】"], 20, [10, 20],former_nodes=["0006.战术"], node_type="MIL")
g.add_node("陶罐希腊火", ["+>【希腊火掷弹兵】"], 20, [10, 20],former_nodes=["希腊火"], node_type="MIL")
g.add_node("东正教", ["+>【僧侣】"], 20, [10, 20],former_nodes=["军事训练"], node_type="MIL")
g.add_node("牧首制", ["->【僧侣】","+>【牧首】"], 20, [10, 20],former_nodes=["东正教"], node_type="MIL")
g.add_node("0008.马镫", ["+>【骑兵】"], 20, [10, 20],former_nodes=["军事训练"], node_type="MIL")
g.add_node("骑枪", ["X>【骑兵】","+>【重骑兵】"], 20, [10, 20],former_nodes=["0008.马镫"], node_type="MIL")
g.add_node("重装战术", ["X>【重骑兵】","+>【甲胄骑士】"], 20, [10, 20],former_nodes=["骑枪"], node_type="MIL")
g.add_node("狄奥多西城墙", ["+>【石墙】"], 30, [10, 20], former_nodes=["0006.战术"], node_type="MIL")
g.add_node("0012.攻城器械", ["+>【冲车】"], 30, [10, 20], former_nodes=["狄奥多西城墙"], node_type="MIL")


g.add_node("0011.马匹育种", ["提高骑兵速度","降低骑兵价格","+>【马厩】"], 30, [10, 20], former_nodes=["重装战术"], node_type="MIL")
g.add_node("0014.军事技术", ["提高攻城器械生产速度","降低攻城器械价格","+>【兵工厂】"], 30, [10, 20], former_nodes=["0015.火炮"], node_type="MIL")

g.add_node("0000.手工业", ["提高攻击力","提高防御力","+>【铁匠铺】"], 30, [10, 20], node_type="SCI")
g.add_node("0001.铸造", ["提高攻击力","提高攻击速度"], 30, [10, 20], former_nodes=["0000.手工业"], node_type="SCI")
g.add_node("0003.锁子甲", ["提高防御力","提高速度"], 30, [10, 20], former_nodes=["0000.手工业"], node_type="SCI")
g.add_node("0004.板甲", ["提高防御力"], 30, [10, 20], former_nodes=["0003.锁子甲"], node_type="SCI")



print(g)
g.save()