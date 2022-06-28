import graphviz
from GraphLinker.GraphLibrary import PathGraph

g = PathGraph()
with open("data.txt", "r",encoding='utf-8') as f:
    data = f.readlines()
    for l in data:
        print(l)
        if l[0] == '%':
            continue
        d = l.split()
        g.add_path(d[0], d[1], float(d[2]))

g.render()