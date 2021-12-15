import math
import threading
from math import cos

import numpy as np
from PIL import Image
from numba import jit
from tqdm import tqdm


# region LIBRARY
# #######################LIBRARY##########################
@jit(nopython=True)
def gaussian(v, r):
    return (1 / (2 * v * np.pi)) * np.exp(-pow(r, 2) / (2 * v))


@jit(nopython=True)
def gaussian2(v, r):
    return np.exp(-np.power(r, 2) / v)


@jit(nopython=True)
def gaussian3(v, r):
    return (1 / np.sqrt(2 * np.pi * v)) * np.exp(-np.power(r, 2) / (2 * v))


@jit(nopython=True)
def norm_diff(r, d):
    return saturate(np.exp(-r / d) + np.exp(-r / (3 * d)) / (8 * np.pi * d * r))


@jit(nopython=True)
def saturate(v):
    return max((.0, min(v, 1.0)))


@jit(nopython=True)
def R_origin(d=.0):
    vl = np.array([.0064, .0484, .187, .567, 1.99, 7.41])
    # 不同颜色光的散射率
    light_weights_tuples = np.array([
        (.233, .455, .649),
        (.1, .336, .344),
        (.118, .198, .0),
        (.113, .007, .007),
        (.358, .004, .0),
        (.078, .0, .0),
    ])
    s = np.zeros(3)
    # 这里可以手动加强散射色彩的强度
    p = 6
    k = 1
    for i, t in enumerate(light_weights_tuples):
        v = np.array(list(t))
        v = np.power(v * k, p)
        s += v * gaussian(vl[i], d)
    return s


@jit(nopython=True)
def R(a=0.0, b=0.0, r=1.0):
    d = abs(r * np.sqrt(2 - 2 * cos(a) * cos(b)))
    return R_origin(d)


# #######################LIBRARY##########################
# endregion

# region INTEGRAL
@jit(nopython=True)
def sample_light(angle, a=0, b=0):
    return np.cos(angle + a) * np.cos(b)


@jit(nopython=True)
def sp_integrate(accuracy=.1, thickness=1.0, k=1.0, theta=0.0, cost=.0):
    delta_b = np.pi * accuracy
    delta_a = 2 * np.pi * accuracy
    b = 0
    total_weights = np.array([.0, .0, .0])
    total_light = np.array([.0, .0, .0])
    total_cost = np.array([.0, .0, .0])
    # 二重积分
    while b <= np.pi:
        a = -np.pi
        sub_weights = np.array([.0, .0, .0])
        sub_light = np.array([.0, .0, .0])
        sub_cost = np.array([.0, .0, .0])
        while a <= np.pi:
            weight = R(b, a, thickness) * k
            sub_weights += weight * delta_a
            light = saturate(sample_light(theta, b, a))
            sub_cost += light * delta_a
            sub_light += light * weight * delta_a
            a += delta_a
        total_weights += sub_weights * delta_b
        total_light += sub_light * delta_b
        total_cost += sub_cost * delta_b
        b += delta_b
    return (total_light, total_weights, cost * total_cost)


@jit(nopython=True)
def ring_integrate(accuracy=.1, thickness=1.0, k=1.0, theta=0.0, cost=.0):
    delta_x = 2 * np.pi * accuracy
    total_weights = np.array([.0, .0, .0])
    total_light = np.array([.0, .0, .0])
    total_cost = np.array([.0, .0, .0])
    x = -np.pi
    while x <= np.pi:
        weight = R(a=x, r=thickness) * k
        total_weights += weight * delta_x
        light = saturate(sample_light(theta, x))
        total_light += light * weight * delta_x
        total_cost += light * delta_x
        x += delta_x
    return (total_light, total_weights, cost * total_cost)


@jit(nopython=True)
def integrate(theta=0.0, thickness=1.0, accuracy=.1, use_sphere=False, k=1.0, cost=.0):
    if use_sphere:
        total_light, total_weights, total_cost = sp_integrate(accuracy, thickness, k, theta, cost=cost)
        rgb = ((1 - 2 * np.pi * np.pi * cost) * total_light) / total_weights + total_cost
        rgb = np.power(rgb, 1 / 2.2)
        return rgb
    else:
        total_light, total_weights, total_cost = ring_integrate(accuracy, thickness, k, theta, cost=cost)
        rgb = ((1 - 2 * np.pi * cost) * total_light) / total_weights + total_cost
        rgb = np.power(rgb, 1 / 2.2)

        return rgb


# endregion

# region PROCESS
global indicator
indicator = 0
global total_indicator
global pbar


def process():
    global indicator
    indicator += 1
    global total_indicator
    global pbar
    pbar.update()
    return


# @cuda.jit
def cal(p, size, accuracy=.1, use_sphere=False, max_r=1, cost=0.0):
    x = p[4]
    y = p[3]
    uv_x = (x / size - .5) * 2
    uv_y = 1 - (y / size)
    col = integrate(np.math.acos(uv_x), 1 / (uv_y * max_r + .001), accuracy=accuracy, use_sphere=use_sphere, cost=cost)
    col = [
        saturate(col[0]),
        saturate(col[1]),
        saturate(col[2]),
    ]
    process()
    return [int(col[0] * 255), int(col[1] * 255), int(col[2] * 255)]


@jit(nopython=True)
def generate_uv_array(size):
    a = np.zeros((size, size, 5))
    for i in range(size):
        for j in range(size):
            a[i, j] = np.array([0, 0, 0, i, j])
    return a.reshape((-1, 5))


def uv_array_to_rgb(a, size):
    return a[:, 0:3].reshape((size, size, 3))


def block_cal(input, rl, i, part_size, total_size, accuracy=.1, use_sphere=False, max_r=1, cost=0.0):
    is_last = (i + 1) * part_size >= total_size * total_size
    rl[i] = np.apply_along_axis(cal,
                                1,
                                input[part_size * i:] if is_last else input[part_size * i:part_size * (i + 1)],
                                total_size,
                                accuracy,
                                use_sphere,
                                max_r,
                                cost)


def generate_pre_integrated(sample_size=64, thread_count=3, accuracy=.1, use_sphere=False, max_r=1.0, cost=0.0,
                            output_size=1024, output_name="LUT"):
    size = sample_size
    global total_indicator
    total_indicator = size * size

    dst = generate_uv_array(size)
    part_size = math.ceil(size * size / thread_count)

    r = [0] * thread_count
    threads = []

    global pbar
    pbar = tqdm(total=total_indicator, ncols=100, unit="pixel")
    pbar.set_description('Processing:')

    for i in range(thread_count):
        t = threading.Thread(target=block_cal, args=(dst, r, i, part_size, size, accuracy, use_sphere, max_r, cost))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    result = np.vstack((r[0], r[1]))
    for i in range(2, thread_count):
        result = np.vstack((result, r[i]))
    r = uv_array_to_rgb(result, size)
    img = Image.fromarray(np.uint8(r))
    img = img.resize((output_size, output_size))
    img.show()
    img.save(output_name + ".png", "png")


# endregion


# 图片的一般参数在这里改
# 如果想让烘出来的LUT色彩更明亮，可以进到R_origin方法里改物理参数
generate_pre_integrated(sample_size=32, thread_count=16, accuracy=.001, max_r=1.0, cost=-0.005, use_sphere=False,
                        output_name="CPU_LUT")
