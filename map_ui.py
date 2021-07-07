'''
This file contains the main widget where placing different objects is possible.
This can be combined with main.py if needed.
'''

from PyQt5 import QtCore, QtGui, QtWidgets

class Label(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super(Label, self).__init__(parent)

		self.names = ["Start-Point", "Gate", "Qual-Gate", "Mat", "No-Pinger-Flare", "Red-Flare", "Pinger-Flare"]

		self.options = {}
		self.options["Start-Point"] = QtGui.QPixmap("assets/start-point.png")
		self.options["Gate"] = QtGui.QPixmap("assets/gate.png")
		self.options["Qual-Gate"] = QtGui.QPixmap("assets/qual-gate.png")
		self.options["Mat"] = QtGui.QPixmap("assets/mat.png")
		self.options["Red-Bucket"] = QtGui.QPixmap("assets/red-bucket.png")
		self.options["No-Pinger-Flare"] = QtGui.QPixmap("assets/no-pinger-flare.png")
		self.options["Red-Flare"] = QtGui.QPixmap("assets/red-flare.png")
		self.options["Pinger-Flare"] = QtGui.QPixmap("assets/pinger-flare.png")

		self.image = QtGui.QPixmap("assets/pool.png")
		self.image1 = QtGui.QPixmap("assets/pool.png")
		
		self.objects = {}
		self.objectsCount = 0

		self.lastPoint = QtCore.QPoint()
		self.angle = 0
		self.drawing = False
		
		self.currentOption = "Start-Point"
		self.currentObject = self.options["Start-Point"]

	def paintEvent(self, event):
		painter = QtGui.QPainter(self)
		painter.drawPixmap(QtCore.QPoint(), self.image)

	def mousePressEvent(self, event):
		if event.button() == QtCore.Qt.LeftButton:
			print("left press")
			self.drawing = True
			self.draw(event.pos())
		if event.button() == QtCore.Qt.RightButton:
			print("right press")
			self.draw()

	def mouseMoveEvent(self, event):
		if event.buttons() and QtCore.Qt.LeftButton and self.drawing:
			self.draw(event.pos())
		if event.buttons() and QtCore.Qt.RightButton and not(self.drawing):
			self.draw()

	def mouseReleaseEvent(self, event):
		if event.button() == QtCore.Qt.LeftButton:
			print("left release")
			self.drawing = False
		if event.button() == QtCore.Qt.RightButton:
			print("right release")
			self.lastPoint = None
			self.draw()

	def sizeHint(self):
		return self.image.size()

	def draw(self, pos=None):

		painter = QtGui.QPainter(self.image)
		painter.drawPixmap(0, 0, self.image1)

		for i in self.objects.keys():
			transform = QtGui.QTransform().rotate(self.objects[i][2])
			painter.drawPixmap(self.objects[i][1][0], self.objects[i][1][1], self.options[self.objects[i][0]].transformed(transform))
				
		if pos != None:
			print(f'pos={pos}')
			if self.currentOption in ["Gate", "Qual-Gate"]:
				self.lastPoint = QtCore.QPoint(pos.x(), pos.y())	
			else:
				self.lastPoint = QtCore.QPoint(pos.x()-self.currentObject.size().width()/2, pos.y()-self.currentObject.size().height()/2)
			
			painter.drawPixmap(self.lastPoint.x(), self.lastPoint.y(), self.currentObject)
		self.update()

	def saveObject(self, objName):
		self.objects[self.objectsCount] = [objName, (self.lastPoint.x(), self.lastPoint.y()), self.angle]
		self.objectsCount += 1
		print(self.objects)

	def changeAngle(self):
		transform = QtGui.QTransform().rotate(self.angle)
		self.currentObject = self.currentObject.transformed(transform)

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.label = Label()
		# self.textedit = QtWidgets.QTextEdit()

		widget = QtWidgets.QWidget()
		self.setCentralWidget(widget)
		lay = QtWidgets.QHBoxLayout(widget)
		lay.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
		# lay.addWidget(self.textedit)


if __name__ == "__main__":
	import sys

	app = QtWidgets.QApplication(sys.argv)
	w = MainWindow()
	w.show()
	sys.exit(app.exec_())