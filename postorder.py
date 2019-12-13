import pprint, subprocess

oper = ["-","+","0"," ","is","<",">","%","#",'dim',"=","*",'/','if','then','com',",","repeat","at","remove"]
comm = ["if"]
null = [" ",","]
wait = ["repeat","dim","at","remove"]
f_wt = ["dim"]
global vars

vars = {'true':1, 'false':0}

def parse(input):
    data = []
    last_loc = None
    sub = False
    num = False
    nam = ""
    val = 0
    deep = 0
    p = 1
    t = 0

    while t < len(input):

        temp = input[t]
        if temp == "(":
            deep += 1

        if deep == 0:
            if temp.isdigit():
                if not num and len(nam) > 1:
                    data.append(nam)
                num = True
                nam = ""
                val = val * p + int(temp)
                p = p * 10
            else:
                if temp in oper:
                    if val != 0:
                        data.append(val)
                    if nam != "":
                        data.append(nam)
                        nam = ""
                    if temp not in null:
                        data.append(temp)
                else:
                    if val > 0:
                        nam += str(val)
                    nam += input[t]
                num = False
                val = 0
                p = 1
        else:
            nam += temp

        if temp == ")":
            deep -= 1

        t += 1

    if len(nam) > 1:
        data.append(nam)
    elif val != 0 and val is not None:
        data.append(val)

    if last_loc == None:
        return data
    else:
        return data[:last_loc-1]

def process(data):
    a = None
    t = 0
    v1 = [None,None]
    v2 = [None,None]

    while len(data) > t:
        sl = None
        ty = None
        o1 = None
        op = None
        #print(str(data) + "\t" + str(t) + "\t" + str(v1) + "\t" + str(v2))

        a = data.pop(t)
        str_a = str(a)

        if a in oper:
            v3 = None
            v4 = None

            if v1[0] == 1:
                v3 = vars[v1[1]]
            elif v1[0] == 3 and a not in wait:
                v3 = process(parse(v1[1][1:-1]))
            else:
                v3 = v1[1]

            if v2[0] == 1:
                v4 = vars[v2[1]]
            elif v2[0] == 3 and a not in f_wt:
                v4 = process(parse(v2[1][1:-1]))
            else: v4 = v2[1]

            if a == '+':
                sl = v3 + v4
            elif a == "-":
                sl = v3 - v4
            elif a == ">":
                sl = 1 if v3 > v4 else 0
            elif a == "<":
                sl = 1 if v3 < v4 else 0
            elif a == "%":
                sl = v3 % v4
            elif a == "*":
                sl = v3 * v4
            elif a == '/':
                sl = v3 / v4
            elif a == "=":
                sl = None
                vars[v1[1]] = v4
            elif a == "is":
                sl = 1 if v3 == v4 else 0
            elif a == "at":
                sl = parse(v3[1:-1])[v4]
            elif a == "remove":
                i = parse(v3[1:-1])
                del i[v4]
                sl = i
                print(sl)
            elif a == "push":
                i = parse(v3[1:-1]).insert(v4)
                sl = i
            elif a == "dim":
                sl = None
                vars[v1[1]] = v4
            elif a == "then":
                sl = None
                if v3 != v4:
                    t = len(data)
            elif a == "repeat":
                for i in range(v4):
                    sl = process(parse(v1[1][1:-1]))
            elif a == "com":
                sl = None
                out = None
                v3 = v3[1:-1]
                if v2[0] == 2: v4 = v4[1:-1]

                if v4 == None or v4 == "]":
                    out = subprocess.call(v3)
                else:
                    out = subprocess.call([v3,str(v4)])

                if str(out) == out:
                    sl = "[" + out + "]"
                else:
                    sl = out

            v1 = [None,None]
            v2 = [None,None]

        else:
            type = 0

            if str(a) == a:
                if a[0] == "[" and a[-1] == "]": type = 2
                if a[0] == "(" and a[-1] == ")": type = 3
                if a in vars: type = 1

            if v1[1] is None:
                v1[0] = type
                v1[1] = a
            elif v2[1] is None:
                v2[0] = type
                v2[1] = a
            else:
                data.insert(t,a)
                data.insert(t,v2[1])
                data.insert(t,v1[1])
                t += 1
                v1 = [None,None]
                v2 = [None,None]
                
        if sl != None:
            data.insert(t,sl)
            t = 0

    print(vars)
    return a

    #return vars

# -----

raw = """


"""

raw = raw.replace('\n','').replace('\t','')
lines = []

for input in raw.split(';'):
    x = parse(input)
    print(x)
    lines.append(x)

line = 0
for data in lines:
    process(data)
    line += 1