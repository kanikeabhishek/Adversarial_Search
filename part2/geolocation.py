#!/usr/bin/env python

# Model Selection
# In the question, we've already made the naive assumption, which says that for any i != j,
# w_i is independent from w_j given L. Multinomial Naive Bayes classifier was used to build
# the model. The reason we use multinomial instead of bernoulli is because we think the
# frequency of a word contained in different location matters. For example, if there was
# an event happened in one city, and became viral in the whole north america.
# We can see the keyword from all of the cities, but usually the city where it happened
# should have more tweets, and a larger weight should be assigned to it.

# Data Cleaning
# If the line was started with a city, the training set was split into a city_list and
# a tweet_list. For each tweet in the tweet_list, we removed selected symbols
# '$%|<>;^&*+={}~@,:()[\]_/\-".' , and remove word that appears in the filtered_word list.
# Some symbols were not included(like '#'), because by removing those will lower the accuracy.
# The filtered_word list includes stop words, and also words with high frequency in every location,
# and by removing these words, the accuracy wouldn't be affected or would be improved.
# A function to filter the frequency of words was barely used simply because a better accuracy
# will be given if no threshold was set.
#
# Model Training
# The next step is to train the model. with the training set, I construct a nested dictionary.
# Format like this: # {city: [number of location appears in the training set, {word: occurrence count} ]}
# (Instead of calculate the distribution while training, I calculated the probability while apply
# to testing data, which I think can help to avoid unnecessary loops)
# While I have the dictionary, I can calculate the probability for each city, and also a set contains
# all unique word in the training set.
#
# Classify testing data
# I used two method to classify the data based on this blog:
# http://sebastianraschka.com/Articles/2014_naive_bayes_1.html.
#
# One is the term frequency, which calculates P(w|L) using
# (word count in each location + a )/ (The total number of words in a location + a*total number of all distinct words)
# where 'a' is the smoothing parameter. A plot was draw to determine the best a (Smoothing parameter & Error rate.png),
# and it is set to 0.04 for the best results. The classifier takes 3.89108490944 second (including training
# and classifying), and return the accuracy of 0.702 (It could increase to 0.704 if we include the symbol ')',
# but I didn't find a reasonable explanation to keep it).
#
# The other one is tf-idf, which calculates weighted term frequency. First, I normalized the
# term frequency, by dividing the (word count in each location) with sqrt(The total number of terms in a location).
# Then calculate the idf using log(the total number of tweets/the number of tweets contain the word)
# Finally multiply the normalized term frequency and idf.
# The classifier takes 287.782369852 second (including training and classifying), and return the accuracy of 0.624.
#
# Consider the accuracy and running time, term frequency method will be used to classify the testing data.
#
# Output
# The top 5 words associated with each of the 12 locations are the words with highest P(w|L=l) for each location.
# Most of the words associate with the location are the abbreviation or nickname, or the state name of the city.
# Be aware that the output file will include some blank lines, this is due to ASCII characters. I didn't remove those
# because I want keep the file format the same as the original dataset.
#

from __future__ import division
import string
import re
import math
import copy
import heapq
import sys
import time
#from matplotlib import pyplot as plt
#from nltk.corpus import stopwords
#cachedStopWords = stopwords.words("english")

start = time.time()
# filter selected symbols, and words
# Return a lists of words for each tweet
def tokenization(tweet):
    return filter(lambda a: a not in filtered_words,
                  re.sub('[$%|<>;^&*+={}~@,:()[\]_/\-".]',
                         '', filter(lambda x: x in string.printable, tweet.lower())).split())


# read the file and split valid tweet into 2 lists
# Return the location name, tokenized word list
def clean_data(filename):
    classified_cities = []
    tweet_content = []
    origin_tweet = []
    for tweet in open(filename).readlines():
        if tweet.startswith(cities): # check if its a valid tweet
            each_tweet = tweet.split(' ', 1)
            classified_cities.append(each_tweet[0])
            tweet_content.append(tokenization(each_tweet[1]))
    #print origin_tweet
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


# get the total number of tweets in the dataset
def get_tweet_total(city_dict):
    return sum(item[0] for item in city_dict.values())


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


# get inverse document frequency count
def get_idf(city_dict,word,tweet_content):
    count = 0
    #print tweet_content
    for tweet in tweet_content:
        if word in tweet:
            count +=1
    return count

# test using tf-idf model
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
                    # calculate the tf-idf
                    p *= (train_dict[city][1][word]/math.sqrt(sum(train_dict[city][1].values()))) * math.log(tweet_total/(get_idf(train_dict,word,train_tweet)+1))
                except KeyError:
                    #print len(train_dict[city][1].keys())
                    p *= 1/math.sqrt(sum(train_dict[city][1].values())) * math.log(tweet_total/(get_idf(train_dict,word,train_tweet)+1))
            if p >= max_p:
                max_p = p
                new = [p, city]
        classified_city.append(new[1])
    return classified_city


# get the error rate
def get_error(classified_list, test_label):
    count = 0
    for n in range(len(classified_list)):
        # print classify[n], list_2[n]
        if classified_list[n] != test_label[n]:
            count += 1
    return count / len(classified_list)


def write_output(original_file,filename,classified_list):
    with open(filename, 'w') as output:
        with open(original_file) as f:
            for tweet in f.readlines():
                if tweet.startswith(cities):
                    #tweet = classified_list.pop(0)+' '+tweet
                    #print classified_list
                    output.write(classified_list.pop(0)+' '+tweet)
        f.close()
    output.close()

# to get the probability for each word in each city
def get_distribution(city_dict,a):
    for city in cities:
        city_dict[city] = city_dict[city][1]
        for word in city_dict[city]:
            city_dict[city][word]=(city_dict[city][word]+a) / (len(city_dict[city]) + a * unique_word_length)
    return city_dict

def top5(city_dict):
    for city in city_dict:
        #print city_dict.get(city)
        k_keys_sorted = heapq.nlargest(5, city_dict[city],key=city_dict[city].get)
        # for x in k_keys_sorted:
        #     print city_dict[city][x]
        print city, k_keys_sorted


def main():

    #declare a filtered word list, which need to be remove from the dataset
    # a city list contains all 12 city names
    global filtered_words
    global cities

    filtered_words = ['1','2','3','4','5','6','7','8','9','0',
                      'we', 'me', 'be', 'the', 'that', 'to', 'as', 'there',
                      'has', 'have', 'and', 'or', 'is', 'not', 'a', 'of',
                      'my', 'this', 'at', 'our', 'you', 'with', "i'm", 'i',
                      'but', 'in', 'by', 'on', 'are', 'it', 'if', 'for', 'from',
                      'with', "we're", 'latest', 'click', 'out', 'just', 'st',
                      'opening', 'up', 'see', '&amp;', 'great', '#hiring', 'can',
                      'here', 'work', 'want', 'so', 'day', 'trucks', 'avenue',
                      '#job', '#jobs', '#careerarc','amp','apply','was','were',
                      'center',"it's",'anyone','about','#job?','recommend',
                      'bw','fit','#hospitality','#hiring!','request','#nursing',
                      '#healthcare','an','us','one','how',"don't",'these','do',
                      'your', 'all', 'night','get','when', 'what','park','street',
                      'love','time','dr', 'rd','via','case','now','good','s', 'n',
                      'w','go','like', 'bar','today','#it','happy','view','home',
                      'game', '#sales', 'drinking', 'back', 'opened', 'read',
                      'manager', 'details','iphone', 'parking', "you're", 'might',
                      'could','photo','health', 'join', 'near', 'interested',
                      'nurse','team!','city', 'care', '#veterans', 'resolved',
                      'closed', 'baths', 'registered', '#retail', 'stop', '#photo',
                      'first', 'united', 'food','south', 'check','more','tonight',
                      'been','#nowhiring','ready', 'clear', 'got','ave','last',
                      'off','weekend', 'services', 'still', 'than','little', 'know',
                      'best', 'world', 'real','blvd', 'minute', 'delay', 'mins',"come",
                      'job','hiring','jobs','job?','careerarc']

    cities = ('Los_Angeles,_CA', 'San_Francisco,_CA', 'Manhattan,_NY', 'San_Diego,_CA', 'Houston,_TX', 'Chicago,_IL',
              'Philadelphia,_PA', 'Toronto,_Ontario', 'Atlanta,_GA', 'Washington,_DC', 'Orlando,_FL', 'Boston,_MA')

    #train_file = 'tweets.train.txt'
    train_file = sys.argv[1]
    #test_file = 'tweets.test1.txt'
    test_file = sys.argv[2]
    #output_file = 'tweet.output.txt'
    output_file = sys.argv[3]
    debug_file_name = 'debug.txt'


    # train the model
    train_city_dict = train(*clean_data(train_file))
    train_city_prob = city_prob(train_city_dict)
    global unique_word_length
    unique_word_length= len(get_unique_word(train_city_dict))

    # use for tf-idf model
    global train_tweet
    train_tweet = clean_data(train_file)[1]
    global tweet_total
    tweet_total = get_tweet_total(train_city_dict)

    # Classify
    a= 0.04
    test_label, test_tweet = clean_data(test_file)
    classified= test_tf(test_tweet, train_city_dict, train_city_prob, unique_word_length, a)
    #print get_error(classified, test_label)


    # print the top 5 associated word
    new_dict = copy.deepcopy(train_city_dict)
    new_dict=get_distribution(new_dict,a)
    top5(new_dict)


    # write to file
    write_output(test_file,output_file,classified)
    #print time.time()-start


    # code to draw plot finding the best a
    # a=[]
    # error =[]
    # for a_0 in range(1, 10):
    #     a.append(a_0/100)
    #     classified = test_tf(test_tweet, train_city_dict, train_city_prob, unique_word_length, a_0/100)
    #     error.append(get_error(classified, test_label))
    #
    # plt.plot(a, error, marker='o', linestyle='--', color='r', label='Naive Bayes Classifier')
    # plt.ylabel('Error rate')
    # plt.xlabel('Smoothing parameter')
    # plt.legend()
    # plt.savefig('Smoothing parameter & Error rate.png')
    # plt.show()


if __name__ == '__main__':
    main()