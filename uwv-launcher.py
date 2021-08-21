#!/usr/bin/python3
'''
This is the main application that needs to be run for a GUI based launch file generator.
'''

from PyQt5 import QtCore, QtGui, QtWidgets
import map_ui
import gen
import math
import os

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("uwv-launcher")
		MainWindow.resize(1800, 1080)

		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.mapUiWidget = QtWidgets.QWidget(self.centralwidget)
		self.mapUiWidget.setGeometry(QtCore.QRect(20, 150, 1319, 659))
		self.mapUiWidget.setObjectName("map_ui")
		self.mapUiWidget.raise_()

		self.heading = QtWidgets.QLabel(self.centralwidget)
		self.heading.setText("<h1>SAUVC Pool</h1>")
		self.heading.move(1400, 50)
		self.heading.setGeometry(20, 70, 1319, 100)
		self.heading.setAlignment(QtCore.Qt.AlignCenter)

		self.mapUI = map_ui.Label()
		self.lay = QtWidgets.QHBoxLayout(self.mapUiWidget)
		self.lay.addWidget(self.mapUI, alignment=QtCore.Qt.AlignCenter)
		
		self.angles = [0, 90, 180, 270]
		self.angleIdx = 0
		self.variables = ["startPoint", "gate", "qualGate", "mat", "redBucket", "blueBucket", "redFlare", "yellowFlare"]
		self.options = []
		
		self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(self.mapUI, 'Select location of uwv-simulator package', '/home')
		assert os.path.isdir(os.path.join(self.folderpath, "uwv_control")), "Wrong path to uwv-simulator"

		self.text1 = QtWidgets.QLabel(self.centralwidget)
		self.text1.setText("<h3>Select an object to place</h3>\n<h5>Left Click to place, Right click to remove</h5>")
		self.text1.move(1400, 200)

		for i, name in enumerate(self.mapUI.names):
			option = QtWidgets.QRadioButton(self.centralwidget)
			option.setGeometry(QtCore.QRect(1400, 300+(i*30), 200, 23))
			option.setObjectName(self.mapUI.names[i])
			option.raise_()
			self.options.append(option)

		self.options[0].setChecked(True)

		self.angleText = QtWidgets.QLabel(self.centralwidget)
		self.angleText.setText("Angle : 0 degrees")
		self.angleText.move(1400, 540)

		angleButton = QtWidgets.QPushButton("Change Angle", self.centralwidget)
		angleButton.move(1400, 570)
		angleButton.clicked.connect(self.changeAngle)

		saveButton = QtWidgets.QPushButton("Confirm Object", self.centralwidget)
		saveButton.move(1400, 620)
		saveButton.clicked.connect(self.saveObject)

		saveButton = QtWidgets.QPushButton("Generate Launch Files!", self.centralwidget)
		saveButton.move(1400, 800)
		saveButton.setGeometry(1400, 700, 300, 50)
		saveButton.clicked.connect(self.generate)

		self.genText = QtWidgets.QLabel(self.centralwidget)
		self.genText.setText("")
		self.genText.setStyleSheet("color: green")
		self.genText.setGeometry(1400, 750, 300, 50)

		launchButton = QtWidgets.QPushButton("Launch", self.centralwidget)
		launchButton.move(1400, 800)
		launchButton.setGeometry(1400, 800, 300, 50)
		launchButton.clicked.connect(self.launch)

		self.launchText = QtWidgets.QLabel(self.centralwidget)
		self.launchText.setText("")
		self.launchText.setStyleSheet("color: red")
		self.launchText.setGeometry(1400, 850, 300, 50)

		MainWindow.setCentralWidget(self.centralwidget)
		self.mapUI.currentObject = self.mapUI.options["Start-Point"]
		self.retranslateUi(MainWindow)

		self.options[0].toggled.connect(lambda:self.btnState(self.options[0]))
		self.options[1].toggled.connect(lambda:self.btnState(self.options[1]))
		self.options[2].toggled.connect(lambda:self.btnState(self.options[2]))
		self.options[3].toggled.connect(lambda:self.btnState(self.options[3]))
		self.options[4].toggled.connect(lambda:self.btnState(self.options[4]))
		self.options[5].toggled.connect(lambda:self.btnState(self.options[5]))
		self.options[6].toggled.connect(lambda:self.btnState(self.options[6]))

		self.mapUI.currentOption = self.options[0].text()
		
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

		for i, option in enumerate(self.options):
			option.setText(_translate("MainWindow", self.mapUI.names[i]))

	def btnState(self, btn):
		
		for option in self.options:
			if btn.text() == option.text():
				if btn.isChecked():
					self.mapUI.currentObject = self.mapUI.options[option.text()]
					self.mapUI.currentOption = option.text()
					self.angleIdx = 0
					self.angleText.setText(f'Angle : {0} degrees')

	def saveObject(self):
		if self.mapUI.lastPoint != None:
			self.mapUI.saveObject(self.mapUI.currentOption)
			self.mapUI.lastPoint = None

	def generate(self):
		
		with open(os.path.join(self.folderpath, "uwv_env/launch/sauvc-pool-autogen.launch"), "w") as f:
			print(gen.head_env, end="\n\n", file=f)
			print(gen.head1_env, end="\n\n", file=f)

			for i in self.mapUI.objects.keys():
				objType = self.mapUI.objects[i][0]
				pos = self.mapUI.objects[i][1]
				angle = self.mapUI.objects[i][2]
				pos = (-((pos[1] / 659 * 25) - 12.5), -((pos[0] / 1319 * 50) - 25), math.radians(angle))
				if objType == "Gate":
					print(gen.task1_gate(pos), end="\n\n", file=f)
				elif objType == "Mat":
					print(gen.task2_mat(pos), end="\n\n", file=f)
				elif objType == "Red-Flare":
					print(gen.task1_flare(pos), end="\n\n", file=f)
				elif objType == "Qual-Gate":
					print(gen.q_gate(pos), end="\n\n", file=f)
				elif objType == "No-Pinger-Flare":
					print(gen.task4_no_pinger(pos), end="\n\n", file=f)
				elif objType == "Pinger-Flare":
					print(gen.task4_pinger(pos), end="\n\n", file=f)
				elif objType == "Start-Point":
					with open(os.path.join(self.folderpath, "uwv_control/launch/sauvc-pool-autogen.launch"), "w") as fs:
						print(gen.head_control, end="\n\n", file=fs)
						print(gen.start(pos) , end="\n\n", file=fs)
						print(gen.tail_control, end="\n\n", file=fs)

			print(gen.tail_env, end="\n\n", file=f)

		print("Launch file generated!")
		self.genText.setText("Launch file generated!")

	def changeAngle(self):
		self.angleIdx += 1
		self.angleIdx %= 4
		self.angleText.setText(f'Angle : {self.angles[self.angleIdx]} degrees')
		transform = QtGui.QTransform().rotate(self.angles[self.angleIdx])
		self.mapUI.angle = self.angles[self.angleIdx]
		self.mapUI.currentObject = self.mapUI.options[self.mapUI.currentOption]
		self.mapUI.currentObject = self.mapUI.currentObject.transformed(transform)

	def launch(self):
		if not os.path.isfile(os.path.join(self.folderpath, "uwv_control/launch/sauvc-pool-autogen.launch")):
			self.launchText.setText("Launch files do not exist! Please generate them")
			print("Launch files do not exist! Please generate them")
			return
		os.system("gnome-terminal -e 'bash -c \"roslaunch uwv_control sauvc-pool-autogen.launch; exec bash\"'")
		exit(0)

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	MainWindow.setWindowTitle("uwv-launcher")
	sys.exit(app.exec_())
