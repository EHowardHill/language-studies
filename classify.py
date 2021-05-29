import nltk.data, pprint, re, spacy
nlp = spacy.load('en_core_web_lg')

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

text = '“Well,” asked a voice nearby. He cleared his throat. “You going to say something?” Her eyes flew open and her hands instinctively folded in front of her. “I.. Good morning.”'
text = re.sub('[“”]', '"', text)
n = nltk.sent_tokenize(text)

for sent in n:
    print("\n\n")
    print(sent)
    doc=nlp(sent)

    sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj") ]

    print(sub_toks) 