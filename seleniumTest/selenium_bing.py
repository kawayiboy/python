# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('UTF8')
from selenium import webdriver
import time
import sys
sys.path.append('../')
import selfCommon
import os
import pickle
from BeautifulSoup import BeautifulSoup
sys.path.append('../thread/taskqueue/')
import taskqueue
# from time import time, sleep
from datetime import datetime

search_txts = ['Justin Bieber','Katy Perry']
username='tenglu2@live.cn'
pwd= 'kawayiboy2'

def selenium_bing(search_txt):
	url = r'http://www.bing.com/?scope=web&mkt=en-US&FORM=QBLH&wlexpsignin=1'
	driver = webdriver.Firefox()
	driver.maximize_window()
	driver.get(url)
	cookies = pickle.load(open("cookies.pkl", "rb"))
	for cookie in cookies:
		driver.add_cookie(cookie)

	search_box = driver.find_element_by_id('sb_form_q')
	search_box.send_keys(search_txt)
	
	submit = driver.find_element_by_id('sb_form_go')
	submit.click()
	
	time.sleep(1)

	driver.close()

def find_elem_id(driver,imgid):
	return driver.find_elements_by_id(imgid)

def selenium_bing_click(imgid):
	try:
		url = r'http://www.bing.com/?scope=web&mkt=en-US&FORM=QBLH&wlexpsignin=1'
		driver = webdriver.Firefox()
		driver.maximize_window()
		driver.get(url)
		cookies = pickle.load(open("cookies.pkl", "rb"))
		for cookie in cookies:
			driver.add_cookie(cookie)

		imgs = selfCommon.wait_and_find(find_elem_id,[driver,imgid])
		imgs[0].click()

		time.sleep(1)
	except Exception, e:
		print e
	finally:
		driver.close()

def find_login(driver):
	return driver.find_elements_by_id("i0116")

def login_save_cookie():
	global username, pwd
	url = 'http://www.bing.com/'
	driver = selfCommon.selenium_visit_url(url)
	submit = selfCommon.wait_and_find(find_elem_id,[driver,'id_s'])[0]
	submit.click()

	time.sleep(3)

	submit = driver.find_element_by_class_name('id_name')
	submit.click()

	elems = selfCommon.wait_and_find(find_login,[driver])
	elems[0].send_keys(username)

	pwd_box = driver.find_element_by_id("i0118")
	pwd_box.send_keys(pwd)

	driver.find_element_by_id('idChkBx_PWD_KMSI0Pwd').click()

	driver.find_element_by_id('idSIButton9').click()

	time.sleep(5)
	pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

def bing_click_multiple_times(lilen):
	for j in xrange(2):
		for i in xrange(lilen):
			imgid = 'crs_itemLink_'+str(i)
			selenium_bing_click(imgid)

def bing_click_task_queue(lilen):
	q = taskqueue.Queue(workers=4)
	for i in xrange(lilen):
		imgid = 'crs_itemLink_'+str(i)
		q.add(selenium_bing_click, imgid)

	for task in q.finished:
		print task.result

def click_images():
	lilen = 24
	try:
		html = selfCommon.urllib_get('http://www.bing.com/hpm?IID=SERP.1000&IG=F3786ADBB0864773992CBD44415620DC')
		soup = BeautifulSoup(html)
		pane = soup.find(id='crs_pane')
		lis = pane.findAll('li')
		if(lis==None or len(lis)==0):
			lilen = 24
		else:
			lilen = len(lis)
			print len(lis)
	except Exception, e:
		raise e

	# bing_click_multiple_times(lilen)
	for j in xrange(2):
		bing_click_task_queue(lilen)

if __name__ == '__main__':
	if(not os.path.exists('cookies.pkl')):
		login_save_cookie()
	# for txt in search_txts:
	# 	selenium_bing(txt)
	else:
		if(len(sys.argv)>1):
			timestr = sys.argv[1]
			print timestr
			struct_time = datetime.strptime(timestr, '%H:%M:%S')
			selfCommon.wait_until(struct_time)
			click_images()
		else:
			click_images()
