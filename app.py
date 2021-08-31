from flask import Flask, render_template, request,jsonify, redirect, url_for
import psycopg2 
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "SkillChen_Secret_Key"

DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "sampledb"
DB_USER = "postgres"
DB_PASS = "dba"

conn = psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)

@app.route("/")
def index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("select distinct office from employee order by office asc")
    empoffice = cur.fetchall()
    print(empoffice)
    return render_template("index.html",empoffice=empoffice)

@app.route("/fetchrecords", methods=["POST","GET"])
def fetchrecords():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        query = request.form['query']
        if query == '':
            cur.execute("select * from employee order by id desc")
            employeelist = cur.fetchall()        
        else:
            search_text = request.form['query']
            cur.execute("select * from employee where office in (%s) order by id desc",[search_text])
            employeelist = cur.fetchall()
    return jsonify({'htmlresponse': render_template('response.html', employeelist=employeelist)})

if __name__ == '__main__':
    app.run(debug=True)