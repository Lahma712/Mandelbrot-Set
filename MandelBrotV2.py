import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image as Bg
from kivy.core.image import Image as CoreImage
from io import BytesIO
from kivy.uix.textinput import TextInput
from PIL import Image, ImageDraw
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.graphics import Line, InstructionGroup, Color
import math
import numpy as np
import numba as nb
from kivy.clock import Clock
from functions import DrawSet
import time
from gradient import polylinear_gradient
kivy.require("2.0.0")


class Draw(Widget):
	Width = 400
	Height =400
	ratio = float(Height/Width)
	maxIt = 20
	WWidth = Width
	WHeight = Height
	Window.size = (WWidth, WHeight)
	xStart = -2.5
	xEnd = 1.5
	xDist = xEnd-xStart
	yStart = -(xDist*ratio)/2
	yEnd = (xDist*ratio)/2
	yDist = yEnd-yStart
	array = np.zeros((Height, Width, 3), dtype=np.uint8)
	colorPoints = 3
	totalColors = 30
	gradient = np.concatenate((np.array(polylinear_gradient(colorPoints, totalColors)), [(0,0,0)]), axis= 0)
	check = 0
	
	print(len(gradient))

	def __init__(self, **kwargs):
		super(Draw, self).__init__(**kwargs)
		with self.canvas:
			self.Zoom = Window.request_keyboard(None, self)
			self.Zoom.bind(on_key_up = self.ZoomInOut)
			
			self.MainSet = Bg(pos=(0, 0), size= (self.Width, self.Height))
			
			self.bytes_io = BytesIO()
			self.array = DrawSet(self.Width, self.Height, self.xStart, self.xDist , self.yStart, self.yDist, self.maxIt, self.gradient)
			
			self.img = Image.fromarray(np.flipud(self.array), 'RGB')
			self.img.save(self.bytes_io, 'PNG')
			self.MainSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture
	
			
	def on_touch_move(self, touch):

		self.secondtouch = touch.pos
		self.array = DrawSet(self.Width, self.Height, self.xStart, self.xDist, self.yStart, self.yDist, self.maxIt, self.gradient)
			
		self.bytes_io = BytesIO()
		self.img = Image.fromarray(np.flipud(self.array), 'RGB')
		self.img.save(self.bytes_io, 'PNG')
		self.MainSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture
		
		self.touch2 = [(self.secondtouch[0]/self.Width)*self.xDist + self.xStart, (self.secondtouch[1]/self.Height)*self.yDist + self.yStart]
		self.touch1 = [(self.firsttouch[0]/self.Width)*self.xDist + self.xStart, (self.firsttouch[1]/self.Height)*self.yDist + self.yStart]
		self.shift = [self.touch2[0]-self.touch1[0], self.touch2[1]-self.touch1[1]]	
		self.xStart = (self.xStart - self.shift[0])
		self.xEnd = (self.xEnd - self.shift[0])

		self.yStart = (self.yStart - self.shift[1])
		self.yEnd = (self.yEnd - self.shift[1])

		self.xDist = (self.xEnd - self.xStart)
		self.yDist = (self.yEnd - self.yStart)
		
		self.firsttouch = self.secondtouch
				
	def on_touch_down(self, touch):
		self.firsttouch = touch.pos
		if touch.pos[1] > self.Height:
			super(Draw, self).on_touch_down(touch)

	def ZoomInOut(self, window, keycode):
		start = time.time()
		if keycode[1] == "w":
			self.xStart = self.xStart + self.xDist*0.20
			self.xEnd = self.xEnd - self.xDist*0.20

			self.yStart = self.yStart + self.yDist*0.20
			self.yEnd = self.yEnd - self.yDist*0.20

			self.xDist = self.xEnd - self.xStart
			self.yDist = self.yEnd - self.yStart

	
		elif keycode[1] == "s":
			self.xStart = self.xStart - self.xDist*0.20
			self.xEnd = self.xEnd + self.xDist*0.20
			self.yStart = self.yStart - self.yDist*0.20
			self.yEnd = self.yEnd + self.yDist*0.20

			self.xDist = self.xEnd - self.xStart
			self.yDist = self.yEnd - self.yStart

		elif keycode[1] == "up":
			self.maxIt += 20
		elif keycode[1] == "down":
			self.maxIt -= 20
		elif keycode[1] == "r":
			self.gradient = np.concatenate((np.array(polylinear_gradient(self.colorPoints, self.totalColors)), [(0,0,0)]), axis= 0)

		elif keycode[1] == "f":
			with self.canvas:

				if self.check == 0:
					self.WidthBox = TextInput(text = "Width: ", font_size = self.Height * 0.022, size = (self.Width * 0.25, self.Height*0.05), pos = (0,self.Height), multiline = False)
					self.HeightBox = TextInput(text = "Height: ", font_size = self.Height * 0.022, size = (self.Width * 0.25, self.Height*0.05), pos = (self.Width * 0.25,self.Height), multiline = False)
					self.AntialiasBox = TextInput(text = "Antialias: ", font_size = self.Height * 0.022, size = (self.Width * 0.25, self.Height*0.05), pos = (self.Width * 0.50, self.Height), multiline = False)
					self.SaveBtn = Button(text="Save", font_size=self.Height*0.03, size = (self.Width *0.25, self.Height*0.05), pos =(self.Width * 0.75, self.Height))
					self.add_widget(self.SaveBtn)
					self.add_widget(self.AntialiasBox)
					self.add_widget(self.HeightBox)
					self.add_widget(self.WidthBox)
					self.SaveBtn.bind(on_press = self.Save)
					self.WidthBox.bind(text = self.WidthText)
					self.HeightBox.bind(text = self.HeightText)
					self.AntialiasBox.bind(text = self.AntialiasText)
					Window.size = (self.Width, self.Height + self.WidthBox.size[1])
					self.check = 1

				else:

					self.remove_widget(self.WidthBox)
					self.remove_widget(self.HeightBox)
					self.remove_widget(self.AntialiasBox)
					self.remove_widget(self.SaveBtn)
					Window.size = (self.Width, self.Height)
					self.check = 0
				

			
	

		self.array = DrawSet(self.Width, self.Height, self.xStart, self.xDist, self.yStart, self.yDist, self.maxIt, self.gradient)
		self.bytes_io = BytesIO()
		self.img = Image.fromarray(np.flipud(self.array), 'RGB')
		self.img.save(self.bytes_io, 'PNG')
		self.MainSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture

		
	
	def WidthText(self, instance, text):
		try:
			self.SWidth = int(''.join(filter(str.isdigit, self.WidthBox.text)))
		except:
			pass

	def HeightText(self, instance, text):
		try:
			self.SHeight = int(''.join(filter(str.isdigit, self.HeightBox.text)))
		except:
			pass

	def AntialiasText(self, instance, text):
		try: 
			self.Antialias = int(''.join(filter(str.isdigit, self.AntialiasBox.text)))
		except:
			pass
	
		
	def Save(self, instance):
		try:
			self.array = DrawSet(self.SWidth*self.Antialias, self.SHeight*self.Antialias, self.xStart, self.xDist, (self.yStart + (self.xDist*self.ratio)/2) - (self.xDist * (self.SHeight/self.SWidth))/2, self.xDist * (self.SHeight/self.SWidth), self.maxIt, self.gradient)
			self.img = Image.fromarray(np.flipud(self.array), 'RGB')
			self.img = self.img.resize((self.SWidth, self.SHeight), Image.ANTIALIAS)
			self.img.save('Fractal.png')
			self.img.show()
		except:
			pass


	def ImageByte(self, instance, ImageByte):
		self.Buffer = BytesIO(ImageByte)
		self.BgIm = CoreImage(self.Buffer, ext= 'png')
		return self.BgIm


class MandelBrot(App):
    def build(self):
        return Draw()

if __name__ == "__main__":
    MandelBrot().run()
