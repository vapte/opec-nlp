#init_corpus

from parse_pdf import *
from get_pdf import *
from datetime import date
import time
import pickle
import random
import sys

class Corpus():
    def __init__(self):
        self.months = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November',
                'December']

        d = date.today().isoformat().split('-')
        self.month = self.months[int(d[1])-1]
        self.year = d[0]
        self.years = [str(y) for y in range(2001, int(self.year)+1)]
        self.texts = dict()
        self.isSentenceChunked = False

    def download_all(self):
        isFuture = False
        for year in self.years:
            for month in self.months:
                if (month == self.month and year == self.year):
                    isFuture= True
                print(' '.join([month,year]), end='')
                get_pdf(month, year)
                print('...', 'Download time:', end-start,' seconds')
                if isFuture: 
                    break
            if isFuture:
                break

    def extract_all_text(self, withPickle=False):
        isFuture = False
        for year in self.years:
            for month in self.months:
                if (month == self.month and year == self.year):
                    isFuture= True
                print(' '.join([month,year]), end='')
                start = time.time()
                self.texts[month+year] = removeTablesGraphs(parse_pdf(month, year).split())
                end = time.time()
                print('...', 'Extracted in ', end-start,' seconds')
                if isFuture: 
                    break
            if isFuture:
                break

        if withPickle:
            with open('pdfm/corpus.pickle', 'wb') as handle:
              pickle.dump(self.texts,handle)

    def load_corpus(self):  #assumes corpus.pickle exists
        for path in sys.path:
            try:
                with open(path+'/corpus.pickle','rb') as handle:
                    self.texts = pickle.load(handle)
                print("Corpus loaded")
                return 
            except:
                pass
        print("Error loading pickle object")

    def corpus_size(self):
        return sum([len(self.texts[key]) for key in self.texts])

    @classmethod
    def load(self):
        x = Corpus()
        x.load_corpus()
        x.sentence_chunk()
        x.remove_underlines()
        return x


    def remove_underlines(self):    #doesn't work
        if (not self.isSentenceChunked):
            print("Chunk by sentences first")
            return
        for key in self.texts:
            for sentence in self.texts[key]:
                #splitting by a string inherently removes it
                sentence = ''.join(sentence.split('_'))
                assert('_' not in sentence)
        print("Underlines removed")


    def sentence_chunk(self):
        for key in self.texts:
            curr_text = self.texts[key]
            new_text = list()
            curr_sentence = list()
            i = 0

            for i in range(len(curr_text)-1):
                if (curr_text[i-1][-1]!='.'):
                    curr_sentence.append(curr_text[i])
                else:   #at end of setnence
                    new_text.append(' '.join(curr_sentence))
                    curr_sentence= [curr_text[i]]
            self.texts[key] = new_text
        self.isSentenceChunked = True
        print("Corpus chunked into sentences")



    def get_sets(self, proportion):
        #generate training/testing data
        if (not self.isSentenceChunked):
            print("Chunk by sentences first")
            return
        if (proportion<0 or proportion>1):
            print("proportion must be in (0,1)")
        
        real_prop = int((proportion*100)//1)
        subset = [random.randint(0,99) for x in range(real_prop)]
        counter= 0
        training ,test = list(),list()

        for key in self.texts:
            for sentence in self.texts[key]:
                if (counter in subset):
                    training.append(sentence)
                else:
                    test.append(sentence)
                counter = (counter+1)%100
        return training, test

    def search_corpus(self,keyword):
        l = list()
        for key in self.texts:
            for sentence in self.texts[key]:
                if (keyword in sentence): 
                    l.append(sentence)
        return l


def print_list(l):
    for e in l:
        print(e,end='\n\n')


if __name__ == '__main__':
    c = Corpus.load()


