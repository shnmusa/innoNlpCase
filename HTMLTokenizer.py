# Clears punctiations and stopwords then gives list of tokens

import re
import nltk
import trafilatura
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class Tokenizer:

    def __init__(self):
        self.stopwords = set(stopwords.words('german') +
        stopwords.words('english') + stopwords.words('spanish') + 
        stopwords.words('italian') + stopwords.words('french'))
        self.tokenizer = nltk.RegexpTokenizer(r"\w+")

    def cleanAndTokenize (self, text):
        text = re.sub(r'\d+', '', text)
        tokenized = self.tokenizer.tokenize(text)
        return [token for token in tokenized if token not in self.stopwords and len(token)>1]

    def getTextFromHtmlFile(self, file):
        text = open('20sites-html/' + file).read().lower()
        text = trafilatura.extract(text)
        if text is None:
            return None
        return text.replace("\n", " ").replace("\'", "")
