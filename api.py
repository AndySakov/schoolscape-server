import numpy as np
import pandas as pd
import pymysql as DB
import sys, os, base64
from threading import Thread
import datetime
# from account_api import buildUp

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

def con(host='localhost', db='scape'):
	return DB.connect(host, "sam", "isaac1023", db)


def After15DaysDelSuggestions():
	db = con()
	sql = """SELECT * FROM suggestion_box"""
	marked = []
	today = BuildStandardDate().split("-")
	with db.cursor() as c:
		try:
			c.execute(sql)
			db.commit()
			res = c.fetchall()
			for row in res:
				if (DayOfYearDiff(row[3].split("-"), today) >= 15):
					marked.append(row[0])
			for i in marked:
				c.execute("DELETE FROM suggestion_box WHERE id=%d" % i)
				db.commit()
			print("Successfully Filter suggestions")
			return 1
		except Exception as e:
			db.rollback()
			return "We tried to do as you asked but this happend: %s" % str(e)

def DayOfYearDiff(d1, d2):
	return ((d2[0] - d1[0]) * 365) + ((datetime.datetime(int(d2[0]),int(d2[1]),int(d2[2])).timetuple().tm_yday)-(datetime.datetime(int(d1[0]),int(d1[1]),int(d1[2])).timetuple().tm_yday))

class Teacher:
	"""docstring for Teacher"""
	def __init__(self, usr):
		self.usr = usr
	def UploadNote(self, sub, term, week, _class, ndir):
		db = con(host = "localhost", db = "scape")
		sql = """
					INSERT INTO notes (sub, term, week, class, ndir)
					VALUES
					('%s', '%s', '%s', '%s', '%s')
			  """ % (sub, term, week, _class, ndir)
		with db.cursor() as c:
			try:
				c.execute(sql)
				db.commit()
				db.close()
				return 1
			except Exception as e:
				db.rollback()
				raise e
		return 0
	def DeleteNote(self, sub, term, week, _class, ndir):
		db = con(host = "localhost", db = "scape")
		sql = """
					DELETE FROM notes WHERE sub='%s' AND term='%s' AND week='%s' AND ndir='%s' AND class='%s'
			  """ % (sub, term, week, ndir, _class)
		with db.cursor() as c:
			try:
				c.execute(sql)
				db.commit()
				os.remove(ndir)
				db.close()
				return 1
			except Exception as e:
				db.rollback()
				raise e
		return 0
	def UploadAssignment(self, sub, term, _class, week, adir, max_score):
		db = con(host = "localhost", db = "scape")
		sql = """
					INSERT INTO assignments (sub, term, week, class, max_score, adir)
					VALUES
					('%s', '%s', '%s', '%s', '%s', '%s')
			  """ % (sub, term, week, _class, max_score, adir)

		with db.cursor() as c:
			try:
				c.execute(sql)
				db.commit()
				id = self.fetchAssID(sub = sub, term = term, _class = _class, week = week)
				sql2 = """CREATE TABLE `assignment %s submits` (
							id INT(255) NOT NULL AUTO_INCREMENT,
							student VARCHAR(55) NOT NULL,
							rdir VARCHAR(255) NOT NULL,
							score INT(255) NOT NULL,
							comment VARCHAR(500) NOT NULL,
							PRIMARY KEY (id),
							UNIQUE KEY (student)
						)
					  """ % id
				c.execute(sql2)
				db.commit()
				db.close()
				return 1
			except Exception as e:
				db.rollback()
				db.rollback()
				raise e
		return 0
	def MarkAssignment(self, qid, s, score):
		db = con(host = "localhost", db = "scape")
		sql = """UPDATE `assignment %s submits` SET score=%d WHERE student='%s' """ % (qid, score, s)
		with db.cursor() as c:
			try:
				c.execute(sql)
				db.commit()
				return 1
			except Exception as e:
				db.rollback()
				raise e
		return 0
	def CommentAssignment(self, qid, s, comment):
		db = con(host = "localhost", db = "scape")
		sql = """UPDATE `assignment %s submits` SET comment='%s' WHERE student='%s' """ % (qid, comment, s)
		with db.cursor() as c:
			try:
				c.execute(sql)
				db.commit()
				return 1
			except Exception as e:
				db.rollback()
				raise e
		return 0
	def fetchAssID(self, sub, term, _class, week):
		db = con(host = "localhost", db = "scape")
		sql = """SELECT * FROM assignments WHERE sub='%s' AND term='%s' AND class='%s' AND week='%s'"""\
		 % (sub, term, _class, week)
		with db.cursor() as c:
			try:
				c.execute(sql)
				db.commit()
				res = c.fetchall()
				if (res != ()):
					return res[0][0]
				else:
					return 'nil'
			except Exception as e:
				db.rollback()
				raise e
		return False

class Student:
	def SubmitAssignment(self, qid, stud, rdir):
		db = con(host = "localhost", db = "scape")
		sql = """INSERT INTO `assignment %s submits` (student, rdir, score, comment) 
					VALUES
					('%s', '%s', 0, 'no comment yet')
				""" % (qid, stud, rdir)
		with db.cursor() as c:
			try:
				c.execute(sql)
				db.commit()
				db.close()
				return 1
			except Exception as e:
				db.rollback()
				raise e
		return 0
	def DropSuggestion(self, name, suggestion):
		db = con(host = "localhost", db = "scape")
		sql = """INSERT INTO suggestion_box (sub, suggestion, date_of_submit)
					VALUES
					('%s', '%s', '%s')
				""" % (name, suggestion, BuildStandardDateTime())
		with db.cursor() as c:
			try:
				c.execute(sql)
				db.commit()
				db.close()
				return 1
			except Exception as e:
				db.rollback()
				raise e
		return 0

class Examination:
	def __init__(self, role):
		self.role = role
	def UploadQuestionObjective(self, sub, term, _class, edir):
		db = con()
		if (self.role != "teacher"):
			return "permission denied"
		else:
			sql = """
							INSERT INTO obj (sub, term, class, edir)
							VALUES
							('%s', '%s', '%s', '%s')
					""" % (sub, term, _class, edir)
			with db.cursor() as c:
				try:
					c.execute(sql)
					db.commit()
					return 1
				except Exception as e:
					db.rollback()
					raise e
			return 0
	def uploadAnswerObjective(self, qid, data):
		# FYI data is a python dict
		if (self.role.lower() != 'teacher'):
			return "permission denied"
		db = con()
		sql = """
					CREATE TABLE `exam objective %s answer` (
						id INT(255) NOT NULL AUTO_INCREMENT,
						question VARCHAR(500) NOT NULL,
						answer VARCHAR(500) NOT NULL,
						PRIMARY KEY (id)
					)
			   """ % qid
		sql2 = """
						CREATE TABLE `exam objective %s responses` (
							id INT(255) NOT NULL AUTO_INCREMENT,
							student VARCHAR(500) NOT NULL,
							score VARCHAR(500) NOT NULL,
							comment VARCHAR(500) NOT NULL,
							PRIMARY KEY (id),
							UNIQUE KEY (student)
						)
				""" % qid
		with db.cursor() as c:
			try:
				c.execute(sql)
				c.execute(sql2)
				db.commit()
				for i in data:
					sql = """INSERT INTO `exam objective %s answer` (question, answer) VALUES ('%s', '%s')""" % (qid,i, data[i])
					c.execute(sql)
					db.commit()
				db.close()
				return 1
			except Exception as e:
				db.rollback()
				raise e
		return 0
	def TakeExamObjective(self, qid, data, student):
		# FYI data is a python dict
		if (self.role != 'student'):
			return "permission denied"
		db = con()
		sql = """
					CREATE TABLE `exam objective %s %s answer` (
						id INT(255) NOT NULL AUTO_INCREMENT,
						question VARCHAR(500) NOT NULL,
						answer VARCHAR(500) NOT NULL,
						PRIMARY KEY (id)
					)
			   """ % (qid, student)
		with db.cursor() as c:
			try:
				c.execute(sql)
				db.commit()
				for i in data:
					sql = """INSERT INTO `exam objective %s %s answer` (question, answer) VALUES ('%s', '%s')""" % \
						(qid, student, i, data[i])
					c.execute(sql)
					db.commit()
				marked = self.MarkObjectiveScript(qid, data)
				sql = """INSERT INTO `exam objective %s responses` 
							(student, score, comment)
							VALUES
							('%s', '%s', '%s')
					""" % (qid, student, marked, 'no comment yet')
				c.execute(sql)
				db.commit()
				db.close()
				return 1
			except Exception as e:
				db.rollback()
				raise e
		return 0
	def MarkObjectiveScript(self, qid, data):
		Topinion = fetchExamAnswersRaw(qid)
		count = 0
		if (Topinion == 'nil'):
			return 0
		for i in range(len(Topinion)):
			if (Topinion[i][-1] == data[i+1]):
				count += 1
		return (count/len(Topinion)*50)
	def UploadQuestionTheory(self, sub, term, _class, edir):
		db = con()
		if (self.role != "teacher"):
			return "permission denied"
		else:
			sql = """
							INSERT INTO theory (sub, term, class, edir)
							VALUES
							('%s', '%s', '%s', '%s')
					""" % (sub, term, _class, edir)
			with db.cursor() as c:
				try:
					c.execute(sql)
					db.commit()
					return 1
				except Exception as e:
					db.rollback()
					raise e
			return 0
	def uploadAnswerTheory(self, qid, data):
		# FYI data is a python dict
		if (self.role.lower() != 'teacher'):
			return "permission denied"
		db = con()
		sql = """
					CREATE TABLE `exam theory %s answer` (
						id INT(255) NOT NULL AUTO_INCREMENT,
						question VARCHAR(500) NOT NULL,
						answer VARCHAR(500) NOT NULL,
						PRIMARY KEY (id)
					)
			   """ % qid
		sql2 = """
						CREATE TABLE `exam theory %s responses` (
							id INT(255) NOT NULL AUTO_INCREMENT,
							student VARCHAR(500) NOT NULL,
							score VARCHAR(500) NOT NULL,
							comment VARCHAR(500) NOT NULL,
							PRIMARY KEY (id),
							UNIQUE KEY (student)
						)
				""" % qid
		with db.cursor() as c:
			try:
				c.execute(sql)
				c.execute(sql2)
				db.commit()
				for i in data:
					sql = """INSERT INTO `exam theory %s answer` (question, answer) VALUES ('%s', '%s')""" % (qid,i, data[i])
					c.execute(sql)
					db.commit()
				db.close()
				return 1
			except Exception as e:
				db.rollback()
				raise e
		return 0
	def TakeExamTheory(self, qid, data, student):
		# FYI data is a python dict
		if (self.role != 'student'):
			return "permission denied"
		db = con()
		sql = """
					CREATE TABLE `exam theory %s %s answer` (
						id INT(255) NOT NULL AUTO_INCREMENT,
						question VARCHAR(500) NOT NULL,
						answer VARCHAR(500) NOT NULL,
						PRIMARY KEY (id)
					)
			   """ % (qid, student)
		with db.cursor() as c:
			try:
				c.execute(sql)
				db.commit()
				for i in data:
					sql = """INSERT INTO `exam theory %s %s answer` (question, answer) VALUES ('%s', '%s')""" % \
						(qid, student, i, data[i])
					c.execute(sql)
					db.commit()
				marked = self.MarkTheoryScript(qid, data)
				sql = """INSERT INTO `exam theory %s responses` 
							(student, score, comment)
							VALUES
							('%s', '%s', '%s')
					""" % (qid, student, marked, 'no comment yet')
				c.execute(sql)
				db.commit()
				db.close()
				return 1
			except Exception as e:
				db.rollback()
				raise e
		return 0
	def MarkTheoryScript(self, qid, data, test=False):
		Topinion = fetchExamAnswersTheoryRaw(qid)
		tp = dict()
		if (Topinion == 'nil'):
			return 0
		for i in range(len(Topinion)):
			tp[i+1] = Topinion[i][-1]
		count = []
		for i in tp:
			curr = 0
			beans = len(tp[i].split(" "))
			for j in tp[i].split(" "):
				if (j in data[i]):
					curr += 1
			if (test==True):
				count.append(((curr/beans) * 25))
			else:
				count.append(((curr/beans) * 100))
		count = np.array(count)
		return count.mean()

class Result:
	def __init__(self, student, _class):
		self.student = student
		self._class = _class
	def getExamScores(self, term):
		db = con()
		sql1 = """SELECT * FROM theory WHERE class='%s' AND term='%s'""" % (self._class, term)
		sql2 = """SELECT * FROM obj WHERE class='%s' AND term='%s'""" % (self._class, term)
		theory_scores = {}
		obj_scores = {}
		with db.cursor() as c:
			try:
				c.execute(sql1)
				db.commit()
				theory = c.fetchall()
				c.execute(sql2)
				db.commit()
				obj = c.fetchall()
			except Exception as e:
				raise e
		for trow in theory:
			sql_dyn = """SELECT * FROM `exam theory %s responses` WHERE student='%s'""" % (trow[0], self.student)
			try:
				c.execute(sql_dyn)
				db.commit()
				dyn = c.fetchall()
				if (trow[1] not in theory_scores):
					theory_scores[trow[1]] = dyn[0][2]
				else:
					theory_scores[trow[1]] += dyn[0][2]
			except Exception as e:
				raise e
		for orow in obj:
			sql_dyn = """SELECT * FROM `exam objective %s responses` WHERE student='%s'""" % (orow[0], self.student)
			try:
				c.execute(sql_dyn)
				db.commit()
				dyn = c.fetchall()
				if (orow[1] not in obj_scores):
					obj_scores[orow[1]] = dyn[0][2]
				else:
					obj_scores[orow[1]] += dyn[0][2]
			except Exception as e:
				raise e
		theory_scores = pd.DataFrame(theory_scores)
		obj_scores = pd.DataFrame(obj_scores)
		return (obj_scores, theory_scores)
	def getCAScores(self, term):
		db = con()
		sql1 = """SELECT * FROM assignments WHERE class='%s' AND term='%s'""" % (self._class, term)
		ass_scores = {}
		with db.cursor() as c:
			try:
				c.execute(sql1)
				db.commit()
				ass = c.fetchall()
			except Exception as e:
				raise e
		for arow in ass:
			sql_dyn = """SELECT * FROM `assignment %s submits` WHERE student='%s'""" % (arow[0], self.student)
			try:
				c.execute(sql_dyn)
				db.commit()
				dyn = c.fetchall()
				ass_scores[arow[1]] = dyn[0][2]
			except Exception as e:
				raise e

def fetchID(usr, role):
	db = con(host = "localhost", db = "scape")
	sql = """SELECT * FROM `%s` WHERE usr='%s'""" % (role, usr)
	with db.cursor() as c:
		try:
			c.execute(sql)
			db.commit()
			res = c.fetchall()
			if (res != ()):
				return res[0][0]
			else:
				return 'nil'
		except Exception as e:
			db.rollback()
			raise e
	return False

def fetchNotes():
	db = con()
	sql = """SELECT * FROM notes"""
	with db.cursor() as c:
		try:
			c.execute(sql)
			res = list()
			_res = c.fetchall()
			ret = ""
			if (_res == ()):
				return 'nil'
			# for x in _res:
			# 	buildUp = "%s,%s,%s,%s,%s" % (x[0], x[1], x[2], x[3], x[4])
			# 	res.append(buildUp)
			# for i in res:
			# 	if (i == res[-1]):
			# 		ret += buildUp
			# 	else:
			# 		ret += buildUp + ";"
			return _res
		except:
			raise Exception

def fetchAssignments():
	db = con()
	sql = """SELECT * FROM assignments"""
	with db.cursor() as c:
		try:
			c.execute(sql)
			res = list()
			_res = c.fetchall()
			ret = ""
			if (_res != ()):
				for x in _res:
					buildUp = "%s,%s,%s,%s,%s" % (x[0], x[1], x[2], x[3], x[4])
					res.append(buildUp)
				for i in res:
					if (i == res[-1]):
						ret += buildUp
					else:
						ret += buildUp + ";"
				return ret
			else:
				return 'nil'
		except:
			raise Exception


def fetchNote(id):
	db = con()
	sql = """SELECT * FROM notes WHERE id='%d'""" % id
	with db.cursor() as c:
		try:
			c.execute(sql)
			_res = c.fetchall()
			return _res[0][-1].replace("static/rep/", 'rep/') if _res != () else 'nil'
		except:
			raise Exception

def fetchAssignment(id):
	db = con()
	sql = """SELECT * FROM assignments WHERE id='%d'""" % id
	with db.cursor() as c:
		try:
			c.execute(sql)
			_res = c.fetchall()
			return _res[0][-1].replace("static/rep/", 'rep/') if _res != () else 'nil'
		except:
			raise Exception

def fetchAssignmentResponses(id):
	db = con()
	sql = """SELECT * FROM `assignment %s submits`""" % id
	with db.cursor() as c:
		try:
			c.execute(sql)
			res = list()
			_res = c.fetchall()
			ret = ""
			if (_res == ()):
				return 'nil'
			for x in _res:
				buildUp = "%s,%s,%s,%s,%s" % (x[0], x[1], x[2], x[3], x[4])
				res.append(buildUp)
			for i in res:
				if (i == res[-1]):
					ret += buildUp
				else:
					ret += buildUp + ";"
			return ret
		except Exception as e:
			raise e

def fetchAssignmentResponse(id, student):
	db = con()
	sql = """SELECT * FROM `assignment %s submits` WHERE student='%s'""" % (id, student)
	with db.cursor() as c:
		try:
			c.execute(sql)
			_res = c.fetchall()
			return _res[0][2].replace("static/rep/", 'rep/') if _res != () else 'nil'
		except:
			raise Exception

def IsSubmitted(id, student):
	db = con()
	sql = """SELECT * FROM `assignment %s submits` WHERE student='%s'""" % (id, student)
	with db.cursor() as c:
		try:
			c.execute(sql)
			_res = c.fetchall()
			return 0 if _res == () else 1
		except:
			raise Exception

def fetchAtt(role, usr):
	db = con(host = "localhost", db = "scape")
	sql = """SELECT * FROM `%s` WHERE usr='%s'""" % (role, usr)
	with db.cursor() as c:
		try:
			c.execute(sql)
			db.commit()
			res = c.fetchall()
			if (res != ()):
				return buildUp(res[0])
			else:
				return 'nil'
		except Exception as e:
			db.rollback()
			raise e
	return False


def BuildStandardDateTime():
	obj = datetime.datetime.now()
	return "%d-%d-%d %s:%s:%s" % (obj.day, obj.month, obj.year, obj.hour, obj.minute, obj.second)
def BuildStandardTime():
	obj = datetime.datetime.now()
	return "%s:%s:%s" % (obj.hour, obj.minute, obj.second)
def BuildStandardDate():
	obj = datetime.datetime.now()
	return "%d-%d-%d" % (obj.day, obj.month, obj.year)

def fetchExamInfo(sub, term, _class):
	db = con(host = "localhost", db = "scape")
	sql = """SELECT * FROM obj WHERE sub='%s' AND term='%s' AND class='%s'"""\
		% (sub, term, _class)
	with db.cursor() as c:
		try:
			c.execute(sql)
			db.commit()
			res = c.fetchall()
			if (res != ()):
				return buildUp(res[0])
			else:
				return 'nil'
		except Exception as e:
			db.rollback()
			raise e
	return False

def fetchExamAnswers(qid):
	db = con(host = "localhost", db = "scape")
	sql = """SELECT * FROM `exam objective %s answer`""" % qid
	with db.cursor() as c:
		try:
			c.execute(sql)
			db.commit()
			res = c.fetchall()
			if (res != ()):
				return res
			else:
				return 'nil'
		except Exception as e:
			db.rollback()
			raise e
	return False

def fetchExamAnswers(qid):
	db = con(host = "localhost", db = "scape")
	sql = """SELECT * FROM `exam objective %s answer`""" % qid
	with db.cursor() as c:
		try:
			c.execute(sql)
			db.commit()
			res = c.fetchall()
			if (res != ()):
				return res
			else:
				return 'nil'
		except Exception as e:
			db.rollback()
			raise e
	return False

def fetchExamAnswersTheory(qid):
	db = con(host = "localhost", db = "scape")
	sql = """SELECT * FROM `exam theory %s answer`""" % qid
	with db.cursor() as c:
		try:
			c.execute(sql)
			db.commit()
			res = c.fetchall()
			if (res != ()):
				return res
			else:
				return 'nil'
		except Exception as e:
			db.rollback()
			raise e
	return False

def fetchExamAnswersTheoryRaw(qid):
	db = con(host = "localhost", db = "scape")
	sql = """SELECT * FROM `exam theory %s answer`""" % qid
	with db.cursor() as c:
		try:
			c.execute(sql)
			db.commit()
			res = c.fetchall()
			if (res != ()):
				return res
			else:
				return 'nil'
		except Exception as e:
			db.rollback()
			raise e
	return False

def fetchExamInfoTheory(sub, term, _class):
	db = con(host = "localhost", db = "scape")
	sql = """SELECT * FROM theory WHERE sub='%s' AND term='%s' AND class='%s'"""\
		% (sub, term, _class)
	with db.cursor() as c:
		try:
			c.execute(sql)
			db.commit()
			res = c.fetchall()
			if (res != ()):
				return buildUp(res[0])
			else:
				return 'nil'
		except Exception as e:
			db.rollback()
			raise e
	return False

