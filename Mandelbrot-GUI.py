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
kivy.require("2.0.0")

class Draw(Widget):
	Width = 500
	Height = 500
	ratio = float(Height/Width)
	glow = 0
	offset = 20
	maxIt = 300
	light = 255
	WWidth = 1000
	WHeight = 500
	Window.size = (WWidth, WHeight)
	array = np.zeros((Height, Width, 3), dtype=np.uint8)
	check = 1
	x1 = -2.5
	x2 = 1.5
	y1 = -(4*ratio)/2
	y2 = (4*ratio)/2


	def __init__(self, **kwargs):
		super(Draw, self).__init__(**kwargs)
		with self.canvas:

			self.MainSet = Bg(pos=(0, self.WHeight - self.Height), size= (self.Width, self.Height))
			self.ZoomSet = Bg(pos=(self.Width, self.WHeight - self.Height), size= (self.Width, self.Height))

			self.bytes_io = BytesIO()
			self.DrawSet(self.Width, self.Height, self.x1, 4 , self.y1, 4*self.ratio, self.maxIt, 0, 0, 0, 0, self.light, 0, True, self.array)
			
			self.img = Image.fromarray(np.flipud(self.array), 'HSV')
			self.img.convert('RGB').save(self.bytes_io, 'PNG')
			self.MainSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture
			
	def on_touch_down(self, touch):

		with self.canvas:

			try:
				self.canvas.remove(self.zoomBox)
			except:
				pass

			
			self.WZoom = 50
			self.HZoom = 50
			self.touchpos = list(touch.pos)

			
			Color(255,255,255)
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
			
			self.zoomArray = np.zeros((self.Height, self.Width, 3), dtype=np.uint8)

			self.DrawSet(self.Width, self.Height, self.xStart, self.xDist, self.yStart, self.yDist, self.maxIt, 0, 0, 0, 0, self.light, 0, True, self.zoomArray)
				
			self.bytes_io = BytesIO()
			self.img = Image.fromarray(np.flipud(self.zoomArray), 'HSV')
			self.img.convert('RGB').save(self.bytes_io, 'PNG')

			if touch.pos[0] > self.Width:
				self.MainSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture

			else:
				self.ZoomSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture

	
	def mandelbrot(self, c,maxIt): #mandelbrot function
		z = 0
		n = 0
		while abs(z) <= 2 and n < maxIt:
			z = z * z + c
			n += 1
		return n 


	def DrawSet(self, W, H, xStart, xDist, yStart, yDist, maxIt, hue, saturation, value, glow, a, b, Qcolor, array):
		for x in range(0, W):
			for y in range (0, H):
				
				c = complex( (x/W)* xDist +xStart, -((y/H) * yDist + yStart))
				
				cIt = self.mandelbrot(c, maxIt)
				color = int((255 * cIt) / maxIt)
				
				if Qcolor == True:
					if color + self.offset > 255:
						hue = (color + self.offset) - 255
					else:
						hue = color + self.offset
						saturation = 255 - glow * color

				array[y,x] = (hue, saturation, value if cIt == maxIt else a+b*glow * color)
				
				
	def ImageByte(self, instance, ImageByte):
		self.Buffer = BytesIO(ImageByte)
		self.BgIm = CoreImage(self.Buffer, ext= 'png')
		return self.BgIm


class MandelBrot(App):
    def build(self):
        return Draw()

if __name__ == "__main__":
    MandelBrot().run()