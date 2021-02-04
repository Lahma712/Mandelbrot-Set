import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image as Bg
from kivy.core.image import Image as CoreImage
from kivy.uix.textinput import TextInput
from PIL import Image, ImageDraw
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.graphics import Line, InstructionGroup, Color
from kivy.clock import Clock
from io import BytesIO
import numpy as np
import glob
import os
import subprocess as sp
import ffmpeg
from ColorPicker import colorbar, colorsquare
from gradient import polylinear_gradient, rand_rgb_color
from functions import DrawSet
import ffmpeg
import copy
import random
kivy.require("2.0.0")


class Draw(Widget):
	Width = 500  #Width of render window
	Height =500  #Height of render window
	ratio = float(Height/Width)
	maxIt = 20 #initial maximal number of iterations 
	Window.size = (Width*2, Height)
	xStart = -2.5 #starting x coord
	xEnd = 1.5 #ending x coord
	xDist = xEnd-xStart 
	yStart = -(xDist*ratio)/2
	yEnd = (xDist*ratio)/2
	yDist = yEnd-yStart
	array = np.zeros((Height, Width, 3), dtype=np.uint8) #numpy array that holds rgb values for every pixel
	numColorPoints = 10 #initial number of control color points that the gradient goes through
	colorPoints = rand_rgb_color(numColorPoints) #array of random control color points
	totalColors = 1000 #total number of colors that the gradient can have
	Selectcolor = [255,0,0] #initial color picker window is set to red
	SqYIndex = 1 #Square Y Index
	SqXIndex = 1 #Square X Index
	gradient = np.concatenate((np.array(polylinear_gradient(colorPoints, totalColors)), [(0,0,0)]) , axis= 0) #array that holds initial gradient, 2D array 
	alg = 0 #variable that is used to check which coloring  algorithm should be used, 0 is the escape time coloring algorithm, 1 is a static coloring algorithm similar to histogram coloring
	
	def __init__(self, **kwargs):
		super(Draw, self).__init__(**kwargs)
		with self.canvas:
			self.Zoom = Window.request_keyboard(None, self) #keyboard function
			self.Zoom.bind(on_key_up= self.ZoomInOut) 
			self.MainSet = Bg(pos=(0, 0), size= (self.Width, self.Height)) #Fractal rendering window
			self.colorbar = Bg(pos=(int(self.Width * 1.80), int(self.Height * 0.5)), size= (int(self.Width * 0.10), int(self.Height * 0.40))) #Vertical rainbow color bar from color picker
			self.colorsquare = Bg(pos=(int(self.Width * 1.10), int(self.Height * 0.5)), size= (int(self.Width * 0.40), int(self.Width*0.40 ))) #color square where you can select the tint/shade of a color
			self.colorwindow = Bg(pos=(int(self.Width * 1.52), int(self.Height * 0.5)), size= (int(self.Width * 0.20), int(self.Width*0.40 ))) #color window which shows the selected color
			self.Gradient = Bg(pos=(int(self.Width), int(self.Height * 0.20)), size= (int(self.Width), int(self.Height*0.10 ))) #image of the gradient control color points
			self.bytes_io = BytesIO() #is used to store the images in the memory buffer
			self.array = DrawSet(self.Width, self.Height, self.xStart, self.xDist , self.yStart, self.yDist, self.maxIt, self.gradient, self.alg) #saves initial mandelbrot set in 3D array
			self.img = Image.fromarray(np.flipud(self.array), 'RGB')
			self.img.save(self.bytes_io, 'PNG') #save image to buffer
			self.MainSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture #replace texture of the MainSet Image

			#Create array images for colorbar, colorsquare, colorwindow and gradient and update the respective images in the GUI
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
			
			#Creates and adds buttons and text inputs for Width, Height, Antialias, Fps
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

	
	def on_touch_move(self, touch): #function that is called when you click and hold/move the mouse cursor, only when you are inside the rendering window
		if touch.pos[0] < self.Width:
			self.secondtouch = touch.pos #new touch position every time you move
			self.array = DrawSet(self.Width, self.Height, self.xStart, self.xDist, self.yStart, self.yDist, self.maxIt, self.gradient, self.alg)
			self.bytes_io = BytesIO()
			self.img = Image.fromarray(np.flipud(self.array), 'RGB')
			self.img.save(self.bytes_io, 'PNG')
			self.MainSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture
			self.touch2 = [(self.secondtouch[0]/self.Width)*self.xDist + self.xStart, (self.secondtouch[1]/self.Height)*self.yDist + self.yStart] #translates the Kivy coord plane to the current mandelbrot coor plane
			self.touch1 = [(self.firsttouch[0]/self.Width)*self.xDist + self.xStart, (self.firsttouch[1]/self.Height)*self.yDist + self.yStart]
			self.shift = [self.touch2[0]-self.touch1[0], self.touch2[1]-self.touch1[1]]	 #calculates the shift direction that happened between the current touch position and the previous one
			
			#Updates all the coords accordingly to the shift
			self.xStart = (self.xStart - self.shift[0])
			self.xEnd = (self.xEnd - self.shift[0])
			self.yStart = (self.yStart - self.shift[1])
			self.yEnd = (self.yEnd - self.shift[1])
			self.xDist = (self.xEnd - self.xStart)
			self.yDist = (self.yEnd - self.yStart)
			
			self.firsttouch = self.secondtouch #first touch position is set to the current touch position
				
	
	def on_touch_down(self, touch):
		#some if conditions if you click inside one of the color picker boxes or inside the gradient window
		if touch.pos[0] > self.Width:
			if ((touch.pos[0] >= self.colorbar.pos[0] and touch.pos[0] <= self.colorbar.pos[0]+self.colorbar.size[0]) and (touch.pos[1] >= self.colorbar.pos[1] and touch.pos[1] <= self.colorbar.pos[1] + self.colorbar.size[1])):
				self.SquareColor(self, touch.pos)

			elif ((touch.pos[0] >= self.colorsquare.pos[0] and touch.pos[0] <= self.colorsquare.pos[0]+self.colorsquare.size[0]) and (touch.pos[1] >= self.colorsquare.pos[1] and touch.pos[1] <= self.colorsquare.pos[1] + self.colorsquare.size[1])):
				self.FinalColor(self, touch.pos)

			elif ((touch.pos[0] >= self.Gradient.pos[0] and touch.pos[0] <= self.Gradient.pos[0]+self.Gradient.size[0]) and (touch.pos[1] >= self.Gradient.pos[1] and touch.pos[1] <= self.Gradient.pos[1] + self.Gradient.size[1])):
				self.SetGradientColor(self, touch.pos)

			return super(Draw, self).on_touch_down(touch)
		self.firsttouch = touch.pos #touch position when you click for the first time

	
	def SetGradientColor(self, instance, pos): #called when you click on a control color point inside the gradient, which gets changed to the current color in colorwindow
		color = copy.deepcopy(self.Selectcolor)
		xIndex = int(pos[0] - self.Gradient.pos[0])
		index = int(xIndex/(int(self.Gradient.size[0]/self.numColorPoints)))
		self.colorPoints[index] = self.Selectcolor
		self.setColor(self)


	def SquareColor(self,instance, pos): #called when you click somewhere on the rainbow colorbar, which then updates the square color
		BarXIndex = int(pos[0] - self.colorbar.pos[0])
		BarYIndex = int(-pos[1] + self.colorbar.pos[1] + self.colorbar.size[1])
		color = copy.copy(self.BarArray[BarYIndex, BarXIndex])
		self.bytes_io = BytesIO()
		self.SquareArray = colorsquare(int(self.Width * 0.40), int(self.Width*0.40), color)
		self.img = Image.fromarray(self.SquareArray, 'RGB')
		self.img.save(self.bytes_io, 'PNG')
		self.colorsquare.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture
		try:
			self.Selectcolor = copy.copy(self.SquareArray[self.SqYIndex, self.SqXIndex])
		except:
			pass

		#also updates the color window with the new color, the shade stays the same
		self.bytes_io = BytesIO()
		self.WindowArray = np.full((self.colorwindow.size[1],self.colorwindow.size[0], 3), self.Selectcolor, dtype=np.uint8)
		self.img = Image.fromarray(self.WindowArray, 'RGB')
		self.img.save(self.bytes_io, 'PNG')
		self.colorwindow.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture

	
	def FinalColor(self, instance, pos): #called when you click somewhere on the color square, updates the color window accordingly
		self.SqXIndex = int(pos[0] - self.colorsquare.pos[0])
		self.SqYIndex = int(-pos[1] + self.colorsquare.pos[1] + self.colorsquare.size[1])
		try:
			self.Selectcolor = copy.copy(self.SquareArray[self.SqYIndex, self.SqXIndex])
		except:
			pass

		self.bytes_io = BytesIO()
		self.WindowArray = np.full((self.colorwindow.size[1],self.colorwindow.size[0], 3), self.Selectcolor, dtype=np.uint8)
		self.img = Image.fromarray(self.WindowArray, 'RGB')
		self.img.save(self.bytes_io, 'PNG')
		self.colorwindow.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture


	def ZoomVideo(self, instance): #Function thats called when you want to render a "Zoom out" video
		self.number = 0 #used for naming the files and ordering them numerically
		self.xStartVid = self.xStart
		self.xEndVid = self.xEnd
		self.yStartVid = self.yStart
		self.yEndVid = self.yEnd
		self.xDistVid = self.xEndVid - self.xStartVid
		self.yDistVid = self.yEndVid - self.yStartVid

		#new Width, Height and Antialias values based on what you entered into the text inputs
		try:
			self.SHeight = int(''.join(filter(str.isdigit, self.HeightBox.text)))
			self.Antialias = int(''.join(filter(str.isdigit, self.AntialiasBox.text)))
			self.SWidth = int(''.join(filter(str.isdigit, self.WidthBox.text)))
		except:
			pass

		while self.xStartVid > -2.5: #zooms out until the X starting coord is -2.5, so the whole mandelbrot fits inside the window
			self.array = DrawSet(self.SWidth*self.Antialias, self.SHeight*Antialias, self.xStartVid, self.xDistVid, self.yStartVid, self.yDistVid, self.maxIt, self.gradient, self.alg)
			self.img = Image.fromarray(np.flipud(self.array), 'RGB')
			self.savename = 'Video\\' + str(self.number) + '.png'
			self.img = self.img.resize((self.SWidth, self.SHeight), Image.ANTIALIAS)
			self.img.save(self.savename, 'PNG')

			#zooms out one step
			self.xStartVid = self.xStartVid - self.xDistVid*0.01
			self.xEndVid = self.xEndVid + self.xDistVid*0.01
			self.yStartVid = self.yStartVid - self.yDistVid*0.01
			self.yEndVid = self.yEndVid + self.yDistVid*0.01
			self.xDistVid = self.xEndVid - self.xStartVid
			self.yDistVid = self.yEndVid - self.yStartVid
			self.number +=1

		self.Video(self) #takes all the frames created in the Video folder and creates a video out of them

	
	def IterVideo(self, instance): #called when you want to create an "iteration" video
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
		self.Video(self) #creates video from frames in Video folder

	
	def ZoomInOut(self, window, keycode): #called when you use the keyboard, like f.ex zooming in/out, adding iterations, randomizing the gradient or adding control color points
		if keycode[1] == "w": #when you zoom in
			self.xStart = self.xStart + self.xDist*0.10
			self.xEnd = self.xEnd - self.xDist*0.10
			self.yStart = self.yStart + self.yDist*0.10
			self.yEnd = self.yEnd - self.yDist*0.10
			self.xDist = self.xEnd - self.xStart
			self.yDist = self.yEnd - self.yStart
	
		elif keycode[1] == "s": #when you zoom out
			self.xStart = self.xStart - self.xDist*0.10
			self.xEnd = self.xEnd + self.xDist*0.10
			self.yStart = self.yStart - self.yDist*0.10
			self.yEnd = self.yEnd + self.yDist*0.10
			self.xDist = self.xEnd - self.xStart
			self.yDist = self.yEnd - self.yStart

		elif keycode[1] == "up": #adding 10 iterations
			self.maxIt += 10
		elif keycode[1] == "down": #subtracting 10 iterations
			self.maxIt -= 10
		elif keycode[1] == "r": #randomizing the gradient
			self.colorPoints = rand_rgb_color(self.numColorPoints)
			self.setColor(self)

		elif keycode[1] == "left": #adding 1 control color point
			self.colorPoints = np.delete(self.colorPoints, self.numColorPoints-1, axis=0)
			self.numColorPoints -=1
			self.setColor(self)

		elif keycode[1] == "right":
			self.colorPoints = np.insert(self.colorPoints, self.numColorPoints, tuple(self.Selectcolor), axis=0)
			self.numColorPoints +=1
			self.setColor(self)
			
		elif keycode[1] == "a": #switching between dynamic escape time coloring algorithm, and the static coloring algorithm (similar to histogram coloring)
			if self.alg == 0:
				self.alg = 1
			else:
				self.alg = 0 


		#updates the rendering window with new changes
		self.array = DrawSet(self.Width, self.Height, self.xStart, self.xDist, self.yStart, self.yDist, self.maxIt, self.gradient, self.alg)
		self.bytes_io = BytesIO()
		self.img = Image.fromarray(np.flipud(self.array), 'RGB')
		self.img.save(self.bytes_io, 'PNG')
		self.MainSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture

		

	def setColor(self, instance): #called when the gradient is updated, applies these changes to the rendering window
		self.gradient = np.concatenate((np.array(polylinear_gradient(self.colorPoints, self.totalColors)), [(0,0,0)]), axis= 0)
		self.bytes_io = BytesIO()

		#creates stretched out numpy array of control color points (colorPoints) so it can be displayed as an image, based on width of the window
		self.GradientArray = np.array(self.colorPoints, dtype=np.uint8)
		self.GradientArray = np.repeat(self.GradientArray, int((self.Width)/len(self.GradientArray)), axis = 0)
		self.GradientArray = np.resize(self.GradientArray, (int(self.Height*0.10), len(self.GradientArray), 3))

		#updates Gradient widget size so its exactly the size of GradientArray
		self.img = Image.fromarray(self.GradientArray, 'RGB')
		self.img.save(self.bytes_io, 'PNG')
		self.Gradient.size[0] = len(self.GradientArray[0])
		self.Gradient.pos[0] = self.Width + int((self.Width - len(self.GradientArray[0]))/2)
		self.Gradient.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture
		
		#updates Mandelbrot set with new gradient
		self.array = DrawSet(self.Width, self.Height, self.xStart, self.xDist, self.yStart, self.yDist, self.maxIt, self.gradient, self.alg)
		self.bytes_io = BytesIO()
		self.img = Image.fromarray(np.flipud(self.array), 'RGB')
		self.img.save(self.bytes_io, 'PNG')
		self.MainSet.texture = self.ImageByte(self, self.bytes_io.getvalue()).texture


	def Video(self, instance): #creates video from frames inside the Video folder
		try:
			self.Fps = int(''.join(filter(str.isdigit, self.FpsBox.text)))
			cmd = 'ffmpeg -framerate {} -i Video\\%d.png -c:v libx264 -crf 1 -pix_fmt yuv420p -framerate {} Video{}.avi'.format(self.Fps, self.Fps, random.randint(1, 9000))
			sp.call(cmd,shell=True)
			files = glob.glob('Video\\*.png') 
			for f in files:
				os.remove(f)
		except:
			pass
		
	
	def SaveImage(self, instance): #saves current Image
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

	def ImageByte(self, instance, ImageByte): #used for saving images to memory buffer
		self.Buffer = BytesIO(ImageByte)
		self.BgIm = CoreImage(self.Buffer, ext= 'png')
		return self.BgIm


class MandelBrot(App):
    def build(self):
        return Draw()

if __name__ == "__main__":
    MandelBrot().run()