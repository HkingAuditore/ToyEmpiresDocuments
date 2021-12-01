from PIL import Image
import numpy as np
import SumOfGaussians
size = 128
img = Image.new('RGB', (size, size))

img_array = np.array(img)#把图像转成数组格式img = np.asarray(image)
shape = img_array.shape

height = shape[0]
width = shape[1]
dst = np.zeros((height,width,3))


for h in range(0,height):
    for w in range (0,width):
        d = np.linalg.norm([h/size - .5,w/size - .5])
        # print(d)
        reflectance = SumOfGaussians.R(d, SumOfGaussians.light_weights_tuples, SumOfGaussians.v)
        RR = SumOfGaussians.saturate(reflectance[0])
        RG = SumOfGaussians.saturate(reflectance[1])
        RB = SumOfGaussians.saturate(reflectance[2])
        dst[h,w] = [RR * 255,RG* 255,RB* 255]

img2 = Image.fromarray(np.uint8(dst))
img2.show(img2)
img2.save("3.png","png")
