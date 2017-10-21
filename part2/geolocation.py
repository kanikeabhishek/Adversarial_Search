#!/usr/bin/env python

from __future__ import division
import string
import re

train_file = 'tweets.train.txt'
test_file = 'tweets.test1.txt'
output_file = 'tweet.output.txt'
debug_file_name = 'debug.txt'
cities = ('Los_Angeles,_CA', 'San_Francisco,_CA', 'Manhattan,_NY','San_Diego,_CA', 'Houston,_TX', 'Chicago,_IL',
                 'Philadelphia,_PA', 'Toronto,_Ontario', 'Atlanta,_GA','Washington,_DC', 'Orlando,_FL', 'Boston,_MA')


# filter all ASCII and symbols
# Return a lists of words for each tweet
def tokenization(tweet):
    return re.sub(r'\W_', ' ', filter(lambda x: x in string.printable, tweet.lower())).split()


# read the file and split valid tweet into two lists
# One is all the location name, and another is
def clean_data(filename):
    classified_cities = []
    tweet_content = []
    for tweet in open(filename).readlines():
        if tweet.startswith(cities): # check if its a valid tweet
            each_tweet = tweet.split(' ', 1)
            classified_cities.append(each_tweet[0])
            tweet_content.append(tokenization(each_tweet[1]))
    return classified_cities, tweet_content


# return the probability of each city into a dict
def filter_frequency(city_dict,n):
    for city in city_dict:
        city_dict[city][1]={k: v for (k, v) in city_dict[city][1].items() if v > n} # filter word frequency > n
    return city_dict

# return the probability of each city into a dict
def city_prob(city_dict):
    city_prob_dict ={}
    tweet_total = sum(item[0] for item in city_dict.values())
    for city in city_dict:
        city_prob_dict[city] = city_dict[city][0]/tweet_total
    return city_prob_dict


# return total unique word of all words into a set
def get_unique_word(city_dict):
    total_unique_words = set()
    for city in city_dict:
        total_unique_words.update(city_dict[city][1].keys())
    return total_unique_words


# train the model
# returns a dict
# {city: [number of location appears in the dataset, {word: occurrence} ]}
def train(classified_cities,tweet_content):
    city_dict = {'Los_Angeles,_CA': [0, {}], 'San_Francisco,_CA': [0, {}], 'Manhattan,_NY': [0, {}],
                         'San_Diego,_CA': [0, {}], 'Houston,_TX': [0, {}], 'Chicago,_IL': [0, {}],
                         'Philadelphia,_PA': [0, {}], 'Toronto,_Ontario': [0, {}], 'Atlanta,_GA': [0, {}],
                         'Washington,_DC': [0, {}], 'Orlando,_FL': [0, {}], 'Boston,_MA': [0, {}]}
    for n in range(len(classified_cities)):
        city_dict[classified_cities[n]][0] += 1
        for word in tweet_content[n]:
            if word in city_dict[classified_cities[n]][1]:
                city_dict[classified_cities[n]][1][word] += 1
            else:
                city_dict[classified_cities[n]][1][word] = 1
    return city_dict


# appply the distribution to the testset
# using multinomial Naive Bayes
def test_tf(word_list,train_dict,train_prob_dict,total_unique_words_length,a):
    classified_city = []
    for wordlist in word_list:
        # print wordlist
        max_p = 0
        # print city_prob_dict
        for city in cities:
            # print city
            p = train_prob_dict[city]
            # print p
            for word in wordlist:
                try:
                    p *= (train_dict[city][1][word] + a) / (len(train_dict[city][1]) + a * total_unique_words_length)
                except KeyError:
                    p *= a / (len(train_dict[city][1]) + a * total_unique_words_length)
            if p >= max_p:
                max_p = p
                new = [p, city]
        classified_city.append(new[1])
    return classified_city

def test_tfidf(word_list,train_dict,train_prob_dict,total_unique_words_length,a):
    classified_city = []
    for wordlist in word_list:
        # print wordlist
        max_p = 0
        # print city_prob_dict
        for city in cities:
            # print city
            p = train_prob_dict[city]
            # print p
            for word in wordlist:
                try:
                    p *= (train_dict[city][1][word]/sum(train_dict[city][1].values()) + a) / (len(train_dict[city][1]) + a * total_unique_words_length)
                except KeyError:
                    p *= a / (len(train_dict[city][1]) + a * total_unique_words_length)
            if p >= max_p:
                max_p = p
                new = [p, city]
        classified_city.append(new[1])
    return classified_city




#print clean_data(train_file)[1]

def main():

    train_city_dict = filter_frequency(train(*clean_data(train_file)),0)
    train_city_prob = city_prob(train_city_dict)
    unique_word_length= len(get_unique_word(train_city_dict))
    test_classified, test_tweet = clean_data(test_file)
    classified = test_tf(test_tweet,train_city_dict,train_city_prob,unique_word_length,0.017)

    count =0
    for n in range(len(classified)):
        #print classify[n], list_2[n]
        if classified[n] != test_classified[n]:
            count +=1
    print 'error', count/len(classified)

if __name__ == '__main__':
    main()
# # print a,error
# # plt.plot(a, error, marker='o', linestyle='--', color='r', label='Insertion Sort')
# # plt.gca().invert_xaxis()
# # plt.gca().set_xlim([1,0.00000001])
# # plt.show()
# # plt.plot(data_size, runtime_2, marker='o', linestyle='--', color='b', label='Merge Sort')
# # plt.plot(data_size, runtime_3, marker='o', linestyle='--', color='g', label='Quick Sort')
# # plt.ylabel('Runtime')
# # plt.xlabel('Input Size')
# # plt.title('Plot2')
# # plt.legend()
# # plt.savefig('Insertion & Merge & Quick plot2.png')
# # plt.show()
#
