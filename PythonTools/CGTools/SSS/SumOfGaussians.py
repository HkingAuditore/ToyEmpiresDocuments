# from numbers import Number
#
# import numpy as np
#
# from matplotlib import pyplot as plt
# from multipledispatch import dispatch
#
# v = [.0064, .0484, .197, .567, 1.99, 7.41]
# light_weights_tuples = [
#     (.233, .455, .649),
#     (.1, .336, .344),
#     (.118, .198, .0),
#     (.113, .007, .007),
#     (.358, .004, .0),
#     (.078, .0, .0),
# ]
#
#
#
# def gaussian(v, r):
#     return (1 / (2 * np.multiply(np.pi, v))) * np.exp(-np.power(r, 2) / (2 * v))
# def gaussian2(v, r):
#     return np.exp(-np.power(r, 2) / v)
# def gaussian3(v, r):
#     return (1 / np.sqrt(2 * np.pi * v)) * np.exp(-np.power(r, 2) / (2 * v))
# def norm_diff(r,d):
#     return saturate(np.exp(-r/d) + np.exp(-r/(3*d)) / (8 * np.pi * d *r))
#
#
# def saturate(v):
#     return max((0, min(v, 1)))
#
#
# @dispatch(object)
# def R_origin(d, l=light_weights_tuples, vl=v):
#     """
#
#     :param d: 距离
#     :param l:
#     :param vl:
#     :return:
#     """
#     s = [0, 0, 0]
#     for i, t in enumerate(l):
#         r, g, b = t
#         v = [r, g, b]
#         # v /= np.linalg.norm(v)
#         # print(v)
#         s[0] += v[0] * gaussian(vl[i], d)
#         s[1] += v[1] * gaussian(vl[i], d)
#         s[2] += v[2] * gaussian(vl[i], d)
#     return s
#
#
# @dispatch(Number, Number, Number)
# def R(a, b, r):
#     d = np.abs(r * np.sqrt(2 - 2 * np.cos(a) * np.cos(b)))
#     return R_origin(d)
#
# @dispatch(Number, Number)
# def R(a, r):
#     """
#
#     :param a: 角度
#     :param r: 半径
#     :return:
#     """
#     d = np.abs(2 * r *np.sin(.5 * a))
#     return R_origin(d)
#
# @dispatch(Number, Number, Number, list, list)
# def R(a, b, r, l=light_weights_tuples, vl=v):
#     d = np.abs(r * np.sqrt(2 - 2 * np.multiply(np.cos(a) * np.cos(b))))
#     return R_origin(d, l, vl)
#
#
# # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# # plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
#
#
# # plt.axis([0, 2.5, 0, 1])
#
# # r = np.arange(0, 2.5, 0.01)
# #
# # # R2 = lambda x, l: l[0] * gaussian(.036, x) \
# # #                  + l[1] * gaussian(.14, x) \
# # #                  + l[2] * gaussian(.91, x) \
# # #                  + l[3] * gaussian(7.0, x)
# #
# # Rr = R_origin(r)
# #
# # # RF = R2(r, [.07,.18,.21,.29]) * r
# # print(R)
# # plt.xlabel('r')
# # plt.ylabel('rR(r)')
# # plt.title("散射拟合")
# # plt.plot(r, Rr[0] * r, color='red')
# # plt.plot(r, Rr[1] * r, color='green')
# # plt.plot(r, Rr[2] * r, color='blue')
# #
# # # plt.plot(r, 2 * np.pi * RF, color='black')
# # plt.show()
