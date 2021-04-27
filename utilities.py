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
# translator_folder = configs.get('Folders', 'translator folder')
# mods_folder = configs.get('Folders', 'mod folder')
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
messages = []
message_key = ["not_ready_msg", "msg", "need_charges_msg", "need_fire_msg", "sound_msg", "no_deactivate_msg","menu_text"]
attacks = []
buffes = []
buffes_key = ["static_buffs", "onmove_buffs", "onmiss_buffs", "onattack_buffs", "onblock_buffs", "ondodge_buffs", "onpause_buffs"]

key_tags = [names, desc, j_desc, start_name, sounds, messages, attacks, buffes]
key_words = ["[Names]",
			"[Descriptions]",
			"[Job_Description]",
			"[Start Names]",
			"[Sound]",
			"[Monster massages]",
			"[Messages]",
			"[Attacks]",
			"[Buffes]"]

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
	if 'intensity_levels' in tags and "name" in item["intensity_levels"][0]:
		get_item(item["intensity_levels"][0], names, "name")
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
		sounds.append(item["sound"])
		check = True

	if "messages" in tags:
		get_item(item, messages,"messages")
		check = True
	if "mutagen_message" in tags:
		get_item(item, messages,"mutagen_message")
		check = True
	if "iv_message" in tags:
		get_item(item, messages,"iv_message")
		check = True
	if "memorial_message" in tags:
		get_item(item, messages,"memorial_message")
		check = True
		
	if "use_action" in tags and "not_ready_msg" in item["use_action"]:
		get_item(item["use_action"], messages,"not_ready_msg")

	if "use_action" in tags and "msg" in item["use_action"]:
		get_item(item["use_action"], messages,"msg")

	if "use_action" in tags and "need_charges_msg" in item["use_action"]:
		get_item(item["use_action"], messages,"need_charges_msg")

	if "use_action" in tags and "need_fire_msg" in item["use_action"]:
		get_item(item["use_action"], messages,"need_fire_msg")

	if "miss_messages" in tags:
		for i in item["miss_messages"]:
			for x in i:
				if type(x) == str:
					messages.append(x)

	if "spawn_item" in tags and "message" in item["spawn_item"]:
		message = item["spawn_item"]
		messages.append(message["message"])
		check = True

	if "attacks" in tags:
		attack = item["attacks"]
		if type(attack) == list:
			attack = attack[0]
		if "attack_text_u" in attack:
			attacks.append(attack["attack_text_u"])
		if "attack_text_npc" in attack:
			attacks.append(attack["attack_text_npc"])
		check = True

	for key in buffes_key:
		if key in tags:
			buff =  unpack_list(item[key])
			if "name" in buff:
				get_item(buff, buffes, "name")
			if "description" in buff:
				get_item(buff, buffes, "description")
			check = True

	return check

def unpack_list(my_list):
	if len (my_list) == 1 and type(my_list) == list:
		return my_list[0]
	else:
		return my_list

def extractor (path, mod, translator_folder):
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
				global messages
				global attacks
				global buffes
				file =_file[ : _file.find(".json") - 0]
				if file not in ignorable:
					new_root = mod + (mod.join(root.split(mod)[-1:]))

					user_root = translator_folder + "\\user\\" + new_root
					user_file = user_root + "\\" + file + ".json"

					string_root = translator_folder + "\\strings\\" + new_root
					string_file = string_root + "\\" + file + ".txt"

					if os.path.isfile(user_file) == True:
						print(f"{file.title()}'s strings have already extracted")
						existed_files += 1
					else:
					# if file == "effect":

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
							messages = cleaning(messages)
							attacks = cleaning(attacks)
							buffes = cleaning(buffes)
							if check:
								if not os.path.exists(user_root):
									os.makedirs(user_root)

								if not os.path.exists(string_root):
									os.makedirs(string_root)

								with open (user_file,'w+', encoding = 'utf-8') as user:
									create_dictionary(user, key_tags)
								
								strings_writer(string_file, user_file, file, update = False)
								count_file += 1
								
						names.clear()
						desc.clear()
						j_desc.clear()
						start_name.clear()
						sounds.clear()
						messages.clear()
						attacks.clear()
						buffes.clear()

	print(f"Already existed files: {existed_files}")
	print(f"Total extracted files: {count_file}")
	print(f"Total errors: {errors}")

def create_dictionary(user, key_tags):

	dict_names = {a  : a for a in names}
	dict_desc = {a  : a for a in desc}
	dict_job = {a : a for a in j_desc}
	dict_sound = {a : a for a in sounds}
	dict_start = {a : a for a in start_name}
	dict_mess = {a : a for a in messages}
	dict_atta = {a : a for a in attacks}
	dict_buff = {a: a for a in buffes}

	check = False
	user.write('[\n  {\n')

	if len(dict_names) != 0:
		check = dict_writer(user, dict_names, "names")

	if len(dict_desc) != 0:
		checking(check, user)
		check = dict_writer(user, dict_desc, "descriptions")

	if len(dict_job) != 0:
		checking(check, user)
		check = dict_writer(user, dict_job, "job_description")

	if len(dict_start) != 0:
		checking(check, user)
		check  = dict_writer(user, dict_start, "start_name")

	if len(dict_sound) != 0:
		checking(check, user)
		check = dict_writer(user, dict_sound, "sound")
		
	if len(dict_mess) != 0:
		checking(check, user)
		check = dict_writer(user, dict_mess, "messages")

	if len(dict_atta) != 0:
		checking(check, user)
		check = dict_writer(user, dict_atta, "attacks")
	if len(dict_buff) != 0:
		checking(check, user)
		check = dict_writer(user, dict_buff, "buffes")
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
		if '\"' in eng:
			eng = eng.replace('\"', '\\"')

		if "\n" in rus:
			rus = rus.replace('\n', "\\n") 
		if '\"' in rus:
			rus = rus.replace('\"', '\\"')
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

def strings_writer(string_path, user_string, file, update):
	try:
		with open (user_string, "r+", encoding = "utf-8") as user:
			text  = user.read()
			objects = json.loads(text)
	except json.decoder.JSONDecodeError:
		print(f"Проблема при извлечении строк из user {file}. Проверьте целостность {file}.json")
	else:
		with open(string_path,"w+", encoding = 'utf-8') as string:
				
			for obj in objects:
				for record, value in obj.items():
					string.write("[" + record.title() + "]\n")
					for item in value.values():
						if "\n" in item:
							item = item.replace("\n","\\n")
						string.write(item + "\n")
					string.write("\n")

		if update == False:
			print(f"Strings from {file}.json successfully extracted")
		else:
			print(f"Strings from {file}.json successfully updated")

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

			if x == "[Job_Description]":
				index = list_writer(j_desc, strings, index)

			if x == "[Start Name]":
				index = list_writer(start_name, strings, index)

			if x == "[Sound]":
				index = list_writer(sounds, strings, index)

			if x == "[Messages]":
				index = list_writer(messages, strings, index)

			if x == "[Attacks]":
				index = list_writer(attacks, strings, index)

def list_writer(e_list, strings, index):
	for item in strings[1+index:]:
		index += 1
		if item in key_words:
			break
		else:
			e_list.append(item)
	return index


def change_dict(dic, lis, file, errors, index):
	for item in dic.keys():
		try:
			dic[item] = lis[index]
			index += 1
		except IndexError:
			print(f"Error 01 - {file}.txt. {dic[item]} - нет соответствующей строки.")
			errors += 1
	lis.clear()
	return errors

### Updater functions ###

def updater(user_folder, translated = True):
	errors = 0
	for root, dirs, files in os.walk(user_folder):
		for file in files:
			mod_file = root.replace("user", "mods") + "\\" + file
			try:
				objects = open_file(mod_file)
			except FileNotFoundError:
				print(f"\nErrno2 - отсутсвует файл {file} в папке с модом\n")


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
							errors = change_dict(record["names"], names, file, errors, index = 0)
						if "descriptions" in record.keys():
							errors = change_dict(record["descriptions"], desc, file, errors, index = 0)
						if "job_description" in record.keys():
							errors = change_dict(record["job_description"], j_desc, file, errors, index = 0)
						if "sound" in record.keys():
							errors = change_dict(record["sound"], sounds, file, errors, index = 0)
						if "messages" in record.keys():
							errors = change_dict(record["messages"], messages, file, errors, index = 0)	
						if "attacks" in record.keys():
							errors = change_dict(record["attacks"], attacks, file, errors, index = 0)
					try:
						if type(objects) == str:
							tags = objects.keys()
							get_items_tags(objects, tags, key_tags, check = False)
						else:
							for item in objects:
								single_tags = list(item.keys())
								get_items_tags(item, single_tags, key_tags, check = False )							
								check_for_new_tags(single_tags, item, record)

					except AttributeError:
						print(f"\nSome problems with {_file}\n")
						errors += 1						
					#### Добавление новых значений ####
					if "names" in record.keys():
						check_for_updates("names", record, names)
					if "descriptions" in record.keys():
						check_for_updates("descriptions", record, desc)
					if "job_description" in record.keys():
						check_for_updates("job_description", record, j_desc)
					if "sound" in record.keys():
						check_for_updates("sound", record, sounds)
					if "messages" in record.keys():
						check_for_updates("messages", record, messages)	
					if "attacks" in record.keys():
						check_for_updates("attacks", record, attacks)			
						
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

						if "messages" in record.keys() and len(record["messages"]) != 0:
							checking(check, user)
							check = dict_writer(user, record["messages"], "messages")

						if "attacks" in record.keys() and len(record["attacks"]) != 0:
							checking(check, user)
							check = dict_writer(user, record["attacks"], "attacks")

						user.write('\n  }\n]')

					strings_writer(root.replace("user", "strings") + "\\" + file.replace("json", "txt"), root +  "\\" + file, file, update = True)

			names.clear()
			desc.clear()
			j_desc.clear()
			start_name.clear()
			sounds.clear()
			messages.clear()
			attacks.clear()

	print(f"Total errors: {errors}")

def check_for_new_tags(tags, item, record):
	if "job_description" in tags and "job_description" not in record.keys():
		record["job_description"]  = {}
	if "start_name" in tags and "start_name" not in record.keys():
		record["start_name"]  = {}
	### Sound ###
	if "sound" in tags and "sound" not in record.keys():
		record["sound"] = {}
	if "bash" in tags and "sound" not in record.keys():
		bash = item["bash"]
		if "sound" in bash or "sound_fail" in bash:
			record["sound"] = {}
	### Messages ###

	if ((("messages" in tags) or
		("iv_message" in tags) or
		("memorial_messages" in tags) or	
		("mutagen_message" in tags)) and 
		("messages" not in record.keys())):

			record["messages"] = {}	
	if "spawn_item" in tags and "message" in item["spawn_item"] and "messages" not in record.keys():
		record["messages"] = {}		

	if (("use_action" in tags) and 
		(("not_ready_msg" in item["use_action"] or "msg" in item["use_action"]) or
		("need_charges_msg" in item["use_action"] or "need_fire_msg" in item["use_action"])) and 
		("messages" not in record.keys())):
		record["messages"] = {}
	### Attacks ###
	if "attacks" in tags and "attacks" not in record.keys():
		if "attack_text_npc" or "attack_text_u" in item["attacks"]:
			record["attacks"] = {}

def check_for_updates(key, old_dict, new_list):
	my_dict = old_dict[key]
	value = list(my_dict.values())
	for item in new_list:
		if item not in my_dict.values() and item not in my_dict.keys():
			if '\n' in item:
				item = item.replace('\n', '\\n')
			my_dict[item] = item

# select_mod(configs)
# extractor(configs.get('Folders', 'mod folder'), configs.get('Mods', 'mod'), translator_folder)
# updater(user_folder, True)