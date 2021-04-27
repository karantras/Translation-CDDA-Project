# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
from configparser import ConfigParser
import tkinter.filedialog as fd

names = []
desc  = []
j_desc = []
start_name = []
sounds = []
mo_mess  = []
messages = []
attacks = []


# configs = ConfigParser()
# configs.read('configs.ini')

# mod = configs.get('Mods', 'mod')
# game_folder = configs.get('Folders', 'game folder')
# translator_folder = configs.get('Folders', 'translator folder')
# mods_folder = configs.get('Folders', 'mod folder')
# string_folder = translator_folder+"\\strings\\"+ configs.get('Mods', 'mod')
# user_folder = translator_folder+"\\user\\"+ configs.get('Mods', 'mod')

### Replacer's functions ###
def open_file(file):
	with open (file,'r', encoding = 'utf-8') as t:
		text = t.read()
	objects = json.loads(text)
	return objects
	
def replacer(user_path, mod_path, mod):
	for root, dirs, files in os.walk(user_path):
		for file in files:	
			### Временная функция для того, чтобы не переписывать файлы игры ###
			new_root = (mod.join(root.split(mod)[-1:]))
			base_file = mod_path + "\\" + new_root + "\\" + file
			user_file = root + "\\" + file

			global names
			global desc
			global j_desc
			global start_name
			global sounds
			global messages
			global attacks

			if file != ".json":
				try:
					user_objects = open_file(user_file)[0]
					base_objects = open_file(base_file)

				except json.decoder.JSONDecodeError:
					print(f"{file} has some problems")
				else:
					if "names" in user_objects.keys():
						names = user_objects["names"]

					if "descriptions" in user_objects.keys():
						desc = user_objects["descriptions"]

					if "job_description" in user_objects.keys():
						j_desc = user_objects["job_description"]

					if "start_name" in user_objects.keys():
						start_name = user_objects["start_name"]
				
					if "sound" in user_objects.keys():
						sounds = user_objects["sound"]

					if "messages" in user_objects.keys():
						messages = user_objects["messages"]

					if "attacks" in user_objects.keys():
						attacks = user_objects["attacks"]

					### Replacer part (Will add new tags)### 
					for objects in base_objects:
						for key, item in objects.items():
							try:
								if key == "name":
									minor_rep(objects, item, key, names)

								if key == "description":
									minor_rep(objects, item, key, desc)
								if key == "desc":
									minor_rep(objects, item, key, desc)

								if key == "job_description":
									minor_rep(objects, item, key, j_desc)
							except KeyError:
								print(f"Errno3 - missing key. Key {item} doesn't exist in user {file}.")

							if key == "sound":
								minor_rep(objects, item, key, sounds)

							if ((key == "messages")	or 
							   (key == "mutagen_message") or
							   (key == "memorial_message") or
							   (key == "iv_message")):
								minor_rep(objects, item, key, messages)

							if key == "spawn_item" and "message" in item:
								minor_rep(item, item["message"], "message", messages)

							if  key == "use_action" and "msg" in item:
								minor_rep(item, item["msg"], "msg", messages)

							if key == "attacks":
								if type(item) == list:
									item = item[0]
								if "attack_text_npc" in item.keys():
									minor_rep(item, item["attack_text_npc"], "attack_text_npc", attacks)
														
					### Write new json part
					final_folder = root.replace("user","translated")
					if not os.path.exists(final_folder):
						os.makedirs(final_folder)
					with open (final_folder + "\\" + file, "w", encoding = "utf-8") as file:
						print("[", file = file)
						count = len(base_objects)
						for record in base_objects:
							print('  {', file = file)
							count -= 1
							m_count  = len(record)
							for key, value in record.items():
								m_count -= 1
								x = 4
								value = req_new(value, x)
								value = final_check(value, x)
								file.write(x*' '+'"' + key + '" : '+ value)
								if m_count > 0:
									file.write(",")
								file.write ('\n')    
							file.write ('  }')
							if count != 0:
								file.write (',\n')
						print(f"\n]", file = file)		

			names.clear()
			desc.clear()				


def minor_rep(objects, item, key, user_objects):
	if type(item) == dict:
		for key, value in item.items():
			item[key] = user_objects[value]
	elif type(item) == list:
		x = 0
		for value in item:
			item[x] = user_objects[value]
			x += 1
	else:
		objects[key] = user_objects[item]

### Formating functions ###
def clear_sym(string):
	string = string
	### Проверка спецсимвола \n ###
	if "\n" in string:
		string = string.replace("\n", "\\n")

	#### Проверка на наличие прямой речи  ####
	if '\"' in string:
		string = string.replace("\"", '\\"')
		
	return string

def req_new(value, x, string = "", key = ""):
	### Конечные случаи ###
	if type(value) == int or type(value) == float:
		value = str(value)
	elif type(value) == bool:
		value = str(value).lower()
	elif type(value) == str:
		value = '"' + clear_sym(value) + '"' #### Проверка на наличие спецсимволов (Необходимо только для строк)

	### Комплексные структуры ###
	elif type(value) == list or type(value) == dict:
		x += 2
		count = len(value)
		### Определение длины структуры
		if len(str(value)) >= 100:
			string_type = "long"
		else: 
			string_type = "short"

		### Распаковка списка ###
		if type(value) == list:
			string = ""
			for item in value:
				count -= 1			
				if string_type == "short":
					value_new = req_new(item, x)
					if count > 0:
						value_new += ", "

				elif string_type == "long":
					value_new = x*" " + req_new(item, x)
					if count > 0:
						value_new += ',\n'
					else:
						value_new += '\n'
				string += value_new
			value = '[' + string + ']'

		### Распаковка словаря ###		
		if type(value) == dict:
			string = ""
			for key, item in value.items():
				count -= 1
				if string_type == "short":
					value_new = req_new(item, x)
					value_new = '"' + key + '" : ' + value_new + "" 
					if count > 0:
						value_new += ", "

				elif string_type == "long":
					value_new = req_new(item, x)
					value_new = x*" " + '"' + key + '" : ' + value_new 
					if count > 0:
						value_new += ',\n'
					else:
						value_new += '\n'
				string += value_new
			value = "{" + string + "}"
		x -= 2
	return value

def final_check(string, x):
	if '[      ["' in string:
		string = string.replace('[      ["', '[\n      ["')
	if '[      "' in string:
		string = string.replace('[      "', '[\n      "')
	if '\n]'in string:
		string = string.replace('\n]', '\n    ]')

	if '{      {"' in string:
		string = string.replace('{      {"', '{\n      {"')
	if '{      "' in string:
		string = string.replace('{      "', '{\n      "')
	if '\n}'in string:
		string = string.replace('\n}', '\n    }')
	return string

# replacer(user_folder, mods_folder)