#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
import  tkinter.messagebox as mb
from tkinter.ttk import Button,Style
import tkinter.filedialog as fd
import os
import json
import utilities as ut

mod = 'No-Hope-master'

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

		btn_replace = Button(self, text='Replace text',command=self.replacer)
		btn_replace.place(x=173,y=10)

		btn_settings = Button(self, text='Extract strings',command=self.extractor)
		btn_settings.place(x=85,y=10)

	def centerWindow(self):
		w = 300
		h = 300

		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()

		x = (sw-w)/2
		y = (sh-h)/2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

	def select_mod(self):
		global mod
		mod_path = fd.askdirectory()
		mod = os.path.basename(mod_path)

	def replacer(self):
		if mod == "NONE":
			print("Сначала выберите мод")
		else: 
			ut.replacer(ut.mods_folder, ut.string_folder, mod)

	def extractor(self):
		if mod == "NONE":
			print("Сначала выберите мод")
		else:
			ut.extractor(ut.mods_folder, mod)

def main():
	root = tk.Tk()
	app = Translator(root)
	root.mainloop()  
		
if __name__ == '__main__':
	main()