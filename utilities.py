# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path
from configparser import ConfigParser
import tkinter.filedialog as fd

configs = ConfigParser()
configs.read('configs.ini')
mod = configs.get('Mods', 'mod')
game_folder = configs.get('Folders', 'Game Folder')
mods_folder = configs.get('Folders', 'Translator Folder')+"\\mods"+ mod
string_folder = configs.get('Folders', 'Translator Folder')+"\\strings\\"+ mod

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
j_desc = []
start_name = []

key_words = ["[Names]","[Descriptions]", "[Job description]", "[Start Name]"]

####### Mod selection's functions #######
def select_mod():
	mod_path = fd.askdirectory()

	global mod
	mod = os.path.basename(mod_path)
	configs['Mods']['Mod'] = mod

	with open ('configs.ini', 'w') as configfiles:
		configs.write(configfiles)

####### Extractor's functions ######

def cleaning (lis):
	temp = []
	for x in lis:
		if x not in temp:
			temp.append(x)
	return temp

def get_item(item, lis, tag):
	if type(item[tag]) == dict:
		for i in item[tag].values():
			lis.append(i)

	elif type(item[tag]) == list:
		for x in item[tag]:
			if x != '':
				lis.append(x)
	else:
		if '\n' in item[tag]:
			item[tag] = item[tag].replace('\n','\\n')
		lis.append(item[tag])	
	
def get_items_tags(item, tags, names, desc, j_desc, start_name, check):
	if 'name' in tags:
		get_item(item, names, "name")
		check = True

	if 'description' in tags:
		get_item(item, desc, "description")
		check = True

	elif 'desc' in tags:
		get_item(item, desc, "desc")
		check = True

	if "job_description" in tags:
			j_desc.append(item['job_description'])
			check = True
								
	if "start_name" in tags:
			start_name.append(item['start_name'])
			check = True
	return check

def extractor (path):
		for root, dirs, files in os.walk(path):
			for _file in files:

				global names
				global desc
				global j_desc
				global start_name

				file =_file[ : _file.find(".json") - 0]
				if file not in ignorable:

					string_f =  root.replace( "\\mods\\","\\strings\\")

					if os.path.isfile(string_f+"\\"+file+".txt") == True:
						print(f"{file.title()}'s strings have aleady extracted")
					else:

					# if file == "effects":

						if _file.endswith(".json"):
							objects = open_file(root+"\\"+_file)

							check = False

							for item in objects:
								tags = item.keys()
								check = get_items_tags(item, tags, names, desc, j_desc, start_name, check)
						
							names = cleaning(names)
							desc = cleaning(desc)

							if check:
								raw_path = root.replace("\\mods\\", "\\raw\\")
								new_root = root.replace("\\mods\\","\\strings\\")

								file_path = new_root+"\\"+file+".txt"

								if not os.path.exists(raw_path):
									os.makedirs(raw_path)

								if not os.path.exists(new_root):
									os.makedirs(new_root)

								strings_writer(file, file_path, names, desc, j_desc, start_name)
								print(f"Strings from {file}.json succefuly extracted")
				names.clear()
				desc.clear()
				j_desc.clear()
				start_name.clear()
			
		print("DONE")

def open_file(file):
	with open (file,'r', encoding = 'utf-8') as t:
		text = t.read()
	objects = json.loads(text)
	return objects

def strings_writer(file, path, names, desc, j_desc, start_name):
	with open(path,"w+", encoding = 'utf-8') as file:
	
		### Names ###
		if len(names) != 0: 
			file.write("[Names]\n")
			for name in names:

				if type(name) == list:
					file.write("".join(str(x) for x in name)+"\n") 

				else:
					file.write(name + '\n')
			file.write("\n")

		### Descriptions ###
		if len(desc) != 0: 
			file.write("[Descriptions]\n")
			for item in desc:
				if type(item) == list:
					file.write("".join(str(x) for x in item)+"\n")
				elif type(item) == dict:
					for item in item.values():
						file.write(item + "\n")  
				else:
					file.write(item + "\n")
			file.write("\n")

		### Job descriptions ###
		if len(j_desc) != 0:
			file.write("[Job description]\n")
			for item in j_desc:
				file.write(item + "\n")
			file.write("\n")

		### Start names ###
		if len(start_name) != 0:
			file.write("[Start Name]\n")
			for item in start_name:
				file.write(item + "\n")
			file.write("\n")

####### Convertor's functions ######

def list_converter (file, index):
	with open (file, 'r', encoding = 'utf-8') as f:
		strings = f.read().splitlines()
		strings = [x for x in strings if x]

		for x in strings:
			if x == "[Names]":
				index = list_writer(names, strings, index)

			if x == "[Descriptions]":
				index = list_writer(desc, strings, index)

			if x == "[Job description]":
				index = list_writer(j_desc, strings, index)

			if x == "[Start Name]":
				index = list_writer(start_name, strings, index)

def list_writer(e_list, strings, index):
	for item in strings[1+index:]:
		index += 1
		if item in key_words:
			break
		else:
			e_list.append(item)
	return index

def converter (strings):
	for root, dirs, files in os.walk(strings):
		for file in files:

			new_root = root.replace("\\strings\\", "\\mods\\")
			filename = new_root+"\\" + file.replace(".txt", ".json")

			raw_root = root.replace("\\strings\\", "\\raw\\")
			raw_name = raw_root+"\\" + file.replace(".txt", ".json")
							
			if not os.path.exists(raw_root):
				os.makedirs(raw_root)

			# if file == "effects.txt":
			# 	with open (filename,'r',encoding = 'utf-8') as t:
			# 		text = json.loads(t.read())
			# 		for item in text:
			# 			tags = item.keys()
			# 			get_items_tags(item, tags, names, desc, j_desc, start_name, check = False)

			# 	dict_names = {a  : a for a in names}
			# 	dict_desc = {a  : a for a in desc}

			# 	desc.clear()
			# 	names.clear()

			# 	list_converter(root+"\\"+file, 0)

			# 	change_dict(dict_names, names, index = 0)
			# 	change_dict(dict_desc, desc, index = 0)

			# 	with open (raw_name,'w+',encoding = 'utf-8') as raw:
			# 		raw.write('[\n  {\n')
			# 		if len(dict_names) != 0:
			# 			dict_writer(raw, dict_names, "names")
			# 		if len(dict_desc) != 0:
			# 			raw.write(',\n')
			# 			dict_writer(raw, dict_desc, "descriptions")
			# 		raw.write('\n  }\n]')

			with open (filename,'r',encoding = 'utf-8') as t:
				text = json.loads(t.read())
				for item in text:
					tags = item.keys()
					get_items_tags(item, tags, names, desc, j_desc, start_name, check = False)

			dict_names = {a  : a for a in names}
			dict_desc = {a  : a for a in desc}

			desc.clear()
			names.clear()

			list_converter(root+"\\"+file, 0)

			change_dict(dict_names, names, index = 0)
			change_dict(dict_desc, desc, index = 0)


			with open (raw_name,'w+',encoding = 'utf-8') as raw:
				raw.write('[\n  {\n')
				if len(dict_names) != 0:
					dict_writer(raw, dict_names, "names")
				if len(dict_desc) != 0:
					raw.write(',\n')
					dict_writer(raw, dict_desc, "descriptions")
				raw.write('\n  }\n]')
		

			desc.clear()
			names.clear()
			print("Strings from  " + file + " were succefuly converted")

def change_dict(dic, lis, index):
	for item in dic.keys():
		dic[item] = lis[index]
		index += 1

def dict_writer(file, dic, name):
	count = len(dic)
	file.write('    "'+ name +'" : {\n')
	for eng, rus in dic.items():

		count -= 1
		file.write('        "' + eng +'" : "' + rus + '"' )
		if count != 0:
			file.write(',\n')
	file.write('\n    }')

# def replacer(path, str_path, mod):

# 			translated_root = root.replace("\\strings\\","\\translated\\")
# 			f_filename = translated_root+"\\"+ file.replace(".txt", ".json")

# 			if not os.path.exists(translated_root):
# 				os.makedirs(translated_root)
			
# 			### Запись файла ###
# 			with open (f_filename, 'w', encoding = 'utf-8' ) as text:
# 				print("[", file =text)
# 				count_1 = len(objects)

# 				for record in objects:
# 					print('  {', file = text)
# 					count_1 -= 1
# 					count_m = len(record)

# 					for key, value in record.items():
# 						count_m -= 1
# 						text.write(f'    "{key}": ')

# 						if type(value) == bool:
# 							text.write(is_bool(value))
# 						elif type(value) == str:
# 							text.write(is_str(value))
# 						elif type(value) == int:
# 							text.write(f'{value}')
# 						elif type(value) == dict or type(value) == list:
# 							text.write(is_list_dict(value))
# 						if count_m != 0:
# 							text.write(',')

# 						text.write(f"\n")
# 					text.write ('  }')
# 					if count_1 != 0:
# 						text.write (',\n')
# 				print(f"\n]", file = text)

# 			names.clear()
# 			desc.clear()
# 			j_desc.clear()
# 			start_name.clear()

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


	if "False" in new_string:
		new_string = new_string.replace('False',"false")
	if "True" in new_string:
		new_string = new_string.replace('True','true')

	return new_string

# print(select_mod())
# extractor(mods_folder, mod)
# replacer(mods_folder, string_folder, mod)
converter(string_folder)
