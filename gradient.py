
from numpy import random as rnd

#Not my code, source: https://bsouthga.dev/posts/color-gradients-with-python 

def linear_gradient(s, f, n):
  ''' returns a gradient list of (n) colors between
    two rgb colors  '''
  # Initilize a list of the output colors with the starting color
  RGB_list = [s]
  # Calcuate a color at each evenly spaced value of t from 1 to n
  for t in range(1, n):
    # Interpolate RGB vector for color at the current value of t
    curr_vector = [int(s[j] + (float(t)/(n-1))*(f[j]-s[j])) for j in range(3)]
    # Add it to our list of output colors
    RGB_list.append(tuple(curr_vector))
  
  return RGB_list


def rand_rgb_color(num=5):
  ''' Generate random rgb colors, default is one,
      returning a string. If num is greater than
      1, an array of strings is returned. '''
  colors = [tuple([rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255)]) for i in range(num)]
  
  if num == 1:
    return colors[0]
  else:
    
    return colors


def polylinear_gradient(colors, n):
  ''' returns a list of colors forming linear gradients between
      all sequential pairs of colors. "n" specifies the total
      number of desired output colors '''
  # The number of colors per individual linear gradient
  
  n_out = int(float(n) / (len(colors) - 1))
  gradient_dict = linear_gradient(colors[0], colors[1], n_out)
  if len(colors) > 1:
    for col in range(1, len(colors) - 1):
      next = linear_gradient(colors[col], colors[col+1], n_out)
      gradient_dict += next
  return gradient_dict


