from flask import *
from flask_cors import CORS, cross_origin
import csv
import os

app = Flask(__name__)
path = os.path.realpath("")
CORS(app)

@app.route("/add", methods=['JSON', 'POST'])
@cross_origin()
def AddRow():
    row = [data[i] for i in data]
    with open("db.csv", "a") as writeFile:
        pen = csv.writer(writeFile)
        pen.writerow([i for i in row])
        return jsonify("yes")
    return jsonify("no")

def Eval(score):
    retro = {'F9': [i for i in range(40)], 'E8': [i for i in range(40, 50)], 'D7': [i for i in range(50, 60)],
              'C6': [i for i in range(60, 65)], 'C5': [i for i in range(65, 70)], 'C4': [i for i in range(70, 75)],
              'B3': [i for i in range(75, 80)], 'B2': [i for i in range(80, 85)], 'A1': [i for i in range(85, 100)]}
    for j in retro:
        if (int(score) in retro[j]):
            return j
        else:
            print(j)

@app.route("/grade", methods=['GET', 'POST', 'JSON'])
def actionGrade():
    if request.method =='GET':
        sub = request.args['sub']
        _class = request.args['class']
        score = request.args['score']
    if request.method =='POST':
        sub = request.form['sub']
        _class = request.form['class']
        score = request.form['score']
    if request.method =='JSON':
        data = get_json()
        sub = data['sub']
        _class = data['class']
        score = data['score']
    return "Subject:%s Class:%s Score:%s Grade:%s" % (sub, _class, score, Eval(score))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)