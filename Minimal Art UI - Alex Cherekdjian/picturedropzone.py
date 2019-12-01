import utils, PIL, error
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# a class for a drag and drop widget for pictures
class PictureDropZone(QLabel):
	def __init__(self, parent):
		super().__init__(parent)
		self.setAcceptDrops(True)
		self.scale_x = 590
		self.scale_y = 400
		self.path = ''

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

		# ensure file is small enough
		im = PIL.Image.open(pathname)
		width, height = im.size 
		if width > 1000 or height > 1000:
			QMessageBox.information(self, "Error", error.error_list["picture size"], QMessageBox.Ok)
			return

		self.path = pathname

		# replace image in window with picture
		self.pic = QLabel(self)
		self.pixmap = QPixmap(pathname)
		self.pixmap = self.pixmap.scaled(self.scale_x, self.scale_y)

		self.pic.setPixmap(self.pixmap)
		self.pic.show()


	def replacePicture(self, pathname):
		# replace image in window with picture
		self.path = pathname

		self.pic = QLabel(self)
		self.pixmap = QPixmap(pathname)
		self.pixmap = self.pixmap.scaled(self.scale_x, self.scale_y)
		self.pic.setPixmap(self.pixmap)
		self.pic.show()
