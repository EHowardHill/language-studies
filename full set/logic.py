import os, sqlite3, pprint, random

conn = sqlite3.connect('dict.db')
curs = conn.cursor()

curs.execute('select count(*) from r_ele;')
size = curs.fetchone()[0]

def get_rand_word():
    word = get_word(random.randint(0,size))
    return get_rand_word() if word == None else word

def get_word(loc):
    curs.execute('select reb, keb, pos, gloss, expl from r_ele join sense on r_ele.word_id = sense.word_id join k_ele on k_ele.word_id = r_ele.word_id where r_ele.word_id = ' + str(loc) + ';')
    return curs.fetchone()

pprint.pprint(get_rand_word())