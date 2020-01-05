import os, sqlite3, pprint, random, json
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

conn = sqlite3.connect('dict.db')
curs = conn.cursor()
curs.execute('select count(*) from r_ele;')
size = curs.fetchone()[0]
conn.close()

def get_rand_word(jlpt,drct):
    word = get_word(random.randint(0,size),jlpt,drct)
    return get_rand_word(jlpt,drct) if word == None else word

def get_word(loc,jlpt,drct):
    conn = sqlite3.connect('dict.db')
    curs = conn.cursor()
    print(drct)
    ordr = "reb, keb, pos, gloss, expl" if drct == '0' else "keb, gloss, pos, reb, expl"

    if jlpt == '0':
        query = ('select ' + ordr + ' from r_ele join sense on r_ele.word_id = sense.word_id join k_ele on k_ele.word_id = r_ele.word_id where r_ele.word_id = ' + str(loc) + ';')
    else:
        query = ('select ' + ordr + ' from r_ele join sense on r_ele.word_id = sense.word_id join k_ele on k_ele.word_id = r_ele.word_id where jlpt >= ' + jlpt + ' order by random() limit 1;')
    curs.execute(query)
    data = curs.fetchone()
    return data
    conn.close()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/fetch_word', methods=['POST'])
def receive_data():
    data = request.get_json()
    resp = get_rand_word(data['jlpt'],data['drct'])
    return jsonify(message=resp)