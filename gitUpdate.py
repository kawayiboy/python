from subprocess import Popen, PIPE
import subprocess
import selfCommon

update_to_date_msg = "Your branch is behind 'origin/master' by"
outs, errs = selfCommon.exec_cmd("git commit")
if(outs):
	# print outs
	if(update_to_date_msg in outs):
		print "need update"
		update_input = raw_input("update(y/n): ")
		if(update_input.lower()=='y'):
			print "updating"
	else:
		print "no update"