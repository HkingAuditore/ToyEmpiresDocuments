# #######################LIBRARY##########################
from math import cos
import numpy as np
import numba as nb

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
    return (1 / (2 * v * 3.14159)) * np.math.exp((-r * r)/ (2 * v))

@nb.jit(nopython=True)
def gaussian2(v, r):
    return np.math.exp((-r*r) / v)

@nb.jit(nopython=True)
def gaussian3(v, r):
    return (1 / np.math.sqrt(2 * 3.14159 * v)) * np.math.exp((-r*r )/ (2 * v))

@nb.jit(nopython=True)
def norm_diff(r, d):
    return saturate(np.exp(-r / d) + np.exp(-r / (3 * d)) / (8 * 3.14159 * d * r))

@nb.jit(nopython=True)
def saturate(v):
    return max((.0, min(v, 1.0)))

@nb.jit(nopython=True)
def R_origin(idx,lw, vli,d):

    # s = np.zeros(3)
    p = 6
    k = 2
    s = 0
    i = 0
    while i < 6:
        s += np.math.pow(lw[i][idx]*k,p) * gaussian(vli[i], d)
        i+=1

    return s

@nb.jit(nopython=True)
def R(idx,lw,vli,a=0.0, b=0.0, r=1.0):
    d = abs(r * np.math.sqrt(2 - 2 * np.math.cos(a) * np.math.cos(b)))
    return R_origin(idx,lw,vli,d)




@nb.jit(nopython=True)
def sample_light(angle, a=0, b=0):
    return np.math.cos(angle + a) * np.math.cos(b)

@nb.jit(nopython=True)
def sp_integrate(idx,lw,vli,accuracy=.1, thickness=1.0, k=1.0, theta=0.0):
    delta_a = 3.14159 * accuracy
    delta_b = 2 * 3.14159 * accuracy
    a = 0
    total_weights = 0
    total_light = 0
    # 对球面积分
    # 二重积分
    while a <= 3.14159:
        b = -3.14159
        while b <= 3.14159:
            d = abs(thickness * np.math.sqrt(2 - 2 * np.math.cos(b)* np.math.cos(a)))
            sub_weights = 0
            sub_light = 0
            weight = R_origin(idx,lw,vli,d) * k
            sub_weights += weight
            light = saturate(sample_light(theta, a, b)) * weight
            sub_light += light
            b += delta_b
        total_weights += sub_weights
        total_light += sub_light
        a += delta_a
    return total_light/total_weights

@nb.jit(nopython=True)
def ring_integrate(idx,lw,vli,accuracy=.1, thickness=1.0, k=1.0, theta=0.0):
    delta_b = 2 * 3.14159 * accuracy
    total_weights = 0.0
    total_light = 0.0
    b = -3.14159
    while b <= 3.14159:
        d = abs(thickness * np.math.sqrt(2 - 2 * np.math.cos(b)))
        weight = R_origin(idx,lw,vli,d) * k
        total_weights += weight
        light = saturate(sample_light(theta, b,0)) * weight
        total_light += light
        b += delta_b
    return total_light/total_weights

# @nb.jit()
@nb.jit(nopython=True)
def integrate(idx,lw,vli,theta=0.0, thickness=1.0, accuracy=.1, use_sphere=False, k=1.0):
    if use_sphere:
        result = sp_integrate(idx,lw,vli,accuracy,thickness,k,theta)

        rgb = np.math.pow(result, 1 / 2.2)
        return rgb
    else:
        result = ring_integrate(idx,lw,vli,accuracy, thickness, k, theta)
        rgb = np.math.pow(result, 1 / 2.2)

        return rgb

# #######################LIBRARY##########################



from numba import cuda, float32
import numpy as np
from time import time
from PIL import Image
from tqdm import tqdm




@cuda.jit
def generate_lut(result, width, height, indicator):

    row, col = cuda.grid(2)
    uv_x = (col / width - .5) * 2
    uv_y = 1 - row / width
    if row < width and col < height:
        result[row,col][0] = integrate(0, light_weights_tuples, vl, np.math.acos(uv_x), 1 / (uv_y * 1.0 + .1), .1, True, 1.0) * 255
        result[row,col][1] = integrate(1, light_weights_tuples, vl, np.math.acos(uv_x), 1 / (uv_y * 1.0 + .1), .1, True, 1.0) * 255
        result[row,col][2] = integrate(2, light_weights_tuples, vl, np.math.acos(uv_x), 1 / (uv_y * 1.0 + .1), .1, True, 1.0) * 255
        print(row)



def uv_array_to_rgb(a, size):
    return a[:, 0:3].reshape((size, size, 3))






def main():
    size = 256
    output_size = 1024
    output_name = "GPU_LUT"

    total_indicator = size * size
    pbar = tqdm(total=total_indicator, ncols=100, unit="pixel")
    pbar.set_description('Processing:')

    gpu_result = cuda.device_array((size,size,3))

    indicator = np.array(0)
    threads_per_block = (16, 16)
    blocks_per_grid = (32, 32)
    generate_lut[blocks_per_grid, threads_per_block](gpu_result, size, size,indicator)
    cuda.synchronize()

    result = gpu_result.copy_to_host()
    img = Image.fromarray(np.uint8(result))
    img = img.resize((output_size, output_size))
    img.show()
    img.save(output_name + ".png", "png")

if __name__ == "__main__":
    main()