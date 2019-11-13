from nltk.corpus import wordnet

syn = set()  # 유의어
ant = set()  # 반의어
for synset in wordnet.synsets("Worse"):
    for lemma in synset.lemmas():
        syn.add(lemma.name())
        if lemma.antonyms():
            ant.add(lemma.antonyms()[0].name())

print('단어, 품사 : ' + synset.name())
print('의미 : ' + synset.definition())
print('예문 : ' + str(synset.examples()))
print('유의어: ' + str(syn))
print('반의어: ' + str(ant))
