import spacy


nlp = spacy.load("en_core_web_sm")
print("Pipeline:", nlp.pipe_names)
doc = nlp("I was reading the paper.")
print("I was reading the paper.")

token = doc[0]  # 'I'
print(token.morph)  # 'Case=Nom|Number=Sing|Person=1|PronType=Prs'
print(token.morph.get("PronType"))  # ['Prs']

token2 = doc[4]  
print(token2.morph)  
print(token2.morph.get("PronType")) 