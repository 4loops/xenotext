import cPickle as pickle
import numpy as np

##primaries = pickle.load(open('partials_unigram_min.pickle','rb'))
#unigrams  = pickle.load(open('unigram_500000_sorted_list.pickle','rb'))
#primaries = pickle.load(open('100000_words_partials_unigram_min.pickle','rb'))
##
#
#print 'sorting...'
#primaries = sorted(primaries.items(),key=lambda x: x[1][0],reverse=True)
#primaries = primaries[:1024*256]
#print 'sorted. saving list'
#pickle.dump(primaries,open('1024_256_primaries_sorted_list.pickle','wb'))
primaries = pickle.load(open('test_1024_primaries.pickle','rb'))
#primaries = pickle.load(open('1024_256_primaries_sorted_list.pickle','rb'))
primaries = primaries[:1024]

el = 'abcdefghijklmnopqrstuvwxyz'
npel = np.array(list(el))

def w2numpy(w):
    n = np.zeros((len(w),26),dtype=bool)
    i = 0
    for l in w:
        n[i][el.index(l)] = True
        i += 1
    return n

def numpy2w(n):
    w = ''
    for l in n:
        c =  npel[l.astype(bool)]
        if len(c) == 1:
            w += c[0]
        else:
            w += '?'
    return w

def encipher(c,w):
    return numpy2w(w2numpy(w).dot(c))


def score_cipher(cipher):
    uni_dict = {}
    c = np.unpackbits(np.array(buffer(cipher)))[:26*26].reshape((26,26))
    total = 0
    for w,score in unigrams:
        wx = encipher(c,w)
        if len(wx) == len(w) and wx in uni_dict:
            print w, wx, score
            total += score
        uni_dict[w] = score
    print '\n\nTOTAL SCORE: ', total

def decompose(cipher):
    return np.where(cipher)

def single_compatable(single):
    compatable = []
    incompatable = []
    a, b = single
    for x in range(26):
        for y in range(x+1,26):
            if (a != x and b != y and a != y and b != x) or (a == x and b == y):
                compatable.append((x,y))
            else:
                incompatable.append((x,y))
    return compatable, incompatable

#def single_incompatable(single):
#    result = []
#    for y in range(single[0]+1,26):
#        result.append(single[0],y)
#    for x in range(0,single[1]):
#        result.append(x,single[1])
#    return result

#for cipher, scr in l[:5]:
#    score(cipher)
#    print 'advertised score:',scr


#returns the minimum score for a cipher (the sum of the primaries it contains)
def min_score(c):
    m_vec = np.zeros(p_dim[(0,8)].shape,dtype=bool) #default because a=i is common 
    xs, ys = decompose(c)
    for x,y in zip(xs,ys):
        if x < y:
            m_vec = np.logical_or(m_vec,p_dim[(x,y)])
    m_vec = np.all(m_vec,axis=1)
    return np.dot(s_vec,m_vec)

def max_score(c):
    xs, ys = decompose(c)
    pairs = zip(xs,ys)
    c_vec = single_ciphers_c[pairs[0]]
    for x,y in pairs[1:]:
        if x<y:
            c_vec = np.logical_and(c_vec,single_ciphers_c[(x,y)])
    return np.dot(c_vec,s_vec)

def cipher_key(c):
    return str(np.packbits(c).data)

def cipher_unkey(key):
    return np.unpackbits(np.array(buffer(key)))[:26*26].reshape((26,26)).astype(bool)

def validCipher(c):
    if np.any(np.diag(c)) or np.any(np.sum(c,axis=0)>1) or np.any(np.sum(c,axis=1)>1):
        return False
    return True

def is_compatable(c1,c2):
    c = np.logical_or(c1,c2)
    return validCipher(c)

max_primary_size = reduce(lambda p1, p2: max(p1, np.sum(cipher_unkey(p2[0]))/2), primaries, 0)

s_vec = np.zeros(len(primaries))
single_ciphers_parent = {}
p_dim = {}
for x in range(26):
    for y in range(x+1,26):
        single_ciphers_parent[(x,y)] = np.zeros(len(primaries),dtype=bool)
        p_dim[(x,y)] = np.zeros((len(primaries),max_primary_size),dtype=bool)

#decompose primaries
for index, p in enumerate(primaries):
    s_vec[index] = p[1][0]
    xs,ys = decompose(cipher_unkey(p[0]))
    num_pairings = len(xs)/2
    i = 0
    for x,y in zip(xs,ys):
        if x < y:
            single_ciphers_parent[(x,y)][index] = True
            p_dim[(x,y)][index][i] = True
            i += 1
            p_dim[(x,y)][index][num_pairings:] = True

single_ciphers_c = {}
for single_cipher in single_ciphers_parent:
    single_ciphers_c[single_cipher] = np.copy(single_ciphers_parent[single_cipher])
    compat, incompat = single_compatable(single_cipher)
    print '\n\n',single_cipher
    print incompat
    for comp in compat:
        single_ciphers_c[single_cipher] = np.logical_or(single_ciphers_c[single_cipher],single_ciphers_parent[comp])  
    for inco in incompat:
        single_ciphers_c[single_cipher] = np.logical_and(single_ciphers_c[single_cipher],np.logical_not(single_ciphers_parent[inco]))

#print 'checking compatibility vector'
#for x,y in single_ciphers_c:
#    c = np.zeros((26,26),dtype=bool)
#    c[x][y] = True
#    c[y][x] = True
#    for index, (key, _) in enumerate(primaries):
#        if single_ciphers_c[(x,y)][index] != is_compatable(c,cipher_unkey(key)):
#            print 'PROBLEM!', x, y,single_ciphers_c[(x,y)][index], decompose(cipher_unkey(key))


#first beam 
beam = []
for x,y in single_ciphers_c:
    c = np.zeros((26,26),dtype=bool)
    c[x][y] = True
    c[y][x] = True
    key = str(np.packbits(c).data)
    beam.append((key,(np.packbits(c),(min_score(c),max_score(c)))))

beam = sorted(beam, key=lambda x:x[1][1],reverse=True)

def compatable(c):
    result = []
    indices = np.where(np.logical_not(np.any(c,axis=0)))
    for x in indices[0]:
        for y in indices[0]:
            if x < y:
                result.append((x,y))
    return result 

def beam_size(n):
    return 1024
    #max_beam = 1024*325
    #m = 13-n
    #mul_factor = m*(m+1)/2
    #return max_beam/mul_factor

def human_cipher(c):
    x,y = np.where(c)
    for i in range(len(x)):
        if x[i] < y[i]:
            print el[x[i]],el[y[i]]

count = 1
while not np.all(np.any(cipher_unkey(beam[0][0]),axis=0)):
    print 'starting beam number', count
    print 'best partial:', beam[0]
    beam = beam[:beam_size(count)]
    count += 1
    next_beam = {}
    for old_key, (comp,_) in beam:
        c = np.unpackbits(np.array(buffer(old_key)))[:26*26].reshape((26,26)).astype(bool)
        for x,y in compatable(c):
            new_c = np.copy(c)
            new_c[x][y] = True
            new_c[y][x] = True
            new_key = str(np.packbits(new_c).data)
            if new_key not in next_beam:
                #new_comp = np.logical_and(np.unpackbits(comp),single_ciphers_c[(x,y)]) 
                #next_beam[new_key] = (new_comp, np.sum(new_comp))
                next_beam[new_key] = (min_score(new_c),max_score((new_c)))
                #next_beam[new_key] = (np.packbits(new_comp), np.dot(s_vec,new_comp))
    beam = sorted(next_beam.items(),key=lambda x:x[1][1],reverse=True)
    beam = sorted(beam,key=lambda x:x[1][0],reverse=True)
    print 'length of full beam:', len(beam)
    




