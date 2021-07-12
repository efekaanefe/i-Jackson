from PIL import Image, ImageOps

for i in range(7):
    path = f"{i}.png"
    im = Image.open(path)

    #im_mirror = ImageOps.mirror(im)
    im.save("R"+path, quality=95)