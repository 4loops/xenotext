import cPickle as pickle

unigrams = {}

el = 'abcdefghijklmnopqrdtuvwxyz'

for l in el:
    l_dict = pickle.load(open(str(l)+'_unigram_dict.pickle','rb'))
    print l, len(l_dict)
    unigrams.update(l_dict)
