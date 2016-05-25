#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append('../')
import selfCommon
import json

# text="import sublime, sublime_plugin\n\
# \n\
# class ExampleCommand(sublime_plugin.TextCommand):\n\
# 		def run(self, edit):\n\
# 				self.view.insert(edit, 0, \"Hello, World!\")"

# menujson='[{\n\
# 		"id": "view",\n\
# 		"children": [\n\
# 			{\n\
# 				"caption": "Example",\n\
# 				"children": [\n\
# 					{\n\
# 						"caption": "Example",\n\
# 						"id": "Example",\n\
# 						"command": "example"\n\
# 					}\n\
# 				]\n\
# 			}]\n\
# }]'

base_dir = "C:\\Users\\Teng\\AppData\\Roaming\\Sublime Text 2\\Packages\\"
keymapfilename = 'Default (Windows).sublime-keymap'
pyfilename = 'Example.py'
menufilename = 'Main.sublime-menu'

def add_enter(lines):
	output = ''
	for line in lines:
		output = output+line+'\n'
	return output

def create_plugin(pluginname):
	global base_dir, keymapfilename, menufilename
	title = pluginname.title()
	dirpath = base_dir+title
	res = selfCommon.makedir(dirpath)
	if(res == False):
		selfCommon.remove_directory(dirpath)
		selfCommon.makedir(dirpath)
	keymapdir = './SublimePluginTemplate/'
	
	keymapfile = selfCommon.read_file_content(keymapdir+keymapfilename)
	ddata = json.loads(keymapfile)
	ddata[0]['command'] = pluginname.lower()
	with open(keymapdir+keymapfilename, 'w') as outfile:
		json.dump(ddata, outfile)
	selfCommon.copy_file(keymapdir+keymapfilename,dirpath+"\\"+keymapfilename)
	text = selfCommon.read_utf8_file(keymapdir+pyfilename)
	text = text.replace("ExampleCommand", title+"Command")
	selfCommon.write_utf8_file(dirpath+"\\"+title+".py",text)
	menujson = selfCommon.read_file_content(keymapdir+menufilename)
	menujson = menujson.replace("Example",title)
	menujson = menujson.replace("example",pluginname.lower())
	selfCommon.write_utf8_file(dirpath+"\\"+menufilename,menujson)

if __name__ == '__main__':
		if(len(sys.argv)<2):
				print "Usage:"
				print os.path.basename(__file__)+" pluginname"
		else:
			create_plugin(sys.argv[1])