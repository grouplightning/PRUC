from tkinter import Tk, Label, Button, PhotoImage, END, N, S, E, W
import configparser


class SensorMenu:
	def __init__(self, ui):
		self.ui=ui

		self.sensors={}
		self.widgets=[]

		#ui.create_image_button(self.widgets,image=ui.menu_back_icon,row=0,column=0,command=ui.back)
		ui.create_menu_option(self.widgets,row=0,command=ui.back,text="Back",back=True)
		ui.create_text(self.widgets,row=0,column=4,text="Sensors")
		self.listbox = ui.create_listbox(self.widgets, row=1, column=2, sticky=N+S+E+W)

		ui.create_text(self.widgets,row=2,column=0,text="0")#display column layout debugging
		ui.create_text(self.widgets,row=2,column=1,text="1")
		ui.create_text(self.widgets,row=2,column=2,text="2")
		ui.create_text(self.widgets,row=2,column=3,text="3")
		ui.create_text(self.widgets,row=2,column=4,text="4")
		ui.create_text(self.widgets,row=2,column=5,text="5")

		ui.create_text_button(self.widgets,row=3,column=4,command=self.delete_selected_sensor,text="Remove sensor", styled=True)
		ui.create_text(self.widgets,row=4,column=0,text="")#spacer
		ui.create_text(self.widgets,row=5,column=2,text="Sensor IP:", sticky=E)
		ui.create_text(self.widgets,row=6,column=2,text="Sensor Name:", sticky=E)

		self.ip_input=ui.create_input(self.widgets,row=5,column=3, sticky=E+W)
		self.ip_input=ui.create_input(self.widgets,row=6,column=3, sticky=E+W)
		ui.create_text_button(self.widgets,row=6,column=4,command=ui.back,text="Add sensor", styled=True)
		#v.set("TEST")

		self.listbox.insert(END, "a list entry das asdjasd laskdjlas asdjkals sadjlasd asd")
		#self.listbox.grid(column=x, row=y, sticky=N + S + E + W)


		#ui.create_menu_option(self.buttons,row=2,command=self.hide_widgets,text="View Hub Status")
		#ui.create_menu_option(self.buttons,row=3,command=self.hide_widgets,text="View Sensor Status")
	def delete_selected_sensor(self):
		items = map(int, self.listbox.curselection())
		for item in items:
			text = self.listbox.get(item)#get text from item
			parts = text.split(" - ",4)
			try:
				id = int(parts[0])

				self.listbox.delete(item)
			except Exception as e:
				print("could not remove sensor")
				print(e)



	def add_sensor_entry(self,id,ip,name):
		self.listbox.insert(END, str(id)+" - "+str(ip)+" - "+str(name))


	def back(self):
		self.ui.switch_menu('main')

	def hide_widgets(self):
		for widget in self.widgets:
			widget.grid_remove()

	def show_widgets(self):
		self.ui.lock_grid()
		self.ui.unlock_row(1)
		self.ui.unlock_col(3)
		for widget in self.widgets:
			widget.grid()