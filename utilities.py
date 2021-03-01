# -*- coding: utf-8 -*-
import os
import json

def file_name(cond, filename):
	folder = filename.rpartition('.')[0] 
	if cond == 'folder':
		path  = "files\\" + folder
		if os.path.exists(path) == False:
			create_folder(folder)
		else:
			print(f'Папка {folder} уже создана')
		return path
	elif cond == 'json':
		path = 'mod\\'+ filename
		return path
	elif cond == 'translated':
		path = 'translated\\'+ filename
		return path

def open_file(file):
	with open  ("mod\\"+file,'r',encoding = 'utf-8') as t:
		text = t.read()
	objects = json.loads(text)
	return objects

def create_folder(name):
	path = "files/"+name
	try:
		os.mkdir(path)
	except OSError:
		print(f'Папка {name} уже создана.')
	else:
		print(f'Создана папка с файлами {name}.')

def creating_folder(name):
	folder = file_name('folder', name)
	return str(folder)

def get_names(item, names):
	name = item['name']
	if type(name) == dict:
		for item in name.values():
			names.write(item +'\n')
	else:
		names.write(name +'\n')

def get_desctiption(item, descriptions):
	if '\n' in item['description']:
		item['description'] =  item['description'].replace('\n','\\n')
	description = item['description']
	descriptions.write(description +'\n')

def get_comments(item, comments):
	comment = item["//"]
	comments.write(comment +'\n')

def get_mo_mes(item, mo_mess):
	for x in item:
		if type(x) == dict:
			if 'monster_message' in x.keys():
				mo_mes =  x['monster_message']
				mo_mess.write(mo_mes +'\n')

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
	if "False"in new_string:
		new_string = new_string.replace('False',"false")
	return new_string
