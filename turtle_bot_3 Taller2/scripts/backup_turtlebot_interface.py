#! /usr/bin/env python3
import rospy
import sys
from PyQt4 import QtGui

'''
Hay que usar la informacion del topic /turtlebot_position para poder graficar
'''

app = QtGui.QApplication(sys.argv)
window = QtGui.QWidget()
window.setGeometry(100, 100, 1000, 600)
window.setWindowTitle("Turtle bot interface")
etiqueta_hola = QtGui.QLabel("wenaas")


window.show()
app.exec_()

'''
Otro ejemplo de PyQt4
#! /usr/bin/env python3
import rospy
import sys
from PyQt4 import QtGui

Hay que usar la informacion del topic /turtlebot_position para poder graficar


class Example(QtGui.QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		button_aceppt = QtGui.QPushButton('Aceptar', self)
		button_cancel = QtGui.QPushButton('Cancelar', self)
		button_cancel.move(900, 650)
		button_aceppt.move(800, 650)
		self.setFixedSize(1000, 700)
		#self.setGeometry(150, 150, 1000, 700) #Permite ajustar el tamaño de la ventana
		self.setWindowTitle('Prueba boton')
		self.show()

def main():
	app = QtGui.QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
'''


'''
 
import sys
import rospy
from std_msgs.msg import String
from PyQt4 import QtGui
from PyQt4.QtGui import QLabel, QVBoxLayout, QHBoxLayout, QSlider, QPushButton
from PyQt4.QtCore import Qt
 
class PyGui(QtGui.QWidget):
    def __init__(self):
        super(PyGui, self).__init__()
        self.setObjectName('PyGui')
        self.pub = rospy.Publisher("pyqt_topic", String, queue_size=10)
        rospy.init_node('pyqt_gui')
        self.current_value = 0
        my_layout = QHBoxLayout()
        my_btn = QPushButton()
        my_btn.setText("Publisher")
        my_btn.setFixedWidth(130)
        my_btn.clicked.connect(self.publish_topic)
        my_layout.addWidget(my_btn)
        my_layout.addSpacing(50)
        self.my_label = QLabel()
        self.my_label.setFixedWidth(140)
        self.my_label.setText("num: " + str(0))
        self.my_label.setEnabled(False)
        my_layout.addWidget(self.my_label)
        my_slider = QSlider()
        my_slider.setMinimum(0)
        my_slider.setMaximum(99)
        my_slider.setOrientation(Qt.Horizontal)
        my_slider.valueChanged.connect(self.changeValue)
        my_vlay = QVBoxLayout()
        my_vlay.addWidget(my_slider)
        layout = QVBoxLayout()
        layout.addLayout(my_layout)
        layout.addLayout(my_vlay)
        self.setLayout(layout)
        # self.show()
 
    def publish_topic(self):
        self.pub.publish(str(self.current_value))
 
    def changeValue(self, value):
        self.my_label.setText("num: " + str(value))
        self.current_value = value
 
 
if __name__ == "__main__":
    app=QtGui.QApplication(sys.argv)
    pyShow = PyGui()
    pyShow.show()
    sys.exit(app.exec_())
    '''