from HTMLTokenizer import Tokenizer
import json

class DocModel:

    def __init__(self, path, text):
        self.path = path
        self.text = text
        self.tokens = []
        self.textRank = None
        self.yake = None
        self.keyBert = None

    def setTokens(self, tokenizer):
        self.tokens = tokenizer.cleanAndTokenize(self.text)

    def saveToJson(self):
        jsonFileName = self.path.replace('.txt', '')
        result = {'textRank': self.textRank, 'yake': self.yake, 'keyBert': self.keyBert}
        with open('results/' + jsonFileName + '.json', "w") as outfile:
            json.dump(result, outfile, indent=4)
