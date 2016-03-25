import selfCommon
import sys
import fileinput
import os

def svg_clean(filename):
	data = selfCommon.read_utf8_file(filename)
	start = data.find('<!-- Generator: Adobe Illustrator')
	if(start!=-1):
		end = data.find('-->',start)
		data = data[:start] + data[end+5:]
		print filename
		selfCommon.write_utf8_file(filename,data)

def svg_clean_inplace(filename):
	textToSearch = '<!-- Generator: Adobe Illustrator 19.2.1, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->\n'
	file = fileinput.FileInput(filename, inplace=True, backup='.bak')
	for line in file:
		sys.stdout.write(line.replace(textToSearch, ''))
	file.close()
	os.remove(filename+'.bak')

def svg_clean_all(dir):
	files = selfCommon.get_all_files_under_dir_with_ext(dir,'svg')
	print files
	for file in files:
		svg_clean(file)

if __name__ == '__main__':
	if(len(sys.argv)>1):
		svg_clean_inplace(sys.argv[1])
	else:
		svg_clean_all('.')