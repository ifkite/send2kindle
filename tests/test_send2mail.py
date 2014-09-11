from ..sendmail import SMTPConn
from ..sendmail import Mail
from ..sendmail import getPasswd
from ..sendmail import Config
from ..sendmail import GetNameEventHandler
from ..sendmail import SendMailThread

from watchdog.observers import Observer

from threading import Event
from multiprocessing import Pipe

import os
import os.path
from nose import with_setup
import time

def setup_module(module):
    os.chdir('tests')
    print os.getcwd()
#       with open('fname.pkl','w'):pass

# @with_setup(create_file,delete_file)
# def test_getFiles_case2():
#       assert 'file.test' in getFiles()
#       time.sleep(2)

#def test_getpasswd():
#    assert getPasswd('holahello@163.com') == 'a'

#PASSED
class Test_Config:
    def __init__(self):
        self.config = Config()

    def test_frompyfile(self):
        print 'in test_frompyfile',os.getcwd()
        self.config.fromPyFile('config.py')
        assert self.config['KINDLE_ACCOUNT'] == 'KINDLE'
        assert self.config['USER'] == 'NOPE'

        self.config['KINDLE_ACCOUNT'] = 'NAMED'
        self.config['USER'] = 'ADMIN'
        assert self.config['KINDLE_ACCOUNT'] == 'NAMED'
        assert self.config['USER'] == 'ADMIN'

    def test_fromobj(self):
        class T:
            def __init__(self):
                pass
            PASSWD_TIMEOUT = 3600
            USER = 'NOPE'
        t = T()

        self.config.fromObj(t)
        assert self.config['PASSWD_TIMEOUT'] == 3600
        assert self.config['USER'] == 'NOPE'

        self.config['PASSWD_TIMEOUT'] = 7200
        self.config['USER'] = 'ADMIN'
        assert self.config['PASSWD_TIMEOUT'] == 7200
        assert self.config['USER'] == 'ADMIN'

# class Test_SMTPConn:
#       def __init__(self):
#               self.smtpConn = SMTPConn()
#       def test_configSMTP_case1_nothavekey(self):
#               assert self.smtpConn.configSMTP('@163.com') == 'smtp.163.com'
#       def test_configSMTP_case1_haskey(self):
#               assert self.smtpConn.configSMTP('@163.com') == 'smtp.163.com'
#       def test_configSMTP_case2_nothavekey(self):
#               assert self.smtpConn.configSMTP('@qq.com') == 'smtp.qq.com'
#       def test_confSMTP_case2_haskey(self):
#               assert self.smtpConn.configSMTP('@qq.com') == 'smtp.qq.com'

# class Test_Mail:
#       def __init__(self):
#               config = Config()
#               config.fromPyFile('config.py')
#               self.mail = Mail(config)

#       def send(self):
#               self.mail.connect()
#               self.mail.login()

#       def test_sendmail_case1(self):
#               self.send()

#       def test_sendmail_case2(self):
#               create_file()
#               self.send()
#               delete_file()
