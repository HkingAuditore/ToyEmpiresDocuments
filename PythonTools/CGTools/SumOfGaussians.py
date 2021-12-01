from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from matplotlib import pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.axis([0,2.5,0,1])

def gaussian(v, r):
    return (1 / (2 * np.pi * v)) * np.exp(-np.power(r, 2) / (2 * v))

v = [.0064,.0484,.197,.567,1.99,7.41]
r = np.arange(0, 2.5, 0.01)
R = lambda x, l: l[0] * gaussian(.0064, x) \
                 + l[1] * gaussian(.0484, x) \
                 + l[2] * gaussian(.187, x) \
                 + l[3] * gaussian(.567, x) \
                 + l[4] * gaussian(1.99, x) \
                 + l[5] * gaussian(7.41, x)
# R2 = lambda x, l: l[0] * gaussian(.036, x) \
#                  + l[1] * gaussian(.14, x) \
#                  + l[2] * gaussian(.91, x) \
#                  + l[3] * gaussian(7.0, x)
RR = R(r, [.233, .1, .118, .113, .358, .078]) * r
RG = R(r, [.455, .336, .198, .007, .004, 0]) * r
RB = R(r, [.649, .344, .0, .007, 0, 0]) * r




# RF = R2(r, [.07,.18,.21,.29]) * r
print(R)
plt.xlabel('r')
plt.ylabel('rR(r)')
plt.title("散射拟合")
plt.plot(r, RR, color='red')
plt.plot(r, RG, color='green')
plt.plot(r, RB, color='blue')

# plt.plot(r, 2 * np.pi * RF, color='black')
plt.show()
