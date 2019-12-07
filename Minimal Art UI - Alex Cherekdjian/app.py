import os, sys, utils, PIL, random, templates, error
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PIL import ImageDraw
from picturedropzone import PictureDropZone
from skimage import io

width = 0
height = 0
number_of_pictures = 0
colors_style = []
colors_gen = []
art_gen = True

# a class for a drag and drop widget for palletes
class ColorDropZone(QLabel):
	def __init__(self, parent):
		super().__init__(parent)
		self.setAcceptDrops(True)
		self.scale_x = 590
		self.scale_y = 400
		self.colors = []

	# only accept data with a url
	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls():
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event):
		# get url data
		data = event.mimeData()
		urls = str(data.urls())

		# clean up url data
		path_initial_trim = urls.replace('[PyQt5.QtCore.QUrl(\'file://', '')
		pathname = path_initial_trim.replace('\')]', '')

		# ensure url is an image file, if not ignore
		try:
			im = PIL.Image.open(pathname)
			im.verify()
			im.close()
		except:
			QMessageBox.information(self, "Error", error.error_list["invalid picture"], QMessageBox.Ok)
			return

		# if image is valid, use colorThief to extract colors

		global colors_gen
		global colors_style
		global art_gen

		if art_gen:
			colors_gen = utils.loadPalette(pathname)
		else:
			colors_style = utils.loadPalette(pathname)

		# replace image in window with picture
		self.pic = QLabel(self)
		self.pixmap = QPixmap(pathname)
		self.pixmap = self.pixmap.scaled(self.scale_x, self.scale_y)

		self.pic.setPixmap(self.pixmap)
		self.pic.show()

	def replacePicture(self, pathname):
		# replace image in window with picture
		self.pic = QLabel(self)
		self.pixmap = QPixmap(pathname)
		self.pixmap = self.pixmap.scaled(self.scale_x, self.scale_y)
		self.pic.setPixmap(self.pixmap)
		self.pic.show()


class Window(QWidget):
	def __init__(self):
		super().__init__()
		self.setFixedSize(1000,600)
		self.setWindowTitle('Minimal Art Generator')
		self.mainUI()
		self.show()

	def finishPage(self):
		if art_gen:		
			# init the finish logo
			self.done = QLabel(self)
			self.done.setGeometry(QRect(0, 0, 1000, 525))
			self.done.setAlignment(Qt.AlignCenter)
			self.done.setStyleSheet('font: 300pt Tahoma;')
			self.done.setText("<font color='white'>"+ "Done" + "</font>")
			self.done.show()

		else:
			# init the finish logo
			self.done = QLabel(self)
			self.done.move(450,10)
			self.done.setAlignment(Qt.AlignCenter)
			self.done.setStyleSheet('font: 40pt Tahoma;')
			self.done.setText("<font color='white'>"+ "Done" + "</font>")
			self.done.show()

			# show picture preview
			self.picture_preview = QLabel(self)
			self.picture_preview.move(250,-25)
			self.picture_preview.setAlignment(Qt.AlignCenter)
			pixmap = QPixmap(os.getcwd() + "/Generated Art/stylepic.png")
			pixmap = pixmap.scaled(400, 400)
			self.picture_preview.resize(500,600)
			self.picture_preview.setPixmap(pixmap)
			self.picture_preview.show()

		# init the description
		self.description = QLabel(self)
		self.description.setGeometry(100, 250, 800, 525)
		self.description.setAlignment(Qt.AlignCenter)
		self.description.setStyleSheet('font: 30pt Tahoma;')

		# plural vs non plural case
		if art_gen:
			self.description.setText("<font color='white'>"+ "Check the \"Generated Art\" folder for your new creations!" + "</font>")
		else:
			self.description.setText("<font color='white'>"+ "Check the \"Generated Art\" folder for your new creation!" + "</font>")

		self.description.show()

		# init the return button
		self.return_button = QPushButton(self)
		self.return_button.move(930,10)
		pixmap = QPixmap(os.getcwd() + '/Graphics/next.png')
		pixmap = pixmap.scaledToWidth(700)
		self.return_button.setIcon(QIcon(pixmap))
		self.return_button.setIconSize(QSize(60, 60))   
		self.return_button.resize(60,60)
		self.return_button.clicked.connect(self.returnClicked)
		self.return_button.setStyleSheet( \
			"QPushButton { background-color: transparent;}" \
			"QPushButton:hover { background-color: transparent; border-style: outset; border-width: 4px; border-radius: 30px; border-color: white; min-width:900em;}" \
			"QPushButton:pressed { background-color: rgba(255, 255, 255, 0.75); border-style: inset; border-width: 4px; border-radius: 30px; border-color: white; min-width:900em;}" \
			)
		self.return_button.show()

		if not art_gen:
			self.go_deeper_button = QPushButton('Go Deeper', self)
			self.go_deeper_button.move(430,545)
			self.go_deeper_button.setFixedWidth(140)
			self.go_deeper_button.setFixedHeight(30)
			self.go_deeper_button.clicked.connect(self.goDeeperClicked)
			self.go_deeper_button.setStyleSheet(\
				"QPushButton {font: 15pt Tahoma; color: grey; background-color: ghostwhite; border-color: ghostwhite; border-radius: 12px; border-style: outset; border-width: 4px;}"\
				"QPushButton:hover { background-color: white; border-color: white; }" \
				"QPushButton:pressed { background-color: silver; border-color: transparent;}" \
				)
			self.go_deeper_button.show()


	def openFileDialog(self):
		pathname = ""
		fname = QFileDialog.getOpenFileName(self, 'Open file')
		pathname = fname[0]

		# ensure url is an image file, if not ignore
		if pathname == "":
			return

		try:
			im = PIL.Image.open(pathname)
			im.verify()
			im.close()
		except:
			QMessageBox.information(self, "Error", error.error_list["invalid picture"], QMessageBox.Ok)
			return

		# if image is valid, use colorThief to extract colors
		global colors_gen
		global colors_style

		if art_gen:
			colors_gen = utils.loadPalette(pathname)
			self.color_drop_region.replacePicture(pathname)
		else:
			colors_style = utils.loadPalette(pathname)
			self.color_drop_region_style.replacePicture(pathname)

		
	def openPictureFileDialog(self):
		pathname = ""
		fname = QFileDialog.getOpenFileName(self, 'Open file')
		pathname = fname[0]

		# ensure url is an image file, if not ignore
		if pathname == "":
			return

		try:
			im = PIL.Image.open(pathname)
			im.verify()
			im.close()

		except:
			QMessageBox.information(self, "Error", error.error_list["invalid picture"], QMessageBox.Ok)
			return

		# get width and height of image
		im = PIL.Image.open(pathname)
		width,height = im.size


		# ensure image does not exceed 1000x1000 max
		if width > 1000 or height > 1000:
			QMessageBox.information(self, "Error", error.error_list["picture size"], QMessageBox.Ok)
			return

		# if image is valid, use colorThief to extract colors
		self.picture_drop_region_style.replacePicture(pathname)

	def openColorDialog(self):
		global colors_gen
		global colors_style
		global art_gen

		# prompt how many colors to pick
		text, ok = QInputDialog.getText(self, 'Input Dialog', 'Number of colors to pick (max 10):')

		try:
			if ok:
				colors_to_pick = int(text)
			else:
				return
		except:
			QMessageBox.information(self, "Error", error.error_list["integer"], QMessageBox.Ok)
			return

		# if valid input, choose colors
		if ok and colors_to_pick <= 10:
			temp_colors = []
			for _ in range (0, colors_to_pick):
				color = QColorDialog.getColor()
				temp_colors.append(color.getRgb())

			if not temp_colors:
				QMessageBox.information(self, "Error", error.error_list["colors"], QMessageBox.Ok)
				return

			# create mock up pallete picture
			img = PIL.Image.new('RGB', (2520, 1700), color = 'white')

			# get a drawing context
			draw = ImageDraw.Draw(img)
			rectangle_width = (2520/len(temp_colors))

			# create the palette
			for color in range(0,len(temp_colors)):
				points = [(color * rectangle_width, 0), ((color+1)*rectangle_width, 1700)]
				draw.rectangle(points, fill=temp_colors[color], outline=temp_colors[color])

			filename_invalid = True
			current_files = os.listdir(os.getcwd() + '/User Palettes')

			# prompt for file name, loop around if file already exists with name
			while filename_invalid:

				text, ok = QInputDialog.getText(self, 'Input Dialog', 'File name for new palette:')
				
				filename = text + '.png'

				if ok and (filename not in current_files) and (text != ""):
					img.save('User Palettes/' + filename)
					filename_invalid = False
					pathname = os.path.abspath('User Palettes/' + filename) 
				elif not ok:
					return
				else:
					QMessageBox.information(self, "Error", error.error_list["file name"], QMessageBox.Ok)

			# add colors to proper color bank
			if art_gen:
				del colors_gen[:]
				colors_gen = temp_colors
			else:
				del colors_style[:]
				colors_style = temp_colors

			# upload the file created and replace drop zone image
			QMessageBox.information(self, "Sucess", "Color palette created and saved in \"User Palettes\"", QMessageBox.Ok)
			
			# replace proper art image
			if art_gen:
				self.color_drop_region.replacePicture(pathname)
			else:
				self.color_drop_region_style.replacePicture(pathname)


		else:
			QMessageBox.information(self, "Error", error.error_list["integer"], QMessageBox.Ok)
			return

	def templateSelectionChange(self):
		# get item selected
		template_key = self.cb_template.currentText()

		# find in dictionary and set the width and height in app
		wh = templates.size_template_dict[template_key]

		self.width_text.setText(str(wh[0]))
		self.height_text.setText(str(wh[1]))


	def returnClicked(self):
		# hide all widgets on finish page, show all values in mainUI depending on process ran
		global art_gen
		if art_gen:
			self.description.hide()
			self.return_button.hide()
			QApplication.processEvents()
			self.done.hide()

			for widget in self.art_gen_widgets:
				widget.show()

		else:
			self.picture_preview.hide()
			self.go_deeper_button.hide()
			self.description.hide()
			self.return_button.hide()
			QApplication.processEvents()
			self.done.hide()

			for widget in self.style_gen_widgets:
				widget.show()


	def artGenPage(self):
		# shows all the art gen widgets
		global art_gen

		for widget in self.style_gen_widgets:
			widget.hide()

		for widget in self.art_gen_widgets:
			widget.show()

		self.drop_palette_label.move(575,170)
		self.arrow_up_palette.move(635,203)

		pixmap = QPixmap(os.getcwd() + "/Graphics/drop.png")
		pixmap = pixmap.scaled(590, 400)
		self.color_drop_region.resize(9000,800)
		self.color_drop_region.move(390,20)
		self.color_drop_region.setPixmap(pixmap)
		self.color_drop_region.scale_x = 590
		self.color_drop_region.show()

		self.color_button.move(130,330)
		self.palette_button.move(130,380)

		art_gen = True


	def StyleTransferPage(self):
		# shows all the style transfer widgets
		global art_gen

		for widget in self.art_gen_widgets:
			widget.hide()

		for widget in self.style_gen_widgets:
			widget.show()

		self.drop_palette_label.move(100, 180)
		self.arrow_up_palette.move(160, 210)
		self.color_button.move(430, 250)
		self.palette_button.move(430, 300)

		art_gen = False

	def goDeeperClicked(self):
			self.picture_preview.hide()
			self.go_deeper_button.hide()
			self.description.hide()
			self.return_button.hide()
			QApplication.processEvents()
			self.done.hide()

			# create metadata 
			filepath = "/Users/alexcherekdjian/Desktop/Fall 2019/coen296B/Minimal Art UI/Generated Art/stylepic.png"
			image = PIL.Image.open(filepath)

			if image.width > image.height:
				scale_factor = (image.width/1000)
			else:
				scale_factor = (image.height/1000)

			height_resize = image.height/scale_factor
			width_resize = image.width/scale_factor
			new_size = (int(width_resize), int(height_resize))
			image.thumbnail(new_size)
			image.save(filepath) 

			image = PIL.Image.open(filepath)
			image = image.filter(PIL.ImageFilter.FIND_EDGES)
			image.save('Graphics/composite.png') 

			# find average color
			img = io.imread('Graphics/composite.png')[:, :, :-1]
			average = img.mean(axis=0).mean(axis=0)

			pixel_list = []
			image2 = PIL.Image.open('Graphics/composite.png')

			# use average color as threshold to pick points from picture
			for y in range(0, image2.height):
				for x in range(0, image2.width):
					xy = (x,y)
					pc_color = image2.getpixel(xy)

					if pc_color > (average[0], average[1], 0):
						x_scaled = x*10
						y_scaled = y*10
						xy_scaled = (x_scaled, y_scaled)
						pixel_list.append(xy_scaled)

			# create an image
			self.createStyleTransfer(pixel_list, image2.width*10, image2.height*10, filepath)

	def mainUI(self):
		# set background to picture gradient
		self.background = QLabel(self)
		pixmap = QPixmap(os.getcwd() + '/Graphics/back.jpeg')
		self.background.resize(pixmap.width(),pixmap.height())
		self.background.setPixmap(pixmap)

		# up arrow image for drop zone
		self.arrow_up_palette = QLabel(self)
		pixmap = QPixmap(os.getcwd() + "/Graphics/up_arrow.png")
		pixmap = pixmap.scaled(105, 125)
		self.arrow_up_palette.resize(500,700)
		self.arrow_up_palette.move(635,203) 
		self.arrow_up_palette.setPixmap(pixmap)
		self.arrow_up_palette.setAlignment(Qt.AlignLeft)

		# palette warning optional
		self.palette_label_optional = QLabel(self)
		self.palette_label_optional.setStyleSheet('font: 12pt Tahoma;')
		self.palette_label_optional.setText("<font color='white'>" + "(optional)" + "</font>")
		self.palette_label_optional.setAlignment(Qt.AlignLeft)
		self.palette_label_optional.setFixedWidth(500)
		self.palette_label_optional.setFixedHeight(30)
		self.palette_label_optional.move(186,330)
		self.palette_label_optional.hide()

		# pic warning size restriction
		self.pic_label_max = QLabel(self)
		self.pic_label_max.setStyleSheet('font: 12pt Tahoma;')
		self.pic_label_max.setText("<font color='white'>" + "(1000x1000 max)" + "</font>")
		self.pic_label_max.setAlignment(Qt.AlignLeft)
		self.pic_label_max.setFixedWidth(500)
		self.pic_label_max.setFixedHeight(30)
		self.pic_label_max.move(743,330)
		self.pic_label_max.hide()

		# picture arrow up image for drop zone
		self.arrow_up_picture = QLabel(self)
		pixmap = QPixmap(os.getcwd() + "/Graphics/up_arrow.png")
		pixmap = pixmap.scaled(105, 125)
		self.arrow_up_picture.resize(500,700)
		self.arrow_up_picture.move(735, 210)
		self.arrow_up_picture.setPixmap(pixmap)
		self.arrow_up_picture.setAlignment(Qt.AlignLeft)
		self.arrow_up_picture.hide()

		# clarify zone for picture
		self.drop_pic_label = QLabel(self)
		self.drop_pic_label.setStyleSheet('font: 27pt Tahoma;')
		self.drop_pic_label.setText("<font color='white'>" + "Drop a Picture Here" + "</font>")
		self.drop_pic_label.setAlignment(Qt.AlignLeft)
		self.drop_pic_label.setFixedWidth(500)
		self.drop_pic_label.setFixedHeight(30)
		self.drop_pic_label.move(670, 180)
		self.drop_pic_label.hide()

		# clarify zone for palette drop
		self.drop_palette_label = QLabel(self)
		self.drop_palette_label.setStyleSheet('font: 27pt Tahoma;')
		self.drop_palette_label.setText("<font color='white'>" + "Drop a Palette Here" + "</font>")
		self.drop_palette_label.setAlignment(Qt.AlignLeft)
		self.drop_palette_label.setFixedWidth(500)
		self.drop_palette_label.setFixedHeight(30)
		self.drop_palette_label.move(575,170)

		# init label for palette description warning
		self.palette_label = QLabel(self)
		self.palette_label.setStyleSheet('font: 12pt Tahoma;')
		self.palette_label.setText("<font color='white'>" + "If no palette is uploaded, a random stock palette will be used " + "</font>")
		self.palette_label.setAlignment(Qt.AlignLeft)
		self.palette_label.setFixedWidth(500)
		self.palette_label.setFixedHeight(30)
		self.palette_label.move(520,330)

		# create the color palette drop zone region
		self.color_drop_region = ColorDropZone(self)
		pixmap = QPixmap(os.getcwd() + "/Graphics/drop.png")
		pixmap = pixmap.scaled(590, 400)
		self.color_drop_region.resize(9000,800)
		self.color_drop_region.move(390,20)
		self.color_drop_region.setPixmap(pixmap)
		self.color_drop_region.setAlignment(Qt.AlignLeft)

		# init text box for width input
		self.width_text = QLineEdit(self)
		self.width_text.setFixedWidth(120)
		self.width_text.setFixedHeight(30)
		self.width_text.move(140,50)
		self.width_text.setAlignment(Qt.AlignCenter)
		self.width_text.setPlaceholderText("2000px")
		self.width_text.setStyleSheet('font: 15pt Tahoma;')

		# init label box for width
		self.width_label = QLabel(self)
		self.width_label.setStyleSheet('font: 15pt Tahoma;')
		self.width_label.setText("<font color='white'>"+ "Width: " + "</font>")
		self.width_label.setFixedWidth(50)
		self.width_label.setFixedHeight(30)
		self.width_label.move(75,50)

		# init text box for height input
		self.height_text = QLineEdit(self)
		self.height_text.setFixedWidth(120)
		self.height_text.setFixedHeight(30)
		self.height_text.move(140,130)
		self.height_text.setAlignment(Qt.AlignCenter)
		self.height_text.setPlaceholderText("2000px")
		self.height_text.setStyleSheet('font: 15pt Tahoma;')

		# init label for height
		self.height_label = QLabel(self)
		self.height_label.setStyleSheet('font: 15pt Tahoma;')
		self.height_label.setText("<font color='white'>"+ "Height: " + "</font>")
		self.height_label.setAlignment(Qt.AlignLeft)
		self.height_label.setFixedWidth(50)
		self.height_label.setFixedHeight(30)
		self.height_label.move(70,135)

		# init text box for number of picture input
		self.picture_number_text = QLineEdit(self) 
		self.picture_number_text.setFixedWidth(120)
		self.picture_number_text.setFixedHeight(30)
		self.picture_number_text.move(140,270) # 140, 230
		self.picture_number_text.setAlignment(Qt.AlignCenter)
		self.picture_number_text.setPlaceholderText("1..100")
		self.picture_number_text.setStyleSheet('font: 15pt Tahoma;')

		# init label for number of picture input
		self.picture_number_label = QLabel(self)
		self.picture_number_label.setStyleSheet('font: 15pt Tahoma;')
		self.picture_number_label.setText("<font color='white'>"+ "# of Pictures: " + "</font>")
		self.picture_number_label.setFixedWidth(100)
		self.picture_number_label.setFixedHeight(30)
		self.picture_number_label.move(30,270) # 30, 230

		# init the generate button
		self.generate_button = QPushButton(self)
		self.generate_button.setText('Generate')
		self.generate_button.move(0,455)
		self.generate_button.setFixedHeight(145)
		self.generate_button.setFixedWidth(1000)
		self.generate_button.clicked.connect(self.generateClicked)
		self.generate_button.setStyleSheet( \
			"QPushButton { font: 35pt Tahoma; color: white; background-color: rgba(253, 157, 154, 255);}" \
			"QPushButton:hover { background-color: rgba(254, 171, 169, 255);}" \
			"QPushButton:pressed { background-color: rgba(250, 200, 200, 255);}" \
			)

		# init the user palette creation button 
		self.color_button = QPushButton('Create a Palette', self)
		self.color_button.move(130,330)
		self.color_button.setFixedWidth(140)
		self.color_button.setFixedHeight(30)
		self.color_button.clicked.connect(self.openColorDialog)
		self.color_button.setStyleSheet(\
			"QPushButton {font: 15pt Tahoma; color: grey; background-color: ghostwhite; border-color: ghostwhite; border-radius: 12px; border-style: outset; border-width: 4px;}"\
			"QPushButton:hover { background-color: white; border-color: white; }" \
			"QPushButton:pressed { background-color: silver; border-color: transparent;}" \
			)

		# select a palette button
		self.palette_button = QPushButton('Select a Palette', self)
		self.palette_button.move(130,380)
		self.palette_button.setFixedWidth(140)
		self.palette_button.setFixedHeight(30)
		self.palette_button.clicked.connect(self.openFileDialog)
		self.palette_button.setStyleSheet(\
			"QPushButton {font: 15pt Tahoma; color: grey; background-color: ghostwhite; border-color: ghostwhite; border-radius: 12px; border-style: outset; border-width: 4px;}"\
			"QPushButton:hover { background-color: white; border-color: white; }" \
			"QPushButton:pressed { background-color: silver; border-color: transparent;}" \
			)

		# init preset template sizes button 
		self.cb_template = QComboBox(self)
		size_keys = templates.size_template_dict.keys() # get dict keys

		for key in size_keys:
			self.cb_template.addItem(str(key)) # add dict keys as options

		self.cb_template.setStyleSheet('font: 12pt Tahoma; color: Grey;')
		self.cb_template.setFixedWidth(130)
		self.cb_template.setFixedHeight(40)
		self.cb_template.currentIndexChanged.connect(self.templateSelectionChange)
		self.cb_template.move(135,175)

		# tab switching button
		self.style_button = QPushButton('Use Style Transfer', self)
		self.style_button.move(-5,-5)
		self.style_button.setFixedWidth(120)
		self.style_button.setFixedHeight(35)
		self.style_button.clicked.connect(self.StyleTransferPage)
		self.style_button.setStyleSheet(\
			"QPushButton {font: 12pt Tahoma; color: grey; background-color: ghostwhite; border-color: ghostwhite; border-radius: 5px; border-style: outset; border-width: 4px;}"\
			"QPushButton:hover { background-color: white; border-color: white; }" \
			"QPushButton:pressed { background-color: silver; border-color: transparent;}" \
			)

		# palette drop zone
		self.color_drop_region_style = ColorDropZone(self)
		pixmap = QPixmap(os.getcwd() + "/Graphics/drop.png")
		pixmap = pixmap.scaled(370, 350)
		self.color_drop_region_style.resize(370,350)
		self.color_drop_region_style.move(30,50)
		self.color_drop_region_style.scale_x = 375
		self.color_drop_region_style.scale_y = 350
		self.color_drop_region_style.setPixmap(pixmap)
		self.color_drop_region_style.setAlignment(Qt.AlignLeft)
		self.color_drop_region_style.hide()

		# picture drop zone
		self.picture_drop_region_style = PictureDropZone(self)
		pixmap = QPixmap(os.getcwd() + "/Graphics/drop.png")
		pixmap = pixmap.scaled(370, 350)
		self.picture_drop_region_style.resize(370,350)
		self.picture_drop_region_style.move(600,50)
		self.picture_drop_region_style.scale_x = 375
		self.picture_drop_region_style.scale_y = 350
		self.picture_drop_region_style.setPixmap(pixmap)
		self.picture_drop_region_style.setAlignment(Qt.AlignLeft)
		self.picture_drop_region_style.hide()

		# picture finder
		self.picture_button = QPushButton('Select a Picture', self)
		self.picture_button.move(430,150)
		self.picture_button.setFixedWidth(140)
		self.picture_button.setFixedHeight(30)
		self.picture_button.clicked.connect(self.openPictureFileDialog)
		self.picture_button.setStyleSheet(\
			"QPushButton {font: 15pt Tahoma; color: grey; background-color: ghostwhite; border-color: ghostwhite; border-radius: 12px; border-style: outset; border-width: 4px;}"\
			"QPushButton:hover { background-color: white; border-color: white; }" \
			"QPushButton:pressed { background-color: silver; border-color: transparent;}" \
			)
		self.picture_button.hide()

		self.art_gen_button = QPushButton('Use Art Generator', self)
		self.art_gen_button.move(-5,-5)
		self.art_gen_button.setFixedWidth(120)
		self.art_gen_button.setFixedHeight(35)
		self.art_gen_button.clicked.connect(self.artGenPage)
		self.art_gen_button.setStyleSheet(\
			"QPushButton {font: 12pt Tahoma; color: grey; background-color: ghostwhite; border-color: ghostwhite; border-radius: 5px; border-style: outset; border-width: 4px;}"\
			"QPushButton:hover { background-color: white; border-color: white; }" \
			"QPushButton:pressed { background-color: silver; border-color: transparent;}" \
			)
		self.art_gen_button.hide()

		self.art_gen_widgets = [self.width_text, self.height_text, self.picture_number_text, \
			self.color_drop_region, self.generate_button, self.width_label, self.height_label, \
			self.picture_number_label, self.palette_label, self.color_button, self.cb_template, \
			self.palette_button, self.style_button, self.drop_palette_label, self.arrow_up_palette]

		self.style_gen_widgets = [self.color_button, self.palette_button, self.color_drop_region_style, \
			self.picture_drop_region_style, self.picture_button, self.art_gen_button, self.generate_button, \
			self.drop_pic_label, self.palette_label_optional, self.pic_label_max, self.drop_palette_label,\
			self.arrow_up_palette, self.arrow_up_picture]
			

	def createImages(self):
		global colors_gen
		global number_of_pictures
		global width
		global height

		# initializing count and images left label
		count = number_of_pictures
		images_left = QLabel(self)
		images_left.setGeometry(QRect(0, 0, 1000, 525))
		images_left.setAlignment(Qt.AlignCenter)
		images_left.setStyleSheet('font: 300pt Tahoma;')
		images_left.setText("<font color='white'>"+ str(count) + "</font>")
		images_left.show()

		clear_palette = False

		# if no palette uploaded, choose one from random in Palettes folder
		if len(colors_gen) == 0:
			filename = random.choice(os.listdir(os.getcwd() + '/Stock Palettes'))
			filepath = "Stock Palettes/" + filename
			colors_gen = utils.loadPalette(filepath)
			clear_palette = True

		# create number of pictures asked for
		for i in range(0,number_of_pictures):
			utils.createPicture(self, colors_gen, str(i), width, height)
			count = count - 1
			images_left.setText("<font color='white'>"+ str(count) + "</font>")
			images_left.show()

		# clean up page
		images_left.hide()

		# if palette chosen at random, clear to make room for another random palette
		if clear_palette == True:
			del colors_gen [:]

		# display done page
		self.finishPage()

	def createStyleTransfer(self, pixel_list, width, height, filepath):
		global colors_style

		# clean up window
		for widget in self.style_gen_widgets:
			widget.hide()

		# write temp labels
		info_label_1 = QLabel(self)
		info_label_1.setGeometry(QRect(0, 0, 1000, 525))
		info_label_1.setAlignment(Qt.AlignCenter)
		info_label_1.setStyleSheet('font: 100pt Tahoma;')
		info_label_1.setText("<font color='white'>Style Transferring . . .</font>")
		info_label_1.show()

		info_label_2 = QLabel(self)
		info_label_2.setGeometry(QRect(0, 100, 1000, 525))
		info_label_2.setAlignment(Qt.AlignCenter)
		info_label_2.setStyleSheet('font: 25pt Tahoma;')
		info_label_2.setText("<font color='white'>This may take a while!</font>")
		info_label_2.show()

		# create style image
		utils.createStyleTransferImage(self, pixel_list, colors_style, width, height, filepath)

		# clean up and display finished window
		info_label_1.hide()
		info_label_2.hide()
		self.finishPage()

	def generateClicked(self):
		global width
		global height
		global number_of_pictures
		global art_gen

		if art_gen:
			# ensure all inputs are an integer
			try:
				width = int(self.width_text.text())
				height = int(self.height_text.text())
				number_of_pictures = int(self.picture_number_text.text())

			except:
				QMessageBox.information(self, "Error", error.error_list["parameters"], QMessageBox.Ok)
				return

			# if all inputs are numbers, ensure all are above 0
			if (width > 0) and (height > 0) and (number_of_pictures > 0):

					# clean up current window and create images
					for widget in self.art_gen_widgets:
						widget.hide()

					self.createImages()
			else: 
				QMessageBox.information(self, "Error", error.error_list["parameters"], QMessageBox.Ok)
				return

		else: 
			# ensure path is not empty
			if self.picture_drop_region_style.path == '':
				QMessageBox.information(self, "Error", error.error_list["no picture"], QMessageBox.Ok)
				return

			# create metadata 
			filepath = self.picture_drop_region_style.path
			image = PIL.Image.open(filepath)
			image = image.filter(PIL.ImageFilter.FIND_EDGES)
			image.save('Graphics/composite.png') 

			# find average color
			img = io.imread('Graphics/composite.png')[:, :, :-1]
			average = img.mean(axis=0).mean(axis=0)

			pixel_list = []
			image2 = PIL.Image.open('Graphics/composite.png')

			# use average color as threshold to pick points from picture
			for y in range(0, image2.height):
				for x in range(0, image2.width):
					xy = (x,y)
					pc_color = image2.getpixel(xy)

					if pc_color > (average[0], average[1], 0):
						x_scaled = x*10
						y_scaled = y*10
						xy_scaled = (x_scaled, y_scaled)
						pixel_list.append(xy_scaled)

			# create an image
			self.createStyleTransfer(pixel_list, image2.width*10, image2.height*10, filepath)



def main():
	app = QApplication(sys.argv)
	window = Window()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()