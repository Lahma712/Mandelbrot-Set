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
import glob
import cv2
import os
from gradient import polylinear_gradient
kivy.require("2.0.0")
import ffmpeg


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
	colorPoints = 100
	totalColors = 1000
	gradient = np.concatenate((np.array(polylinear_gradient(colorPoints, totalColors)), [(255,0,0)]), axis= 0)
	check = 0
	

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
		
		if keycode[1] == "w":
			self.xStart = self.xStart + self.xDist*0.10
			self.xEnd = self.xEnd - self.xDist*0.10

			self.yStart = self.yStart + self.yDist*0.10
			self.yEnd = self.yEnd - self.yDist*0.10

			self.xDist = self.xEnd - self.xStart
			self.yDist = self.yEnd - self.yStart

	
		elif keycode[1] == "s":
			self.xStart = self.xStart - self.xDist*0.10
			self.xEnd = self.xEnd + self.xDist*0.10
			self.yStart = self.yStart - self.yDist*0.10
			self.yEnd = self.yEnd + self.yDist*0.10

			self.xDist = self.xEnd - self.xStart
			self.yDist = self.yEnd - self.yStart

		elif keycode[1] == "up":
			self.maxIt += 100
		elif keycode[1] == "down":
			self.maxIt -= 10
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

		elif keycode[1] == "i":
			self.ItVid = self.maxIt
			while self.ItVid != 0:
				self.array = DrawSet(self.Width, self.Height, self.xStart, self.xDist, self.yStart, self.yDist, self.ItVid, self.gradient)
				self.img = Image.fromarray(np.flipud(self.array), 'RGB')
				self.savename = r'Video\I' + str(self.ItVid) + r'.png'
				self.img.save(self.savename, 'PNG')
				self.ItVid -= 1

			img_array = []

			for filename in sorted(glob.glob(r'Video\*.png'), key=lambda name: int(name[7:-4])):
				img = cv2.imread(filename)
				height, width, layers = img.shape
				size = (width,height)
				img_array.append(img)


 
			
			out = cv2.VideoWriter(r'Video\Video.avi',0, 15, size)
			for i in range(len(img_array)):
				out.write(img_array[i])
			out.release()

			files = glob.glob(r'Video\*.png')
			for f in files:
				os.remove(f)

		elif keycode[1] == "k":
			self.number = 0
			while self.xStart > -2:

				self.array = DrawSet(self.Width, self.Height, self.xStart, self.xDist, self.yStart, self.yDist, self.maxIt, self.gradient)
				self.img = Image.fromarray(np.flipud(self.array), 'RGB')
				self.savename = r'Video\I' + str(self.number) + r'.png'
				self.img.save(self.savename, 'PNG')

				self.xStart = self.xStart - self.xDist*0.001
				self.xEnd = self.xEnd + self.xDist*0.001
				self.yStart = self.yStart - self.yDist*0.001
				self.yEnd = self.yEnd + self.yDist*0.001

				self.xDist = self.xEnd - self.xStart
				self.yDist = self.yEnd - self.yStart
				self.number +=1

			img_array = []

			for filename in sorted(glob.glob(r'Video\*.png'), key=lambda name: int(name[7:-4])):
				img = cv2.imread(filename)
				height, width, layers = img.shape
				img_array.append(img)


 
			
			out = cv2.VideoWriter(r'Video\Video.avi',0, 60, (self.Width, self.Height))
			for i in range(len(img_array)):
				out.write(img_array[i])
			out.release()

			files = glob.glob(r'Video\*.png')
			for f in files:
				os.remove(f)
				

			

			
	

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
