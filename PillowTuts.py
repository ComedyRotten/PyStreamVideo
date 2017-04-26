from PIL import Image

img = Image.open("cah.jpg")
print(img.size)
print(img.format)

area = (150, 10, 850, 600)
cropped_img = img.crop(area)
r, g, b = cropped_img.split()

new_img = Image.merge("RGB", (b, r, g))
square_img = new_img.resize((250, 250))
flip_img = square_img.transpose(Image.FLIP_LEFT_RIGHT)
spin_img = flip_img.transpose(Image.ROTATE_90)
# uses the default image program to open a temp copy of the image
spin_img.show()


