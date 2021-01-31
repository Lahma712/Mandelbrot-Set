from PIL import Image, ImageDraw
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)


def loop(index, HStart, HEnd, H, W, array, colorBar, op):

	division = 255/(H/6)
	remainder = division % 1
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
	

def colorbar(W, H):
	array = np.zeros((H, W, 3), dtype=np.uint8)
	colorBar = [255,0,0]

	loop(1, 0, int(H*1*(1/6)), H, W, array, colorBar, 1)
	loop(0, int(H*1*(1/6)), int(H*1*(2/6)), H, W, array, colorBar, -1)
	loop(2, int(H*1*(2/6)), int(H*1*(3/6)), H, W, array, colorBar, 1)
	loop(1, int(H*1*(3/6)), int(H*1*(4/6)), H, W, array, colorBar, -1)
	loop(0, int(H*1*(4/6)), int(H*1*(5/6)), H, W, array, colorBar, 1)
	loop(2, int(H*1*(5/6)), H, H, W, array, colorBar, -1)
	return array


def colorsquare(W, H, start):

	array = np.zeros((H, W, 3), dtype=np.uint8)
	YStart = start
	Ycolor = YStart

	for index in range(3):
		Ydivision = H/(start[index]+1)
		Yremainder = Ydivision % 1
		YremainderCount = Yremainder
		array = yDiv(YStart, Ycolor, Ydivision, YremainderCount, Yremainder, index, array)

	for y in range(H):
		for index in range(3):

			XStart = array[y, 0]
			XColor = array[y, 0, index]

			Xdivision = W/(max(XStart)-XStart[index]+1)
			Xremainder = Xdivision % 1
			XremainderCount = Xremainder
			xDiv(XStart, XColor, Xdivision, XremainderCount, Xremainder, index, array, y)
	
	return array


def yDiv(start, Ycolor, Ydivision, YremainderCount, Yremainder, index, array):
	y=0
	for _ in range(start[index]+1):
		for _ in range(int(Ydivision) + int(YremainderCount)):
			try:
				array[y,0,index] = Ycolor[index]
			except:
				return array
			y +=1
		if int(YremainderCount) == 1:
			YremainderCount -= 1
		YremainderCount += Yremainder
		Ycolor[index] -= 1


	return array



def xDiv(start, Xcolor, Xdivision, XremainderCount, Xremainder, index, array, Y):
	x=1
	Max = max(array[Y,0])
	for _ in range(Max - array[Y, 0, index]+1):
		
		for _ in range(int(Xdivision) + int(XremainderCount)):
			try:
				array[Y,x,index] = Xcolor
			except:
				return array
			x+=1
			
		if int(XremainderCount) == 1:
			XremainderCount -= 1
		XremainderCount += Xremainder
		Xcolor += 1
		
	return array
