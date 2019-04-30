from tkinter import Tk, Label, Button, PhotoImage, E,W

import shutil

class StatusMenu:
	def __init__(self, ui):
		self.ui=ui

		self.widgets = []

		ui.create_menu_option(self.widgets, row=0, command=ui.back, text="Back", back=True)
		ui.create_text(self.widgets,row=0, column=3, text="System Info")

		ui.create_text(self.widgets,row=1, column=2, text="Total Count records: ",sticky=E)
		self.count_records = ui.create_input(self.widgets, row=1, column=3, sticky=E + W)

		ui.create_text(self.widgets,row=2, column=2, text="Hub Disk Usage: ",sticky=E)
		self.disk_usage = ui.create_input(self.widgets, row=2, column=3, sticky=E + W)

		self.count_records.set("populating...")
		self.disk_usage.set("populating...")

	def populate_info(self):
		self.populate_counts()
		self.populate_usage()

	def populate_usage(self):
		try:
			total, used, free = shutil.disk_usage("\\")

			print("Total: %d GB" % (total // (2 ** 30)))
			print("Used: %d GB" % (used // (2 ** 30)))
			print("Free: %d GB" % (free // (2 ** 30)))

			total = (total // (2 ** 30))
			free = (free // (2 ** 30))

			self.disk_usage.set(str(free)+" / "+str(total)+" GB Free")
		except Exception as e:
			print("could not populate info")
			print(e)
			self.disk_usage.set("Error")


	def populate_counts(self):
		try:
			results = self.ui.db.query("SELECT COUNT(*) FROM counts")
			for row in results:
				self.count_records.set(str(row))
		except Exception as e:
			print("could not populate info")
			print(e)
			self.count_records.set("Error")

	def back(self):
		self.ui.switch_menu('main')

	def hide_widgets(self):
		for widget in self.widgets:
			widget.grid_remove()

	def show_widgets(self):
		self.ui.lock_grid()
		self.ui.unlock_col(3)
		for widget in self.widgets:
			widget.grid()
		self.populate_info()