import os, pprint, nltk, ety

sentence = input("Input sentence to work with: ")

sentence = ''.join([t if t.isalpha() else " " + t for t in sentence])
sentence = sentence.lower()
words = []

print()
for s in sentence.split(' '):
    w = ety.origins(s, recursive=True)
    if w != []:
        words.append([w[-1].word,w[-1].language.name])
    else:
        words.append([s,None])


print(' '.join([t[0] for t in words]))
print(",\n".join([t[1] for t in words if t[1] is not None]))
print("\n")