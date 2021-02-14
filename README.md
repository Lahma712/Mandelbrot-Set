# Mandelbrot-Set

This is my Python application that lets you render the Mandelbrot Set. I implemented the GUI with <i>Kivy</i> as well as <i>PIL</i> (<i>Python Imaging Library</i>). 
To increase performance, I used the <i>Numba</i> library which translates a part of my <i>Python</i> code into fast <i>machine code</i>.

The Mandelbrot Set is a self-similar fractal, which has been discovered by the French-American Mathematician <b><i>Benoit B. Mandelbrot</i></b>. A fractal is a geometrical shape with a finite area but inifite perimeter. 

The Mandelbrot Set is the set of complex numbers <b><i>c</i></b> for which the function <b><i>z<sub><i>n+1</i></sub> = z<sub>n</sub><sup>2</sup> + c</i></b>  remains bounded when iterated from <b><i>z = 0</b></i>.

# Preview:
<img src = "https://imgur.com/1oMCbzP.png" width = 500>

# How to use:

<b>Download the lastest release</b> and follow the instructions <b>or download the source code</b> and run the <i>MandelBrot.py</i> from an IDE

## <b>Keyboard actions:</b>

- Use the <b>mouse cursor</b> to drag the plane around
- Press <b>W</b> or <b>S</b> to zoom in/out
- Press the <b>Up</b> or <b>Down</b> arrow keys to increase/decrease the number of iterations
- Press <b>R</b> to randomize the color gradient
- Press the <b>Left</b> or <b>Right</b> arrow keys to add/subtract colors from the color gradient
- Press <b>A</b> to switch between two different coloring algorithms

## <b>Changing the colors:</b>

- Select a color with the color picker. The selected color will be displayed in the middle color window.
- You can then change some color within the gradient: 

    <img src = "https://media.giphy.com/media/DSpt7wE9rQstDbqrto/giphy.gif" width = 500>

- By adding colors to the gradient with the <b>Right</b> arrow key, the picture will become more colorful:

    <img src = "https://imgur.com/DEhi7Xr.png" width = 500>

## <b>Saving as wallpaper: </b>

- Enter your desired resolution into the <b>Width</b> and <b>Height</b> input box. Then enter an <b>antialias factor</b> (1 = no antialias, 2 = 2x antialias, ...).
Save the image by pressing on <b>Save Image</b>. The image will be saved on your desktop, inside the <i><b>Mandelbrot</b></i> folder which will be created.

## <b>Rendering videos: </b>

<b>NOTE:</b> While rendering the video, the application will stop responding until the video has been created. Rendering speed depends on your PC specs as well as the desired resolution and antialiasing of the video.

- You can also use this application to render <i><b>zoom videos</b></i>. Simply zoom into the Mandelbrot Set until you've reached the desired depth. Then, fill in the <b>Width</b>, <b>Height</b>, <b>Antialias</b> and <b>FPS</b> input box accordingly. Finally, press on <b>Zoom Video</b>. The video will be saved on your desktop inside the <i><b>Mandelbrot</b></i> folder.


    <img src = "https://media.giphy.com/media/pcizXQxGO3UeNm5jxC/giphy.gif" width = 500>



- You can also render another type of video which I called <i><b>iteration videos</i></b>. You zoom into the desired depth, then fill in the <b>Width</b>, <b>Height</b>, <b>Antialias</b> and <b>FPS</b> input box accordingly. Finally, press on <b>Iter. Video</b>. The video will stay at the current depth and gradually increase the iterations from 0 up to the current number of iterations. The video will be saved on your desktop inside the <i><b>Mandelbrot</b></i> folder:

    This is the default <b>coloring algorithm</b>, which is the standard <i>escape time coloring algorithm</i>. You can see that is is <b>dynamic</b>, meaning that, as you increase the number of iterations, the colors kind of "flow" towards the Mandelbrot Set:

    <img src = "https://media.giphy.com/media/0fLhxVk8Dutw0yuzBL/giphy.gif" width = 500>

    By pressing <b>A</b> you change the default coloring algorithm to a <b>static</b> coloring algorithm. This coloring algorithm is similar to the <i>histogram coloring algorithm</i>, in the sense that the colors do not "flow" or change as much, but just gradually iterate through the gradient as they get closer to the Mandelbrot Set:

    <img src= "https://media.giphy.com/media/MpfPn0uU8OJzVPbP0R/giphy.gif" width = 500>


For more details on the coloring algorithms, see https://en.wikipedia.org/wiki/Plotting_algorithms_for_the_Mandelbrot_set

# Dependencies:

- Python
- Kivy 2.0.0
- PIL (Python Imaging Library)
- ffmpeg
- Numba

# Sources:
- <i>gradient.py</i>: Credits to https://bsouthga.dev/posts/color-gradients-with-python
- https://en.wikipedia.org/wiki/Mandelbrot_set
- https://en.wikipedia.org/wiki/Plotting_algorithms_for_the_Mandelbrot_set
