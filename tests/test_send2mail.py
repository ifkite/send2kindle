from ..sendmail import getSMTP,updateFile,getFiles
from ..sendmail import SMTPConn
from ..sendmail import Mail
import os
import os.path
from nose import with_setup
import time

def setup_module(module):
	os.chdir('tests')
	with open('fname.pkl','w'):pass
	# print os.getcwd()

def test_getSMTP():
	assert getSMTP(lambda mailName:"smtp.163.com")("holahello@163.com") == "smtp.163.com"

def test_updateFile():
	assert type(updateFile()) is list or type(None)

def test_getFiles_case1():
	assert len(getFiles()) == 0
	time.sleep(2)

def create_file():
	with open('file.test','w') as f:
		f.write('this is a test file')

def delete_file():
	os.remove('file.test')

@with_setup(create_file,delete_file)
def test_getFiles_case2():
	assert 'file.test' in getFiles() 
	time.sleep(2)

class Test_Config:
	def __init__(self):
		self.mail = Mail()
	
	def test_frompyfile(self):
		self.mail.config.fromPyFile('config.py')
		assert self.mail.config['DEBUG_LEV'] == 1
		assert self.mail.config['PATH'] == '.'

	def test_fromobj(self):
		class T:
			def __init__(self):
				pass
			DEBUG_LEV = 1
			PATH = '.'
		t = T()

		self.mail.config.fromObj(t)
		assert self.mail.config['DEBUG_LEV'] == 1
		assert self.mail.config['PATH'] == '.'

class Test_SMTPConn:
	def __init__(self):
		self.smtpConn = SMTPConn()
	def test_configSMTP_case1_nothavekey(self):
		assert self.smtpConn.configSMTP('holahello@163.com') == 'smtp.163.com'
	def test_configSMTP_case1_haskey(self):
		assert self.smtpConn.configSMTP('holahello@163.com') == 'smtp.163.com'
	def test_configSMTP_case2_nothavekey(self):
		assert self.smtpConn.configSMTP('if.miracle@qq.com') == 'smtp.qq.com'
	def test_confSMTP_case2_haskey(self):
		assert self.smtpConn.configSMTP('if.miracle@qq.com') == 'smtp.qq.com'

class Test_Mail:
	def __init__(self):
		self.mail = Mail(kindleAccount='yourmail@qq.com',validMail='yourmail@163.com',mailPasswd='passwd')	
	def send(self):
		self.mail.connect()
		self.mail.login()
		self.mail.send2kindle()
	
	def test_sendmail_case1(self):
		self.send()
	
	def test_sendmail_case2(self):
		create_file()
		self.send()
		delete_file()
