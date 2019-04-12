from tkinter import Tk, Label, Button, PhotoImage
import configparser
import os
import subprocess


class StatusMenu:
	def __init__(self, ui):
		self.ui=ui

		self.buttons = []
		self.spacing = []


		ui.create_menu_option(self.buttons,row=1,command=ui.back,text="Back",back=True)
		ui.create_menu_option(self.buttons,row=2,command=self.hide_widgets,text="View Hub Status")
		ui.create_menu_option(self.buttons,row=3,command=self.hide_widgets,text="View Sensor Status")

		self.widgets = self.buttons
	def back(self):
		self.ui.switch_menu('main')

	def hide_widgets(self):
		for widget in self.widgets:
			widget.grid_remove()

	def show_widgets(self):
		for widget in self.widgets:
			widget.grid()