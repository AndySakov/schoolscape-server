import numpy as np
import pymysql as DB
import sys, os
from api import con, fetchID
from threading import Thread
import requests

__PATH__ = os.path.realpath("")


class Teacher(Thread):
	"""docstring for Teacher"""
	def __init__(self):
		self.db = con()
	def Create(self, name, usr, pwd, ques, ans):
		self.db = con()
		sql = """
					INSERT INTO teacher (name, usr, pwd, sub)
					VALUES
					('%s', '%s', '%s', '%s')
			  """ % (name, usr, pwd, 'nil')
		with self.db.cursor() as c:
			try:
				c.execute(sql)
				c.execute("INSERT INTO security_ques (usr, ques, ans) VALUES ('%s', '%s', '%s')" % (usr, ques, ans))
				self.db.commit()
				self.db.close()
				os.chdir("static/rep")
				id = fetchID(usr=usr, role="teacher")
				os.mkdir("%d" % id)
				os.chdir("%s" % id)
				os.mkdir("pp")
				os.chdir(__PATH__)
				return 1
			except Exception as e:
				self.db.rollback()
				raise e
		return 0
	def AddSub(self, sub, usr):
		self.db = con()
		s = self.fetchSub(usr)
		id = fetchID(usr = usr, role = "teacher")
		if (s != 0):
			if (sub in s.split(";")):
				sub = s
			elif (s is 'nil'):
				sub = sub
				os.chdir("static/rep/%s" % id)
				os.mkdir("%s" % sub)
				print(sub)
				os.chdir(sub)
				for i in range(0, 3):
					l = i + 1
					os.mkdir("%d" % l)
					os.chdir("%d" % l)
					os.mkdir("notes")
					os.mkdir("assignments")
					os.mkdir("exam")
					os.mkdir("test")
					os.chdir("..")
				os.chdir(__PATH__)
			else:
				os.chdir("static/rep/%s" % id)
				os.mkdir("%s" % sub)
				print(sub)
				os.chdir(sub)
				for i in range(0, 3):
					l = i + 1
					os.mkdir("%d" % l)
					os.chdir("%d" % l)
					os.mkdir("notes")
					os.mkdir("assignments")
					os.mkdir("exam")
					os.chdir("..")
				os.chdir(__PATH__)
				sub = s + ";"+ sub
		elif (s == 'invalid'):
			return 'invalid'
		else:
			sub = sub
		sql = """
					UPDATE teacher SET sub='%s' WHERE usr='%s'
			  """ % (sub, usr)
		with self.db.cursor() as c:
			try:
				c.execute(sql)
				self.db.commit()
				self.db.close()
				return 1
			except Exception as e:
				self.db.rollback()
				raise e
		return 0
	def fetchSub(self, usr):
		db = con()
		sql = """
					SELECT * FROM teacher WHERE usr='%s'
			  """ % (usr)
		with db.cursor() as c:
			try:
				c.execute(sql)
				db.commit()
				db.close()
				res = c.fetchall()
				if (res == ()):
					return 'invalid'
				if (res[0][-1] != 'nil'):
					return res[0][-1]
			except Exception as e:
				db.rollback()
				raise e
		return 'nil'

class Student:
	"""docstring for Student"""
	def __init__(self):
		self.db = con()
	def Create(self, name, usr, pwd, _class, ques, ans):
		db = con()
		sql = """
					INSERT INTO student (name, usr, pwd, class)
					VALUES
					('%s', '%s', '%s', '%s')
			  """ % (name, usr, pwd, _class)
		with db.cursor() as c:
			try:
				c.execute(sql)
				c.execute("INSERT INTO security_ques (usr, ques, ans) VALUES ('%s', '%s', '%s')" % (usr, ques, ans))
				db.commit()
				db.close()
				id = fetchID(usr = usr, role = "student")
				os.chdir("static/rep/student")
				os.mkdir("%d" % id)
				os.chdir("%d" % id)
				os.mkdir("pp")
				for i in range(0, 3):
					l = i + 1
					os.mkdir("%d" % l)
					os.chdir("%d" % l)
					os.mkdir("assignments")
					os.chdir("..")
				os.chdir(__PATH__)
				return 1
			except Exception as e:
				raise e
		return 0

def ChangeAtt(usr, node, val, role):
	self.db = con()
	sql = """UPDATE `%s` SET `%s`='%s' WHERE usr='%s'""" % (role, node, val, usr)
	with self.db.cursor() as c:
		try:
			c.execute(sql)
			self.db.commit()
			self.db.close()
			return 1
		except pymysql.err.IntegrityError:
			return 400.1
		except pymysql.err.InternalError:
			return 400.2
		except Exception as e:
			self.db.rollback()
			raise e
	return 0

def verify_(usr, ques, ans):
	db = con()
	with db.cursor() as c:
		try:
			c.execute("SELECT * FROM security_ques WHERE usr='%s' AND ques='%s' AND ans='%s'" % \
			(usr, ques, ans))
			db.commit()
			return True
		except Exception as e:
			db.rollback()
			raise e
	return False

def setPathTeacher(id):
	os.chdir("static/rep")
	os.mkdir("%s" % id)
	os.chdir(__PATH__)
	return True

def login(usr, pwd, role='student'):
	sql = """SELECT * FROM `%s` WHERE usr='%s' AND pwd='%s'""" % (role, usr, pwd)
	db = con()
	with db.cursor() as c:
		try:
			c.execute(sql)
			_res = c.fetchall()
			if (_res == ()):
				return 0
			else:
				return _res[0]
		except Exception as e:
			db.rollback()
			raise e


def buildUp(args):
	end = ""
	for i in range(len(args)):
		if (args[i] == args[-1]):
			end += str(args[i])
		else:
			end += str(args[i]) + ","
	return end
def superBuildUp(args):
	end = ""
	for i in range(len(args)):
		if (args[i] == args[-1]):
			end += buildUp(args[i])
		else:
			end += buildUp(args[i]) + ";"
	return end

def sendBackground(ip, data):
	requests.post("http://%s:9000/push" % ip.split("/")[-1], data = data)
	return ''

# obj = Teacher()
# teachers_report = {#'create account': obj.Create("Smith Jones", "smones", 'smilie234', 'whats my name', 'smones'),
# 		  'add subject': obj.AddSub("chemistry", "smones")
# 		}
# print(teachers_report)

# obj = Student()
# students_report = {
# 					'create new student': obj.Create("Bob Sue", "Sob", "BobbySue", "ss3", 'whats my name', 'smones'),
# 					'change password': obj.ChangePwd('Sob', 'Sob'),
# 					'change username': obj.ChangeUsr('Sob')
# 					}
# print(students_report)
