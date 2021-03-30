#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
import  tkinter.messagebox as mb
from tkinter.ttk import Button, Style, Label
import utilities as ut
import os
from configparser import ConfigParser

configs = ConfigParser()
configs.read('configs.ini')

game_folder = configs.get('Folders', 'game folder')
mods_folder = configs.get('Folders', 'mod folder')
translator_folder = configs.get('Folders', 'translator folder')


if translator_folder != os.path.dirname(os.path.abspath(__file__)):
	trans_path = os.path.dirname(os.path.abspath(__file__))
	configs['Folders']["translator folder"] = trans_path
	with open ('configs.ini', 'w') as configfiles:
		configs.write(configfiles)	
	translator_folder = configs.get('Folders', 'translator folder')

class Translator(tk.Frame):
	
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, background="#334")   
		self.parent = parent
		self.name = 'name'
		self.parent.title("CDDA Translator")
		self.text = tk.StringVar()
		self.text.set("Current mod: "+ configs.get('Mods', 'mod'))
		self.pack(fill=tk.BOTH, expand=1)
		self.centerWindow()

		btn_file = Button(self, text="Select mod",command=self.select_mod)
		btn_file.place(x=5, y=10)	

		btn_replace = Button(self, text='Convert strings',command=self.converter)
		btn_replace.place(x=173,y=10)

		btn_settings = Button(self, text='Extract strings',command=self.extractor)
		btn_settings.place(x=85,y=10)

		dynlabel = Label(self, textvariable = self.text)
		dynlabel.place (x = 0, y = 130)

	def centerWindow(self):
		w = 267
		h = 150

		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()

		x = (sw-w)/2
		y = (sh-h)/2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

	def select_mod(self):
		ut.select_mod(configs)
		self.text.set("Current mod: " + configs.get('Mods', 'mod'))

	def converter(self):
		if configs.get('Mods', 'mod') == "NONE":
			print("Сначала выберите мод")
		else: 
			ut.converter(translator_folder+"\\strings\\"+ configs.get('Mods', 'mod'))

	def extractor(self):
		if configs.get('Mods', 'mod') == "NONE" or configs.get('Mods', 'mod') == "":
			print("Сначала выберите мод")
		else:
			ut.extractor(configs.get('Folders', 'mod folder'), configs.get('Mods', 'mod'))

def main():
	root = tk.Tk()
	app = Translator(root)
	root.iconbitmap('icon.ico')
	root.mainloop()

		
if __name__ == '__main__':
	main()