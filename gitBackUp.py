import selfCommon
import os
from datetime import datetime
import sys

modified_str = 'modified:'
newfile_str = 'new file:'
paths = []
outs, errs = selfCommon.exec_cmd("git status")
rootdir = "C:\\Users\\telu\\Desktop\\powerflowaddin-fortest3\\"
stash_name = raw_input("stash name:")
rootdir+=stash_name.strip()
if not os.path.exists(rootdir):
	# curdate = datetime.now()
	# rootdir+='_'+str(curdate.hour)+'_'+str(curdate.minute)
	os.makedirs(rootdir)
else:
	print rootdir+' exist!'
	sys.exit(0)
if(outs):
	lines = outs.split('\n')
	for line in lines:
		modify_idx = line.find(modified_str)
		path = ''
		if(modify_idx!=-1):
			path = line[modify_idx+len(modified_str):].strip()
		else:
			newfile_idx = line.find(newfile_str)
			if(newfile_idx!=-1):
				path = line[newfile_idx+len(newfile_str):].strip()

		if(len(path)>0):
			selfCommon.copy_file_with_dir(path,rootdir)
			paths.append(path)

	print paths