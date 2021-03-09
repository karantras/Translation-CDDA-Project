# -*- coding: utf-8 -*-

import os
import json
import tkinter.filedialog as fd
from pathlib import Path
from configparser import ConfigParser


configs = ConfigParser()
configs.read('config.ini')
mods_folder = configs.get('Folders', 'Mods Folder')
base_folder = configs.get('Folders', 'Translator Folder')
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

def extractor (path, mod):
	for root, dirs, files in os.walk(path):
		for _file in files:
			file =_file[ : _file.find(".json") - 0]

			if file not in ignorable:
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

						if '//' in tags:
							comment.append(item['//'])
							check = True

					if check:
						new_root = root.replace("\\mods\\","\\strings\\")
						file_path = new_root+"\\"+file+".txt"

						if not os.path.exists(new_root):
							os.makedirs(new_root)

						writer(file, file_path, names, desc, comment, mo_mess)
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

		### Names ###
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