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


configs = ConfigParser()
configs.read('configs.ini')

mod = configs.get('Mods', 'mod')
game_folder = configs.get('Folders', 'game folder')
translator_folder = configs.get('Folders', 'translator folder')
mods_folder = configs.get('Folders', 'mod folder')
string_folder = translator_folder+"\\strings\\"+ configs.get('Mods', 'mod')
user_folder = translator_folder+"\\user\\"+ configs.get('Mods', 'mod')

### Replacer's functions ###
def open_file(file):
	with open (file,'r', encoding = 'utf-8') as t:
		text = t.read()
	objects = json.loads(text)
	return objects
	
def replacer(user_path, mod_path):
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
							if key == "name":
								minor_rep(objects, item, key, names)

							if key == "description": ### Add desc
								minor_rep(objects, item, key, desc)
							if key == "desc":
								minor_rep(objects, item, key, desc)

							if key == "job_description":
								minor_rep(objects, item, key, j_desc)

							if key == "start_name":
								minor_rep(objects, item, key, start_name)

							if key == "sound":
								minor_rep(objects, item, key, sounds)

							if ((key == "messages")	or 
							   (key == "mutagen_message") or
							   (key == "memorial_message") or
							   (key == "iv_message")):
								minor_rep(objects, item, key, messages)
							if key == "spawn_item" and "message" in item:
								minor_rep(item, item["message"], "message", messages)

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
								value = req_value(value, x)
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
def req_value(value, x):
    if type(value) == int:
        value = str(value)

    elif type(value) == str:
        value = '"' + value + '"'
        
    elif type(value) == bool:
        value = str(value).lower()

    elif type(value) == dict:
        if len(str(value)) >= 100:
            string = ""
            count = len(value)
            x += 2
            for key, item in value.items():
                count -= 1
                value_new = '"' + key + '":' + req_value(item, x)
                if count > 0:
                    value_new += ","
                string += " "*x + value_new + "\n"
            x -= 2
            value = '{\n' + string + x*" " +"}"
        else:
            value = str(value).replace("'",'"')

    elif type(value) == list:
        if len(str(value)) >= 90:
            string = ""
            count = len(value)
            x += 2
            for item in value:
                count -= 1
                value_new = req_value(item, x)
                if count > 0:
                    value_new += ","
                string += " "*x + value_new + "\n"
            x -= 2
            value = "[\n" + string + x*" " +"]"
        else:
            value = str(value).replace("'",'"')

    return value

replacer(user_folder, mods_folder)