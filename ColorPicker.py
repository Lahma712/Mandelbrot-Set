from PIL import Image, ImageDraw
import numpy as np
import sys

<<<<<<< HEAD
def loop(index, HStart, HEnd, H, W, array, colorBar, op): #loop that is used to create rainbow colorbar
	division = 255/(H/6) #colorbar can be divided into 6 smaller units where in each unit, one RGB value goes up/down by 255 
	remainder = division % 1 
=======
def loop(index, HStart, HEnd, H, W, array, colorBar, op):

	division = 255/(H/6)
	remainder = division % 1
>>>>>>> 01553416c71f22a94baba66c42a2fdf44c69c3e2
	remainderCount = remainder
	for y in range(HStart, HEnd):
		colorBar[index] = colorBar[index] + op * (int(division) + int(remainderCount))
		if colorBar[index] > 255:
			colorBar[index] = 255
		elif colorBar[index] < 0:
			colorBar[index] = 0
		if int(remainderCount) == 1:
			remainderCount -= 1
		remainderCount += remainder
		for x in range(W):
			array[y,x] = tuple(colorBar)
	return colorBar
	

def colorbar(W, H): #used to create rainbow colorbar
	array = np.zeros((H, W, 3), dtype=np.uint8) #array that holds rgb values for each pixel
	colorBar = [255,0,0] #colorbar starts with red
	
	#calls loop 6 times to build the colorbar
	loop(1, 0, int(H*1*(1/6)), H, W, array, colorBar, 1)
	loop(0, int(H*1*(1/6)), int(H*1*(2/6)), H, W, array, colorBar, -1)
	loop(2, int(H*1*(2/6)), int(H*1*(3/6)), H, W, array, colorBar, 1)
	loop(1, int(H*1*(3/6)), int(H*1*(4/6)), H, W, array, colorBar, -1)
	loop(0, int(H*1*(4/6)), int(H*1*(5/6)), H, W, array, colorBar, 1)
	loop(2, int(H*1*(5/6)), H, H, W, array, colorBar, -1)
	return array


def colorsquare(W, H, start): #used to create color square 
	array = np.zeros((H, W, 3), dtype=np.uint8) #array that holds rgb values for each pixel
	Ycolor = start #starting color on which 1D Y axis is being built

	for index in range(3): #loops through this 3 times, for each R, G and B value
		Ydivision = H/(start[index]+1) #division to keep track how often the RGB values should be incremented/decremented
		Yremainder = Ydivision % 1 #remainder that is used to sometimes skip an increment/decrement so that the whole Height/Width can be utilized
		YremainderCount = Yremainder
		yAxis(Ycolor, Ydivision, YremainderCount, Yremainder, index, array)

	for y in range(H): #each row gets extended to a 2D plane
		for index in range(3): #loops through this 3 times, for each R, G and B value
			XColor = array[y, 0, index] #starting RGB value on which the X axis is built
			XStart = array[y,0] #entire starting rgb value 
			Xdivision = W/(max(XStart)-XStart[index]+1)#division to keep track how often the RGB values should be incremented/decremented
			Xremainder = Xdivision % 1 #remainder that is used to sometimes skip an increment/decrement so that the whole Height/Width can be utilized
			XremainderCount = Xremainder
			Plane(XColor, Xdivision, XremainderCount, Xremainder, index, array, y)
	
	return array


def yAxis(Ycolor, Ydivision, YremainderCount, Yremainder, index, array): #builds 1D Y axis
	y=0
	for _ in range(Ycolor[index]+1): #how many times there needs to be a decrement 
		for _ in range(int(Ydivision) + int(YremainderCount)): #for loop that spaces the decrements. If the remainder gets bigger than 1, it gets added and one decrement is skipped
			try:
				array[y,0,index] = Ycolor[index] #current row gets assigned its correct color
			except:
				return array
			y +=1
		if int(YremainderCount) == 1: 
			YremainderCount -= 1
		YremainderCount += Yremainder
		Ycolor[index] -= 1 #color value (R, G or B depending on index) gets decremented
	return array



def Plane(Xcolor, Xdivision, XremainderCount, Xremainder, index, array, Y): #extends 1D Y axis to a 2D plane
	x=1
	Max = max(array[Y,0]) #maximum value from RGB is taken
	for _ in range(Max - array[Y, 0, index]+1):  #how many times there needs to be an increment
		for _ in range(int(Xdivision) + int(XremainderCount)): #for loop that spaces the increments accordingly (again with remainder)
			try:
				array[Y,x,index] = Xcolor #current column gets assigned its correct color
			except:
				return array 
			x+=1
			
		if int(XremainderCount) == 1:
			XremainderCount -= 1
		XremainderCount += Xremainder
		Xcolor += 1 #R, G or B value gets incremented
	return array


		
			



			
		
