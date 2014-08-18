import bsddb
import pickle
import time
import types
import re
import os
import sys
from argparse import ArgumentParser
import smtplib
import socket

import Queue
from multiprocessing import Pipe
from threading import Thread
from threading import Event

from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.header import Header
from email.Utils import COMMASPACE,formatdate
from email import Encoders

from getpass import getpass

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class GetNameEventHandler(FileSystemEventHandler):
        # there are other ways to communicate between each threads,
        # for exampes, Queue, Pipe, shared memory
    def __init__(self,pipe,stop_event):
        super(GetNameEventHandler,self).__init__()
        self.pipe = pipe
        self._stop_event = stop_event

    def getSet(self):
        return self._stop_event.is_set()

    def on_created(self,event):
        if not self.getSet():
            try:
                # self.queue.put(event.src_path)
                # self.queue.join()
                self.pipe.send(event.src_path)
                time.sleep(0.1)
            except:
                pass

    def stop(self):
        self._stop_event.set()

class SendMailThread(Thread):
    def __init__(self,pipe,stop_event,mail):
        Thread.__init__(self)
        self._stop_event = stop_event
        self.pipe = pipe
        self.mail = mail
        if hasattr(self,'daemon'):
            self.daemon = True
        else:
            self.setDaemon(True)

    def getSet(self):
        return self._stop_event.is_set()

    def stop(self):
        self._stop_event.set()

    #send mail
    def run(self):
        while not self.getSet():
            try:
            # src_path = self.queue.get()
            # print src_path
            # self.queue.task_done()
                attFile = self.pipe.recv()
                self.mail.send2kindle(attFile)
                print 'sent %s to kindle' %(attFile)
                time.sleep(0.1)
            except:
                break

#PASSED @Aug.7th.2014
class Config(dict):
    def __init__(self):
        dict.__init__(self)

    def fromPyFile(self,filename):
        '''examples'''
        mod = type(os)('config')
        mod.__file__ = filename
        try:
            execfile(filename,mod.__dict__)
            self.fromObj(mod)
        except IOError:
            print 'No such config file %s.\
                   Check the spelling of config file name \
                   or settings in code.' % (filename)
            sys.exit()
                   
    # class or object except basestring
    def fromObj(self,obj):
        '''exampes'''
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj,key)

class Mail:
    def __init__(self,config,send_strategy):
        self.kindleAccount = config['KINDLE_ACCOUNT']
        self.user = config['USER']
        self.passwd = getPasswd(self.user)
        self.config = config
        self.send = types.MethodType(send_strategy,self)

    # connect smtp server
    def connect(self):
        try:
            self.smtpConn = SMTPConn(timeout=config['CONNECT_TIMEOUT'])
            smtpServer = self.smtpConn.configSMTP(self.user)
            self.smtpConn.connect(smtpServer)
        except socket.timeout:
            print 'error occured in connection with SMTP server,\n\
                  1. check your network\n\
                  2. check whether the imput of SMTP server is right'
            sys.exit()

    # login smtp server with user account and passwd
    def login(self):
        self.smtpConn.login(self.user,self.passwd)

    def logout(self):
        #close connection to smtp server
        pass

    def send2kindle(self,attFile):
        msg = MIMEMultipart()
        send_to = [self.kindleAccount]
        msg['Subject'] = 'python email2kindle '+attFile
        msg['From'] = self.user
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        with open(attFile) as f:
            book = f.read()
        # code that may take effect,@Jun.27th.2014
        # att = MIMEText(book,'base64','utf-8')
        # att["Content-Type"] = 'application/octet-stream'
        # att["Content-Disposition"] = 'attachment; filename="%s"' %(attFile)
        part = MIMEBase('application', "octet-stream")
        part.set_payload(book)
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; \
                        filename="%s"' % attFile)
        msg.attach(part)
        self.smtpConn.sendmail(self.user,send_to,msg.as_string())

    def send(self):
        pass

def send_watchdog(self):
    r_pipe,w_pipe = Pipe()
    event = Event()
    event_handler = GetNameEventHandler(w_pipe,event)
    send_mail_thread = SendMailThread(r_pipe,event,self)
    send_mail_thread.start()

    observer = Observer()
    path = self.config['BOOK_PATH']
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        event.set()
        observer.stop()
        #NOTICE:kill threads by force, need to change
        sys.exit()

# PASSED
def getInput(input_func):
    def wrapper(inputStr):
        return input_func(inputStr)
    return wrapper

@getInput
def inputSMTP(mailName):
    return raw_input('please input %s smtp Server: ' %(mailName))

def checkMailFormat(mailName):
    pass

def isPklExist():
    return 'fname.pkl' in os.listdir('.')

def createPkl():
    with open('fname.pkl','wb'):pass
#PASSED
def getFiles():
    # IOError
    with open('fname.pkl','rb') as fnamesPkl:
        try:
            fnames = pickle.load(fnamesPkl)
        except EOFError:
            fnames = []
        # need to MODIFY
        newFnames = [f for f in os.listdir('.') if os.path.isfile(f)]
        newFiles = findNewFiles(fnames,newFnames)
        return newFiles
            # print fnames
#PASSED
def updateFile():
    with open('fname.pkl','wb') as fnamesPkl:
        fileNames = [f for f in os.listdir('.') if os.path.isfile(f)]
        pickle.dump(fileNames,fnamesPkl)
        return fileNames

#PASSED
# suppose that all names in dir not changed
def findNewFiles(fnames,newFnames):
    return list(set(newFnames) - set(fnames))

#PASSED
def getPasswd(userName):
    getPassTwice = lambda:(getpass('input passwd of %s: '%(userName)),
                           getpass('input passwd again: '))
    p1,p2 = getPassTwice()
    while p1 != p2:
        p1,p2 = getPassTwice()
    return p1

class SMTPConn(smtplib.SMTP):
    def __init__(self,timeout=10):
        smtplib.SMTP.__init__(self,timeout=10)

    #recognise the smtp server for user,return the suitable SMTP server
    def configSMTP(self,mailName):
        mailPat = '[^@]+@([^@]+\.[^@]+)'
        m = re.match(mailPat,mailName)
        # should check after user inputing their mail
        # if not m:
        serverName = m.groups()[0]
        smtpName = None
        smtpDb = bsddb.hashopen('smtp.db')
        if smtpDb.has_key(serverName):
            smtpName = smtpDb[serverName]
        else:
            smtpName = inputSMTP(mailName)
            smtpDb[serverName] = smtpName
            smtpDb.sync()
        smtpDb.close()
        return smtpName

def modify_smtp(modify_mail):
    smtp_db = bsddb.hashopen('smtp.db')
    smtp = raw_input('please input new smtp server: ')
    #NOTICE:add some code to try to connect server
    smtp_db[modify_mail] = smtp
    print 'data modifed\n{0:18}  {1:18}'.format(modify_mail,smtp)
    smtp_db.sync()
    smtp_db.close()

def show_smtp():
    smtp_db = bsddb.hashopen('smtp.db')
    print '{0:18}  {1:18}'.format('mail','smtp server')
    for key,val in smtp_db.items():
        print '{0:18}  {1:18}'.format(key,val)
    smtp_db.close()

def any_parse():
    parser = ArgumentParser()
    parser.add_argument('--show',action='store_true',help='show mails and \
                         their smtp servers in local database')
    parser.add_argument('--modify',dest='mail',default=None,help='modify \
                        mail and smtp server')
    args=parser.parse_args()
    if args.show:
        show_smtp()
        return True
    elif args.mail is not None:
        modify_smtp(args.mail)
        return True
    else:
        return False

if __name__ == '__main__':
    if(not any_parse()):
        config = Config()
        config.fromPyFile('config.py')
        mail = Mail(config,send_watchdog)
        mail.connect()
        mail.login()
        mail.send()
