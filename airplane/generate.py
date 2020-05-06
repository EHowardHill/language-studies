import pymongo, pprint, sqlite3, os

sq = sqlite3.connect('./master_dict.db')
curs = sq.cursor()
curs.execute("select kana, kanji, english from dictionary order by jlpt desc;")
dictionary = [[x[0],x[1],x[2]] for x in curs.fetchall()]

ms = sqlite3.connect('./master.db')
curz = ms.cursor()

ent_seq = []
example = []
prev_done = []
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.admin.jisho

tags = {
    "&MA;": "martial arts term",
    "&X;": "rude or X-rated term (not displayed in educational software)",
    "&abbr;": "abbreviation",
    "&adj-i;": "adjective (keiyoushi)",
    "&adj-ix;": "adjective (keiyoushi) - yoi/ii class",
    "&adj-na;": "adjectival nouns or quasi-adjectives (keiyodoshi)",
    "&adj-no;": "nouns which may take the genitive case particle `no'",
    "&adj-pn;": "pre-noun adjectival (rentaishi)",
    "&adj-t;": "`taru' adjective",
    "&adj-f;": "noun or verb acting prenominally",
    "&adv;": "adverb (fukushi)",
    "&adv-to;": "adverb taking the `to' particle",
    "&arch;": "archaism",
    "&ateji;": "ateji (phonetic) reading",
    "&aux;": "auxiliary",
    "&aux-v;": "auxiliary verb",
    "&aux-adj;": "auxiliary adjective",
    "&Buddh;": "Buddhist term",
    "&chem;": "chemistry term",
    "&chn;": "children's language",
    "&col;": "colloquialism",
    "&comp;": "computer terminology",
    "&conj;": "conjunction",
    "&cop;": "copula",
    "&ctr;": "counter",
    "&derog;": "derogatory",
    "&eK;": "exclusively kanji",
    "&ek;": "exclusively kana",
    "&exp;": "expressions (phrases, clauses, etc.)",
    "&fam;": "familiar language",
    "&fem;": "female term or language",
    "&food;": "food term",
    "&geom;": "geometry term",
    "&gikun;": "gikun (meaning as reading) or jukujikun (special kanji reading)",
    "&hon;": "honorific or respectful (sonkeigo) language",
    "&hum;": "humble (kenjougo) language",
    "&iK;": "word containing irregular kanji usage",
    "&id;": "idiomatic expression",
    "&ik;": "word containing irregular kana usage",
    "&int;": "interjection (kandoushi)",
    "&io;": "irregular okurigana usage",
    "&iv;": "irregular verb",
    "&ling;": "linguistics terminology",
    "&m-sl;": "manga slang",
    "&male;": "male term or language",
    "&male-sl;": "male slang",
    "&math;": "mathematics",
    "&mil;": "military",
    "&n;": "noun (common) (futsuumeishi)",
    "&n-adv;": "adverbial noun (fukushitekimeishi)",
    "&n-suf;": "noun, used as a suffix",
    "&n-pref;": "noun, used as a prefix",
    "&n-t;": "noun (temporal) (jisoumeishi)",
    "&num;": "numeric",
    "&oK;": "word containing out-dated kanji",
    "&obs;": "obsolete term",
    "&obsc;": "obscure term",
    "&ok;": "out-dated or obsolete kana usage",
    "&oik;": "old or irregular kana form",
    "&on-mim;": "onomatopoeic or mimetic word",
    "&pn;": "pronoun",
    "&poet;": "poetical term",
    "&pol;": "polite (teineigo) language",
    "&pref;": "prefix",
    "&proverb;": "proverb",
    "&prt;": "particle",
    "&physics;": "physics terminology",
    "&quote;": "quotation",
    "&rare;": "rare",
    "&sens;": "sensitive",
    "&sl;": "slang",
    "&suf;": "suffix",
    "&uK;": "word usually written using kanji alone",
    "&uk;": "word usually written using kana alone",
    "&unc;": "unclassified",
    "&yoji;": "yojijukugo",
    "&v1;": "Ichidan verb",
    "&v1-s;": "Ichidan verb - kureru special class",
    "&v2a-s;": "Nidan verb with 'u' ending (archaic)",
    "&v4h;": "Yodan verb with `hu/fu' ending (archaic)",
    "&v4r;": "Yodan verb with `ru' ending (archaic)",
    "&v5aru;": "Godan verb - -aru special class",
    "&v5b;": "Godan verb with `bu' ending",
    "&v5g;": "Godan verb with `gu' ending",
    "&v5k;": "Godan verb with `ku' ending",
    "&v5k-s;": "Godan verb - Iku/Yuku special class",
    "&v5m;": "Godan verb with `mu' ending",
    "&v5n;": "Godan verb with `nu' ending",
    "&v5r;": "Godan verb with `ru' ending",
    "&v5r-i;": "Godan verb with `ru' ending (irregular verb)",
    "&v5s;": "Godan verb with `su' ending",
    "&v5t;": "Godan verb with `tsu' ending",
    "&v5u;": "Godan verb with `u' ending",
    "&v5u-s;": "Godan verb with `u' ending (special class)",
    "&v5uru;": "Godan verb - Uru old class verb (old form of Eru)",
    "&vz;": "Ichidan verb - zuru verb (alternative form of -jiru verbs)",
    "&vi;": "intransitive verb",
    "&vk;": "Kuru verb - special class",
    "&vn;": "irregular nu verb",
    "&vr;": "irregular ru verb, plain form ends with -ri",
    "&vs;": "noun or participle which takes the aux. verb suru",
    "&vs-c;": "su verb - precursor to the modern suru",
    "&vs-s;": "suru verb - special class",
    "&vs-i;": "suru verb - included",
    "&kyb;": "Kyoto-ben",
    "&osb;": "Osaka-ben",
    "&ksb;": "Kansai-ben",
    "&ktb;": "Kantou-ben",
    "&tsb;": "Tosa-ben",
    "&thb;": "Touhoku-ben",
    "&tsug;": "Tsugaru-ben",
    "&kyu;": "Kyuushuu-ben",
    "&rkb;": "Ryuukyuu-ben",
    "&nab;": "Nagano-ben",
    "&hob;": "Hokkaido-ben",
    "&vt;": "transitive verb",
    "&vulg;": "vulgar expression or word",
    "&adj-kari;": "`kari' adjective (archaic)",
    "&adj-ku;": "`ku' adjective (archaic)",
    "&adj-shiku;": "`shiku' adjective (archaic)",
    "&adj-nari;": "archaic/formal form of na-adjective",
    "&n-pr;": "proper noun",
    "&v-unspec;": "verb unspecified",
    "&v4k;": "Yodan verb with `ku' ending (archaic)",
    "&v4g;": "Yodan verb with `gu' ending (archaic)",
    "&v4s;": "Yodan verb with `su' ending (archaic)",
    "&v4t;": "Yodan verb with `tsu' ending (archaic)",
    "&v4n;": "Yodan verb with `nu' ending (archaic)",
    "&v4b;": "Yodan verb with `bu' ending (archaic)",
    "&v4m;": "Yodan verb with `mu' ending (archaic)",
    "&v2k-k;": "Nidan verb (upper class) with `ku' ending (archaic)",
    "&v2g-k;": "Nidan verb (upper class) with `gu' ending (archaic)",
    "&v2t-k;": "Nidan verb (upper class) with `tsu' ending (archaic)",
    "&v2d-k;": "Nidan verb (upper class) with `dzu' ending (archaic)",
    "&v2h-k;": "Nidan verb (upper class) with `hu/fu' ending (archaic)",
    "&v2b-k;": "Nidan verb (upper class) with `bu' ending (archaic)",
    "&v2m-k;": "Nidan verb (upper class) with `mu' ending (archaic)",
    "&v2y-k;": "Nidan verb (upper class) with `yu' ending (archaic)",
    "&v2r-k;": "Nidan verb (upper class) with `ru' ending (archaic)",
    "&v2k-s;": "Nidan verb (lower class) with `ku' ending (archaic)",
    "&v2g-s;": "Nidan verb (lower class) with `gu' ending (archaic)",
    "&v2s-s;": "Nidan verb (lower class) with `su' ending (archaic)",
    "&v2z-s;": "Nidan verb (lower class) with `zu' ending (archaic)",
    "&v2t-s;": "Nidan verb (lower class) with `tsu' ending (archaic)",
    "&v2d-s;": "Nidan verb (lower class) with `dzu' ending (archaic)",
    "&v2n-s;": "Nidan verb (lower class) with `nu' ending (archaic)",
    "&v2h-s;": "Nidan verb (lower class) with `hu/fu' ending (archaic)",
    "&v2b-s;": "Nidan verb (lower class) with `bu' ending (archaic)",
    "&v2m-s;": "Nidan verb (lower class) with `mu' ending (archaic)",
    "&v2y-s;": "Nidan verb (lower class) with `yu' ending (archaic)",
    "&v2r-s;": "Nidan verb (lower class) with `ru' ending (archaic)",
    "&v2w-s;": "Nidan verb (lower class) with `u' ending and `we' conjugation (archaic)",
    "&archit;": "architecture term",
    "&astron;": "astronomy, etc. term",
    "&baseb;": "baseball term",
    "&biol;": "biology term",
    "&bot;": "botany term",
    "&bus;": "business term",
    "&econ;": "economics term",
    "&engr;": "engineering term",
    "&finc;": "finance term",
    "&geol;": "geology, etc. term",
    "&law;": "law, etc. term",
    "&mahj;": "mahjong term",
    "&med;": "medicine, etc. term",
    "&music;": "music term",
    "&Shinto;": "Shinto term",
    "&shogi;": "shogi term",
    "&sports;": "sports term",
    "&sumo;": "sumo term",
    "&zool;": "zoology term",
    "&joc;": "jocular, humorous term",
    "&anat;": "anatomical term",
    "&Christn;": "Christian term",
    "&net-sl;": "Internet slang",
    "&dated;": "dated term",
    "&hist;": "historical term",
    "&lit;": "literary or formal term",
    "&litf;": "literary or formal term",
    "&surname;": "family or surname",
    "&place;": "place name",
    "&unclass;": "unclassified name",
    "&company;": "company name",
    "&product;": "product name",
    "&work;": "work of art, literature, music, etc. name",
    "&person;": "full name of a particular person",
    "&given;": "given name or forename, gender not specified",
    "&station;": "railway station",
    "&organization;": "organization name"
}

bigboi = """
<html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    
        <style>

            .note {
                color:darkgray;
                font-weight: bold;
                font-size: smaller;
            }

            .block {
                margin: 10px;
            }

            body {
                font-size: smaller;
            }

        </style>
    
    </head>
    <body>
"""

bit = """
        <div style="margin: 24px;" class="row">
            <div class="col-xs-4">
                <div class="block" style="font-size: xx-large;">
                    <ruby>
                        @keb
                        <rt>@reb</rt>
                    </ruby>
                </div>
            </div>
            <div class="col-xs-4">
                <div class="block">
                    <div class="note">
                        @pos, @misc
                    </div>
                    <div>
                        @gloss
                    </div>
                    <div>
                        Alternate Kanji: @alternate-kanji
                    </div>
                </div>
            </div>
            <div class="col-xs-4">
                <div class="block">
                    @sentence-jp<br>
                    @sentence-en
                </div>
            </div>
        </div>
"""

#query = {"r_ele" : {"reb" : "あからさま"}}

for word in dictionary:
    temp = ''

    try:
        if word[1] != '':
            if word[1] not in prev_done:
                prev_done.append(word[1])
                docs = db.find({"k_ele" : {'$elemMatch': { "keb" : word[1]}}})
                if docs.count() == 0: docs = db.find({"k_ele" : { "keb" : word[1]}})
                for doc in docs:
                    if doc['ent_seq'] not in ent_seq:
                        ent_seq.append(doc['ent_seq'])
                        temp += """
                        <div style="margin: 24px; width:100%;" class="row">
                            <div class="col-xs-4" style="min-width: 100px">
                                <div class="block" style="font-size: xx-large;">
                                    <ruby>
                                        @keb
                                        <rt>@reb</rt>
                                    </ruby>
                                </div>
                            </div>
                        """.replace('@keb',word[1]).replace('@reb',word[0])

                        temp += """
                            <div class="block" style="min-width:40%;">
                                <ul>
                                """
                        
                        temp += """
                                    <li>
                                        @gloss
                                    </li>
                        """.replace('@gloss',word[2].replace(',','; '))

                        for entry in doc['sense']:
                            try:
                                e = entry['gloss']
                                try:
                                    m = entry['misc']
                                    p = entry['pos']
                                    mp = (
                                            tags[m] if isinstance(m,str) else '; '.join([tags[t] for t in m])
                                            + ' - '
                                            + p if isinstance(p,str) else '; '.join(p))
                                except:
                                    mp = ''

                                temp += """
                                        <li>
                                            <div class="note">
                                                @note
                                            </div>
                                            @gloss
                                        </li>
                                """.replace('@gloss',e if isinstance(e,str) else '; '.join(e)).replace('@note',mp)
                            except:
                                pass
                        
                        temp += """
                                </ul>
                            </div>
                        """

                        curz.execute("""select l.id, text from
                                        (select * from links where id = (select id from sentences where language = 'jpn' and text like '%?%' limit 1)) l
                                        left join
                                        (select * from sentences where language = 'eng' or language = 'jpn') b
                                        on l.link = b.id or l.id = b.id
                                        where text is not null
                                        group by language""".replace('?',word[1]))
                        ex = curz.fetchall()

                        if ex[0][0] not in example:
                            example.append(ex[0][0])

                            temp += """
                        <div class="col-xs-4">
                            <div class="block">
                                @sentence-jp<br>
                                @sentence-en
                            </div>
                        </div>
                            """.replace('@sentence-jp',ex[1][1]).replace('@sentence-en',ex[0][1])

                        temp += '</div>'

        else:
            if word[0] not in prev_done:
                prev_done.append(word[0])
                docs = db.find({"r_ele" : {'$elemMatch': { "reb" : word[0]}}})
                if docs.count() == 0: docs = db.find({"r_ele" : { "reb" : word[0]}})
                for doc in docs:
                    if doc['ent_seq'] not in ent_seq:
                        ent_seq.append(doc['ent_seq'])
                        temp += """
                        <div style="margin: 24px;" class="row">
                            <div class="col-xs-4">
                                <div class="block" style="font-size: xx-large;">
                                    <ruby>
                                        @reb
                                    </ruby>
                                </div>
                            </div>
                        """.replace('@reb',word[0])

                        temp += """
                            <div class="block" style="min-width:40%;">
                                <ul>
                                """
                        
                        temp += """
                                    <li>
                                        @gloss
                                    </li>
                        """.replace('@gloss',word[2].replace(',','; '))

                        for entry in doc['sense']:
                            try:
                                e = entry['gloss']
                                try:
                                    m = entry['misc']
                                    p = entry['pos']
                                    mp = (
                                            tags[m] if isinstance(m,str) else '; '.join([tags[t] for t in m])
                                            + ' - '
                                            + p if isinstance(p,str) else '; '.join(p))
                                except:
                                    mp = ''

                                temp += """
                                        <li>
                                            <div class="note">
                                                @note
                                            </div>
                                            @gloss
                                        </li>
                                """.replace('@gloss',e if isinstance(e,str) else '; '.join(e)).replace('@note',mp)
                            except:
                                pass
                        
                        temp += """
                                </ul>
                            </div>
                        """

                        curz.execute("""select l.id, text from
                                        (select * from links where id = (select id from sentences where language = 'jpn' and text like '%?%' limit 1)) l
                                        left join
                                        (select * from sentences where language = 'eng' or language = 'jpn') b
                                        on l.link = b.id or l.id = b.id
                                        where text is not null
                                        group by language""".replace('?',word[1]))
                        ex = curz.fetchall()

                        if ex[0][0] not in example:
                            example.append(ex[0][0])

                            temp += """
                        <div class="col-xs-4">
                            <div class="block">
                                @sentence-jp<br>
                                @sentence-en
                            </div>
                        </div>
                            """.replace('@sentence-jp',ex[1][1]).replace('@sentence-en',ex[0][1])

                        temp += '</div>'
                        bigboi += temp
    except Exception as e:
        print(str(e))
        pass

with open('cache.html', 'w', encoding='utf8') as file:
    file.write(bigboi)

    """

    docs = db.find({"r_ele" : {'$elemMatch': { "reb" : "あからさま"}}})
    if docs.count() == 0: docs = db.find({"r_ele" : { "reb" : "あからさま"}})

    if docs.count() > 0:
    """

"""
for doc in docs:
    pprint.pprint(doc)
"""