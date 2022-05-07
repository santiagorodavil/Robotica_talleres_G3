#! /usr/bin/env python3
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
except ImportError:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

from geometry_msgs.msg import Twist
import rospy
import os

LARGE_FONT=("Verdana",12)
style.use("ggplot")

f=Figure(figsize=(5,5),dpi=100)
a=f.add_subplot(111) 

xList = []
yList = []

i = 0
x = []
y = []
z = []

ax = Axes3D(f)
##################################################
def callback(data):
	global x
	global y
	global z
	x.append(data.linear.x)
	y.append(data.linear.y)
	z.append(data.linear.z)

###################################################
# Función de dibujo dinámico
def drawImg(u):
    global x
    global y
    global z
    ax.clear()
    ax.plot(x, y, z)
    
    



# def animate(i):
# 	pullData = open("/home/robotica/catkin_ws/src/robotica_pkg/src/scripts/datos.txt","r").read()
# 	dataList = pullData.split('\n')
	
# 	for eachLine in dataList:
# 		if len(eachLine) > 1:
# 			x, y=eachLine.split(',')
			
# 			xList.append(int(x))
# 			yList.append(int(y))
			
# 	a.clear()
# 	a.plot(xList, yList)

class SeaofBTCapp(tk.Tk):
	"""docstring for SeaofBTCapp"""
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		container=tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames={}
# PageOne, PageThree,
		for F in (StartPage,  PageTwo):
			frame = F(container, self)
			self.frames[F]=frame
			frame.grid(row=0,column=0,sticky="nsew")
		self.show_frame(StartPage)
	def show_frame(self,cont):
		frame=self.frames[cont]
		frame.tkraise()

class StartPage(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		label=tk.Label(self,text="StartPage",font=LARGE_FONT)
		label.pack(pady=10,padx=10)
		# button=ttk.Button(self,text="Visit Page 1", command=lambda:controller.show_frame(PageOne))
		# button.pack()

		button2=ttk.Button(self,text="3d Graph", command=lambda:controller.show_frame(PageTwo))
		button2.pack()

		# button3=ttk.Button(self,text="Graph Page", command=lambda:controller.show_frame(PageThree))
		# button3.pack()

# class PageOne(tk.Frame):
# 	def __init__(self,parent,controller):
# 		tk.Frame.__init__(self,parent)
# 		label=tk.Label(self,text="Page 1",font=LARGE_FONT)
# 		label.pack(pady=10,padx=10)

# 		button1=ttk.Button(self,text="BackHome", command=lambda:controller.show_frame(StartPage))
# 		button1.pack()

# 		button2=ttk.Button(self,text="Page 2", command=lambda:controller.show_frame(PageTwo))
# 		button2.pack()

class PageTwo(tk.Frame):
 	def __init__(self,parent,controller):
 		tk.Frame.__init__(self,parent)
 		label=tk.Label(self,text="Page 2",font=LARGE_FONT)
 		label.pack(pady=10,padx=10)

 		button1=ttk.Button(self,text="BackHome", command=lambda:controller.show_frame(StartPage))
 		button1.pack()

 		button2=ttk.Button(self,text="Page 3", command=lambda:controller.show_frame(PageThree))
 		button2.pack()

 		canvas = FigureCanvasTkAgg(f, self)
 		canvas.draw()
 		# Mostrar lienzo
 		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
 		

# class PageThree(tk.Frame):
# 	def __init__(self,parent,controller):
# 		tk.Frame.__init__(self,parent)
# 		label=tk.Label(self,text="Graph Page",font=LARGE_FONT)
# 		label.pack(pady=10,padx=10)

# 		button1=ttk.Button(self,text="BackHome", command=lambda:controller.show_frame(StartPage))
# 		button1.pack()

# 		canvas=FigureCanvasTkAgg(f,self)
# 		canvas.draw()
# 		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# 		toolbar = NavigationToolbar2TkAgg(canvas,self)
# 		toolbar.update()
# 		canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH,expand=True)


def listener():

	rospy.init_node('turtlebot_interface3d')
	rospy.Subscriber("robot_manipulator_position", Twist, callback)
	app = SeaofBTCapp()
	ani = animation.FuncAnimation(f,drawImg,interval = 1000)
	app.mainloop()
	rospy.spin()


if __name__=='__main__':
	listener()

# ani = animation.FuncAnimation(f,animate,interval = 1000)
