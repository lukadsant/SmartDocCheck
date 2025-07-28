import spacy

nlp = spacy.load('pt_core_news_sm')


print('Labels disponíveis:')
for label in nlp.get_pipe('ner').labels:
    print(label)
