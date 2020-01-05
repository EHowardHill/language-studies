val = 9

for t in range(1,100):
    s = []
    n = t
    while n > 0:
        if len(s) > 2:
            if s[1] < 5 and s[2] < 5:
                while(n % val) < 5:
                    n += 1
                    t += 1
        s.append(n % val)
        n = int(n / val)
    print(str(t) + "\n" + str(s))