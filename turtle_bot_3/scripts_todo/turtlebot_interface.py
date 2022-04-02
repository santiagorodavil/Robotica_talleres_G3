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
from geometry_msgs.msg import Pose2D
import rospy
import os


LARGE_FONT=("Verdana",12)
style.use("ggplot")

f=Figure(figsize=(5,5),dpi=100)
a=f.add_subplot(111)


#######################################################################3
pData = []
pData.append([0.0])
pData.append([0.0])

def callback(data):
    global pData
    #rospy.loginfo(rospy.get_caller_id()+ "Estoy escuchando: %s", data)
    pData[0].append(data.x)
    pData[1].append(data.y)
    
######################################################################
def animate(i):

	global pData
			
	a.clear()
	a.plot(pData[0], pData[1])

class SeaofBTCapp(tk.Tk):
	"""docstring for SeaofBTCapp"""
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		container=tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames={}
#  PageTwo,
		for F in (StartPage,PageOne, PageThree):
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
		label=tk.Label(self,text="Turtle bot interface - Inicio",font=LARGE_FONT)
		label.pack(pady=10,padx=10)
		button=ttk.Button(self,text="Guardar recorrido", command=lambda:controller.show_frame(PageOne))
		button.pack()
		


		# button2=ttk.Button(self,text="Visit Page 2", command=lambda:controller.show_frame(PageTwo))
		# button2.pack()

		button3=ttk.Button(self,text="Pagina de grafica", command=lambda:controller.show_frame(PageThree))
		button3.pack()

class PageOne(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		label=tk.Label(self,text="Page 1",font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		button1=ttk.Button(self,text="BackHome", command=lambda:controller.show_frame(StartPage))
		button1.pack()
		actor=ttk.Button(self,text="File", command=self.safeFile)
		actor.pack()

		button2=ttk.Button(self,text="Page 2", command=lambda:controller.show_frame(PageTwo))
		button2.pack()

	def safeFile(self):
		question=simpledialog.askstring("Introducir nombre deseado de archivo ","")
		messagebox.showinfo("...",f"Guardando archivo como; {question}.txt")
		oldFile = r"./src/turtle_bot_3/results/info_recorrido.txt"
		newFile = r"./src/turtle_bot_3/results/" + str(question) + ".txt"
		os.rename(oldFile,	newFile)

# class PageTwo(tk.Frame):
# 	def __init__(self,parent,controller):
# 		tk.Frame.__init__(self,parent)
# 		label=tk.Label(self,text="Page 2",font=LARGE_FONT)
# 		label.pack(pady=10,padx=10)

# 		button1=ttk.Button(self,text="BackHome", command=lambda:controller.show_frame(StartPage))
# 		button1.pack()

# 		button2=ttk.Button(self,text="Page 3", command=lambda:controller.show_frame(PageThree))
# 		button2.pack()

class PageThree(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		label=tk.Label(self,text="Graph Page",font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		button1=ttk.Button(self,text="BackHome", command=lambda:controller.show_frame(StartPage))
		button1.pack()

		canvas=FigureCanvasTkAgg(f,self)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

		toolbar = NavigationToolbar2TkAgg(canvas,self)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH,expand=True)




#####################################################################################
def listener():
	global pData
	rospy.init_node('turtlebot_interface')
	rospy.Subscriber("turtlebot_position", Pose2D, callback)
	app = SeaofBTCapp()
	ani = animation.FuncAnimation(f,animate,interval = 1000)
	app.mainloop()   


	#Inicia hilo que va a correr en paralelo (y por siempre) la función miPintura()    
	#plot_figure = Thread(target = miPintura)
	#plot_figure.start()
	rospy.spin()

########################################################################################

if __name__=='__main__':
    listener()
