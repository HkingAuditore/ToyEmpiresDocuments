import numpy as np

from matplotlib import pyplot as plt

v = [.0064, .0484, .197, .567, 1.99, 7.41]
light_weights_tuples = [
    (.233,.455,.649),
    (.1,.336,.344),
    (.118,.198,.0),
    (.113,.007,.007),
    (.358,.004,.0),
    (.078,.0,.0),
    ]

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# plt.axis([0, 2.5, 0, 1])


def gaussian(v, r):
    return (1 / (2 * np.pi * v)) * np.exp(-np.power(r, 2) / (2 * v))

def saturate(v):
    return max(0,min(v,1))

def gaussian2(v, r):
    return np.exp(-np.power(r, 2) / v)


def R(d,l,vl):
    s = [0,0,0]
    for i,t in enumerate(l):
        r,g,b = t
        v =[r,g,b]
        # v /= np.linalg.norm(v)
        # print(v)
        s[0] += v[0] * gaussian2(vl[i],d)
        s[1] += v[1] * gaussian2(vl[i],d)
        s[2] += v[2] * gaussian2(vl[i],d)
    return s






r = np.arange(0, 2.5, 0.01)

# R2 = lambda x, l: l[0] * gaussian(.036, x) \
#                  + l[1] * gaussian(.14, x) \
#                  + l[2] * gaussian(.91, x) \
#                  + l[3] * gaussian(7.0, x)

Rr = R(r,light_weights_tuples,v)

# RF = R2(r, [.07,.18,.21,.29]) * r
# print(R)
plt.xlabel('r')
plt.ylabel('rR(r)')
plt.title("散射拟合")
plt.plot(r,Rr[0] * r, color='red')
plt.plot(r,Rr[1] * r, color='green')
plt.plot(r,Rr[2] * r, color='blue')

# plt.plot(r, 2 * np.pi * RF, color='black')
plt.show()
