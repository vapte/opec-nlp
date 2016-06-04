from pdf_convert import *
from get_pdf import *
import pickle
import time



#takes in pdf, returns list of strings
def parse_pdf(month, year):
    path = 'output/'+'OPEC_'+month+'_'+year+'.pdf'
    f = pdf2txt(path)
    return f


def removeTablesGraphs(corpus): #list of whole pdf
    '''   Reference Basket  Arabian Light  Dubai  Bonny Light  Saharan Blend  Minas  Tia Juana Light  Isthmus  Other crudes  Brent  WTI US $/b  Mar. 23.70 23.77 23.67 24.35 24.82 25.64 21.08 22.60  24.42 27.27 Apr. 24.38 24.24 24.06 25.43 25.65 27.64 20.79 22.86  25.37 27.37 25.36 24.87 23.84 26.19 26.44 25.65 24.56 25.96  25.89 28.14  Differentials      WTI/Brent  Brent/Dubai 2.85 0.75 2.00 1.31 2.25 2.05 - 5 - \x0c 
    example table '''
    toRemove = []
    for i in range(len(corpus)):
        if (is_in_table(corpus, i)):
            toRemove.append(i)

    corpus_new = list()
    for i in range(len(corpus)):
        if (i in toRemove):
            continue
        else:
            corpus_new.append(corpus[i])
    return corpus_new

def is_in_table(corpus, idx):
    if ('Table' in corpus[idx] or 'Graph' in corpus[idx]):
        return True
    offset = 3
    back_check = [item for item in corpus[idx-offset+1:idx+1] if item.isalpha()]
    front_check = [item for item in corpus[idx:idx+offset] if item.isalpha()]
    if (len(back_check)==0 or len(front_check)==0):
        return True
    return False













