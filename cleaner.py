# -*- coding: utf-8 -*-
### Скрипт, подготавливающий configs к публикации
from configparser import ConfigParser

configs = ConfigParser()
configs.read('configs.ini')

configs['Folders']["translator folder"] = "NONE"
configs['Folders']['mod folder'] = "NONE"
configs['Mods']['mod'] = "NONE"

with open ('configs.ini', 'w') as configfiles:
	configs.write(configfiles)