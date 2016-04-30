import cPickle as pickle

l = pickle.load(open('unigram_500000_sorted_list.pickle','rb'))

def i_of(word):
    count = 0
    for w, score in l:
        if w == word:
            return count
        count += 1

print i_of('actly')


