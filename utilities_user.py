# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
from configparser import ConfigParser
import tkinter.filedialog as fd

configs = ConfigParser()
configs.read('configs.ini')

mod = configs.get('Mods', 'mod')
game_folder = configs.get('Folders', 'game folder')
mods_folder = configs.get('Folders', 'mod folder')
translator_folder = configs.get('Folders', 'translator folder')
string_folder = translator_folder+"\\strings\\"+ mod
user_folder = translator_folder+"\\user\\"+ mod

### Replacer's functions ###
def open_file(file):
	with open (file,'r', encoding = 'utf-8') as t:
		text = t.read()
	objects = json.loads(text)
	return objects

def replacer(user_path, mod_path):
	print(user_path)
	for root, dirs, files in os.walk(user_path):
		for file in files:
			print(file)
			base_file = mod_path + "\\" + file.replace(".txt", ".json")
			user_file = user_path + "\\" + file

			user_objects = open_file(user_file)
			base_objects = open_file(base_file)

			if file == "scenarios":
				for item in base_objects:
					print(item)
			### Исходный json ###

			


			### Временная функция для того, чтобы не переписывать файлы игры ###
			translated_path = root.replace("\\user\\","\\translated\\")
			f_filename = translated_root + "\\" + file.replace(".txt", ".json")

			if not os.path.exists(translated_path):
				os.makedirs(translated_path)
			
			# with open(f_filename, 'w', encoding = 'utf-8') as text:


replacer(user_folder, mods_folder)