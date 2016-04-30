from google_ngram_downloader import readline_google_store
import re
import numpy as np
import cPickle as pickle
p = re.compile('^[a-z]*$',re.IGNORECASE)


el = 'bcdefghijklmnopqrstuvwxyz'

for l in el:
    fname, url, records = next(readline_google_store(ngram_len=1,indices=l))
    unigrams = {}
    count = 0
    for r in records:
        w = r.ngram.lower()
        if p.match(w):
            if w in unigrams:
                unigrams[w] += np.array([r.match_count,r.volume_count])
            else:
                unigrams[w] = np.array([r.match_count,r.volume_count])
    with open(str(l)+'_unigram_dict.pickle','w') as f:
        pickle.dump(unigrams,f)        
    

