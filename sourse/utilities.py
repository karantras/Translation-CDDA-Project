# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path
from configparser import ConfigParser
import tkinter.filedialog as fd


# configs = ConfigParser()
# configs.read('configs.ini')

# mod = configs.get('Mods', 'mod')
# game_folder = configs.get('Folders', 'game folder')
# mods_folder = configs.get('Folders', 'mod folder')
# translator_folder = configs.get('Folders', 'translator folder')
# string_folder = translator_folder+"\\strings\\"+ configs.get('Mods', 'mod')
# user_folder = translator_folder+"\\user\\"+ configs.get('Mods', 'mod')

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
messages = []

key_tags = [names, desc, j_desc, start_name, sounds, mo_mess, messages]
key_words = ["[Names]",
			"[Descriptions]",
			"[Job_Description]",
			"[Start Names]",
			"[Sound]",
			"[Monster massages]",
			"[Messages]"]

####### Folder selection's functions #######

def select_mod(configs):
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
	messages.clear()

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

	if "messages" in tags:
		message = item["messages"]
		if type(message) == dict:
			for word in message.values():
				messages.append(word)	
		check = True
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
					string_path =  root.replace( "\\mods\\","\\strings\\")

					if os.path.isfile(string_path+"\\"+file+".txt") == True:
						print(f"{file.title()}'s strings have already extracted")
						existed_files += 1
					# if file == "species":

					else:
						if _file.endswith(".json"):
							objects = open_file(root + "\\" + _file)
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
								user_root = root.replace("\\mods\\", "\\user\\")
								string_root = root.replace("\\mods\\","\\strings\\")

								string_file = string_root + "\\" + file + ".txt"
								user_file = user_root + "\\" + file + ".json"

								if not os.path.exists(user_root):
									os.makedirs(user_root)

								if not os.path.exists(string_root):
									os.makedirs(string_root)

								with open (user_file,'w+', encoding = 'utf-8') as user:
									create_dictionary(user, key_tags)
								
								strings_writer(string_file, user_file, file)

								count_file += 1
								print(f"Strings from {file}.json successfully extracted")
						names.clear()
						desc.clear()
						j_desc.clear()
						start_name.clear()
						sounds.clear()
						messages.clear()

	print(f"Already existed files: {existed_files}")
	print(f"Total extracted files: {count_file}")
	print(f"Total errors: {errors}")

def create_dictionary(user, key_tags):

	dict_names = {a  : a for a in names}
	dict_desc = {a  : a for a in desc}
	dict_job = {a : a for a in j_desc}
	dict_sound = {a : a for a in sounds}

	check = False
	user.write('[\n  {\n')

	if len(dict_names) != 0:
		check = dict_writer(user, dict_names, "names")
		print(check)

	if len(dict_desc) != 0:
		print(check)
		checking(check, user)
		check = dict_writer(user, dict_desc, "descriptions")
		print(check)

	if len(dict_job) != 0:
		checking(check, user)
		check = dict_writer(user, dict_job, "job_description")

	if len(dict_sound) != 0:
		checking(check, user)
		check = dict_writer(user, dict_sound, "sound")
	user.write('\n  }\n]')
	
def checking(check, file):
	if check == True:
		file.write(',\n')

def dict_writer(file, dic, name):
	count = len(dic)
	file.write('    "'+ name +'" : {\n')
	for eng, rus in dic.items():

		count -= 1
		if "\n" in eng:
			eng = eng.replace('\n', "\\n") 
		if "\n" in rus:
			rus = rus.replace('\n', "\\n") 
		file.write('        "' + eng +'" : "' + rus + '"' )
		if count != 0:
			file.write(',\n')
	file.write('\n    }')
	check = True
	return check

def open_file(file):
	with open (file,'r', encoding = 'utf-8') as t:
		text = t.read()
	objects = json.loads(text)
	return objects

def strings_writer(string_path, user_string, file):
	try:
		with open (user_string, "r+", encoding = "utf-8") as user:
			text  = user.read()
			objects = json.loads(text)
	except json.decoder.JSONDecodeError:
		print(f"Проблема при извлечении строк из user {file}")
	else:
		with open(string_path,"w+", encoding = 'utf-8') as string:
				
			for obj in objects:
				for record, value in obj.items():
					string.write("[" + record.title() + "]\n")
					for item in value.values():
						string.write(item + "\n")
					string.write("\n")
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

			if x == "[Sound]":
				index = list_writer(sounds, strings, index)

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
			list_converter(root + "\\" + file, 0)

			user_root = root.replace("\\strings\\", "\\user\\")
			user_name = user_root+"\\" + file.replace(".txt", ".json")

			with open(user_name, "r+", encoding = "utf-8") as user:
				text = user.read()
				new_dict = json.loads(text)
				# print(new_dict)



			# with open()
							
			# if not os.path.exists(user_root):
			# 	os.makedirs(user_root)

			# try:
			# 	with open (filename,'r',encoding = 'utf-8') as t:
			# 		text = json.loads(t.read())

			# 		if type(text) == dict:
			# 			tags = text.keys()
			# 			check = get_items_tags(text, tags, key_tags, check = False)
			# 		else:
			# 			for item in text:
			# 				tags = item.keys()
			# 				get_items_tags(item, tags, key_tags, check = False)
			# except AttributeError:
			# 	print(file)

			# dict_names = {a  : a for a in names}
			# dict_desc = {a  : a for a in desc}
			# dict_job = {a : a for a in j_desc}
			

			# try:
			# 	change_dict(dict_names, names, index = 0)
			# 	change_dict(dict_desc, desc, index = 0)
			# 	change_dict(dict_job, j_desc, index = 0)
			# except IndexError:
			# 	print("ops")


			# with open (user_name,'w+',encoding = 'utf-8') as user:
			# 	user.write('[\n  {\n')
			# 	if len(dict_names) != 0:
			# 		dict_writer(user, dict_names, "names")
			# 	if len(dict_desc) != 0:
			# 		user.write(',\n')
			# 		dict_writer(user, dict_desc, "descriptions")
			# 	if len(dict_job) != 0:
			# 		user.write(',\n')
			# 		dict_writer(user, dict_job, "job_description")
			# 	user.write('\n  }\n]')
		
			clear_list()
			# print("Strings from " + file + " were successfully converted")

def change_dict(dic, lis, file, errors, index):
	for item in dic.keys():
		try:
			dic[item] = lis[index]
			index += 1
		except IndexError:
			print(f"Проблемы при извлечении строк из {file}.txt. Недостающие строки.")
			errors += 1

### Updater functions ###

def updater(user_folder, translated = True):
	errors = 0
	for root, dirs, files in os.walk(user_folder):
		for file in files:
			mod_file = root.replace("user", "mods") + "\\" + file
			objects = open_file(mod_file)

			#### Обновление файла ####
			with open (root + "\\" + file, "r+", encoding = "utf-8") as raw:
				text = raw.read()
				try:
					user_objects = json.loads(text)
					record = user_objects[0]
				except json.decoder.JSONDecodeError:
					print(f"Проблемы с декодированием {file}")
					errors += 1
				else:

				#### Синхронизация с текущим переводом ####
					if translated == True:
						list_converter(root.replace("user", "strings") + "\\" + file.replace("json", "txt"), 0)
						if "names" in record.keys():
							change_dict(record["names"], names, file, errors, index = 0)
						if "descriptions" in record.keys():
							change_dict(record["descriptions"], desc, file, errors, index = 0)
						if "job_description" in record.keys():
							change_dict(record["job_description"], j_desc, file, errors, index = 0)
						if "sound" in record.keys():
							change_dict(record["sound"], sounds, file, errors, index = 0)
					
					try:
						if type(objects) == str:
							tags = objects.keys()
							get_items_tags(objects, tags, key_tags, check = False)
						else:
							for item in objects:
								tags = item.keys()
								get_items_tags(item, tags, key_tags, check = False )

					except AttributeError:
						print(f"\nSome problems with {_file}\n")
						errors += 1

					#### Добавление новых тэгов ####

					### Sound ###
					if "sound" in tags and "sound" not in record.keys():
						record["sound"]  = {}
					if "bash" in tags and "sound" not in record.keys():
						bash = item["bash"]
						if "sound" in bash or "sound_fail" in bash:
							record["sound"]  = {}

					#### Добавление новых значений ####
					if "names" in record.keys():
						check_for_updates("names", record, names)
					if "descriptions" in record.keys():
						check_for_updates("descriptions", record, desc)
					if "job_description" in record.keys():
						check_for_updates("job_description", record, j_desc)
					if "sound" in record.keys():
						check_for_updates("sound", record, sounds)

					with open (root + "\\" + file, "w+", encoding = "utf-8") as user:
						user.write('[\n  {\n')
						check = False
						if "names" in record.keys() and len(record["names"]) != 0:
							check = dict_writer(user, record["names"], "names")

						if "descriptions" in record.keys() and len(record["descriptions"]) != 0:
							checking(check, user)
							check = dict_writer(user, record["descriptions"], "descriptions")

						if "job_description" in record.keys() and len(record["job_description"]) != 0:
							checking(check, user)
							check = dict_writer(user, record["job_description"], "job_description")

						if "sound" in record.keys() and len(record["sound"]) != 0:
							checking(check, user)
							check = dict_writer(user, record["sound"], "sound")

						user.write('\n  }\n]')

					strings_writer(root.replace("user", "strings") + "\\" + file.replace("json", "txt"), root +  "\\" + file, file)

			names.clear()
			desc.clear()
			j_desc.clear()
			start_name.clear()
			sounds.clear()
			messages.clear()

	print(f"Total errors: {errors}")

				
def check_for_updates(key, old_dict, new_list):
	my_dict = old_dict[key]
	value = my_dict.values()
	for item in new_list:
		if item not in my_dict.values() and item not in my_dict.keys():
			if '\n' in item:
				item = item.replace('\n', '\\n')
			my_dict[item] = item


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