import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Let\'s go to N.Y.!")
for token in doc:
    print(token.text)