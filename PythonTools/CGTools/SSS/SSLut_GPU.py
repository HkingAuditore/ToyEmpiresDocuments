# #######################LIBRARY##########################
import numba as nb
import numpy as np

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


@nb.jit(nopython=True)
def gaussian(v, r):
    return (1 / (2 * v * np.math.pi)) * np.math.exp((-r * r) / (2 * v))


@nb.jit(nopython=True)
def gaussian2(v, r):
    return np.math.exp((-r * r) / v)


@nb.jit(nopython=True)
def gaussian3(v, r):
    return (1 / np.math.sqrt(2 * np.math.pi * v)) * np.math.exp((-r * r) / (2 * v))


@nb.jit(nopython=True)
def gaussian4(d, r):
    return saturate((np.math.exp(-r / d) + np.math.exp(-r / (3 * d))) / (8 * np.math.pi * d * r + .00000000001))


@nb.jit(nopython=True)
def saturate(v):
    return max((.0, min(v, 1.0)))


@nb.jit(nopython=True)
def R_origin(idx, lw, vli, d):
    # s = np.zeros(3)

    p = 1.0
    k = 1.0
    s = 0.0
    i = 0
    while i < len(vli):
        s += np.math.pow(lw[i][idx] * k, p) * gaussian(vli[i], d)
        i += 1

    return s


@nb.jit(nopython=True)
def R(idx, lw, vli, a=0.0, b=0.0, r=1.0):
    d = abs(r * np.math.sqrt(2 - 2 * np.math.cos(a) * np.math.cos(b)))
    return R_origin(idx, lw, vli, d)


@nb.jit(nopython=True)
def sample_light(angle, a=0.0, b=0.0):
    return np.math.cos(angle + a) * np.math.cos(b)


@nb.jit(nopython=True)
def sp_integrate(idx, lw, vli, accuracy=.1, thickness=1.0, k=1.0, theta=0.0):
    delta_b = np.math.pi * accuracy
    delta_a = 2 * np.math.pi * accuracy
    b = 0.0
    total_weights = 0
    total_light = 0
    # 对球面积分
    # 二重积分
    while b <= np.math.pi:
        a = -np.math.pi
        while a <= np.math.pi:
            d = abs(thickness * np.math.sqrt(2 - 2 * np.math.cos(a) * np.math.cos(b)))
            sub_weights = 0.0
            sub_light = 0.0
            weight = R_origin(idx, lw, vli, d) * k
            sub_weights += weight * delta_a
            light = saturate(sample_light(theta, b, a)) * weight
            sub_light += light * delta_a
            a += delta_a
        total_weights += sub_weights * delta_b
        total_light += sub_light * delta_b
        b += delta_b
    return total_light / total_weights


@nb.jit(nopython=True)
def ring_integrate(idx, lw, vli, accuracy=.1, thickness=1.0, k=1.0, theta=0.0):
    delta_a = 2 * np.math.pi * accuracy
    total_weights = 0.0
    total_light = 0.0
    a = -np.math.pi
    while a <= np.math.pi:
        d = abs(thickness * np.math.sqrt(2 - 2 * np.math.cos(a)))
        weight = R_origin(idx, lw, vli, d) * k
        total_weights += weight * delta_a
        light = saturate(sample_light(theta, a, 0)) * weight
        total_light += light * delta_a
        a += delta_a
    return total_light / total_weights


# @nb.jit()
@nb.jit(nopython=True)
def integrate(idx, lw, vli, theta=0.0, thickness=1.0, accuracy=.1, use_sphere=False, k=1.0):
    result = 0
    if use_sphere:
        result = sp_integrate(idx, lw, vli, accuracy, thickness, k, theta)
    else:
        result = ring_integrate(idx, lw, vli, accuracy, thickness, k, theta)
    rgb = np.math.pow(result, 1 / 2.2)
    return rgb


@nb.jit(nopython=True)
def integrate_cost(theta=0.0, accuracy=.1, use_sphere=False,cost = 0.0):
    if use_sphere:
        delta_b = np.math.pi * accuracy
        delta_a = 2 * np.math.pi * accuracy
        b = 0.0
        total_cost = 0.00000
        # 对球面积分
        # 二重积分
        while b <= np.math.pi:
            a = -np.math.pi
            sub_cost = 0.0000
            while a <= np.math.pi:
                light = saturate(sample_light(theta, b, a))
                sub_cost += light * delta_a
                a += delta_a
            total_cost += sub_cost * delta_b
            b += delta_b
        return cost * total_cost
    else:
        delta_a = 2 * np.math.pi * accuracy
        total_cost = 0.0
        a = -np.math.pi
        while a <= np.math.pi:
            light = saturate(sample_light(theta, a, 0))
            total_cost += light * delta_a
            a += delta_a
        return cost * total_cost


# #######################LIBRARY##########################


from numba import cuda
import numpy as np
from PIL import Image
from time import time


@cuda.jit
def generate_lut(result, accuracy, use_sphere, k, cost, max_r):
    row, col = cuda.grid(2)
    width = result.shape[0]
    height = result.shape[1]

    if row < width and col < height:
        uv_x =((col / height) - .5) * 2.0
        uv_y = 1.0 - (row / width)
        theta = np.math.acos(uv_x)
        rr = 1.0 / (uv_y * max_r + .0000001)
        c = ((1.0 - 2.0 * np.math.pi * np.math.pi * cost* accuracy) if use_sphere else (1.0 - 2.0 * np.math.pi * cost* accuracy))

        r = integrate(0, light_weights_tuples, vl, theta, rr, accuracy, use_sphere, k) * c
        g = integrate(1, light_weights_tuples, vl, theta, rr, accuracy, use_sphere, k) * c
        b = integrate(2, light_weights_tuples, vl, theta, rr, accuracy, use_sphere, k) * c
        co = integrate_cost(theta,accuracy,use_sphere,cost)
        r = saturate(r + co)
        g = saturate(g + co)
        b = saturate(b + co)
        result[row, col][0] = r * 255
        result[row, col][1] = g * 255
        result[row, col][2] = b * 255


def uv_array_to_rgb(a, size):
    return a[:, 0:3].reshape((size, size, 3))



size = 256
output_size = 1024
output_name = "GPU_LUT_1024_3_R_0"
accuracy = .005
use_sphere = True
k = 1.0
cost = -.001
max_r = 1

gpu_result = cuda.device_array((size, size, 3))

threads_per_block = (16, 16)
blocks_per_grid = (32, 32)
start = time()
generate_lut[blocks_per_grid, threads_per_block](gpu_result, accuracy, use_sphere, k, cost, max_r)

cuda.synchronize()
print("gpu cost time " + str(time() - start))
result = gpu_result.copy_to_host()
img = Image.fromarray(np.uint8(result))
img = img.resize((output_size, output_size))
img.show()
img.save(output_name + ".png", "png")

