import os
from PIL import Image
from resizeimage import resizeimage
from constant import defaultSize
img = './image.jpg'
def resizeImage(img):
    imgSizeByte = os.path.getsize(img)
    print(imgSizeByte)
    while (imgSizeByte > defaultSize):
        with open(img, 'r+b') as f:
            with Image.open(f) as image:
                print(image.size)
                cover = resizeimage.resize_cover(image, [image.size[0]/2, image.size[1]/2])
                cover.save('./image.jpg', image.format)
                imgSizeByte = os.path.getsize(img)
                print(imgSizeByte)
resizeImage(img)