import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import config
import tweepy
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)



def setup():
    memory_limiter = 0
    TweetUrl = '../Twitter_Data.csv'
    tweet_dataframe = pd.read_csv(TweetUrl)

    wordDict = {}
    idCounter = 0
    i = 0
    maxNum = (tweet_dataframe.shape[0] - memory_limiter)
    numUsed = 0
    while i < maxNum:
        while tweet_dataframe.iloc[i, 1] == 0:
            i += 1
        allWords = str(tweet_dataframe.iloc[i, 0]).split(" ")
        for word in allWords:
            if word not in wordDict:
                wordDict[word] = idCounter
                idCounter += 1
        numUsed += 1
        i += 1
    X = np.zeros((numUsed, idCounter), dtype='float')

    while i < maxNum:
        while tweet_dataframe.iloc[i, 1] == 0:
            i += 1
        allWords = str(tweet_dataframe.iloc[i, 0]).split(" ")
        for word in allWords:
            X[i, wordDict[word]] = 1
        i += 1

    np.sum(X[0:5, ], axis=1)

    arrayOfNums = []
    j = 0
    while j < maxNum:
        if tweet_dataframe.iloc[j, 1] != 0:
            arrayOfNums.append(tweet_dataframe.iloc[j, 1])
        j += 1
    y = np.array(arrayOfNums)

    numNeg = np.sum(y < 0)
    numPos = np.sum(y > 0)

    xTrain, xTest, yTrain, yTest = train_test_split(X, y, test_size=0.2, random_state=0)
    probWordGivenPositive, probWordGivenNegative, priorPositive, priorNegative = compute_distros(
        xTrain, yTrain)

    min_prob = 1 / yTrain.shape[0]
    logProbWordPresentGivenPositive, logProbWordAbsentGivenPositive = compute_logdistros(probWordGivenPositive,
                                                                                         min_prob)
    logProbWordPresentGivenNegative, logProbWordAbsentGivenNegative = compute_logdistros(probWordGivenNegative,
                                                                                         min_prob)
    logPriorPositive, logPriorNegative = compute_logdistros(priorPositive, min_prob)

    return logProbWordPresentGivenPositive, logProbWordAbsentGivenPositive, logProbWordPresentGivenNegative, logProbWordAbsentGivenNegative, logPriorPositive, logPriorNegative


def compute_distros(x, y):
    probWordGivenPositive = np.sum(x[y >= 0, :], axis=0)
    probWordGivenPositive = probWordGivenPositive / np.sum(y >= 0)

    probWordGivenNegative = np.sum(x[y < 0, :], axis=0)
    probWordGivenNegative = probWordGivenNegative / np.sum(y < 0)

    priorPositive = np.sum(y > 0) / y.shape[0]  # Number of positive examples vs. all examples
    priorNegative = 1 - priorPositive

    return probWordGivenPositive, probWordGivenNegative, priorPositive, priorNegative


def compute_logdistros(distros, min_prob):
    distros = np.where(distros >= min_prob, distros, min_prob)
    distros = np.where(distros <= (1 - min_prob), distros, 1 - min_prob)

    return np.log(distros), np.log(1 - distros)


def classifyNB(words, logProbWordPresentGivenPositive, logProbWordAbsentGivenPositive,
               logProbWordPresentGivenNegative, logProbWordAbsentGivenNegative,
               logPriorPositive, logPriorNegative):
    sumPositive = logPriorPositive
    count = 0
    for word in words:
        if word == 1:
            sumPositive += logProbWordPresentGivenPositive[count]
        elif word == 0:
            sumPositive += logProbWordAbsentGivenPositive[count]
        count += 1

    sumNegative = logPriorNegative
    count = 0
    for word in words:
        if word == 1:
            sumNegative += logProbWordPresentGivenNegative[count]
        elif word == 0:
            sumPositive += logProbWordAbsentGivenNegative[count]
        count += 1

    return sumPositive - sumNegative


if __name__ == '__main__':
    (logProbWordPresentGivenPositive, logProbWordAbsentGivenPositive, logProbWordPresentGivenNegative,
     logProbWordAbsentGivenNegative, logPriorPositive, logPriorNegative) = setup()
    keyword = input("Enter the term you want to search for: ")
    tweets = api.search(keyword)
    for tweet in tweets:
        bayes = classifyNB(tweet.text, logProbWordPresentGivenPositive, logProbWordAbsentGivenPositive,
                       logProbWordPresentGivenNegative, logProbWordAbsentGivenNegative,
                       logPriorPositive, logPriorNegative)
        print(bayes)
