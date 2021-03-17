# -*- coding: utf-8 -*-

import os
import json
import tkinter.filedialog as fd
from pathlib import Path
from configparser import ConfigParser


configs = ConfigParser()
configs.read('config.ini')
base_folder = configs.get('Folders', 'Translator Folder')
mods_folder = configs.get('Folders', 'Translator Folder')+"\\mods"
string_folder = configs.get('Folders', 'Translator Folder')+"\\strings\\"
ignorable = {
    "ascii_art",
    "ammo_effect",
    "behavior",
    "butchery_requirement",
    "charge_removal_blacklist",
    "city_building",
    "colordef",
    "disease_type",
    "emit",
    "enchantment",
    "event_transformation",
    "EXTERNAL_OPTION",
    "hit_range",
    "ITEM_BLACKLIST",
    "item_group",
    "MIGRATION",
    "mod_tileset",
    "monster_adjustment",
    "MONSTER_BLACKLIST",
    "MONSTER_FACTION",
    "monstergroup",
    "MONSTER_WHITELIST",
    "mutation_type",
    "obsolete_terrain",
    "overlay_order",
    "overmap_connection",
    "overmap_location",
    "overmap_special",
    "profession_item_substitutions",
    "region_overlay",
    "region_settings",
    "relic_procgen_data",
    "requirement",
    "rotatable_symbol",
    "SCENARIO_BLACKLIST",
    "scent_type",
    "score",
    "skill_boost",
    "TRAIT_BLACKLIST",
    "trait_group",
    "uncraft",
    "vehicle_group",
    "vehicle_placement",
}

names = []
desc  = []
key_words = ["[Names]","[Descriptions]"]
temp_list = []
x = 0
####### Extractor functions ######

def extractor (path, mod):
	for root, dirs, files in os.walk(path):
		for _file in files:

			file =_file[ : _file.find(".json") - 0]
			if file not in ignorable:

				string_f =  root.replace( "\\mods\\","\\strings\\")
				if os.path.isfile(string_f+"\\"+file+".txt") == True:
					print(f"{file.title()}'s strings have aleady extracted")

				else:
					if _file.endswith(".json"):
						objects = open_file(root+"\\"+_file)

						check = False
						names = []
						desc = []
						comment = []
						mo_mess = []

						for item in objects:
							tags = item.keys()

							if 'name' in tags:
								names.append(item['name'])
								check = True

							if 'description' in tags:
								if '\n' in item['description']:
									item['description'] =  item['description'].replace('\n','\\n')
								desc.append(item['description'])
								check = True

							elif 'desc' in tags:
								if '\n' in item['desc']:
									item['desc'] =  item['desc'].replace('\n','\\n')
								desc.append(item['desc'])
								check = True

							if '//' in tags:
								comment.append(item['//'])
								check = True

						if check:
							new_root = root.replace("\\mods\\","\\strings\\")
							file_path = new_root+"\\"+file+".txt"

							if not os.path.exists(new_root):
								os.makedirs(new_root)

							writer(file, file_path, names, desc, comment, mo_mess)
							print(f"Strings from {file} succefuly extracted")
	print("DONE")


def open_file(file):
	with open (file,'r',encoding = 'utf-8') as t:
		text = t.read()
	objects = json.loads(text)
	return objects

def writer (file, path, names, desc, comment, mo_mess):
	with open(path,"w+",encoding = 'utf-8') as file:
	
		### Names ###
		if len(names) != 0: 
			file.write("[Names]"+"\n")
			for name in names:
				if type(name) == dict:
					for item in name.values():
						file.write(item + "\n")
				elif type(name) == list:
					file.write("".join(str(x) for x in name)+"\n") 

				else:
					file.write(name + '\n')
			file.write("\n")

		### Descriptions ###
		if len(desc) != 0: 
			file.write("[Descriptions]"+"\n")
			for item in desc:
				if type(item) == list:
					file.write("".join(str(x) for x in item)+"\n") 
				else:
					file.write(item +"\n")
			file.write("\n")

		### Comments ###
		if len(comment) != 0:
			file.write("[Comments]"+"\n")
			for item in comment:
				file.write(item+"\n")
			file.write("\n")

####### Replacer functions ######

def replacer(path, str_path, mod):
	for root, dirs, files in os.walk(str_path+ "\\" +mod):
		for file in files: 
			list_converter(root+"\\"+file, 0)

			print(file)
			new_root = root.replace("\\strings\\", "\\mods\\")
			filename = new_root+"\\" + file.replace(".txt", ".json")

			objects = open_file(filename)
			global temp_list

			for item in objects:
				for key, value in item.items():

					if key == "name":
						if type(value) == list:
							temp_list.append(names)
							item[key] = temp_list.pop(0)

						elif type(value) == dict:
							new_dict = item['name']
							for key, value in item['name'].items():
								value = names.pop(0)
								new_dict[key] = value

						else:
							item[key] = names.pop(0)
					if key == "desc":
						if type(value) == list:
							temp_list.append(desc)
							item[key] = temp_list.pop(0)
						else:
							item[key]  = desc.pop(0)
					if key == "description":
						item[key]  = desc.pop(0)

			translated_root = root.replace("\\strings\\","\\translated\\")
			f_filename = translated_root+"\\"+ file.replace(".txt", ".json")

			if not os.path.exists(translated_root):
				os.makedirs(translated_root)
			
			with open (f_filename, 'w', encoding = 'utf-8' ) as text:
				print("[", file =text)
				count_1 = len(objects)

				for record in objects:
					print('  {', file = text)
					count_1 -= 1
					count_m = len(record)

					for key, value in record.items():
						count_m -= 1
						text.write(f'    "{key}": ')

						if type(value) == bool:
							text.write(is_bool(value))
						elif type(value) == str:
							text.write(is_str(value))
						elif type(value) == int:
							text.write(f'{value}')
						elif type(value) == dict or type(value) == list:
							text.write(is_list_dict(value))
						if count_m != 0:
							text.write(',')

						text.write(f"\n")
					text.write ('  }')
					if count_1 != 0:
						text.write (',\n')
				print(f"\n]", file = text)

def list_converter (file, index):
	with open (file, 'r', encoding = 'utf-8') as f:
		strings = f.read().splitlines()
		strings = [x for x in strings if x]

		global names
		names = []
		global desc
		desc  = []

		for x in strings:
			if x == "[Names]":
				index = list_writer(names, strings, index)

			if x == "[Descriptions]":
				index = list_writer(desc, strings, index)

def open_file(file):
	with open (file,'r',encoding = 'utf-8') as t:
		text = t.read()
	objects = json.loads(text)
	return objects

def list_writer(e_list, strings, index):
	for item in strings[1+index:]:
		index += 1	
		if item in key_words:
			break
		else:
			e_list.append(item)
	return index

def format_check( e_list, temp_list):
	temp_list.clear()
	temp_list.append(e_list.pop(0))

	return temp_list

### Formating functions ###

def is_str(value):
	if '"' in value:
		value = value.replace('"','\\"')
	new_string = '"' + value +'"'
	return new_string

def is_bool(value):
	new_value = str(value)
	return(new_value.lower())

def is_list_dict(value):
	new_string = str(value)
	new_string = new_string.replace("'", '"')
	new_string = new_string.replace('"s ',"'s ")
	new_string = new_string.replace('["', '[ "')
	new_string = new_string.replace('"]', '" ]')
	new_string = new_string.replace('{"', '{ "')
	new_string = new_string.replace('}', ' }')


	if "False"in new_string:
		new_string = new_string.replace('False',"false")

	return new_string

extractor(mods_folder, 'No-Hope-master')