from subprocess import Popen, PIPE
import subprocess

update_to_date_msg = "Your branch is behind 'origin/master' by"
p = Popen("git commit", shell=True, stdout=PIPE, stderr=PIPE)
outs, errs = p.communicate()
if p.returncode != 0 and errs and errs!="":
	print p.returncode
	print errs
else:
	# print outs
	if(update_to_date_msg in outs):
		print "need update"
	else:
		print "no update"