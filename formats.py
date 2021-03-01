# -*- coding: cp1251 -*-

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
