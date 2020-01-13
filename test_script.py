from api import *
# from account_api import *

teacher = Teacher("smones")

report1 = {
    'UploadNote': teacher.UploadNote("physics", 1, 1, "ss3", "static/rep/1/physics/1/notes/my name is Beans.rtf"),
    'DeleteNote': teacher.DeleteNote("physics", 1, 1, "ss3", "static/rep/1/physics/1/notes/my name is Beans.rtf"),
    'UploadAssignment': teacher.UploadAssignment("physics", 1, "ss3", 1, "static/rep/1/physics/1/assignments/my name is Beans.rtf", 10),
    'fetchAssID': teacher.fetchAssID("physics", 1, "ss3", 1)
}

student = Student("Sob")
report2 = {
    'SubmitAssignment': student.SubmitAssignment(1, "Bob Sue", "static/rep/student/1/1/assignments/my name is Beans.rtf"),
    'DropSuggestion': student.DropSuggestion("Bob Sue", "We want more noodles")
}

examObject = Examination(role="student")
report3 = {
	'UploadQuestionObjective': examObject.UploadQuestionObjective("physics", "1", "ss3", "static/rep/1/physics/1/exam/my name is Beans.rtf"),
	'uploadAnswerObjective': examObject.uploadAnswerObjective(1, {1: 'A', 2:'B', 3:'C'}), 
	'TakeExamObjective': examObject.TakeExamObjective(1, {1: 'C',  2:'B', 3:'C'}, 'Sob'),
	'UploadQuestionTheory': examObject.UploadQuestionTheory("physicio", "3", "ss2", "static/rep/1/physics/1/exam/my name is Beans.rtf"),
	'uploadAnswerTheory': examObject.uploadAnswerTheory(1, {1: 'volume temperature constant inversely proportional pressure'}), 
	'TakeExamTheory': examObject.TakeExamTheory(1, {
		1: 'boyles law states that the volume of a fixed mass of a gas is inversely proportional to its pressure'}, 'bob')
	}

report4 = {
    'fetchNotes': fetchNotes(),
    'fetchAssignments': fetchAssignments(),
    'fetchNote': fetchNote(1),
    'fetchAssignment': fetchAssignment(1),
    'fetchAssignmentResponses': fetchAssignmentResponses(1),
    'fetchAssignmentResponse': fetchAssignmentResponse(1, "Bob Sue"),
    'IsSubmitted': IsSubmitted(1, "Bob Sue"),
    'IsNotSubmitted': IsSubmitted(1, "Linda Ikeji"),
    'BuildStandardDateTime': BuildStandardDateTime(),
    'BuildStandardDate': BuildStandardDate(),
    'BuildStandardTime': BuildStandardTime(),
    'fetchExamInfo': fetchExamInfo("physics", 1, "ss3"),
    'fetchExamAnswers': fetchExamAnswers(1),
    'fetchAtt': fetchAtt("Sob")
}

print("~~~~~~~~Test result for test1: teacher student and general~~~~~~~~\n")
for i in report1:
    print(i, report1[i])
for i in report2:
    print(i, report2[i])
for i in report3:
    print(i, report3[i])
for i in report4:
    print(i, report4[i])
