from tkinter import Tk, Label, Button, PhotoImage
import configparser
import os
import subprocess

from ui_modules.MainMenu import MainMenu
from ui_modules.StatusMenu import StatusMenu


class HubUI:
	def __init__(self, master):
		self.master = master
		master.title("PRUC Hub")

		columnw = 10
		rowh = 5
		fontsize = 15
		font = ("TkDefaultFont", fontsize)


		self.widget_bounds={'width':10, 'height':5}
		self.widget_style={'master':master, 'background':'white', 'font':("TkDefaultFont", 15),'borderwidth':0}

		master.configure(background='white')


		self.menu_icon=PhotoImage(file="menu.gif")
		self.menu_back_icon=PhotoImage(file="menu_back.gif")
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
		self.load_menu('main',MainMenu(self))
		#... more

		self.switch_menu('main')


	def create_widget_settings(self):
		return self.widget_style.copy()

	def create_bounded_settings(self):
		widget_settings = self.widget_style.copy()
		widget_settings.update(self.widget_bounds)

		return widget_settings
	def create_spacing(self,owningList,row,column):
		widget_settings = self.create_bounded_settings()
		widget_settings.update({'text':""})
		widget = Label(**widget_settings)
		widget.grid(row=row,column=column)
		owningList.append(widget)

	def create_text(self,owningList,row,column,text=""):
		widget_settings = self.create_widget_settings()
		widget_settings.update({'text':text})#,'width':self.widget_bounds['width']})
		widget = Label(**widget_settings)
		widget.grid(row=row,column=column)
		owningList.append(widget)

	def create_image_button(self,owningList,row,column,image,command,text=""):
		widget_settings = self.create_widget_settings()
		widget_settings.update({'image':image,'text':text,'command':command})
		widget = Button(**widget_settings)
		widget.grid(row=row,column=column)
		owningList.append(widget)

	def create_text_button(self,owningList,row,column,command,text="",anchor="center",justify="center"):
		widget_settings = self.create_widget_settings()
		widget_settings.update({'text':text,'command':command,'anchor':anchor,'justify':justify})#,'width':self.widget_bounds['width']})
		#print(text+" :: "+anchor+" "+justify)
		widget = Button(**widget_settings)
		widget.grid(row=row,column=column)
		owningList.append(widget)

	def create_menu_option(self,owningList,row,command,text,back=False):
		icon = self.menu_icon
		if back:
			icon = self.menu_back_icon
			print(str(back)+" "+str(icon))
		self.create_image_button(owningList, image=icon, row=row, column=1, command=command)
		self.create_text_button(owningList, row=row, column=2, command=command, text=text, anchor="w", justify="left")

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