import numba as nb
import numpy as np

@nb.jit
def mandelbrot(c,maxIt): #mandelbrot function
		z = 0
		n = 0
		while abs(z) <= 2 and n < maxIt:
			z = z * z + c
			n += 1
		return n 

@nb.jit
def DrawSet( W, H, xStart, xDist, yStart, yDist, maxIt, hue, saturation, value, glow, a, b, Qcolor, offset):
		array = np.zeros((H, W, 3), dtype=np.uint8)
		for x in range(0, W):
			for y in range (0, H):
				
				c = complex( (x/W)* xDist +xStart, -((y/H) * yDist + yStart))
				
				cIt = mandelbrot(c, maxIt)
				color = int((255 * cIt) / maxIt)
				
				if Qcolor == True:
					if color + offset > 255:
						hue = (color + offset) - 255
					else:
						hue = color + offset
						saturation = 255 - glow * color

				array[y,x] = (hue, saturation, value if cIt == maxIt else a+b*glow * color)
		return array