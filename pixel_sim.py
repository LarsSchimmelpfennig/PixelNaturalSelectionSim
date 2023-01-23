import time
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
import random

t1 = time.time()
#return a tuple of two lists, locations of empty and color pixels
def find_neighbor_pixels(h, w, d_pixels):
	"""
	Filters neighboring pixels at the position (h, w)
	into two lists for empty and color pixels
	"""
	l_empty_pixels = []
	l_color_pixles = []
	if (h-1, w) in d_pixels:
		l_color_pixles.append((h-1, w))
	else:
		l_empty_pixels.append((h-1, w))
	if (h-1, w-1) in d_pixels:
		l_color_pixles.append((h-1, w-1))
	else:
		l_empty_pixels.append((h-1, w-1))
	if (h, w-1) in d_pixels:
		l_color_pixles.append((h, w-1))
	else:
		l_empty_pixels.append((h, w-1))
	if (h+1, w) in d_pixels:
		l_color_pixles.append((h+1, w))
	else:
		l_empty_pixels.append((h+1, w))
	if (h+1, w+1) in d_pixels:
		l_color_pixles.append((h+1, w+1))
	else:
		l_empty_pixels.append((h+1, w+1))
	if (h+1, w-1) in d_pixels:
		l_color_pixles.append((h+1, w-1))
	else:
		l_empty_pixels.append((h+1, w-1))
	if (h, w+1) in d_pixels:
		l_color_pixles.append((h, w+1))
	else:
		l_empty_pixels.append((h, w+1))
	if (h-1, w+1) in d_pixels:
		l_color_pixles.append((h-1, w+1))
	else:
		l_empty_pixels.append((h-1, w+1))	
	return l_empty_pixels, l_color_pixles


#credit to https://medium.com/@BrendanArtley/matplotlib-color-gradients-21374910584b
def hex_to_RGB(hex_str):
    """ #FFFFFF -> [255,255,255]"""
    #Pass 16 to the integer function for change of base
    return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

def get_color_gradient(c1, c2, n):
    """
    Given two hex colors, returns a color gradient
    with n colors.
    """
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]

def genetic_difference(code, threat_code):
	"""
	Given two strings, returns the number of differences
	to be used as a color index.
	"""
	count = 0
	for a, b in zip(list(code), list(threat_code)):
		if a != b:
			count+=1
	if count == len(code):
		return count-1
	return count

width = 640
height = 480
birth_percent = 20
death_percent = 10
mutation_percent = 15
FPS = 60
seconds = 60
fourcc = VideoWriter_fourcc(*'MP42')
video = VideoWriter('natural_selection_pixel_sim_images/noise.avi', fourcc, float(FPS), (width, height))
global d_pixels
d_pixels = {}
colors = [(255, 51, 51), (255, 153, 51), (255, 255, 51), (51, 255, 51), (51, 255, 153), (51, 255, 255), (51, 153, 255),
						 (153, 51, 255), (255, 51, 255), (255, 51, 153)]

code_length = 9
threat_code = ''.join(random.choices(['A', 'C', 'G', 'T'], k=code_length))
print('threat code',threat_code)

color1 = "#fcba03"
color2 = "#3803ab"

hex_colors = get_color_gradient(color1, color2, code_length)
gradient_colors = []
for hex in hex_colors:
	gradient_colors.append(hex_to_RGB(hex))

def draw_frame(a):
	"""
	Takes the current matrix a then removes
	and adds new pixels based on given parameters.
	"""
	new_pixels = []
	dead_pixels = []
	for h, w in d_pixels:
		if random.randint(1, 100) <= death_percent and d_pixels[(h, w)] != threat_code:
			a[h, w, 0] = 0
			a[h, w, 1] = 0
			a[h, w, 2] = 0
			dead_pixels.append((h, w))
			continue
		if random.randint(1, 100) <= birth_percent:
			empty_pixels, color_pixels = find_neighbor_pixels(h, w, d_pixels)
			if len(empty_pixels) == 0:
				continue
			empty_h, empty_w = random.choices(empty_pixels, k=1)[0]
			if empty_w >= width or empty_h >= height or empty_w <= 0 or empty_h <= 0:
				continue
			curr_code = d_pixels[(h, w)]
			curr_color = gradient_colors[genetic_difference(curr_code, threat_code)]
			new_pixels.append((empty_h, empty_w, curr_color, curr_code))
			
	for new_h, new_w, old_color, old_code in new_pixels:
		if random.randint(1, 100) <= mutation_percent:
			idx_to_change = random.choices(list(range(code_length)), k=1)[0]
			temp_l = list(old_code) 
			temp_l[idx_to_change] = random.choices(['A', 'C', 'G', 'T'], k=1)[0]
			code = ''.join(temp_l)
			d_pixels[(new_h, new_w)] = code
			new_color = gradient_colors[genetic_difference(code, threat_code)]
			a[new_h, new_w, 2] = new_color[0]
			a[new_h, new_w, 1] = new_color[1]
			a[new_h, new_w, 0] = new_color[2]
		else:
			d_pixels[(new_h, new_w)] = old_code
			a[new_h, new_w, 2] = old_color[0]
			a[new_h, new_w, 1] = old_color[1]
			a[new_h, new_w, 0] = old_color[2]

	for dead_h, dead_w in dead_pixels:
		if (dead_h, dead_w) in d_pixels:
			del d_pixels[(dead_h, dead_w)]
	return a

for _ in range(FPS*seconds):
	if _ == 0:
		a = np.zeros((height, width, 3), dtype=np.uint8)
		starting_code = ''.join(random.choices(['A', 'C', 'G', 'T'], k=code_length))
		print('starting code', starting_code)
		d_pixels[(int(height/2), int(width/2))] = starting_code
		color = gradient_colors[genetic_difference(starting_code, threat_code)]
		num_start = 10
		i = 0
		while i <= num_start:
			x_change = random.randint(-319, 319)
			y_change = random.randint(-239, 239)
			if (int(height/2) + y_change, int(width/2) + x_change) not in d_pixels:
				d_pixels[(int(height/2) + y_change, int(width/2) + x_change)] = starting_code
				a[int(height/2) + y_change, int(width/2) + x_change,2] = color[0]
				a[int(height/2) + y_change, int(width/2) + x_change,1] = color[1]
				a[int(height/2) + y_change, int(width/2) + x_change,0] = color[2]
			i+=1
		video.write(a)
	else:	
		frame = draw_frame(a)
		video.write(frame)
video.release()
print((time.time() - t1)/60, 'mins to complete')