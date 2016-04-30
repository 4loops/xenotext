import cPickle as pickle
dic = pickle.load(open('all_unigrams_dict.pickle','rb'))
total_list = sorted(dic.items(), key=lambda x:x[1][1],reverse=True)
pickle.dump(total_list,open('all_unigrams_sorted_list.pickle','wb'))
