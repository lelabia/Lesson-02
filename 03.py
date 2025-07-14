import spacy


nlp = spacy.load("fr_core_news_sm")
lemmatizer = nlp.get_pipe("lemmatizer")
print(lemmatizer.mode) 

doc = nlp("Pour comprendre l\' IA sans bullshit. Le Lab IA coupe a travers le brouillard marketing.")
print([token.lemma_ for token in doc])
