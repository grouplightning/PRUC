from tkinter import *
from tkinter import messagebox #not sure why this is necessary but * doesn't pull this in
#Tk, Label, Button, PhotoImage, Listbox, Grid, BOTH, Entry, StringVar
import configparser
import os
import subprocess

from ui_modules.MainMenu import MainMenu
from ui_modules.ExportMenu import ExportMenu
from ui_modules.SensorMenu import SensorMenu
from ui_modules.StatusMenu import StatusMenu

from db.db import DB


class HubUI:
	def __init__(self, master):
		try:
			self.db = DB()
		except:
			print("DB support initialization failed")
			messagebox.showerror("Error", "Could not connect to Hub Database\r\nThis utility may not work correctly.")
			self.db=None

		self.master = master
		self.master.minsize(800,600)
		master.title("PRUC Hub")

		#columnw = 10
		#rowh = 5
		#fontsize = 15
		#font = ("TkDefaultFont", fontsize)


		self.widget_bounds={'width':10, 'height':5}
		self.widget_style={'master':master, 'background':'white', 'font':("TkDefaultFont", 15),'borderwidth':0}

		master.configure(background='white')


		self.menu_icon=PhotoImage(file="ui_images/menu.gif")
		self.menu_back_icon=PhotoImage(file="ui_images/menu_back.gif")
		#w=10*12*7
		#h=10*12*3 + 12
		#x=0
		#y=0
		#root.geometry('%dx%d+%d+%d' % (w, h, x, y))

		self.config = configparser.ConfigParser()
		os.chdir(os.path.abspath(os.path.dirname(__file__)))
		self.config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'hub.ini'))

		self.menus = {}
		self.current_menu = None# MainMenu(self)
		self.previous_menu = None

		self.load_menu('status',StatusMenu(self))
		self.load_menu('sensors',SensorMenu(self))
		self.load_menu('main',MainMenu(self))
		self.load_menu('export',ExportMenu(self))
		#... more

		self.switch_menu('main')

		print(self.master.grid_size())


	def lock_col(self,x):
		Grid.columnconfigure(self.master, x, weight=0)
	def lock_row(self,y):
		Grid.rowconfigure(self.master, y, weight=0)
	def unlock_col(self,x):
		Grid.columnconfigure(self.master, x, weight=1)
	def unlock_row(self,y):
		Grid.rowconfigure(self.master, y, weight=1)
	def unlock_grid(self):
		(cols,rows) = self.master.grid_size()
		for x in range(cols):
			Grid.columnconfigure(self.master, x, weight=1)
		for y in range(rows):
			Grid.rowconfigure(self.master, y, weight=1)
	def lock_grid(self):
		(cols,rows) = self.master.grid_size()
		for x in range(cols):
			Grid.columnconfigure(self.master, x, weight=0)
		for y in range(rows):
			Grid.rowconfigure(self.master, y, weight=0)

	def create_widget_settings(self):
		return self.widget_style.copy()

	def create_bounded_settings(self):
		widget_settings = self.widget_style.copy()
		widget_settings.update(self.widget_bounds)

		return widget_settings

	def create_listbox(self,owningList,row,column, sticky=None):
		widget_settings = self.create_bounded_settings()
		widget_settings.update({'relief':'sunken','background':'#ccc9b8','activestyle':'none','borderwidth':'2'})#,'width':self.widget_bounds['width']})
		widget = Listbox(**widget_settings)
		widget.grid(row=row, column=column, sticky=sticky,columnspan=3)
		owningList.append(widget)
		return widget


	def create_spacing(self,owningList,row,column, sticky=None):
		widget_settings = self.create_bounded_settings()
		widget_settings.update({'text':""})
		widget = Label(**widget_settings)
		widget.grid(row=row,column=column, sticky=sticky)
		owningList.append(widget)
	def create_text(self,owningList,row,column,text="", sticky=None):
		widget_settings = self.create_widget_settings()
		widget_settings.update({'text':text})#,'width':self.widget_bounds['width']})
		widget = Label(**widget_settings)
		widget.grid(row=row,column=column, sticky=sticky)
		owningList.append(widget)

	def create_input(self,owningList,row,column,text="", sticky=None, readonly=False):
		widget_settings = self.create_widget_settings()
		v = StringVar()
		widget_settings.update({'relief':'sunken','background':'lightgray','borderwidth':'2'})#,'width':self.widget_bounds['width']})
		widget_settings.update({'textvariable':v})#,'width':self.widget_bounds['width']})
		widget = Entry(**widget_settings)
		if readonly:
			widget.configure(state='readonly')
		widget.grid(row=row,column=column, sticky=sticky)
		v.set(text)
		owningList.append(widget)
		return v


	def create_image_button(self,owningList,row,column,image,command,text="", sticky=None):
		widget_settings = self.create_widget_settings()
		widget_settings.update({'image':image,'text':text,'command':command})
		widget = Button(**widget_settings)
		widget.grid(row=row,column=column, sticky=sticky)
		owningList.append(widget)

	def create_text_button(self,owningList,row,column,command,text="",anchor="center",justify="center", sticky=None, styled=False):
		widget_settings = self.create_widget_settings()
		widget_settings.update({'text':text,'command':command,'anchor':anchor,'justify':justify})#,'width':self.widget_bounds['width']})
		if styled:
			widget_settings.update({'relief': 'raised','background':'#ece9d8','borderwidth': '2'})  # ,'width':self.widget_bounds['width']})
		#print(text+" :: "+anchor+" "+justify)
		widget = Button(**widget_settings)
		widget.grid(row=row,column=column, sticky=sticky)
		owningList.append(widget)

	def create_menu_option(self,owningList,row,command,text,back=False, sticky=None):
		icon = self.menu_icon
		if back:
			icon = self.menu_back_icon
			print(str(back)+" "+str(icon))
		self.create_image_button(owningList, image=icon, row=row, column=1, command=command, sticky=sticky)
		self.create_text_button(owningList, row=row, column=2, command=command, text=text, anchor="w", justify="left", sticky=sticky)

	def load_menu(self,name,menu):
		self.menus[name]=menu
		self.current_menu = menu
		menu.hide_widgets()

	def switch_menu(self,name):
		self.current_menu.hide_widgets()
		self.previous_menu = self.current_menu
		self.current_menu = self.menus[name]
		self.current_menu.show_widgets()

	def back(self):
		self.current_menu.hide_widgets()
		self.current_menu = self.previous_menu #note should replace this with a stack / push-pop for deeper forward-back mechanics
		self.current_menu.show_widgets()


root = Tk()
my_gui = HubUI(root)
root.mainloop()