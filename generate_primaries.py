import numpy as np
import cPickle as pickle

unigrams = pickle.load(open('unigram_500000_sorted_list.pickle','rb'))
unigrams = unigrams[:100000]
el = 'abcdefghijklmnopqrstuvwxyz'
h = '1234567890!@#$%^&*()[]{}=+'
empty = np.array([[False]*26]*26)
def analogue(s):
    index = 0
    analogue = ''
    pairings = {}
    for l in s:
        if l not in pairings:
            pairings[l] = h[index]
            index +=1
        analogue += pairings[l]
    return analogue

def validCipher(c):
    if np.any(np.diag(c)) or np.any(np.sum(c,axis=0)>1) or np.any(np.sum(c,axis=1)>1):
        return False
    return True

def mutuallyEncipher(w1,w2):
    cipher  = np.zeros((26,26),dtype=bool)
    for i in range(len(w1)):
        one = el.index(w1[i])
        two = el.index(w2[i])
        cipher[one][two] = True
        cipher[two][one] = True
    if validCipher(cipher):
        return cipher


an = {}
partials = {}
#partialsWords = {}
#scores = {]
key2 = str(np.packbits(mutuallyEncipher('as','in')).data)
for w,score in unigrams:
    anW = analogue(w)
    if anW in an:
        for w2 in an[anW]:
            part = mutuallyEncipher(w,w2)
            if part is not  None:
                key = str(np.packbits(part).data) #pack bits to reduce memory requirements 8X
                #c = np.unpackbits(np.array(buffer(key)))[:26*26].reshape((26,26)).astype(bool)
                if key in partials:
                    partials[key] +=  score#this will be the minimum, because we are reading each word in a sorted way.
                    #partialsWords[key].add((w,w2))
                    #print partials[key]
                else:
                    partials[key] = np.copy(score)
                    #partialsWords[key] = set()
                    #partialsWords[key].add((w,w2))
                print w,w2
        an[anW].append(w)
        #scores[w] = score
    else:
        an[anW] = []
        an[anW].append(w)
        #scores[w] = score
prefix = '100000_words_'
pickle.dump(partials,open(prefix+'partials_unigram_min.pickle','wb'))
#pickle.dump(partialsWords,open(prefix+'partials_unigram_words.pickle','wb'))
pickle.dump(an,open(prefix+'unigram_analogue.pickle','wb'))


