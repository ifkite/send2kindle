import smtplib	
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.header import Header
from email.Utils import COMMASPACE,formatdate
from email import Encoders
import bsddb
import re
import pickle
import os

class Config(dict):
	def __init__(self):
		dict.__init__(self)
	
	def fromPyFile(self,filename):
		mod = type(os)('config')
		mod.__file__ = filename
		execfile(filename,mod.__dict__)
		self.fromObj(mod)
		
	def fromObj(self,obj):
		for key in dir(obj):
			if key.isupper():
				self[key] = getattr(obj,key)

class Mail:
	def __init__(self,kindleAccount=None,validMail=None,mailPasswd=None):
	    self.kindleAccount = kindleAccount
	    self.mail = (validMail,mailPasswd)
	    self.smtpConn = SMTPConn()
	    self.config = Config()
	# connect smtp server  
	def connect(self):
		# self.smtp=smtplib.SMTP()
		smtpServer = self.smtpConn.configSMTP(self.mail[0])
		self.smtpConn.connect(smtpServer)

	# login smtp server with user account and passwd
	def login(self):
		self.smtpConn.login(self.mail[0],self.mail[1])

	def logout(self):
		#clear passwd
		pass

	#return status of send
	def send2kindle(self):
		#EOFError,pickle file can not be empty
		if not isPklExist():
			createPkl()
		attFiles = getFiles()
		for attFile in attFiles:
			# for each file, send an email
			msg = MIMEMultipart()
			send_to = [self.kindleAccount]
			msg['Subject'] = 'python email2kindle ' + attFile
			msg['From'] = self.mail[0]
			msg['To'] = COMMASPACE.join(send_to)
			msg['Date'] = formatdate(localtime=True)
			
			with open(attFile) as f:
				book = f.read()
			# att = MIMEText(book,'base64','utf-8')
			# att["Content-Type"] = 'application/octet-stream'  
			# att["Content-Disposition"] = 'attachment; filename="%s"' %(attFile)
			part = MIMEBase('application', "octet-stream")
			part.set_payload(book)
			Encoders.encode_base64(part)
			part.add_header('Content-Disposition', 'attachment; filename="%s"' % attFile)
			msg.attach(part)

			self.smtpConn.sendmail(self.mail[0],send_to,msg.as_string())
		updateFile()

def getInput():
	pass

# PASSED
def getSMTP(input_func):
	def wrapper(mailName):
		return input_func(mailName)
	return wrapper

@getSMTP
def inputSMTP(mailName):
	return raw_input('please input %s smtp Server: ' %(mailName))

def checkMailFormat(mail):
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

class SMTPConn(smtplib.SMTP):
	def __init__(self):
		smtplib.SMTP.__init__(self)

	#detect the smtp server for user,return the suitable SMTP server
	def configSMTP(self,mail):	
		mailPat = '[^@]+@([^@]+\.[^@]+)'
		m = re.match(mailPat,mail)
		# should check after user inputing their mail 
		# if not m:		
		serverName = m.groups()[0]
		smtpName = None
		smtpDb = bsddb.hashopen('smtp.db')
		if smtpDb.has_key(serverName):
			smtpName = smtpDb[serverName]
		else:
			smtpName = inputSMTP(mail)
			smtpDb[serverName] = smtpName
			smtpDb.sync()
		smtpDb.close()
		return smtpName
# --------
	def modifySMTP(self,mail):
		smtpDb = bsddb.hashopen('smtp.db')
		if smtpDb.has_key(serverName):
			smtpDb[serverName] = inputSMTP(mail)
			smtpDb.sync()
			smtpDb.close()

	def displaySMTP(self,mail):
		smtpDb = bsddb.hashopen('smtp.db')
		if smtpDb.has_key(serverName):
			print mail,':',smtpDb[mail]
		else:
			print mail,':','None'
		smtpDb.close()
# --------

if __name__ == '__main__':
	mail = Mail(kindleAccount='example@kindle.me',validMail='yourmail@163.com',mailPasswd='passwd')
	mail.connect()
	mail.login()
	mail.send2kindle()
	mail.logout()