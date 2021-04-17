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
string_folder = translator_folder+"\\strings\\"+ configs.get('Mods', 'mod')

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
sounds = []
mo_mess  = []
message = []

key_tags = [names, desc, j_desc, start_name, sounds, mo_mess, message]
key_words = ["[Names]",
			"[Descriptions]",
			"[Job descriptions]",
			"[Start Names]",
			"[Sounds]",
			"[Monster massages]",
			"[Messages]"]

####### Folder selection's functions #######

def select_mod(configs = configs):
	mod_path = fd.askdirectory()

	if '/' in mod_path:
		mod_path = mod_path.replace("/","\\")

	if '%' in mod_path:
		mod_path = mod_path.replace('%', '%%')

	global mod
	mod = os.path.basename(mod_path)

	configs['Folders']['mod folder'] = mod_path
	configs['Mods']['mod'] = mod

	with open ('configs.ini', 'w') as configfiles:
		configs.write(configfiles)
		
	mod = configs.get('Mods', 'mod')
	
def clear_list():
	names.clear()
	desc.clear()
	j_desc.clear()
	start_name.clear()
	sounds.clear()
	message.clear()

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
		if '"' in item[tag]:
			item[tag] = item[tag].replace('"',"'")
		lis.append(item[tag])	
	
def get_items_tags(item, tags, key_tags, check):

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
		get_item(item, j_desc,'job_description')
		check = True
								
	if "start_name" in tags:
		start_name.append(item['start_name'])
		check = True

	if "bash" in tags:
		bash = item["bash"]
		if "sound" in bash:
			sounds.append(bash["sound"])
		if "sound_fail" in bash:
			sounds.append(bash["sound_fail"])
	if "sound" in tags:
		# if "\""
		sounds.append(item["sound"])
		check = True

	if "message" in tags:
		message = item["message"]
		if message == dict:
			for word in message.values():
				print(word)  	
	return check

def extractor (path, mod):
	if mod != 'NONE':
		existed_files = 0
		errors = 0
		count_file = 0

		for root, dirs, files in os.walk(path):
			for _file in files:

				global names
				global desc
				global j_desc
				global start_name
				global sounds
				file =_file[ : _file.find(".json") - 0]
				if file not in ignorable:
					string_f =  root.replace( "\\mods\\","\\strings\\")

					# if os.path.isfile(string_f+"\\"+file+".txt") == True:
					# 	print(f"{file.title()}'s strings have already extracted")
					# 	existed_files += 1
					if file == "gates":
						print("ops")
					# else:
						if _file.endswith(".json"):
							print(root+"\\"+_file)
							objects = open_file(root+"\\"+_file)
							check = False
							try:
								if type(objects) == str:
									tags = objects.keys()
									check = get_items_tags(objects, tags, key_tags, check)
								else:
									for item in objects:
										tags = item.keys()
										check = get_items_tags(item, tags, key_tags, check)

							except AttributeError:
								print(f"\nSome problems with {_file}\n")
								errors += 1


							names = cleaning(names)
							desc = cleaning(desc)
							sounds = cleaning(sounds)

							if check:
								user_path = root.replace("\\mods\\", "\\user\\")
								new_root = root.replace("\\mods\\","\\strings\\")

								file_path = new_root+"\\"+file+".txt"

								if not os.path.exists(user_path):
									os.makedirs(user_path)

								if not os.path.exists(new_root):
									os.makedirs(new_root)

								strings_writer(file, file_path, names, desc, j_desc, start_name)
								count_file += 1
								print(f"Strings from {file}.json successfully extracted")

						# names.clear()
						# desc.clear()
						# j_desc.clear()
						# start_name.clear()
						# sounds.clear()
						clear_list()

	print(f"Already existed files: {existed_files}")
	print(f"Total extracted files: {count_file}")
	print(f"Total errors: {errors}")

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
			file.write("[Job descriptions]\n")
			for item in j_desc:
				file.write(item + "\n")
			file.write("\n")

		### Start names ###
		if len(start_name) != 0:
			file.write("[Start Names]\n")
			for item in start_name:
				file.write(item + "\n")
			file.write("\n")

		### Sounds ###
		if len(sounds) != 0:
			file.write("[Sounds]\n")
			for item in sounds:
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

			if x == "[Job descriptions]":
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

			user_root = root.replace("\\strings\\", "\\user\\")
			user_name = user_root+"\\" + file.replace(".txt", ".json")
							
			if not os.path.exists(user_root):
				os.makedirs(user_root)

			# if file == "species.txt":
			# 	with open (filename,'r',encoding = 'utf-8') as t:
			# 		text = json.loads(t.read())
			# 		for item in text:
			# 			tags = item.keys()
			# 			get_items_tags(item, tags, key_tags, check = False)

			# 	dict_names = {a  : a for a in names}
			# 	dict_desc = {a  : a for a in desc}

			# 	desc.clear()
			# 	names.clear()

			# 	list_converter(root+"\\"+file, 0)

			# 	change_dict(dict_names, names, index = 0)
			# 	change_dict(dict_desc, desc, index = 0)

			# 	with open (user_name,'w+',encoding = 'utf-8') as user:
			# 		user.write('[\n  {\n')
			# 		if len(dict_names) != 0:
			# 			dict_writer(user, dict_names, "names")
			# 			if len(dict_desc) != 0:
			# 				user.write(',\n')

			# 		if len(dict_desc) != 0:
			# 			# user.write(',\n')
			# 			dict_writer(user, dict_desc, "descriptions")
			# 		user.write('\n  }\n]')

			try:
				with open (filename,'r',encoding = 'utf-8') as t:
					text = json.loads(t.read())

					if type(text) == dict:
						tags = text.keys()
						check = get_items_tags(text, tags, key_tags, check = False)
					else:
						for item in text:
							tags = item.keys()
							get_items_tags(item, tags, key_tags, check = False)
			except AttributeError:
				print(file)

			dict_names = {a  : a for a in names}
			dict_desc = {a  : a for a in desc}
			dict_job = {a : a for a in j_desc}

			clear_list()
			list_converter(root + "\\" + file, 0)

			change_dict(dict_names, names, index = 0)
			change_dict(dict_desc, desc, index = 0)
			change_dict(dict_job, j_desc, index = 0)

			with open (user_name,'w+',encoding = 'utf-8') as user:
				user.write('[\n  {\n')
				if len(dict_names) != 0:
					dict_writer(user, dict_names, "names")
				if len(dict_desc) != 0:
					user.write(',\n')
					dict_writer(user, dict_desc, "descriptions")
				if len(dict_job) != 0:
					user.write(',\n')
					dict_writer(user, dict_job, "job_description")
				user.write('\n  }\n]')
		
			clear_list()
			# print("Strings from " + file + " were successfully converted")

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


select_mod()
extractor(mods_folder, mod)
# replacer(mods_folder, string_folder, mod)
# converter(string_folder)
