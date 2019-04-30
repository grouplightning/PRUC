from tkinter import Tk, Label, Button, PhotoImage, END, N, S, E, W, filedialog
import configparser


class ExportMenu:
	def __init__(self, ui):
		self.ui=ui

		self.sensors={}
		self.widgets=[]

		#ui.create_image_button(self.widgets,image=ui.menu_back_icon,row=0,column=0,command=ui.back)
		ui.create_menu_option(self.widgets,row=0,command=ui.back,text="Back",back=True)
		ui.create_text(self.widgets,row=0,column=3,text="Export & Clear")

		ui.create_text(self.widgets,row=2,column=0,text="0")#display column layout debugging
		ui.create_text(self.widgets,row=2,column=1,text="1")
		ui.create_text(self.widgets,row=2,column=2,text="2")
		ui.create_text(self.widgets,row=2,column=3,text="3")
		ui.create_text(self.widgets,row=2,column=4,text="4")
		ui.create_text(self.widgets,row=2,column=5,text="5")

		#filedialog.asksaveasfilename(initialdir="/", title="Export Counter CSV",filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))

		ui.create_text_button(self.widgets,row=3,column=3,command=self.export_sensors,text="Export Sensor List ...", styled=True, sticky=E+W)
		ui.create_text_button(self.widgets,row=4,column=3,command=self.export_counts,text="Export Count Records ...", styled=True, sticky=E+W)
		ui.create_text(self.widgets,row=5,column=0,text="")#spacer
		ui.create_text_button(self.widgets,row=7,column=3,command=self.drop_counts,text="Clear Count Records", styled=True, sticky=E+W)
		#v.set("TEST")

		#self.listbox.insert(END, "a list entry das asdjasd laskdjlas asdjkals sadjlasd asd")
		#self.listbox.grid(column=x, row=y, sticky=N + S + E + W)


		#ui.create_menu_option(self.buttons,row=2,command=self.hide_widgets,text="View Hub Status")
		#ui.create_menu_option(self.buttons,row=3,command=self.hide_widgets,text="View Sensor Status")
	def drop_counts(self):
		try:
			self.ui.db.dropCounts()
		except Exception as e:
			print("could not drop counts")
			print(e)
	def export_counts(self):
		try:
			filename = filedialog.asksaveasfilename(initialdir="/", title="Export Counts CSV", filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
			if not filename.lower().endswith('.csv'):
				filename += '.csv'
			print("selected file: "+filename)
			with open(filename, 'w') as the_file:
				results = self.ui.db.query("SELECT id,sensor,time,count_people,count_horses,count_dogs,count_vehicles,count_bicycles,count_unknown FROM counts")
				the_file.write('ip,name\n')
				for row in results:
					idn,sensor,time,count_people,count_horses,count_dogs,count_vehicles,count_bicycles,count_unknown = row
					the_file.write('%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (idn,sensor,time,count_people,count_horses,count_dogs,count_vehicles,count_bicycles,count_unknown))
		except Exception as e:
			print("could not export counts")
			print(e)
	def export_sensors(self):
		try:
			filename = filedialog.asksaveasfilename(initialdir="/", title="Export Sensors CSV", filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
			if not filename.lower().endswith('.csv'):
				filename += '.csv'
			print("selected file: "+filename)
			with open(filename, 'w') as the_file:
				results = self.ui.db.query("SELECT ip,name FROM sensors")
				the_file.write('ip,name\n')
				for row in results:
					ip,name = row
					the_file.write('%s,%s\n' % (ip,name))
		except Exception as e:
			print("could not export sensors")
			print(e)


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