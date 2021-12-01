from PIL import Image
import numpy as np
img = Image.new('RGB', (512, 512))

img_array = np.array(img)#把图像转成数组格式img = np.asarray(image)
shape = img_array.shape

height = shape[0]
width = shape[1]
dst = np.zeros((height,width,3))
for h in range(0,height):
    for w in range (0,width):
        img_array[h, w] = (255,0,0)
        dst[h,w] = img_array[h,w]
img2 = Image.fromarray(np.uint8(dst))
img2.show(img2)
img2.save("3.png","png")
