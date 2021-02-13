# Mandelbrot-Set

This is a Python application that lets you render the Mandelbrot Set. I implemented the GUI with <i>Kivy</i> as well as <i>PIL</i> (<i>Python Imaging Library</i>). 
To increase performance, I used the <i>Numba</i> library which translates a part of my <i>Python</i> code into fast <i>machine code</i>.
# Preview:
<img src = "https://imgur.com/1oMCbzP.png" width = 500>

# How to use:

<b>Download the lastest release</b> and follow the instructions <b>or download the source code</b> and run the <i>MandelBrot.py</i> from an IDE

<b>Keyboard actions:</b>

- Use the <b>mouse cursor</b> to drag the plane around
- Press <b>W</b> or <b>S</b> to zoom in/out
- Press the <b>Up</b> or <b>Down</b> arrow keys to increase/decrease the number of iterations
- Press <b>R</b> to randomize the color gradient
- Press the <b>Left</b> or <b>Right</b> arrow keys to add/subtract colors from the color gradient
- Press <b>A</b> to switch between two different coloring algorithms

<b>Changing the colors:</b>

- Select a color with the color picker. The selected color will be displayed in the middle color window.
- You can then change some color within the gradient: 

<img src = "https://media.giphy.com/media/DSpt7wE9rQstDbqrto/giphy.gif" width = 500>

- By adding colors to the gradient with the <b>Right</b> arrow key, the picture will become more colorful:

<img src = "https://imgur.com/DEhi7Xr.png" width = 500>

<b>Saving as Wallpaper: </b>

- Enter your desired resolution into the <b>Width</b> and <b>Height</b> input box. Then enter an <b>antialias factor</b> (1 = no antialias, 2 = 2x antialias, ...).
Save the image by pressing on <b>Save Image</b>. The image will be saved on your desktop, inside the <i><b>Mandelbrot</b></i> folder which will be created.

<b>Rendering videos: </b>

- You can also use this application to render zoom videos. Simply zoom into the Mandelbrot Set until you've reached the desired depth. Then, fill in the <b>Width</b>, <b>Height</b>, <b>Antialias</b> and <b>FPS</b> input box accordingly. Finally, press on <b>Zoom Video</b>
  The video will be saved on your desktop inside the <b>Mandelbrot</b> folder.

<b>NOTE:</b> While rendering the video, the application will stop responding until the video has been created. Rendering speed depends on your PC specs as well as the desired resolution and antialiasing of the video.



<img src = "https://media.giphy.com/media/pcizXQxGO3UeNm5jxC/giphy.gif" width = 500>
![gif](https://media.giphy.com/media/pcizXQxGO3UeNm5jxC/giphy.gif)
<img src = "https://media.giphy.com/media/0CCPmjrPJVP1FtqmhN/giphy.gif" width = 500>

