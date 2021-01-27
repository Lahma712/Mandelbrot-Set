import numba as nb
import numpy as np
import math

@nb.njit(cache= True, fastmath = True)
def mandelbrot(c_r, c_i,maxIt, length): #mandelbrot function
        z_r = 0 
        z_i = 0
        z_r2 = 0
        z_i2= 0

        for y in range( maxIt):
            z_i = 2 * z_r * z_i + c_i
            z_r = z_r2 - z_i2 + c_r
            z_r2 = z_r * z_r
            z_i2 = z_i * z_i
            
            if z_r2 + z_i2 > 4:

                #return int((y/maxIt) * length)
                return y%length
        return length -1

@nb.njit(cache= True, fastmath= True, parallel = True, nogil = True)
def DrawSet(W, H, xStart, xDist, yStart, yDist, maxIt, gradient):

        array = np.zeros((H, W, 3), dtype=np.uint8) #array that holds 'rgb' tuple for every pixel
        for x in nb.prange(0, W):
            c_r = ((x/W)* xDist + xStart) #some math to calculate real part
            for y in nb.prange(0, H):
                c_i = (-((y/H) * yDist + yStart)) #some more math to calculate imaginary part
                color = mandelbrot(c_r, c_i, maxIt, len(gradient))
        
                array[y,x] = gradient[color] #adds rgb value
        
        return array #returns rgb array, gets later displayed using PIL



