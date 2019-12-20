import os, sqlite3
from flask import Flask, render_template, jsonify
app = Flask(__name__)

conn = sqlite3.connect('dict.db')
curs = conn.cursor()

curs.execute('select id from sense order by id desc limit 1;')
size = curs.fetchone()[0]

print(size)

@app.route('/')
def hello_world():
    return render_template('index.html', size=size)

@app.route('/reset')
def reset():
    return jsonify(status="success")