import spacy

nlp = spacy.load("fr_core_news_sm")
doc = nlp("Jerome Fortias est le fondateur de la chaine Youtube, le lab I.A.")

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)