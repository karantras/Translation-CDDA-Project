#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
import  tkinter.messagebox as mb
from tkinter.ttk import Button, Style, Label, Scrollbar
import utilities as ut
import os
import sys
from configparser import ConfigParser

configs = ConfigParser()
configs.read('configs.ini')

game_folder = configs.get('Folders', 'game folder')
mods_folder = configs.get('Folders', 'mod folder')
translator_folder = configs.get('Folders', 'translator folder')
user_folder = translator_folder+"\\user\\"+ configs.get('Mods', 'mod')

if translator_folder != os.path.dirname(os.path.abspath(__file__)):
	trans_path = os.path.dirname(os.path.abspath(__file__))
	configs['Folders']["translator folder"] = trans_path
	with open ('configs.ini', 'w') as configfiles:
		configs.write(configfiles)	
	translator_folder = configs.get('Folders', 'translator folder')

class Translator(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, background="#333333")   
		self.parent = parent
		self.name = 'name'
		self.parent.title("CDDA Translator")
		self.mod = tk.StringVar()
		self.mod.set("Current mod: "+ configs.get('Mods', 'mod'))

		modbar = tk.Frame(self, background="#424242")
		modbar.pack(side="top", fill="x")
		toolbar = tk.Frame(self, background="light grey")
		toolbar.pack(side="top", fill="y")

		self.text = tk.Text(self, wrap="word")
		self.text.pack(side="top", fill="both", expand=True)
		self.text.tag_configure("stderr", foreground="#b22222")
		scroll = Scrollbar(command=self.text.yview)
		scroll.pack(side="right", fill="y")
		self.text.config(yscrollcommand=scroll.set)


		self.pack(fill=tk.BOTH, expand=1)
		self.centerWindow()

		sys.stdout = TextRedirector(self.text, "stdout")
		sys.stderr = TextRedirector(self.text, "stderr")

		btn_file = Button(self, text="Select mod",command=self.select_mod, width = 14 )
		btn_file.pack(in_=toolbar, side="left", padx = 3, pady = 1)	

		btn_settings = Button(self, text='Extract strings',command=self.extractor, width = 14)
		btn_settings.pack(in_=toolbar, side="left", padx = 3, pady = 1)	

		btn_convert = Button(self, text='Update strings',command=self.converter, width = 14)
		btn_convert.pack(in_=toolbar, side="left", padx = 3, pady = 1)	

		dynlabel = Label(self, textvariable = self.mod, background="#424242", foreground ="#dddddd", font = "Courier 10 bold")
		dynlabel.pack(in_= modbar, side = "bottom", fill ="y", anchor=tk.NW)

	def centerWindow(self):
		w = 320
		h = 150

		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()

		x = (sw-w)/2
		y = (sh-h)/2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

	def select_mod(self):
		ut.select_mod(configs)
		self.mod.set("Current mod: " + configs.get('Mods', 'mod'))

	def converter(self):
		if configs.get('Mods', 'mod') == "NONE":
			print("Сначала выберите мод")
		else: 
			ut.updater(user_folder)

	def extractor(self):
		if configs.get('Mods', 'mod') == "NONE" or configs.get('Mods', 'mod') == "":
			print("Сначала выберите мод")
		else:
			ut.extractor(configs.get('Folders', 'mod folder'), configs.get('Mods', 'mod'))

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")


def main():
	root = tk.Tk()
	app = Translator(root)
	root.iconbitmap('icon.ico')
	root.mainloop()

		
if __name__ == '__main__':
	main()