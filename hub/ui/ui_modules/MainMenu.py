from tkinter import Tk, Label, Button, PhotoImage
import configparser
import os
import subprocess


class MainMenu:
	def __init__(self, ui):
		self.ui=ui
		#self.master = ui.master

		self.icon_a=PhotoImage(file="status.gif")
		self.icon_b=PhotoImage(file="download.gif")
		self.icon_c=PhotoImage(file="gear.gif")



		self.buttons = []
		ui.create_image_button(self.buttons,row=1,column=1,image=self.icon_a,command=self.status,text="Sensors")
		ui.create_image_button(self.buttons,row=1,column=3,image=self.icon_b,command=self.export,text="Export")
		ui.create_image_button(self.buttons,row=1,column=5,image=self.icon_c,command=self.configure,text="Configure")

		self.labels = []
		ui.create_text(self.labels, row=2, column=1, text="Sensors")
		ui.create_text(self.labels, row=2, column=3, text="Export")
		ui.create_text(self.labels, row=2, column=5, text="Configure")

		self.spacing = []
		ui.create_spacing(self.spacing, 0, 0)
		ui.create_spacing(self.spacing, 3, 0)
		ui.create_spacing(self.spacing, 1, 2)
		ui.create_spacing(self.spacing, 1, 4)
		ui.create_spacing(self.spacing, 1, 6)

		self.widgets = self.buttons + self.labels + self.spacing


	def hide_widgets(self):
		for widget in self.widgets:
			widget.grid_remove()

	def show_widgets(self):
		self.ui.lock_grid()
		self.ui.unlock_row(0)
		self.ui.unlock_row(3)
		self.ui.unlock_col(0)
		self.ui.unlock_col(2)
		self.ui.unlock_col(4)
		self.ui.unlock_col(6)
		for widget in self.widgets:
			widget.grid()
	def status(self):
		print("sensors")
		self.ui.switch_menu('sensors')
	def export(self):
		print("export")
		self.ui.switch_menu('export')
	def configure(self):
		print("configure")
		self.ui.switch_menu('configure')