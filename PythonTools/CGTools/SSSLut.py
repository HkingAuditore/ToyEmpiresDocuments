from PIL import Image
import numpy as np
from multipledispatch import dispatch

import SumOfGaussians

size = 128
img = Image.new('RGB', (size, size))


def sample_light(angle, a=0, b=0):
    return np.cos(angle + a) * np.cos(b)


def integrate_up(theta, radius, accuracy=.1, use_sphere = False):
    if use_sphere:
        delta_a = np.math.pi * accuracy
        delta_b = 2 * np.math.pi * accuracy
        a = - .5 * np.math.pi
        result = [0, 0, 0]
        while a <= .5 * np.math.pi:
            b = -np.math.pi
            while b <= np.math.pi:
                result += np.multiply(SumOfGaussians.saturate(sample_light(theta, a, b)), SumOfGaussians.R(a, b, radius))
                b += delta_b
            a += delta_a
        return result
    else:
        delta_b = 2 * np.math.pi * accuracy
        result = [0, 0, 0]
        b = -np.math.pi
        while b <= np.math.pi:
            result += np.multiply(SumOfGaussians.saturate(sample_light(theta, b)), SumOfGaussians.R(b, radius))
            b += delta_b
        return result



def integrate_bottom(radius, accuracy=.1, use_sphere = False):
    if use_sphere:
        delta_a = np.math.pi * accuracy
        delta_b = 2 * np.math.pi * accuracy
        a = - .5 * np.math.pi
        result = [0, 0, 0]
        while a <= .5 * np.math.pi:
            b = -np.math.pi
            while b <= np.math.pi:
                r = SumOfGaussians.R(a, b, radius)
                result[0] += r[0]
                result[1] += r[1]
                result[2] += r[2]
                b += delta_b
            a += delta_a
        return result
    else:
        delta_b = 2 * np.math.pi * accuracy
        result = [0, 0, 0]
        b = -np.math.pi
        while b <= np.math.pi:
            r = SumOfGaussians.R(b, radius)
            result[0] += r[0]
            result[1] += r[1]
            result[2] += r[2]
            b += delta_b
        return result



def integrate(theta, thickness, accuracy=.1):
    up = integrate_up(theta, thickness, accuracy)
    bottom = integrate_bottom(thickness, accuracy)
    return [up[0] / bottom[0], up[1] / bottom[1], up[2] / bottom[2]]




img_array = np.array(img)  # 把图像转成数组格式img = np.asarray(image)
shape = img_array.shape

height = shape[0]
width = shape[1]
dst = np.zeros((height, width, 3))

for h in range(0, height):
    for w in range(0, width):
        uv = [w / width - .5, h / height - .5]
        col = integrate(np.acos(uv[0]), uv[1],accuracy=.1)

        # print(col)
        dst[w, h] = [col[0] * 255, col[1] * 255, col[2] * 255]
        # print(dst[w, h])
        # reflectance = SumOfGaussians.R(d, SumOfGaussians.light_weights_tuples, SumOfGaussians.v)
        # RR = SumOfGaussians.saturate(reflectance[0])
        # RG = SumOfGaussians.saturate(reflectance[1])
        # RB = SumOfGaussians.saturate(reflectance[2])
        # dst[h,w] = [RR * 255,RG* 255,RB* 255]

img2 = Image.fromarray(np.uint8(dst))
img2.show(img2)
img2.save("3.png", "png")
