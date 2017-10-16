from __future__ import division
import string
import re


train_file = 'tweets.train.txt'
test_file = 'tweets.test1.txt'
debug_file_name = 'new.txt'
cities = ['Los_Angeles,_CA', 'San_Francisco,_CA', 'Manhattan,_NY','San_Diego,_CA', 'Houston,_TX', 'Chicago,_IL',
                 'Philadelphia,_PA', 'Toronto,_Ontario', 'Atlanta,_GA','Washington,_DC', 'Orlando,_FL', 'Boston,_MA']
city_dict = {'Los_Angeles,_CA': [0, {}], 'San_Francisco,_CA': [0, {}], 'Manhattan,_NY': [0, {}],
                 'San_Diego,_CA': [0, {}], 'Houston,_TX': [0, {}], 'Chicago,_IL': [0, {}],
                 'Philadelphia,_PA': [0, {}], 'Toronto,_Ontario': [0, {}], 'Atlanta,_GA': [0, {}],
                 'Washington,_DC': [0, {}], 'Orlando,_FL': [0, {}], 'Boston,_MA': [0, {}]}

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
    tweet = tweet.lstrip(city)  # remove leading city name
    tweet = re.sub(r'[\W_]', ' ', filter(lambda x: x in string.printable, tweet)).lower()  # filter all ASCII
                                                                                            # and symbols
    return tweet.split()  # tokenization


def preprocessing(file):
    # value[0] = location count, value[1] = dictionary of word frequency
    city_dict = {'Los_Angeles,_CA': [0, {}], 'San_Francisco,_CA': [0, {}], 'Manhattan,_NY': [0, {}],
                 'San_Diego,_CA': [0, {}], 'Houston,_TX': [0, {}], 'Chicago,_IL': [0, {}],
                 'Philadelphia,_PA': [0, {}], 'Toronto,_Ontario': [0, {}], 'Atlanta,_GA': [0, {}],
                 'Washington,_DC': [0, {}], 'Orlando,_FL': [0, {}], 'Boston,_MA': [0, {}]}

    with open(file) as f:
        for tweet in f.readlines():
            for city in city_dict:
                if tweet.startswith(city): # check if its a valid tweet
                    word_list = tokenization(city,tweet)
                    city_dict[city][0] += 1  # city count += 1
                    for word in word_list:  # if exists, count += 1, otherwise count = 1
                        if word in city_dict[city][1]:
                            city_dict[city][1][word] +=1
                        else:
                            city_dict[city][1][word] = 1
    return city_dict # return a dictionary and total unique word of all tweets into a set

def get_unique_word(city_dict):
    total_unique_words = set()
    for city in city_dict:
        total_unique_words.update(city_dict[city][1].keys())
    return total_unique_words


def get_word_length(city_dict):
    for city in city_dict:
        word_length = 0
        word_length += len(city_dict[city][1].keys())
    return word_length

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
            word_prob[city][word]=(city_dict[city][1][word]+1)/(len(city_dict[city][1])+length_unique_word)
            # else:
                # word_prob[city][word] = 1/(len(city_dict[city][1])+length_unique_word)
    return word_prob

train_city_dict = preprocessing(train_file)
test_city_dict = preprocessing(test_file)
#train_city_dict = filter_frequency(train_city_dict,500)
train_unique_word = get_unique_word(train_city_dict)
#print train_city_dict
train_unique_word_length = len(train_unique_word)
city_prob_dict = city_prob(train_city_dict)
word_prob = train(train_city_dict,len(train_unique_word))
#print word_prob

def get_test_word_list(test_file):
    city_dict = {'Los_Angeles,_CA': [0, {}], 'San_Francisco,_CA': [0, {}], 'Manhattan,_NY': [0, {}],
                 'San_Diego,_CA': [0, {}], 'Houston,_TX': [0, {}], 'Chicago,_IL': [0, {}],
                 'Philadelphia,_PA': [0, {}], 'Toronto,_Ontario': [0, {}], 'Atlanta,_GA': [0, {}],
                 'Washington,_DC': [0, {}], 'Orlando,_FL': [0, {}], 'Boston,_MA': [0, {}]}
    word_list_list =[]
    with open(test_file) as f:
        for tweet in f.readlines():
            for city in city_dict:
                if tweet.startswith(city): # check if its a valid tweet
                    word_list = tokenization(city, tweet)
                    word_list_list.append(word_list)
    return word_list_list

def test(word_list,city_dict):
    listnew = []
    for wordlist in word_list:
        #print wordlist
        max_p = 0
        #print city_prob_dict
        for city in cities:
            #print city
            p = city_prob_dict[city]
            for word in wordlist:
                if word in word_prob[city].keys():
                    p *= word_prob[city][word]
                else:
                    p *= 1 / (len(city_dict[city][1]) + len(train_unique_word))
            if p >max_p:
                max_p = p
                new= [p, city]
        listnew.append(new[1])
    return listnew


                    #print city
            #print p_dict[str(max_p)]
    #return p_dict[str(max_p)]


#calculate_likelihood('in',train_city_dict,train_unique_word)


word_list = get_test_word_list(test_file)
classify = test(word_list,city_dict)
#print len(classify)


list2 = []
with open(test_file) as f:
    for tweet in f.readlines():
        for city in city_dict:
            if tweet.startswith(city):  # check if its a valid tweet
                list2.append(city)
#print len(list2)
count =0
for n in range(500):
    if classify[n] != list2[n]:
        count +=1
print 'error rate', str(count/500)


