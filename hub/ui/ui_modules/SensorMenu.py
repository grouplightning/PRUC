from tkinter import Tk, Label, Button, PhotoImage, END, N, S, E, W
import configparser

class SensorMenu:
	def __init__(self, ui):
		self.ui=ui

		self.other=[]
		self.buttons = []
		self.spacing = []

		ui.create_menu_option(self.buttons,row=0,command=ui.back,text="Back",back=True)
		self.listbox = ui.create_listbox(self.other, row=1, column=2, sticky=N+S+E+W)

		self.listbox.insert(END, "a list entry das asdjasd laskdjlas asdjkals sadjlasd asd")
		#self.listbox.grid(column=x, row=y, sticky=N + S + E + W)


		#ui.create_menu_option(self.buttons,row=2,command=self.hide_widgets,text="View Hub Status")
		#ui.create_menu_option(self.buttons,row=3,command=self.hide_widgets,text="View Sensor Status")
		self.widgets = self.buttons + self.spacing + self.other
	def back(self):
		self.ui.switch_menu('main')

	def hide_widgets(self):
		for widget in self.widgets:
			widget.grid_remove()

	def show_widgets(self):
		self.ui.lock_grid()
		self.ui.unlock_row(1)
		self.ui.unlock_col(2)
		for widget in self.widgets:
			widget.grid()