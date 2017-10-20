from __future__ import division
import string
import re
import numpy as np
import matplotlib.pyplot as plt

train_file = 'tweets.train.txt'
test_file = 'tweets.test1.txt'
debug_file_name = 'new.txt'
cities = ('Los_Angeles,_CA', 'San_Francisco,_CA', 'Manhattan,_NY','San_Diego,_CA', 'Houston,_TX', 'Chicago,_IL',
                 'Philadelphia,_PA', 'Toronto,_Ontario', 'Atlanta,_GA','Washington,_DC', 'Orlando,_FL', 'Boston,_MA')


# Initialize a dict of dict
# https://stackoverflow.com/questions/651794/whats-the-best-way-to-initialize-a-dict-of-dicts-in-python
class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


def tokenization(city,tweet):
    #tweet = tweet.lstrip(city)  # remove leading city name
    tweet = re.sub(r'[\W_]', ' ', filter(lambda x: x in string.printable, tweet.lstrip(city))).lower()  # filter all ASCII
                                                                                            # and symbols
    return tweet.split()  # tokenization


def preprocessing(file):
    initial_city_dict = {'Los_Angeles,_CA': [0, {}], 'San_Francisco,_CA': [0, {}], 'Manhattan,_NY': [0, {}],
                         'San_Diego,_CA': [0, {}], 'Houston,_TX': [0, {}], 'Chicago,_IL': [0, {}],
                         'Philadelphia,_PA': [0, {}], 'Toronto,_Ontario': [0, {}], 'Atlanta,_GA': [0, {}],
                         'Washington,_DC': [0, {}], 'Orlando,_FL': [0, {}], 'Boston,_MA': [0, {}]}
    # value[0] = location count, value[1] = dictionary of word frequency
    tweet_content = []
    token_word_list = []
    city_dict = initial_city_dict
    with open(file) as f:
        for tweet in f.readlines():
            for city in cities:
                if tweet.startswith(city): # check if its a valid tweet
                    word_list = tokenization(city,tweet)
                    token_word_list.append(word_list)
                    tweet_content.append(city)
                    city_dict[city][0] += 1  # city count += 1
                    for word in word_list:  # if exists, count += 1, otherwise count = 1
                        if word in city_dict[city][1]:
                            city_dict[city][1][word] +=1
                        else:
                            city_dict[city][1][word] = 1
    return token_word_list,tweet_content,city_dict # return a dictionary and total unique word of all tweets into a set


def get_unique_word(city_dict):
    total_unique_words = set()
    for city in city_dict:
        total_unique_words.update(city_dict[city][1].keys())
    return total_unique_words


def filter_frequency(city_dict,n):
    for city in city_dict:
        city_dict[city][1]={k: v for (k, v) in city_dict[city][1].items() if v > n} # filter word frequency > n
    return city_dict


def debug(city_dict,file_name):
    writefile = open(file_name, 'w')
    for city in city_dict:
        writefile.write("%s\n" % city_dict[city]) # write dict (value only) into file


def city_prob(city_dict):
    city_prob_dict ={}
    tweet_num = 0
    for city in city_dict:
        tweet_num +=  city_dict[city][0]
    for city in city_dict:
        city_prob_dict[city] = city_dict[city][0]/tweet_num
    return city_prob_dict


def train(city_dict,length_unique_word):
    word_prob = AutoVivification()
    for city in city_dict:
        for word in city_dict[city][1].keys():
            word_prob[city][word]=(city_dict[city][1][word])
        #word_prob[city]['notshow'] = 0 #/ (len(city_dict[city][1]) + 1*train_unique_word_length)
    return word_prob


def test(word_list,city_dict,a): # a is the additive smoothing parameter
    listnew = []
    for wordlist in word_list:
        #print wordlist
        max_p = 0
        #print city_prob_dict
        for city in cities:
            #print city
            p = city_prob_dict[city]
            #print p
            for word in wordlist:
                try:
                    p *= (word_prob[city][word]+a)/((len(city_dict[city][1])+a*len(train_unique_word)))
                except:
                    #print word
                    word_prob[city][word] = word_prob[city]['notshow']
                    p *= a/( (len(city_dict[city][1]) + a * len(train_unique_word)))
                    #print len(city_dict[city][1])
            if p >max_p:
                max_p = p
                new= [p, city]
        listnew.append(new[1])
    return listnew


train_city_dict = preprocessing(train_file)[2]
#print train_city_dict
#train_city_dict = filter_frequency(train_city_dict,1)
#print train_city_dict
test_city_dict = preprocessing(test_file)[2]
#print test_city_dict
#test_city_dict = filter_frequency(test_city_dict,1)
#train_city_dict = filter_frequency(train_city_dict,500)
train_unique_word = get_unique_word(train_city_dict)
#print train_city_dict
train_unique_word_length = len(train_unique_word)
city_prob_dict = city_prob(train_city_dict)
word_prob = train(train_city_dict,train_unique_word_length)
#print word_prob


word_list = preprocessing(test_file)[0]
#print test_city_dict
#print word_list[0]
error =[]
a = 0.001
# classify = test(word_list,train_city_dict,a)
# list_2 = preprocessing(test_file)[1]
# count =0
# for n in range(len(classify)):
#     #print classify[n], list_2[n]
#     if classify[n] != list_2[n]:
#         count +=1
# print 'error', count/len(classify)
a=[0.002]
#a = [0.01,0.001,0.0001,0.00001,0.0000001]
for a_0 in a:
    classify = test(word_list,train_city_dict,a_0)


    list_2 = preprocessing(test_file)[1]
    print len(classify),len(list_2)
    count =0
    for n in range(len(classify)):
        #print classify[n], list_2[n]
        if classify[n] != list_2[n]:
            count +=1
    error.append(count/len(classify))
    print 'error rate', str(count/len(classify))
#print classify

# print a,error
# plt.plot(a, error, marker='o', linestyle='--', color='r', label='Insertion Sort')
# plt.gca().invert_xaxis()
# plt.gca().set_xlim([1,0.00000001])
# plt.show()
# plt.plot(data_size, runtime_2, marker='o', linestyle='--', color='b', label='Merge Sort')
# plt.plot(data_size, runtime_3, marker='o', linestyle='--', color='g', label='Quick Sort')
# plt.ylabel('Runtime')
# plt.xlabel('Input Size')
# plt.title('Plot2')
# plt.legend()
# plt.savefig('Insertion & Merge & Quick plot2.png')
# plt.show()

