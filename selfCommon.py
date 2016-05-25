from datetime import datetime
from collections import deque
from apns import APNs, Frame, Payload
import os
import datetime as dt
import calendar
from StringIO import StringIO
import csv
import codecs
import urllib2
import urllib
from StringIO import StringIO
import sys
import cookielib
import simplejson as json
import shutil, errno
import time
from stat import *
import requests
import codecs
from subprocess import Popen, PIPE
import subprocess
from selenium import webdriver
import pickle

def get_tomorrow():
    today = datetime.now()
    nextdate = today + dt.timedelta(days=1)
    return nextdate

def get_nextdate(anydate):
    nextdate = anydate + dt.timedelta(days=1)
    return nextdate

def get_next_nth_date(anydate, daynum):
    nextdate = anydate + dt.timedelta(days=daynum)
    return nextdate

def set_time(datestr):
    dateval = datetime.strptime(datestr, '%d %b %Y')
    return dateval

def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime(year,month,day)

def get_current_datestr():
	curdate = datetime.now()
	formatstr = ""
	if curdate.day < 10:
	    formatstr = "0"
	monthformatstr = ""
	if curdate.month<10:
	    monthformatstr = "0"
	date_object = str(curdate.year)+'_'+monthformatstr+str(curdate.month)+'_'+formatstr+str(curdate.day)
	return date_object

def get_format_datestr(curdate, format='mm/dd/yyyy'):
    formatstr = ""
    date_object =""
    if curdate.day < 10:
        formatstr = "0"
    monthformatstr = ""
    if curdate.month<10:
        monthformatstr = "0"
    if(format=='mm/dd/yyyy'):
        date_object = monthformatstr+str(curdate.month)+'/'+formatstr+str(curdate.day)+'/'+str(curdate.year)
    elif(format=='yyyy-mm-dd'):
        date_object = str(curdate.year)+'-'+monthformatstr+str(curdate.month)+'-'+formatstr+str(curdate.day)
    elif(format=='yyyy_mm_dd'):
        date_object = str(curdate.year)+'_'+monthformatstr+str(curdate.month)+'_'+formatstr+str(curdate.day)
    return date_object

def date_to_str(indate):
    formatstr = ""
    if indate.day < 10:
        formatstr = "0"
    monthformatstr = ""
    if indate.month<10:
        monthformatstr = "0"
    date_object = str(indate.year)+'_'+monthformatstr+str(indate.month)+'_'+formatstr+str(indate.day)
    return date_object

def date_to_str_dash(indate):
    formatstr = ""
    if indate.day < 10:
        formatstr = "0"
    monthformatstr = ""
    if indate.month<10:
        monthformatstr = "0"
    date_object = str(indate.year)+'-'+monthformatstr+str(indate.month)+'-'+formatstr+str(indate.day)
    return date_object

curdate = datetime.now()
formatstr = ""
if curdate.day < 10:
    formatstr = "0"
monthformatstr = ""
if curdate.month<10:
    monthformatstr = "0"
date_object = str(curdate.year)+'_'+monthformatstr+str(curdate.month)+'_'+formatstr+str(curdate.day)

formatstr2 = ""
if curdate.day-1 < 10:
    formatstr2 = "0"
yesterday_object = str(curdate.year)+'_'+monthformatstr+str(curdate.month)+'_'+formatstr2+str(curdate.day-1)

def get_first_line(filename):
    with open(filename) as file:
        for line in file:
            return line

def get_first_n_line(filename,n):
    head = []
    with open(filename) as myfile:
        head = [next(myfile) for x in xrange(n)]
    return head


def get_last_row(reader):
    return deque(reader, 1)[0]


def last_3lines(filename):
    with open(filename) as fin:
        last3 = deque(fin, 3)
        return last3

def remove_last_line(filename):
	f = open(filename, "r")
	lines=f.readlines()
	lines=lines[:-1]
	f.close()

	f = open(filename, "w")
	for line in lines:
		f.write(line)
	f.close()

def last_line(filename):
    with open(filename) as fin:
        last = deque(fin, 1)
        return last

def last_lines(filename,lineno):
    with open(filename) as fin:
        last = deque(fin, lineno)
        return last

def read_csv_column_to_list(content,columns):
    reader = csv.DictReader(StringIO(content))
    desired_cols = (tuple(row[col] for col in columns) for row in reader)
    desiredlist = list(desired_cols)
    finallist = []
    for i in range(len(desiredlist)):
        finallist.append(float(desiredlist[i][0]))
    return finallist

apns = APNs(use_sandbox=True, cert_file='apns/apns-dev-cert.pem',
            key_file='apns/apns-dev-key-noenc.pem')
# Send a notification
token_hex = 'aa9951774c49b971c527e7511d6a0b60bef31811b6ff07fb496ccb1d3f3362ae'
def ApnsSendNotification(info):
    try:
        payload = Payload(alert=info, sound="default", badge=1)
        apns.gateway_server.send_notification(token_hex, payload)
    except Exception,e:
        print e

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def deletefirstline(filename):
    with open(filename, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(filename, 'w') as fout:
        fout.writelines(data[1:])

def makedir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    else:
        print directory+" exist"
        return False

def remove_directory(directory):
    try:
        shutil.rmtree(directory)
    except Exception, e:
        raise e

def read_utf8_file(filename):
    data = ''
    try:
        with codecs.open(filename, "r","utf-8") as myfile:
            data = myfile.read()
        return data
    except Exception, e:
        raise e

def read_file_content_lines(filename):
    lines = []
    try:
        with open (filename, "r") as myfile:
            for line in myfile:
                lines.append(line)
        return lines
    except Exception, e:
        raise e

def write_utf8_file(filename,content,append=False):
    myfile = codecs.open(filename,"w","utf-8")
    if(append==True):
        myfile = codecs.open(filename,"a","utf-8")
    myfile.write(content)
    myfile.close()

def read_csv_column_to_tuplelist(content,columns):
    reader = csv.DictReader(StringIO(content))
    desired_cols = (tuple(row[col] for col in columns) for row in reader)
    return list(desired_cols)

def read_csv(filename):
    try:
        reader = csv.reader(open(filename))
        data_list = list(reader)
        return data_list 
    except Exception, e:
        raise e

def read_csv_column(filename, idx, format_type=None):
    csvlist = read_csv(filename)
    columnlist = []
    listlen = len(csvlist)
    if(csvlist and listlen>0 and idx>=0):
        for i in xrange(listlen):
            try:
                obj = csvlist[i][idx]
                if(format_type!=None):
                    if(format_type=='int'):
                        obj = int(obj)
                    elif(format_type=='float'):
                        obj = float(obj)
                columnlist.append(obj)
            except Exception, e:
                print i
                raise e
    return columnlist

def lastmonth_stockinfo_bycolumn(symbol,columnname):
    today = datetime.now()
    thismonth = today.month-1
    daystr = str(today.day)
    monthstr=''
    if thismonth<10:
        monthstr='0'+str(thismonth)
    else:
        monthstr=str(thismonth)
    last2month = thismonth-1
    lastmonthstr=''
    if last2month<10:
        lastmonthstr='0'+str(last2month)
    else:
        lastmonthstr=str(last2month)
    yearstr=str(today.year)
    url = "http://ichart.yahoo.com/table.csv?s=" + symbol+"&a="+lastmonthstr+"&b="+daystr+"&c="+yearstr+"&d="+monthstr+"&e="+daystr+"&f="+yearstr+"&g=d"
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)
    html = res.read()
    # print html

    columns =[columnname]
    columnlist = read_csv_column_to_list(html,columns)
    return columnlist

def bought_stock():
    url = 'http://xueqiu.com/user/login'
    post_data = urllib.urlencode(
        {
            'username': 'tenglu2@gmail.com',
            'areacode': 86,
            'telephone': '',
            'remember_me': 1,
            'password': '645503250D82F15EC417AFF778068DAA'
        })
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36'
    req = urllib2.Request(url)

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36'),
                         ('Referer', 'http://xueqiu.com'),
                         ('Connection', 'keep-alive')]
    urllib2.install_opener(opener)

    req = urllib2.Request(url, post_data)
    req.add_header('host', 'xueqiu.com')
    req.add_header('Referer', 'http://xueqiu.com')
    req.add_header('User-Agent', user_agent)
    req.add_header('Connection', 'keep-alive')
    req.add_header('Accept-Language', 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4')
    req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
    req.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
    res = urllib2.urlopen(req)
    html = res.read()

    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36'
    req = urllib2.Request(url)
    req = urllib2.Request(
        'https://xueqiu.com/stock/portfolio/performances.json?size=100&page=1&showshort=1&group_id=382447&_=1410419191414')
    conn = urllib2.urlopen(req)
    html = conn.read()

    ddata = json.loads(str(html))

    boughtstocks = []
    stockslist = ddata[0]['list']
    for i in xrange(1, len(stockslist)):
        if(int(stockslist[i]['shares']) != 0):
            boughtstocks.append(stockslist[i]['symbol'])

    return boughtstocks

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def copy_file(src, dst):
    try:
        shutil.copy2(src, dst)
    except Exception, e:
        raise e

# src/test.txt --> D:\\dst
def copy_file_with_dir(src, dst):
    splitlocaldir = src.split('/')
    splitlocaldir.remove(splitlocaldir[-1:][0])
    localdir = dst
    for item in splitlocaldir:
        localdir += os.sep + item
    print localdir
    if not os.path.exists(localdir):
        os.makedirs(localdir)
    shutil.copy2(src, localdir)

def get_all_files_under_dir(dirpath):
    csvfiles = []
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            csvfiles.append(file)
    return csvfiles

def get_all_files_under_dir_full_path(dirpath,relative = True):
    csvfiles = []
    for path, subdirs, files in os.walk(dirpath):
        for file in files:
            fullpath = ''
            if(relative==True):
                fullpath = os.path.join(path,file)
            else:
                # print path
                paths = path.split('\\')[1:]
                path = "\\".join(paths)
                # print path
                fullpath = os.path.join(os.getcwd(),os.path.join(path,file))
            csvfiles.append(fullpath)
    return csvfiles

def get_all_files_under_dir_with_ext(dirpath, ext, filename_only=False):
    csvfiles = []
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if file.endswith("."+ext):
                if(filename_only):
                    csvfiles.append(file)
                else:
                    csvfiles.append(os.path.join(root,file))
    return csvfiles

def list_allfiles(dirpath):
    csvfiles = []
    for item in os.listdir(dirpath):
        if os.path.isfile(os.path.join(dirpath, item)):
            # print item
            csvfiles.append(item)
    return csvfiles

def change_modification_time(timestr,filename):
    if not os.path.exists(filename):
        print filename+"not exist"
        return
    ConverTime = time.mktime(time.strptime(timestr,'%Y-%m-%d'))
    #update file timestamp
    times=(ConverTime,ConverTime)
    os.utime(filename, times)

def read_file_content(filename):
    data = ''
    try:
        with open (filename, "r") as myfile:
            data = myfile.read()
        return data
    except Exception, e:
        raise e

def read_file_content_trim_enter(filename):
    data = read_file_content(filename)
    return data.replace('\n', '')

# optional parameter
def url_request(url, method='GET', encode_ascii=False, **kwargs):
    response = None
    if ('data' in kwargs):
        if('headers' in kwargs):
            response = requests.request(method, url, data=kwargs['data'], headers=kwargs['headers'])
        else:
            response = requests.request(method, url, data=kwargs['data'])
    else:
        response = requests.request(method, url)

    returntext = response.text
    if(encode_ascii):
        returntext = returntext.encode('ascii', 'ignore')
    return returntext

def urllib_get(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36'
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    req.add_header('Connection', 'keep-alive')
    res = urllib2.urlopen(req)
    html = res.read()
    return html

def print_utf8(text):
    s = unicode(text).decode('utf8')
    sys.stdout.write(s)

def print_list(text_list):
    for x in text_list:
        print x

def print_dictionary(dictionary):
    for key, value in dictionary.iteritems():
            print str(key) + ":" + str(value)

def dumpclean(obj):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print k
                dumpclean(v)
            else:
                print '%s : %s' % (k, v)
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                dumpclean(v)
            else:
                print v
    else:
        print obj

def exec_cmd(cmd):
    try:
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        outs, errs = p.communicate()
        if p.returncode != 0 and errs and errs!="":
            print p.returncode
            print errs
        else:
            return (outs, errs)
    except Exception, e:
        raise e

def dump_dict_to_json_file(filename, content):
    with open(filename, 'w') as fp:
        json.dump(content, fp)

def load_json(filename):
    content = read_file_content(filename)
    json_map = json.loads(str(content))
    return json_map

def get_stock_market(code):
    checkcode=code[0]
    stock_market = ''
    if int(checkcode)<=4:
        stock_market="sz"
    elif int(checkcode)>=5:
        stock_market="sh"
    return stock_market

def get_cn_stock_name_from_code(code):
    if(len(code)!=6):
        return None
    stock_market = get_stock_market(code)
    url = 'http://hq.sinajs.cn/list='+stock_market+code
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)
    html = res.read()
    begIdx = html.find('=')
    endIdx = html.find(',')
    # print html[begIdx+2:endIdx].decode('gb2312')
    return html[begIdx+2:endIdx].decode('gb2312')

def jpush_push(msg,dev=False):
    try:
        sys.path.append('../jpush-api-python-client-3.0.2')
        import jpush as jpush
        # from examples.push.conf import app_key, master_secret
        app_key = u'129df7dc599474e8a4dc1495'
        master_secret = u'6c8411a96d5a04e37c11401d'
        dev_app_key = u'5115e359060dbc792d5abc74'
        dev_master_secret = u'1596e0fb1b06f2fafd2fb9ea'

        if(dev):
           app_key = dev_app_key
           master_secret = dev_master_secret
        _jpush = jpush.JPush(app_key, master_secret)
        push = _jpush.create_push()
        push.audience = jpush.all_
        android_msg = jpush.android(alert=msg)

        push.notification = jpush.notification(alert=msg, android=android_msg)
        push.options = {"time_to_live":86400, "sendno":12345,"apns_production":True}
        push.platform = jpush.platform("android")
        push.send()
    except Exception, e:
        print e

def download_image(url,filename):
    """
    download a comic in the form of

    url = http://www.example.com
    filename = '00000000.jpg'
    """
    image=urllib.URLopener()
    image.retrieve(url,filename)

import pyautogui
def auto_gui_on_image(image_name):
    try:
        buttonx, buttony = pyautogui.locateCenterOnScreen(image_name)
        return (buttonx,buttony)
    except Exception, e:
        print e
        return (None,None)

def get_random_list(origlist,drawsize):
    listsize = len(origlist)
    
    randidx = []
    while(len(randidx)<drawsize):
        r = randint(0,listsize-1)
        if(r not in randidx):
            randidx.append(r)
    randlist = []
    for i in range(len(randidx)):
        randlist.append(origlist[randidx[i]])

    return randlist

def selenium_visit_url(url):
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(url)
    return driver

def login_save_cookie(driver,url,username_id, pwd_id, username, pwd, submit_id, cookie_filename):
    driver = selenium_visit_url(url)

    time.sleep(1)

    username_input = driver.find_element_by_id(username_id)
    username_input.send_keys(username)

    pwd_input = driver.find_element_by_id(pwd_id)
    pwd_input.send_keys(pwd)

    submit = driver.find_element_by_id(submit_id)
    submit.click()

    time.sleep(5)
    pickle.dump(driver.get_cookies() , open(cookie_filename,"wb"))
    driver.close()

def selenium_visit_with_cookie(url, cookie_filename):
    driver = selenium_visit_url(url)
    cookies = pickle.load(open(cookie_filename, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(url)
    return driver

def get_source_from_selenium(driver):
    return driver.execute_script("return document.documentElement.outerHTML;").encode("utf-8")

def switch_to_next_window_and_close(driver,next_win=True):
    win_handle = None
    current_handle = driver.current_window_handle
    if(next_win):
        window_after = driver.window_handles[1]
        print window_after
        win_handle = window_after
    else:
        window_before = driver.window_handles[0]
        print window_before
        win_handle = window_before

    driver.switch_to_window(win_handle)
    driver.close()
    driver.switch_to_window(current_handle)

def wait_and_find(func, args):
    time.sleep(2)
    elems = func(*args)
    while(len(elems)==0):
        time.sleep(1)
        elems = func(*args)
    return elems

def get_struct_time(timestr):
    return time.strptime(timestr,'%H:%M:%S')

def wait_until(struct_time):
    try:
        # sleep until 2AM
        t = datetime.today()
        future = datetime(t.year,t.month,t.day,struct_time.hour,struct_time.minute,struct_time.second)
        if t.hour >= struct_time.hour:
            future += dt.timedelta(days=1)
        time.sleep((future-t).seconds)
    except Exception, e:
        raise e

# def get_env_var(key):
#     try:  
#        return os.environ[str(key)]
#     except KeyError: 
#        print "Please set the environment variable " + str(key)

# def set_env_var(key,value):
#     try:
#         os.environ[str(key)] = str(value)
#     except Exception, e:
#         print e
#         raise e