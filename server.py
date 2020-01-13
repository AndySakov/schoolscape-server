from flask import *
from werkzeug.utils import secure_filename
import api
import os
import base64
from threading import Thread
from api import fetchAtt, fetchID
import account_api
from flask_cors import CORS, cross_origin

api.After15DaysDelSuggestions()

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'

# cors = CORS(app, resources={r"/note/add": {"origins": "http://localhost:port"}})
cors = CORS(app)

app.secret_key = base64.b64encode(">>>Huncho on the beat<<<".encode('ascii'))

__PATH__ = os.path.realpath("")


# note services
@app.route("/note/add", methods=['GET', 'POST', 'JSON'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def add_note():
	if request.method == 'POST':
		teacher = request.form['u']
		sub = request.form['s']
		term = request.form['t']
		week = request.form['w']
		file = request.files['f']

		i = fetchID(teacher, role="teacher")
		filename = secure_filename(file.filename)
		ndir = "static/rep/%s/%s/%s/notes/%s" % (i, sub, term, filename)
		obj = api.Teacher(usr = teacher)
		
		# now for action
		if (i == None):
			return "invalid"
		
		res = obj.UploadNote(sub= sub, term = term, week = week, ndir = ndir)
		
		if (res == 1):
			os.chdir("static/rep/%s/%s/%s/notes" % (i, sub, term))
			file.save(filename)
			os.chdir(__PATH__)
			return 1
	return 0

@app.route("/note/all", methods=['GET', 'POST', 'JSON'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_notes():
	return api.fetchNotes()

@app.route("/note", methods=['GET', 'POST', 'JSON'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_note():
	# the notes ID
	if request.method == 'POST':
		id = request.form['i']
	elif request.method == 'GET':
		id = request.args['i']
	else:
		id = request.get_json()['i']
	return url_for('static', filename = api.fetchNote(id = id))


@app.route("/note/remove", methods=['GET', 'POST', 'JSON'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def remove_note():
	if request.method == 'POST':
		teacher = request.form['u']
		sub = request.form['s']
		term = request.form['t']
		week = request.form['w']
		ndir = request.form['n']

		i = fetchID(teacher, role="teacher")
		obj = api.Teacher(usr = teacher)
		res = obj.DeleteNote(sub= sub, term = term, week = week, ndir = ndir)
		return res
# end of note services

# assignment services
@app.route("/ass/add", methods=['GET', 'POST', 'JSON'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def add_ass():
	if request.method == 'POST':
		teacher = request.form['u']
		sub = request.form['s']
		term = request.form['t']
		week = request.form['w']
		file = request.files['f']

		i = fetchID(teacher, role="teacher")
		filename = secure_filename(file.filename)
		adir = "static/rep/%s/%s/%s/assignments/%s" % (i, sub, term, filename)
		obj = api.Teacher(usr = teacher)
		
		# now for action
		if (i == None):
			return "invalid"
		
		res = obj.UploadAssignment(sub= sub, term = term, week = week, adir = adir)
		
		if (res == 1):
			os.chdir("static/rep/%s/%s/%s/assignments" % (i, sub, term))
			file.save(filename)
			os.chdir(__PATH__)
			return 1
	return 0

@app.route("/ass/comment", methods=['GET', 'POST', 'JSON'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def comment_ass():
	if request.method == 'JSON':
		data = request.get_json()
		obj = api.Teacher(usr = data['usr'])
		res = obj.CommentAssignment(qid = data['qid'], s = data['stud'], comment = data['comment'])
		return res

@app.route("/ass/mark", methods=['GET', 'POST', 'JSON'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def mark_ass():
	if request.method == 'JSON':
		data = request.get_json()
		obj = api.Teacher(usr = data['usr'])
		res = obj.MarkAssignment(qid = data['qid'], s = data['stud'], score = data['score'])
		if (res):
			if ('comment' in data):
				res2 = obj.CommentAssignment(qid = data['qid'], s = data['stud'], comment = data['comment'])
		return res

@app.route("/ass/all", methods=['GET', 'POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_assignments():
	return api.fetchAssignments()

@app.route("/pwd_reset", methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def pwd_reset():
	usr = request.form['user']
	ques = request.form['ques']
	ans = request.form['ans']
	if (account_api.verify_(usr, ques, ans) == True ):
		return redirect("localhost:9000/reset")
	return redirect("localhost:9000/forgot")

@app.route("/ass", methods = ['GET', 'POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_ass():
	# assignment ID
	if (request.method == 'GET'):
		id = request.args['id']
	elif (request.method == 'POST'):
		id = request.form['id']
	return api.fetchAssignment(id)

@app.route("/ass/all/res", methods = ['GET', 'POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_ass_res_all():
	# assignments ID
	if (request.method == 'GET'):
		id = request.args['id']
	elif (request.method == 'POST'):
		id = request.form['id']
	return api.fetchAssignmentResponses(id = id)

@app.route("/ass/res")
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_ass_res_spec():
	# assignments ID
	# students full name
	if (request.method == 'GET'):
		id = request.args['id']
		stud = request.args['stud']
	elif (request.method == 'POST'):
		id = request.form['id']
		stud = request.form['stud']
	return api.fetchAssignmentResponse(id = id, student = stud)

@app.route("/ass/submit", methods = ['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def ass_submit():
	if (request.method == 'POST'):
		qid = request,form['qid']
		usr = request.form['u']
		term = request.form['t']
		file = request.files['f']

		obj = api.Student(usr)
		stud = api.fetchAtt('student', usr).split(",")[1]
		i = fetchID(stud, role="student")
		filename = "%s term %s" % (term, secure_filename(file.filename))

		rdir = "static/rep/student/%s/%s/assignments/%s" % (i, term, filename)

		# now for action
		if (i == None):
			return "invalid"

		res = obj.SubmitAssignment(qid = qid, stud = stud, rdir = rdir)

		if (res == 1):
			os.chdir("static/rep/student/%s/%s/assignments" % (i, term))
			file.save(filename)
			os.chdir(__PATH__)
			return 1
	return 0
# end of assignment service

# teacher user service
@app.route("/teacher/create", methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def create_teacher():
	pwd = request.form['p']
	usr = request.form['u']
	name = request.form['n']
	pp = request.files['pp']
	obj = account_api.Teacher()
	res = obj.Create(name, usr, pwd)
	if (res == 1):
		os.chdir("static/rep/1/pp")
		pp.save(secure_filename(pp.filename))
		os.chdir(__PATH__)
		return res
	return redirect("http://localhost:9000/")

@app.route("/teacher/auth", methods=['GET', 'POST', 'JSON'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def auth_teacher():
	if (request.method == 'GET'):
		usr = request.args['u']
		pwd = request.args['p']
	elif (request.method == 'POST'):
		usr = request.form['u']
		pwd = request.form['p']
	else:
		data = request.get_json()
		usr = data['usr']
		pwd = data['pwd']
	role = "teacher"
	res = jsonify({'id': res[0], 'name': res[1], 'user': res[2], 'pass': res[3], 'sub': res[4]})
	return res

@app.route("/teacher/sub/add", methods=['GET', 'POST', 'JSON'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def add_sub():
	if (request.method == 'GET'):
		usr = request.args['u']
		sub = request.args['s']
	elif (request.method == 'POST'):
		usr = request.form['u']
		sub = request.form['s']
	else:
		data = request.get_json()
		usr = data['usr']
		sub = data['sub']
	obj = account_api.Teacher()
	res = obj.AddSub(usr, sub)
	return res

@app.route("/teacher/<id>/profilepicture/fetch", methods=['GET', 'POST', 'JSON'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def fetch_pp_teacher(id):
	os.chdir("static/rep/%s/pp" % id)
	pp = os.listdir()[0]
	os.chdir(__PATH__)
	return url_for('static', filename="rep/teacher/%s/pp/%s" % (id, pp))

# student user service
@app.route("/student/auth", methods=['GET', 'POST', 'JSON'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def auth_student():
	if (request.method == 'GET'):
		usr = request.args['user']
		pwd = request.args['pass']
		ip  = request.args['ip']
	elif (request.method == 'POST'):
		usr = request.form['user']
		pwd = request.form['pass']
		ip  = request.form['ip']
	else:
		data = request.get_json()
		usr = data['user']
		pwd = data['pass']
		ip  = data['ip']
	role = "student"
	res = account_api.login(usr, pwd, role=role)
	if (res == False):
		return redirect("http://localhost:9000?failure=False")
	else:
		junk = {'id': res[0], 'name': res[1], 'user': res[2], 'pass': res[3], 'class': res[4]}
		t1 = Thread( target = account_api.sendBackground, args = (ip, junk) )
		t1.run()
	return redirect("http://localhost:9000/home_test")

@app.route("/student/create", methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def create_student():
	pwd = request.form['pass']
	usr = request.form['user']
	name = request.form['full']
	_class = request.form['class']
	ass = request.form['ques']
	_s = request.form['ans']
	obj = account_api.Student()
	res = obj.Create(name, usr, pwd, _class, ass, _s)
	if (res == 1):
		info = api.fetchAtt("student", usr).split(",")
		return redirect("http://localhost:9000/login/success")
	return res

@app.route("/student/<id>/profilepicture/fetch", methods=['GET', 'POST', 'JSON'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def fetch_pp_student(id):
	os.chdir("static/rep/student/%s/pp" % id)
	pp = os.listdir()[0]
	os.chdir(__PATH__)
	return url_for('static', filename="rep/student/%s/pp/%s" % (id, pp))
# end of student user service

# misc services
@app.route("/change-<role>-attribute-<node>", methods = ['GET', 'POST', 'JSON'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def changePass(role, node):
	usr = request.form['user']
	val = request.form['pass']
	return account_api.ChangeAtt(usr, node, val, role)

@app.route("/drop/suggestion", methods = ['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def dropSuggestion():
	sug = request.form['suggestion']
	sub = request.form['sub']
	obj = api.Student("anonymous")
	return jsonify(obj.DropSuggestion(suggestion = sug, name = sub))
# end of misc services

# Examination services
@app.route("/set/exam/obj/<sub>/<term>/<_class>")
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def UploadExamQuestionObjective(sub, term, _class):

	file = request.files['f']

	i = fetchID(teacher, role="teacher")
	filename = secure_filename(file.filename)
	edir = "static/rep/%s/%s/%s/exam/%s" % (i, sub, term, filename)
	obj = api.Examination(role = 'teacher')
	
	# now for action
	if (i == 'nil'):
		return "invalid"
	
	res = obj.UploadQuestionObjective(sub = sub, term = term, week = week, edir = edir)
	
	if (res == 1):
		os.chdir("static/rep/%s/%s/%s/exam" % (i, sub, term))
		file.save(filename)
		os.chdir(__PATH__)
		return 1
	return 0

@app.route("/upload/exam/answer/obj/<qid>", methods=['JSON'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def upload_answer_exam_obj(qid):
	data = request.get_json()
	obj = api.Examination(role='teacher')
	return obj.uploadAnswerObjective(qid = qid, data = data)

@app.route("/<student>/submit/exam/obj/<qid>", methods = ['JSON'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def submit_exam_obj(student, qid):
	data = request.get_json()
	obj = api.Examination(role = 'student')
	return obj.TakeExamObjective(qid, data, student)

@app.route("/exam/info/<sub>/<term>/<_class>", methods=['GET', 'POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def exam_info(sub, term, _class):
	return api.fetchExamInfo(sub, term, _class)

@app.route("/exam/<qid>/answer", methods=['GET', 'POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def exam_answer(qid):
	# exam ID
	return api.fetchExamAnswers(qid)

@app.route("/exam/<qid>/theory/answer")
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def exam_theory_answer(qid):
	# exam ID
	return jsonify(api.fetchExamAnswersTheory(qid))


@app.route("/upload/exam/answer/theory/<qid>", methods=['JSON'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def upload_answer_exam_theory(qid):
	# exam ID
	data = request.get_json()
	obj = api.Examination(role='teacher')
	return obj.uploadAnswerTheory(qid = qid, data = data)

@app.route("/<student>/submit/exam/theory/<qid>", methods = ['JSON'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def submit_exam_theory(student, qid):
	# exam ID
	data = request.get_json()
	obj = api.Examination(role = 'student')
	return obj.TakeExamTheory(qid, data, student)

@app.route("/exam/info/theory/<sub>/<term>/<_class>", methods=['GET', 'POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def exam_info_theory(sub, term, _class):
	return api.fetchExamInfoTheory(sub, term, _class)

@app.route("/set/exam/theory/<sub>/<term>/<_class>")
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def UploadExamQuestionTheory(sub, term, _class):

	file = request.files['f']

	i = fetchID(teacher, role="teacher")
	filename = secure_filename(file.filename)
	edir = "static/rep/%s/%s/%s/exam/%s" % (i, sub, term, filename)
	obj = api.Examination(role = 'teacher')
	
	# now for action
	if (i == 'nil'):
		return "invalid"
	
	res = obj.UploadQuestionTheory(sub= sub, term = term, week = week, edir = edir)
	
	if (res == 1):
		os.chdir("static/rep/%s/%s/%s/exam" % (i, sub, term))
		file.save(filename)
		os.chdir(__PATH__)
		return 1
	return 0
# end of exam service

@app.route("/")
def kk():
	for _ in range(3):
		print("dodo is sweet")
	return jsonify("JJJJJJJ")

if __name__ == '__main__':
	app.run(debug = True, host = '0.0.0.0')
