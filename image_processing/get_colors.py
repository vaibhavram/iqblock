from PIL import Image
import numpy as np

im = Image.open("images/IMG_0387.jpg")

width = im.size[0]
height = im.size[1]

pixel_values = list(im.getdata())
pixel_values = np.array(pixel_values).reshape((width, height, 3))

grid = np.zeros((8,8,3))

increment = width//8

for r in range(8):
	row = r*increment
	for c in range(8):
		column = c*increment
		subset = pixel_values[column:(column + increment), row:(row + increment),]
		grid[c, r, 0] = np.mean(subset[,,0])
		grid[c, r, 1] = np.mean(subset[,,1])
		grid[c, r, 2] = np.mean(subset[,,2])

print(grid)