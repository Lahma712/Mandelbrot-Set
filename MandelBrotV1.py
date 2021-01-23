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
from functions import DrawSet
import time
kivy.require("2.0.0")

class Draw(Widget):
	Width = 500
	Height = 500
	ratio = float(Height/Width)
	glow = 0
	offset = 10
	maxIt = 1000
	light = 255
	WWidth = Width*2
	WHeight = Height
	Window.size = (WWidth, WHeight)
	check = 1
	x1 = -2
	x2 = 2
	xDist = abs(x2-x1)
	y1 = -(xDist*ratio)/2
	y2 = -y1
	array = np.zeros((Height, Width, 3), dtype=np.uint8)


	def __init__(self, **kwargs):
		super(Draw, self).__init__(**kwargs)
		with self.canvas:

			self.MainSet = Bg(pos=(0, self.WHeight - self.Height), size= (self.Width, self.Height))
			self.ZoomSet = Bg(pos=(self.Width, self.WHeight - self.Height), size= (self.Width, self.Height))

			self.bytes_io = BytesIO()
			self.array = DrawSet(self.Width, self.Height, self.x1, abs(self.x2-self.x1) , self.y1, abs(self.x2-self.x1)*self.ratio, self.maxIt)
			
			self.img = Image.fromarray(np.flipud(self.array), 'HSV')
			self.img.convert('RGB').save(self.bytes_io, 'PNG')
			self.MainSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture
			
	def on_touch_down(self, touch):

		

		with self.canvas:

			try:
				self.canvas.remove(self.zoomBox)
			except:
				pass

			
			self.WZoom = self.Width/10
			self.HZoom = self.Height/10
			self.touchpos = list(touch.pos)

			
			Color(0,0,0)
			self.zoomBox = Line(rectangle = (touch.pos[0], touch.pos[1] ,self.WZoom, self.HZoom), width = 1)
			
			if touch.pos[0] > self.Width:
				self.touchpos[0] = self.touchpos[0] - self.Width
				if self.check == 1:
					
					self.x1 = self.xStart
					self.x2 = self.xEnd
					self.y1 = self.yStart
					self.y2 = self.yEnd
					self.check = 0

					
			else:
				if self.check == 0:
					self.x1 = self.xStart
					self.x2 = self.xEnd
					self.y1 = self.yStart
					self.y2 = self.yEnd
					self.check = 1
				

			self.xStart = float((self.touchpos[0]/self.Width) * (abs(self.x1-self.x2)) + self.x1)
			self.xEnd = float(((self.touchpos[0]+self.WZoom)/self.Width) * (abs(self.x1-self.x2)) + self.x1)

			self.xDist = float(abs(self.xStart - self.xEnd))
			self.yDist = float(self.xDist * self.ratio) 
				
			self.yStart =float((((self.touchpos[1]) - (self.WHeight - self.Height))/self.Height) * (abs(self.y1-self.y2)) + self.y1)
			self.yEnd = float((((self.touchpos[1]+self.HZoom - (self.WHeight - self.Height)))/self.Height) * (abs(self.y1-self.y2)) + self.y1)
			


			self.zoomArray = DrawSet(self.Width, self.Height, self.xStart, self.xDist, self.yStart, self.yDist, self.maxIt)
				
			self.bytes_io = BytesIO()
			self.img = Image.fromarray(np.flipud(self.zoomArray), 'HSV')
			self.img.convert('RGB').save(self.bytes_io, 'PNG')

			if touch.pos[0] > self.Width:
				self.MainSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture

			else:
				self.ZoomSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture

	
			
				
				
	def ImageByte(self, instance, ImageByte):
		self.Buffer = BytesIO(ImageByte)
		self.BgIm = CoreImage(self.Buffer, ext= 'png')
		return self.BgIm


class MandelBrot(App):
    def build(self):
        return Draw()

if __name__ == "__main__":
    MandelBrot().run()
