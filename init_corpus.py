#init_corpus

from parse_pdf import *
from get_pdf import *
from datetime import date
import time
import pickle

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
            with open('corpus.pickle', 'wb') as handle:
              pickle.dump(self.texts,handle)

    def load_corpus(self):  #assumes corpus.pickle exists
        try:
            with open('corpus.pickle','rb') as handle:
                self.texts = pickle.load(handle)
        except:
            print("Error loading pickle object")

    def corpus_size(self):
        return sum([len(self.texts[key]) for key in self.texts])

    @classmethod
    def load(self):
        x = Corpus()
        x.load_corpus()
        return x


