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

def get_tomorrow():
    today = datetime.now()
    nextdate = today + dt.timedelta(days=1)
    return nextdate

def get_nextdate(anydate):
    nextdate = anydate + dt.timedelta(days=1)
    return nextdate

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

def get_all_files_under_dir(dirpath):
    csvfiles = []
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            csvfiles.append(file)
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