import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image as Bg
from kivy.core.image import Image as CoreImage
from io import BytesIO
from PIL import Image, ImageDraw
from kivy.core.window import Window
from kivy.graphics import Line, InstructionGroup, Color
import math
import numpy as np
import numba as nb
from kivy.clock import Clock
from functions import DrawSet
import time
kivy.require("2.0.0")

class Draw(Widget):
	Width = 500
	Height =500
	ratio = float(Height/Width)
	glow = 0
	offset = 10
	maxIt = 300
	light = 255
	WWidth = Width
	WHeight = Height
	Window.size = (WWidth, WHeight)
	check = 1
	xStart = -2
	xEnd = 2
	xDist = abs(xEnd-xStart)
	yStart = -(xDist*ratio)/2
	yEnd = (xDist*ratio)/2
	yDist = abs(yEnd-yStart)
	array = np.zeros((Height, Width, 3), dtype=np.uint8)


	def __init__(self, **kwargs):
		super(Draw, self).__init__(**kwargs)
		with self.canvas:

			self.Zoom = Window.request_keyboard(None, self)
			self.Zoom.bind(on_key_up = self.ZoomInOut)
			
			self.MainSet = Bg(pos=(0, self.WHeight - self.Height), size= (self.Width, self.Height))
			
			self.bytes_io = BytesIO()
			self.array = DrawSet(self.Width, self.Height, self.xStart, self.xDist , self.yStart, self.yDist, self.maxIt)
			
			self.img = Image.fromarray(np.flipud(self.array), 'HSV')
			self.img.convert('RGB').save(self.bytes_io, 'PNG')
			self.MainSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture
	
			
	def on_touch_move(self, touch):
		self.secondtouch = touch.pos
		self.Array = DrawSet(self.Width, self.Height, self.xStart, self.xDist, self.yStart, self.yDist, self.maxIt)
			
		self.bytes_io = BytesIO()
		self.img = Image.fromarray(np.flipud(self.Array), 'HSV')
		self.img.convert('RGB').save(self.bytes_io, 'PNG')
		self.MainSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture
		
		self.touch2 = [(self.secondtouch[0]/self.Width)*self.xDist + self.xStart, self.secondtouch[1]/self.Height*self.yDist + self.yStart]
		self.touch1 = [(self.firsttouch[0]/self.Width)*self.xDist + self.xStart, self.firsttouch[1]/self.Height*self.yDist + self.yStart]
		self.shift = [self.touch2[0]-self.touch1[0], self.touch2[1]-self.touch1[1]]	
		self.xStart = self.xStart - self.shift[0]
		self.xEnd = self.xEnd - self.shift[0]

		self.yStart = self.yStart - self.shift[1]
		self.yEnd = self.yEnd - self.shift[1]

		self.xDist = abs(self.xEnd - self.xStart)
		self.yDist = abs(self.yEnd - self.yStart)
		
		self.firsttouch = self.secondtouch
				
	def on_touch_down(self, touch):
		self.firsttouch = touch.pos

	def ZoomInOut(self, window, keycode):
		
		if keycode[1] == "w":
			self.xStart = self.xStart + self.xDist*0.20
			self.xEnd = self.xEnd - self.xDist*0.20

			self.yStart = self.yStart + self.yDist*0.20
			self.yEnd = self.yEnd - self.yDist*0.20

			self.xDist = abs(self.xEnd - self.xStart)
			self.yDist = abs(self.yEnd - self.yStart)

	
		elif keycode[1] == "s":
			self.xStart = self.xStart - self.xDist*0.20
			self.xEnd = self.xEnd + self.xDist*0.20
			self.yStart = self.yStart - self.yDist*0.20
			self.yEnd = self.yEnd + self.yDist*0.20

			self.xDist = abs(self.xEnd - self.xStart)
			self.yDist = abs(self.yEnd - self.yStart)

		self.Array = DrawSet(self.Width, self.Height, self.xStart, self.xDist, self.yStart, self.yDist, self.maxIt)
		self.bytes_io = BytesIO()
		self.img = Image.fromarray(np.flipud(self.Array), 'HSV')
		self.img.convert('RGB').save(self.bytes_io, 'PNG')

		self.MainSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture
			
		

	def ImageByte(self, instance, ImageByte):
		self.Buffer = BytesIO(ImageByte)
		self.BgIm = CoreImage(self.Buffer, ext= 'png')
		return self.BgIm


class MandelBrot(App):
    def build(self):
        return Draw()

if __name__ == "__main__":
    MandelBrot().run()
