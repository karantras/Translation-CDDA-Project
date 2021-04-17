# -*- coding: utf-8 -*-

import os
import polib
from pathlib import Path
from configparser import ConfigParser

configs = ConfigParser()
configs.read('configs.ini')

mod = configs.get('Mods', 'mod')
game_folder = configs.get('Folders', 'game folder')
translator_folder = configs.get('Folders', 'translator folder')
mods_folder = configs.get('Folders', 'mod folder')
string_folder = translator_folder+"/strings/"+ configs.get('Mods', 'mod')
user_folder = translator_folder+"/user/"+ configs.get('Mods', 'mod')
po_folder = translator_folder+"\\po\\"+ configs.get('Mods', 'mod')

#### Po creating ####


po = polib.POFile()
po.metadata = {
    'POT-Creation-Date': '2021-04-13 14:00+0100',
    'Last-Translator': 'Karantras',
    'Language': 'Russian',
    'Content-Type': 'text/plain; charset=utf-8',
    'Content-Transfer-Encoding': '8bit',
    'Plural-Forms': 'nplurals=4; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<12 || n%100>14) ? 1 : n%10==0 || (n%10>=5 && n%10<=9) || (n%100>=11 && n%100<=14)? 2 : 3);'
}

# entry = polib.POEntry()
# entry.msgid = "Joppa"
# entry.msgid_plural = "Joppas"
# entry.msgstr = u"ЖОПА"
# entry.msgstr_plural[0] = u""
# entry.msgstr_plural[1] = u""
# entry.msgstr_plural[2] = u""
# entry.tcomment = u"~ Descriptions for Joppa"
# entry.occurrences = [('Joppa.py', False)]

# po = polib.pofile('C:/Users/User/Documents/Translation-CDDA-Project/po/test3.po', encoding='utf-8')
# merge_file = polib.pofile('C:/Users/User/Documents/Translation-CDDA-Project/po/test2.po', encoding='utf-8')
# #### Merge po files ####
# for x in merge_file:
# 	if x not in po:
# 		po.append(x)

po.save(po_folder +'\\'+ 'ru.po')