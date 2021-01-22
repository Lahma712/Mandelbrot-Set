import numba as nb
import numpy as np


@nb.njit(cache= True, parallel = True)
def mandelbrot(c_r, c_i,maxIt): #mandelbrot function
		z_r = 0 
		z_i = 0
		z_r2 = 0
		z_i2= 0
		for i in nb.prange(maxIt):
			z_i = 2 * z_r * z_i + c_i
			z_r = z_r2 - z_i2 + c_r
			z_r2 = z_r * z_r
			z_i2 = z_i * z_i
			if z_r2 + z_i2 > 4:
				return i
		return maxIt

@nb.njit(cache= True, parallel = True)
def DrawSet( W, H, xStart, xDist, yStart, yDist, maxIt):
		array = np.zeros((H, W, 3), dtype=np.uint8)
		for x in nb.prange(0, W):
			c_r = (x/W)* xDist + xStart
			for y in nb.prange(0, H):
				c_i = -((y/H) * yDist + yStart)
				cIt = mandelbrot(c_r, c_i, maxIt)
				color = int((255 * cIt) / maxIt)
				array[y,x] = (color, 255, 255)
		return array
