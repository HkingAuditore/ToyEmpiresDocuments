import math
import threading
import numpy as np
from PIL import Image
from numba import jit
from tqdm import tqdm

import SSSLutLibrary


@jit(nopython=True)
def sample_light(angle, a=0, b=0):
    return np.cos(angle + a) * np.cos(b)

@jit(nopython=True)
def sp_integrate(accuracy=.1, thickness=1.0, k=1.0, theta=0.0):
    delta_a = np.pi * accuracy
    delta_b = 2 * np.pi * accuracy
    a = 0
    total_weights = np.array([.0, .0, .0])
    total_light = np.array([.0, .0, .0])
    # 对球面积分
    # 二重积分
    while a <= np.pi:
        b = -np.pi
        while b <= np.pi:
            sub_weights = np.array([.0, .0, .0])
            sub_light = np.array([.0, .0, .0])
            weight = SSSLutLibrary.R(a, b, thickness) * k
            sub_weights += weight
            light = SSSLutLibrary.saturate(sample_light(theta, a, b)) * weight
            sub_light += light
            b += delta_b
        total_weights += sub_weights
        total_light += sub_light
        a += delta_a
    return (total_light,total_weights)

@jit(nopython=True)
def ring_integrate(accuracy=.1, thickness=1.0, k=1.0, theta=0.0):
    delta_b = 2 * np.pi * accuracy
    total_weights = np.array([.0, .0, .0])
    total_light = np.array([.0, .0, .0])
    b = -np.pi
    while b <= np.pi:
        weight = SSSLutLibrary.R(a=b, r=thickness) * k
        total_weights += weight
        light = SSSLutLibrary.saturate(sample_light(theta, b)) * weight
        total_light += light
        b += delta_b
    return (total_light,total_weights)

# @nb.jit()
@jit(nopython=True)
def integrate(theta=0.0, thickness=1.0, accuracy=.1, use_sphere=False, k=1.0):
    if use_sphere:
        total_light, total_weights = sp_integrate(accuracy,thickness,k,theta)
        rgb = total_light / total_weights
        rgb = np.power(rgb, 1 / 2.2)
        # print(rgb)
        # rgb = [saturate(c) for c in rgb]
        return rgb
    else:
        total_light, total_weights = ring_integrate(accuracy, thickness, k, theta)
        rgb = total_light / total_weights
        rgb = np.power(rgb, 1 / 2.2)

        return rgb


# @cuda.jit

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
def cal(p, size, accuracy=.1, use_sphere=False, max_r=1, cost=0):
    x = p[4]
    y = p[3]
    uv_x = (x / size - .5) * 2
    uv_y = 1 - (y / size)
    col = integrate(np.math.acos(uv_x), 1 / (uv_y * max_r + .001) * 2, accuracy=accuracy, use_sphere=use_sphere) * (
            1.0 - 2.0 * math.pi * cost)
    col = [
        SSSLutLibrary.saturate(col[0]),
        SSSLutLibrary.saturate(col[1]),
        SSSLutLibrary.saturate(col[2]),
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

def block_cal(input, rl, i, part_size, total_size, accuracy=.1, use_sphere=False, max_r=1, cost=0):
    is_last = (i + 1) * part_size >= total_size * total_size
    rl[i] = np.apply_along_axis(cal,
                                1,
                                input[part_size * i:] if is_last else input[part_size * i:part_size * (i + 1)],
                                total_size,
                                accuracy,
                                use_sphere,
                                max_r,
                                cost)


def generate_pre_integrated(sample_size=64, thread_count=3, accuracy=.1, use_sphere=False, max_r=1.0, cost=0,
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
    print(r.shape)
    img = Image.fromarray(np.uint8(r))
    img = img.resize((output_size, output_size))
    img.show()
    img.save(output_name + ".png", "png")


generate_pre_integrated(sample_size=256, thread_count=16, accuracy=.01, max_r=1.0, use_sphere=False,output_name="NEW_LUT3")

