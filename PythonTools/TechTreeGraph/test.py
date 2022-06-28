# Import libraries
import math
import queue


class Node:
    FormerTechs = []

    def __init__(self, name, former=[]):
        self.name = name
        self.FormerTechs = former
        self.AfterTechs = []
        for n in self.FormerTechs:
            n.AfterTechs.append(self)

    def __str__(self):
        f = ''
        a = ''
        for n in self.FormerTechs:
            f += n.name + ','
        for n in self.AfterTechs:
            a += n.name + ','
        return "[" + self.name + '::former{' + f + '}, after{' + a + '}'+']'


n0 = Node('0', )
n1 = Node('1', former=[n0])
n2 = Node('2', former=[n1])
n3 = Node('3', former=[n1])
n4 = Node('4', former=[n2,n3])

# n5 = Node('5', former=[n2])
# n6 = Node('6', former=[n2,n5])
# print(n0)
# print(n1)
# print(n2)
# print(n3)


# def ImptNode(c, t, vd):
#     print('------------------------')
#     for x, y in vd.items():
#         print(x,':', y)
#     print('------------------------')
#     if c not in vd.keys():
#         vd[c] = 0
#     for n in c.AfterTechs:
#         vd[c] += vd[n] / len(n.FormerTechs)
#     if c == t:
#         return vd[c]
#     for n in c.FormerTechs:
#         return ImptNode(n, t, vd)


def Impt(t, T):
    q = queue.Queue()
    vd ={t : 1}
    q.put(t)
    while not q.empty():
        n = q.get()
        print('------------------------')
        for x, y in vd.items():
            print(x,':', y)
        print('------------------------')
        if n not in vd.keys():
            vd[n] = 0
        for i in n.AfterTechs:
            vd[n] += vd[i] / len(i.FormerTechs)
        if n == T:
            return vd[n]
        for f in n.FormerTechs:
            q.put(f)


print(Impt(n4, n1))
