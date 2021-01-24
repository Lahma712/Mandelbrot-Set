import numba as nb
import numpy as np
import math

@nb.njit(cache= True, fastmath = True, parallel = True)
def mandelbrot(c_r, c_i,maxIt): #mandelbrot function
        z_r = 0 
        z_i = 0
        z_r2 = 0
        z_i2= 0
        for y in nb.prange(maxIt):
            z_i = 2 * z_r * z_i + c_i
            z_r = z_r2 - z_i2 + c_r
            z_r2 = z_r * z_r
            z_i2 = z_i * z_i
            if z_r2 + z_i2 > 4:

                x = int(y + 1 - math.log(math.log(z_r2 + z_i2)/math.log(2)))
                #smooth = double(math.log((math.log(z_r2+z_i2)/math.log(2)/2))/math.log(2))
                #color = int((math.sqrt(x + 10 - smooth)*256) % 17)

                x = x % 398
                return x
        return 399

@nb.njit(cache= True, fastmath= True, parallel = True)
def DrawSet(W, H, xStart, xDist, yStart, yDist, maxIt, gradient):

        array = np.zeros((H, W, 3), dtype=np.uint8) #array that holds 'hsv' tuple for every pixel
        for x in nb.prange(0, W):
            c_r = ((x/W)* xDist + xStart) #some math to calculate real part
            for y in nb.prange(0, H):
                c_i = (-((y/H) * yDist + yStart)) #some more math to calculate imaginary part
                color = mandelbrot(c_r, c_i, maxIt)
        
                array[y,x] = gradient[color] #adds hue value
                
        return array #returns rgb array, gets later displayed using PIL
