import string
import re

train_file = 'tweets.train.txt'
# value[0] = location count, value[1] = dictionary of word frequency
city_dict = {'Los_Angeles,_CA':[0,{}], 'San_Francisco,_CA':[0,{}], 'Manhattan,_NY':[0,{}], 'San_Diego,_CA':[0,{}], 'Houston,_TX':[0,{}], 'Chicago,_IL':[0,{}],
             'Philadelphia,_PA':[0,{}], 'Toronto,_Ontario':[0,{}], 'Atlanta,_GA':[0,{}], 'Washington,_DC':[0,{}], 'Orlando,_FL':[0,{}], 'Boston,_MA':[0,{}]}


writefile = open('new.txt','w')
with open(train_file) as f:
    for tweet in f.readlines():
        for city in city_dict:
            if tweet.startswith(city): # check if its a valid tweet
                tweet = tweet.lstrip(city) # remove leading city name
                tweet = re.sub(r'[\W_]', ' ', filter(lambda x: x in string.printable, tweet)).lower()  # filter all ASCII
                                                                                                       # and symbols
                word_list=tweet.split()  # tokenization
                city_dict[city][0] += 1 # city_count += 1
                for word in word_list: # if exists, count += 1, otherwise count = 1
                    if word in city_dict[city][1]:
                        city_dict[city][1][word] +=1
                    else:
                        city_dict[city][1][word] = 1

for city in city_dict:
    city_dict[city][1]={k: v for (k, v) in city_dict[city][1].items() if v > 10} # filter word frequency > 10
    writefile.write("%s\n" % city_dict[city]) # print dict (value only) into file
    print city_dict[city][0],len(city_dict[city][1].keys())  # location count & word frequency
