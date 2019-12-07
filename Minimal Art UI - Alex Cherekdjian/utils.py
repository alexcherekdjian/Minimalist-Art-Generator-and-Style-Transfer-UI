import cairo, copy, math, random, colorthief, os, PIL
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# float number generator
float_gen = lambda a, b: random.uniform(a, b)

def createPicture(window, colors, iteration, width_input, height_input):
	# establishing canvas width and height, canvas center, final result picture filename, and setting alpha of colors
	width, height = width_input, height_input # from gui

	x_canvas_center = width / 2
	y_canvas_center = height / 2
	shapealpha = 0.3

	picture_file_name = 'picture' + str(iteration) + '.png'

	# creating the actual canvas
	ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
	cr = cairo.Context(ims)

	context = cairo.Context(ims)
	cairo.Pattern.set_filter(context.get_source(), cairo.Filter.BEST)


	# choosing a random color from palette to paint background
	color_chosen = random.choice(colors)
	cr.set_source_rgba(color_chosen[0]/255, color_chosen[1]/255, color_chosen[2]/255, 1)

	# drawing objects
	cr.rectangle(0, 0, width, height)
	cr.fill()

	# setting the line width for drawing lines
	cr.set_line_width(4)

	# generating random values for the length (l) of a line and angle (perm_angle)
	line_length = random.randint(2000,9000)
	perm_angle = random.randint(5,190)

	# setting up a progress bar
	window.progress = QProgressBar(window)
	window.progress.setGeometry(100, 250, 800, 525)
	window.progress.show()
	window.completed = 0

	# setting zoom parameter, very slight adjustments to the placement of lines to try and better fit design in window 
	if perm_angle >= 60:
		zoom = random.randint(round(perm_angle/60), round(perm_angle/60 + 1))
	else:
		zoom = float_gen(perm_angle/50, perm_angle/50+ 1)

	# setting curent x and y, angle_temp, drawing cursor at the center of the page, and count for progress bar
	cr.move_to(x_canvas_center, y_canvas_center)
	x_current = x_canvas_center
	y_current = y_canvas_center
	current_angle = perm_angle

	# setting style for more minimal look if randomness allows
	more_minimal = random.randint(1,10)

	# start with small lengths of lines and loop through max length 
	for side in range(1, line_length):

		# calculate sin and cos of angle 
		sine = math.sin(math.radians(current_angle))
		cos = math.cos(math.radians(current_angle))

		# choose a random color and set drawing source as color
		color_chosen = random.choice(colors)
		cr.set_source_rgba(color_chosen[0]/255, color_chosen[1]/255, color_chosen[2]/255, shapealpha)

		# create the next line / shape we will draw
		shape = [(x_current,y_current), (line_length * cos, line_length * sine)]

		# deform the initial shape
		baseshape = deform(shape, 1, random.randint(20,120))

		# add more layers to that shape (20-25 layers per shape)
		for j in range(random.randint(10, 15)):

			# copy the shape and deform it extremely
			tempshape = copy.deepcopy(baseshape)
			layer = deform(tempshape, 3, random.randint(200,300)) # for more hectic designs use 100- 300

			# draw the lines for the layers and account for randomness if applicable
			if more_minimal > 5:
				xfactor = random.randint(0,width)
				yfactor = random.randint(0,height)
			else:
				xfactor = 0
				yfactor = 0

			for i in range(len(layer)):
				cr.line_to(layer[i][0] + xfactor, layer[i][1] + yfactor)

			# fill in the object with the color specified above
			cr.fill()

		# update our current x and y values to follow pattern with adjustments of zoom parameter
		y_current += side * sine + zoom
		x_current += side * cos + zoom

		# # increment angle
		current_angle += perm_angle

		# increment angle
		#current_angle -= perm_angle

		# increase counter for progress bar and update the bar		
		window.completed = (side/line_length)*100
		window.progress.setValue(window.completed)
		QApplication.processEvents()
	# save image to a png file

	ims.write_to_png(os.getcwd() + "/Generated Art/" + picture_file_name)
	window.progress.hide()
	return


def createStyleTransferImage(window, pixel_list, colors, width_input, height_input, filename):
	# establishing canvas width and height, canvas center, final result picture filename, and setting alpha of colors
	width, height = width_input, height_input 

	shapealpha = 0.3

	# if palette used then grabbing colors from palette, else grabbing from original picture
	palette_used = False
	if len(colors) > 0:
		palette_used = True
	else:
		guide_image = PIL.Image.open(filename)

	# creating the actual canvas
	ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
	cr = cairo.Context(ims)

	context = cairo.Context(ims)
	cairo.Pattern.set_filter(context.get_source(), cairo.Filter.BEST)

	# setting curent x and y, angle_temp, drawing cursor at the center of the page, and count for progress bar
	x_current = pixel_list[0][0]
	y_current = pixel_list[0][1]

	xy = (x_current, y_current)

	cr.set_source_rgba(255, 255, 255, 1)

	# # drawing objects
	cr.rectangle(0, 0, width, height)
	cr.fill()

	cr.move_to(x_current, y_current)

	pixel_len = len(pixel_list)

	# setting up a progress bar
	window.progress = QProgressBar(window)
	window.progress.setGeometry(100, 250, 800, 525)
	window.progress.show()
	window.completed = 0

	# start with small lengths of lines and loop through max length 
	for pixel in range(1, pixel_len-1):

		if pixel_list[pixel][0] < x_current or pixel_list[pixel][1] > y_current: 
			x_current = pixel_list[pixel][0]
			y_current = pixel_list[pixel][1]
			continue

		# choose a random color and set drawing source as color
		xy = (pixel_list[pixel][0]/10, pixel_list[pixel][1]/10)

		# grab a color
		if palette_used:
			color_chosen = random.choice(colors)
		else:
			color_chosen = guide_image.getpixel(xy)

		cr.set_source_rgba(color_chosen[0]/255, color_chosen[1]/255, color_chosen[2]/255, shapealpha)

		# create the next line / shape we will draw
		shape = [(x_current,y_current),(pixel_list[pixel][0], pixel_list[pixel][1])]

		# deform the initial shape
		baseshape = deform(shape, 1, random.randint(50, 60))

		# add more layers to that shape (20-25 layers per shape)
		for j in range(random.randint(20, 25)):

			# copy the shape and deform it extremely
			tempshape = copy.deepcopy(baseshape)
			layer = deform(tempshape, 3, random.randint(25,65)) #75 # for more hectic designs use 100- 300
			
			for i in range(len(layer)):
				cr.line_to(layer[i][0], layer[i][1])

			cr.fill()

		# update our current x and y values to follow pattern
		x_current = pixel_list[pixel][0]
		y_current = pixel_list[pixel][1]

		# increase counter for progress bar and update the bar		
		window.completed = (pixel/pixel_len)*100
		window.progress.setValue(window.completed)
		QApplication.processEvents()

	# save image to a png file
	ims.write_to_png(os.getcwd() + "/Generated Art/stylepic.png")
	window.progress.hide()
	return


def loadPalette(filepath):
	# from the Palettes directory, select a file
	color_thief = colorthief.ColorThief(filepath)

	# build a color palette
	colors = color_thief.get_palette(color_count = 10)

	return colors


def deform(shape, iterations, variance):
	# go through shape iteration # of times
	for i in range(iterations):
		# for all the points in the shape starting with the end
		for j in range(len(shape)-1, 0, -1):
			# calculate the midpoint and adjust it with variance to get randomness of shape designs
			midpoint = (((shape[j-1][0] + shape[j][0])/ 2 + float_gen(-variance, variance)), (((shape[j-1][1] + shape[j][1])/ 2 + float_gen(-variance, variance))))
			
			# add the midpoint to the list of points in the shape
			shape.insert(j, midpoint)

	return shape
