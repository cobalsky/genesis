
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFrame

class Frame(QFrame):
	
	"""  Clase que contiene las funciones que hacen posible el poder arrastrar y soltar el video o audio para ser reproducidos por el Reproductor. """

	origen = pyqtSignal(str)
	def __init__(self, *args, **kwargs):
		super(Frame, self).__init__(*args, **kwargs)
		self.setAcceptDrops(True)	
		
		self.ruta = ""

    # funciones para arrastrar y soltar
	def dragEnterEvent(self, e):

		if e.mimeData().hasUrls():
			e.accept()
			
		else:
			e.ignore()

	def dropEvent(self, e):

		if e.mimeData().hasUrls():
			e.accept()
			for url in e.mimeData().urls():
				self.ruta = url.toLocalFile()
			self.origen.emit(self.ruta)
		else:
			e.ignore()