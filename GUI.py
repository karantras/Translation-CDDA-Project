#!/usr/bin/python
# -*- coding: utf-8 -*-

from pathlib import Path
from tkinter import Tk, Frame, BOTH, messagebox
from tkinter.ttk import Button,Style
import tkinter.filedialog as fd
import os
import json
import utilities as ut

folder = 'NONE'
file = "NONE"
objects = []

class Translator(Frame):
	
	def __init__(self, parent):
		Frame.__init__(self, parent, background="dark grey")   
		self.parent = parent
		self.name = 'name'
		self.parent.title("CDDA Translator")
		self.pack(fill=BOTH, expand=1)
		self.centerWindow()

		btn_file = Button(self, text="Select file",command=self.select_file)
		btn_file.place(x=5, y=270)	

		btn_replace = Button(self, text='Replace text',command=self.replacer)
		btn_replace.place(x=85,y=270)

	def select_file(self):
		global file
		file = get_file()

		response =  messagebox.askyesnocancel('Запись файла', 'Перезаписать файл?')
		if response == False:
			print('Joppa')
		elif response == True:
			global folder
			folder = ut.creating_folder(file)

			global objects
			objects = ut.open_file(file)

			names = open(folder+'\\names.txt','w')
			descriptions = open(folder+'\\description.txt','w')
			comments = open(folder+'\\comments.txt','w')
			mo_mess = open(folder+'\\mo_mes.txt','w')

			
	def extractor(self):
		for item in objects:
			tags = item.keys()
			if 'name' in tags:
				ut.get_names(item, names)
			if 'description' in tags:
				ut.get_desctiption(item, descriptions)
			if '//' in tags:
				ut.get_comments(item, comments)
			if 'special_attacks' in tags:
				ut.get_mo_mes(item['special_attacks'], mo_mess)

	def replacer(self):
		if file == 'NONE':
			print('You must select a file first.')
		else:
			with open(folder+'\\names.txt',"r", encoding = 'utf-8') as n:
				names = n.read().splitlines()
			with open(folder+'\\description.txt', "r", encoding = 'utf-8') as n:
				descriptions = n.read().splitlines()
			with open(folder+'\\comments.txt',  "r", encoding = 'utf-8') as n:
				comments = n.read().splitlines()

			for item in objects:
				tags = item.keys()
				if 'name' in tags:
					if type(item['name']) == dict:
						new_dict = item['name']
						for key, value in item['name'].items():
							value = names.pop(0)
							new_dict[key] = value
					else:
						item['name'] = names.pop(0)
				if 'description' in tags:
					item['description'] = descriptions.pop(0)
				if '//' in tags:
					item['//'] = comments.pop(0)

			with open(ut.file_name('translated', file), 'w', encoding = 'utf-8' ) as text:
				print ('[',  file = text)
				count_1 = len(objects)
				for record in objects:
					count_1 -= 1
					print('  {', file = text)
					count = len(record)
					for key, value in record.items():
						count -= 1
						text.write(f'    "{key}": ')
						if type(value) == bool:
							text.write(ut.is_bool(value))
						if type(value) == str:
							text.write(ut.is_str(value))
						elif type(value) == int:
							text.write(f'{value}')
						elif type(value) == dict or type(value) == list:
							text.write(ut.is_list_dict(value))
						if count != 0:
							text.write(',')

						text.write(f"\n")
					text.write ('  }')
					if count_1 != 0:
						text.write (',\n')
				print ('\n]',  file = text)

	def formating(self):
		y = 0


	def centerWindow(self):
		w = 300
		h = 300

		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()

		x = (sw-w)/2
		y = (sh-h)/2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

def main():
	root = Tk()
	app = Translator(root)
	root.mainloop()  

def get_file():
	filetypes = (("json files", "*.json"),("all files", "*"))
	filename = fd.askopenfilename(title="Select file", initialdir= Path.cwd()/'mod', filetypes=filetypes)
	if filename:
		file = os.path.basename(filename)
		return file
		
if __name__ == '__main__':
	main()