from HTMLTokenizer import Tokenizer
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
from TextRank import TextRank
import yake
from keybert import KeyBERT
from DocModel import DocModel

file_list = [f for f in listdir('20sites-html') if f.endswith('.txt')]
tokenizer = Tokenizer()

docs = []
print('Html file parsing->')
for path in tqdm(file_list):
    text = tokenizer.getTextFromHtmlFile(path) 
    if text != None:
        docs.append(DocModel(path,text))

print('Tokenization and cleaning->')
for doc in docs:
    doc.setTokens(tokenizer)

fqWords = {}
print('Most frequent 10 words and their accurancies->')
for doc in docs:
    for word in doc.tokens:
        if word not in fqWords.keys():
            fqWords[word] = 1
        else:
            fqWords[word] += 1

mostFqWords = {k: v for k, v in sorted(fqWords.items(), key=lambda item: item[1],reverse=True)[:10]}
print(mostFqWords)

nextToFqWords = {}
print('First 10 words appearing next to the most frequent 10 words and their accurancies->')
for doc in docs:
    for i in range(len(doc.tokens)-1):
        if doc.tokens[i] in mostFqWords.keys():
            if doc.tokens[i+1] not in nextToFqWords.keys():
                nextToFqWords[doc.tokens[i+1]] = 1
            else:
                nextToFqWords[doc.tokens[i+1]] += 1

nextToFqWords = {k: v for k, v in sorted(nextToFqWords.items(), key=lambda item: item[1],reverse=True)[:10]}
print(nextToFqWords)

print('Keyword extraction with Textrank->')
textrank = TextRank()
for doc in tqdm(docs):
    doc.textRank = textrank.getKeywords(doc.tokens)

print('Keyword extraction with yake->')
yake_extractor = yake.KeywordExtractor(stopwords=tokenizer.stopwords)
for doc in tqdm(docs):
    keywords = yake_extractor.extract_keywords(doc.text)
    doc.yake = {key:value for (key,value) in keywords}

print('Keybert downloads necessary models if it is first run')
print('Keyword extraction with keyBert->')
kw_model = KeyBERT()
for doc in tqdm(docs):
    keywords = kw_model.extract_keywords(doc.text, stop_words=tokenizer.stopwords)
    doc.keyBert = {key:value for (key,value) in keywords}

print('Saving keywords to json files')
for doc in tqdm(docs):
    doc.saveToJson()
