#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
import  tkinter.messagebox as mb
from tkinter.ttk import Button, Style
import os
import utilities as ut

class Translator(tk.Frame):
	
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, background="#334")   
		self.parent = parent
		self.name = 'name'
		self.parent.title("CDDA Translator")
		self.pack(fill=tk.BOTH, expand=1)
		self.centerWindow()

		btn_file = Button(self, text="Select mod",command=self.select_mod)
		btn_file.place(x=5, y=10)	

		btn_replace = Button(self, text='Convert strings',command=self.replacer)
		btn_replace.place(x=173,y=10)

		btn_settings = Button(self, text='Extract strings',command=self.extractor)
		btn_settings.place(x=85,y=10)

		# logs = tk.Text(width= 35, height=  105, bg="white", fg='white')
		# logs.pack(fill=tk.left, expand=True)

	def centerWindow(self):
		w = 300
		h = 300

		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()

		x = (sw-w)/2
		y = (sh-h)/2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

	def select_mod(self):
		ut.select_mod()

	def replacer(self):
		if ut.mod == "NONE":
			print("Сначала выберите мод")
		else: 
			ut.converter( ut.string_folder)

	def extractor(self):
		if ut.mod == "NONE":
			print("Сначала выберите мод")
		else:
			ut.extractor(ut.mods_folder)

def main():
	root = tk.Tk()
	app = Translator(root)
	root.mainloop()  
		
if __name__ == '__main__':
	main()
