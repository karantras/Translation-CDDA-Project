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
def replacer(user_path, mod_path):
	for root, dirs, files in os.walk(user_path):
		for file in files:

			### Временная функция для того, чтобы не переписывать файлы игры ###
			translated_path = root.replace("\\user\\","\\translated\\")

			if not os.path.exists(translated_path):
				os.makedirs(translated_path)

replacer(user_folder, mods_folder)