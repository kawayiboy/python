import selfCommon
import os
from datetime import datetime

modified_str = 'modified:'
newfile_str = 'new file:'
paths = []
outs, errs = selfCommon.exec_cmd("git status")
rootdir = "C:\\Users\\telu\\Desktop\\powerflowaddin-fortest3\\pf_"+selfCommon.date_object
if not os.path.exists(rootdir):
	curdate = datetime.now()
	rootdir+='_'+str(curdate.hour)+'_'+str(curdate.minute)
	os.makedirs(rootdir)
else:
	os.makedirs(rootdir)
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