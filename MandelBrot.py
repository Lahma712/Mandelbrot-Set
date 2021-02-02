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
from gradient import polylinear_gradient, rand_rgb_color
import subprocess as sp
import ffmpeg
from ColorPicker import colorbar, colorsquare
kivy.require("2.0.0")
import ffmpeg
import copy
import random


class Draw(Widget):
	Width = 500
	Height =500
	ratio = float(Height/Width)
	maxIt = 20
	WWidth = Width
	WHeight = Height
	Window.size = (WWidth*2, WHeight)
	xStart = -2.5
	xEnd = 1.5
	xDist = xEnd-xStart
	yStart = -(xDist*ratio)/2
	yEnd = (xDist*ratio)/2
	yDist = yEnd-yStart
	array = np.zeros((Height, Width, 3), dtype=np.uint8)
	numColorPoints = 10
	colorPoints = rand_rgb_color(numColorPoints)
	totalColors = 1000
	Selectcolor = [255,0,0]
	SqyIndex = 1
	SqxIndex = 1
	gradient = np.concatenate((np.array(polylinear_gradient(colorPoints, totalColors)), [(0,0,0)]) , axis= 0)
	check = 0
	alg = 0
	
	def __init__(self, **kwargs):
		super(Draw, self).__init__(**kwargs)
		with self.canvas:
			self.Zoom = Window.request_keyboard(None, self)
			self.Zoom.bind(on_key_up= self.ZoomInOut)
			self.MainSet = Bg(pos=(0, 0), size= (self.Width, self.Height))
			self.colorbar = Bg(pos=(int(self.Width * 1.80), int(self.Height * 0.5)), size= (int(self.Width * 0.10), int(self.Height * 0.40)))
			self.colorsquare = Bg(pos=(int(self.Width * 1.10), int(self.Height * 0.5)), size= (int(self.Width * 0.40), int(self.Width*0.40 )))
			self.colorwindow = Bg(pos=(int(self.Width * 1.52), int(self.Height * 0.5)), size= (int(self.Width * 0.20), int(self.Width*0.40 )))
			self.Gradient = Bg(pos=(int(self.Width), int(self.Height * 0.20)), size= (int(self.Width), int(self.Height*0.10 )))
			self.bytes_io = BytesIO()
			self.array = DrawSet(self.Width, self.Height, self.xStart, self.xDist , self.yStart, self.yDist, self.maxIt, self.gradient, self.alg)
			self.img = Image.fromarray(np.flipud(self.array), 'RGB')
			self.img.save(self.bytes_io, 'PNG')
			self.MainSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture

			self.bytes_io = BytesIO()
			self.BarArray = colorbar(self.colorbar.size[0], self.colorbar.size[1])
			self.img = Image.fromarray(self.BarArray, 'RGB')
			self.img.save(self.bytes_io, 'PNG')
			self.colorbar.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture

			self.bytes_io = BytesIO()
			self.SquareArray = colorsquare(self.colorsquare.size[0], self.colorsquare.size[1], [255,0, 0])
			self.img = Image.fromarray(self.SquareArray, 'RGB')
			self.img.save(self.bytes_io, 'PNG')
			self.colorsquare.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture

			self.bytes_io = BytesIO()
			self.WindowArray = np.full((self.colorwindow.size[1],self.colorwindow.size[0], 3), self.Selectcolor, dtype=np.uint8)
			self.img = Image.fromarray(self.WindowArray, 'RGB')
			self.img.save(self.bytes_io, 'PNG')
			self.colorwindow.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture

			self.bytes_io = BytesIO()
			self.GradientArray = np.array(self.colorPoints, dtype=np.uint8)
			self.GradientArray = np.repeat(self.GradientArray, int((self.Width)/len(self.GradientArray)), axis = 0)
			self.GradientArray = np.resize(self.GradientArray, (int(self.Height*0.10), len(self.GradientArray), 3))
			self.img = Image.fromarray(self.GradientArray, 'RGB')
			self.img.save(self.bytes_io, 'PNG')
			self.Gradient.size[0] = len(self.GradientArray[0])
			self.Gradient.pos[0] = self.Width + int((self.Width - len(self.GradientArray[0]))/2)
			self.Gradient.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture
			
			self.WidthBox = TextInput(text = "Width: ", font_size = self.Height * 0.022, size = (self.Width * 0.25, self.Height*0.05), pos = (self.Width ,self.Height*0.07), multiline = False)
			self.HeightBox = TextInput(text = "Height: ", font_size = self.Height * 0.022, size = (self.Width * 0.25, self.Height*0.05), pos = (self.Width*1.25,self.Height*0.07 ), multiline = False)
			self.AntialiasBox = TextInput(text = "Antialias: ", font_size = self.Height * 0.022, size = (self.Width * 0.25, self.Height*0.05), pos = (self.Width *1.50, self.Height*0.07), multiline = False)
			self.FpsBox = TextInput(text = "FPS: ", font_size = self.Height * 0.022, size = (self.Width * 0.25, self.Height*0.05), pos = (self.Width *1.75, self.Height*0.07), multiline = False)
			self.SaveImageBtn = Button(text="Save Image", font_size=self.Height*0.03, size = (self.Width *0.20, self.Height*0.05), pos =(self.Width , 0))
			self.ZoomVideoBtn = Button(text="Zoom Video", font_size=self.Height*0.03, size = (self.Width *0.20, self.Height*0.05), pos =(self.Width*1.25 , 0))
			self.IterVideoBtn = Button(text="Iter. Video", font_size=self.Height*0.03, size = (self.Width *0.20, self.Height*0.05), pos =(self.Width*1.50 , 0))
			self.add_widget(self.SaveImageBtn)
			self.add_widget(self.AntialiasBox)
			self.add_widget(self.HeightBox)
			self.add_widget(self.WidthBox)
			self.add_widget(self.FpsBox)
			self.add_widget(self.ZoomVideoBtn)
			self.add_widget(self.IterVideoBtn)
			self.SaveImageBtn.bind(on_press = self.SaveImage)
			self.ZoomVideoBtn.bind(on_press = self.ZoomVideo)
			self.IterVideoBtn.bind(on_press = self.IterVideo)

	
	def on_touch_move(self, touch):
		if touch.pos[0] < self.Width:
			self.secondtouch = touch.pos
			self.array = DrawSet(self.Width, self.Height, self.xStart, self.xDist, self.yStart, self.yDist, self.maxIt, self.gradient, self.alg)
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
		if touch.pos[0] > self.Width:
			if ((touch.pos[0] >= self.colorbar.pos[0] and touch.pos[0] <= self.colorbar.pos[0]+self.colorbar.size[0]) and (touch.pos[1] >= self.colorbar.pos[1] and touch.pos[1] <= self.colorbar.pos[1] + self.colorbar.size[1])):
				self.SquareColor(self, touch.pos)

			elif ((touch.pos[0] >= self.colorsquare.pos[0] and touch.pos[0] <= self.colorsquare.pos[0]+self.colorsquare.size[0]) and (touch.pos[1] >= self.colorsquare.pos[1] and touch.pos[1] <= self.colorsquare.pos[1] + self.colorsquare.size[1])):
				self.FinalColor(self, touch.pos)

			elif ((touch.pos[0] >= self.Gradient.pos[0] and touch.pos[0] <= self.Gradient.pos[0]+self.Gradient.size[0]) and (touch.pos[1] >= self.Gradient.pos[1] and touch.pos[1] <= self.Gradient.pos[1] + self.Gradient.size[1])):
				self.SetGradientColor(self, touch.pos)

			return super(Draw, self).on_touch_down(touch)
		self.firsttouch = touch.pos

	def SetGradientColor(self, instance, pos):
		color = copy.deepcopy(self.Selectcolor)
		xIndex = int(pos[0] - self.Gradient.pos[0])
		index = int(xIndex/(int(self.Gradient.size[0]/self.numColorPoints)))
		self.colorPoints[index] = self.Selectcolor
		self.setColor(self)


	def SquareColor(self,instance, pos):
		BarxIndex = int(pos[0] - self.colorbar.pos[0])
		BaryIndex = int(-pos[1] + self.colorbar.pos[1] + self.colorbar.size[1])
		color = copy.copy(self.BarArray[BaryIndex, BarxIndex])
		self.bytes_io = BytesIO()
		self.SquareArray = colorsquare(int(self.Width * 0.40), int(self.Width*0.40), color)
		self.img = Image.fromarray(self.SquareArray, 'RGB')
		self.img.save(self.bytes_io, 'PNG')
		self.colorsquare.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture
		try:
			self.Selectcolor = copy.copy(self.SquareArray[self.SqyIndex, self.SqxIndex])
		except:
			pass

		self.bytes_io = BytesIO()
		self.WindowArray = np.full((self.colorwindow.size[1],self.colorwindow.size[0], 3), self.Selectcolor, dtype=np.uint8)
		self.img = Image.fromarray(self.WindowArray, 'RGB')
		self.img.save(self.bytes_io, 'PNG')
		self.colorwindow.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture



	def FinalColor(self, instance, pos):
		self.SqxIndex = int(pos[0] - self.colorsquare.pos[0])
		self.SqyIndex = int(-pos[1] + self.colorsquare.pos[1] + self.colorsquare.size[1])
		try:
			self.Selectcolor = copy.copy(self.SquareArray[self.SqyIndex, self.SqxIndex])
		except:
			pass

		self.bytes_io = BytesIO()
		self.WindowArray = np.full((self.colorwindow.size[1],self.colorwindow.size[0], 3), self.Selectcolor, dtype=np.uint8)
		self.img = Image.fromarray(self.WindowArray, 'RGB')
		self.img.save(self.bytes_io, 'PNG')
		self.colorwindow.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture


	def ZoomVideo(self, instance):
		self.number = 0
		self.xStartVid = self.xStart
		self.xEndVid = self.xEnd
		self.yStartVid = self.yStart
		self.yEndVid = self.yEnd
		self.xDistVid = self.xEndVid - self.xStartVid
		self.yDistVid = self.yEndVid - self.yStartVid
		try:
			self.SHeight = int(''.join(filter(str.isdigit, self.HeightBox.text)))
			self.Antialias = int(''.join(filter(str.isdigit, self.AntialiasBox.text)))
			self.SWidth = int(''.join(filter(str.isdigit, self.WidthBox.text)))
		except:
			pass

		while self.xStartVid > -2.5:
			self.array = DrawSet(self.SWidth*self.Antialias, self.SHeight*Antialias, self.xStartVid, self.xDistVid, self.yStartVid, self.yDistVid, self.maxIt, self.gradient, self.alg)
			self.img = Image.fromarray(np.flipud(self.array), 'RGB')
			self.savename = 'Video\\' + str(self.number) + '.png'
			self.img = self.img.resize((self.SWidth, self.SHeight), Image.ANTIALIAS)
			self.img.save(self.savename, 'PNG')

			self.xStartVid = self.xStartVid - self.xDistVid*0.01
			self.xEndVid = self.xEndVid + self.xDistVid*0.01
			self.yStartVid = self.yStartVid - self.yDistVid*0.01
			self.yEndVid = self.yEndVid + self.yDistVid*0.01

			self.xDistVid = self.xEndVid - self.xStartVid
			self.yDistVid = self.yEndVid - self.yStartVid
			self.number +=1
		self.Video(self)

	def IterVideo(self, instance):
		self.ItVid = self.maxIt

		try:
			self.SHeight = int(''.join(filter(str.isdigit, self.HeightBox.text)))
			self.Antialias = int(''.join(filter(str.isdigit, self.AntialiasBox.text)))
			self.SWidth = int(''.join(filter(str.isdigit, self.WidthBox.text)))
		except:
			pass

		while self.ItVid != 0:
			self.array = DrawSet(self.SWidth*self.Antialias, self.SHeight*self.Antialias, self.xStart, self.xDist, self.yStart, self.yDist, self.ItVid, self.gradient, self.alg)
			self.img = Image.fromarray(np.flipud(self.array), 'RGB')
			self.savename = 'Video\\' + str(self.ItVid) + '.png'
			self.img = self.img.resize((self.SWidth, self.SHeight), Image.ANTIALIAS)
			self.img.save(self.savename, 'PNG')
			self.ItVid -= 1
		self.Video(self)

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
			self.maxIt += 10
		elif keycode[1] == "down":
			self.maxIt -= 10
		elif keycode[1] == "r":
			self.colorPoints = rand_rgb_color(self.numColorPoints)
			self.setColor(self)

		elif keycode[1] == "left":
			self.colorPoints = np.delete(self.colorPoints, self.numColorPoints-1, axis=0)
			self.numColorPoints -=1
			self.setColor(self)

		elif keycode[1] == "right":
			self.colorPoints = np.insert(self.colorPoints, self.numColorPoints, tuple(self.Selectcolor), axis=0)
			self.numColorPoints +=1
			self.setColor(self)
			
		elif keycode[1] == "a":
			if self.alg == 0:
				self.alg = 1
			else:
				self.alg = 0 

		self.array = DrawSet(self.Width, self.Height, self.xStart, self.xDist, self.yStart, self.yDist, self.maxIt, self.gradient, self.alg)
		self.bytes_io = BytesIO()
		self.img = Image.fromarray(np.flipud(self.array), 'RGB')
		self.img.save(self.bytes_io, 'PNG')
		self.MainSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture

		

	def setColor(self, instance):
		self.gradient = np.concatenate((np.array(polylinear_gradient(self.colorPoints, self.totalColors)), [(0,0,0)]), axis= 0)
		self.bytes_io = BytesIO()
		self.GradientArray = np.array(self.colorPoints, dtype=np.uint8)
		self.GradientArray = np.repeat(self.GradientArray, int((self.Width)/len(self.GradientArray)), axis = 0)
		self.GradientArray = np.resize(self.GradientArray, (int(self.Height*0.10), len(self.GradientArray), 3))

		self.img = Image.fromarray(self.GradientArray, 'RGB')
		self.img.save(self.bytes_io, 'PNG')
		self.Gradient.size[0] = len(self.GradientArray[0])
		self.Gradient.pos[0] = self.Width + int((self.Width - len(self.GradientArray[0]))/2)
		self.Gradient.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture
		
		self.array = DrawSet(self.Width, self.Height, self.xStart, self.xDist, self.yStart, self.yDist, self.maxIt, self.gradient, self.alg)
		self.bytes_io = BytesIO()
		self.img = Image.fromarray(np.flipud(self.array), 'RGB')
		self.img.save(self.bytes_io, 'PNG')
		self.MainSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture


	def Video(self, instance):
		try:
			self.Fps = int(''.join(filter(str.isdigit, self.FpsBox.text)))
			cmd = 'ffmpeg -framerate {} -i Video\\%d.png -c:v libx264 -crf 1 -pix_fmt yuv420p -framerate {} Video{}.avi'.format(self.Fps, self.Fps, random.randint(1, 9000))
			sp.call(cmd,shell=True)
			files = glob.glob('Video\\*.png') #-pix_fmt yuv420p
			for f in files:
				os.remove(f)
		except:
			pass
		
	
	def SaveImage(self, instance):
		try:
			self.SHeight = int(''.join(filter(str.isdigit, self.HeightBox.text)))
			self.Antialias = int(''.join(filter(str.isdigit, self.AntialiasBox.text)))
			self.SWidth = int(''.join(filter(str.isdigit, self.WidthBox.text)))
		except:
			pass

		self.xStartSave = self.xStart
		self.yStartSave = self.yStart
		try:
			self.array = DrawSet(self.SWidth*self.Antialias, self.SHeight*self.Antialias, self.xStartSave, self.xDist, (self.yStartSave + (self.xDist*self.ratio)/2) - (self.xDist * (self.SHeight/self.SWidth))/2, self.xDist * (self.SHeight/self.SWidth), self.maxIt, self.gradient, self.alg)
			self.img = Image.fromarray(np.flipud(self.array), 'RGB')
			self.img = self.img.resize((self.SWidth, self.SHeight), Image.ANTIALIAS)
			self.img.save('Fractal{}.png'.format(random.randint(1,9000)))
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