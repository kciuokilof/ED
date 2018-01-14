from langdetect import detect
import csv

with open('C:\\Users\\Kamil\\Desktop\\studia\\ED\\1000\\tweets.csv', 'r',
          encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    tweet_num = 0;
    pl_tweet_num = 0;
    for line in reader:
        if line[2][0:2] != 'RT':
            tweet = line[2]
            tweet_num = tweet_num+1
            try:
                if detect(tweet)=='pl':
                    print('tweet:')
                    pl_tweet_num = pl_tweet_num + 1

                    print(tweet)
            except Exception as e:
                print('Lang detect ERROR!' )
print(str(pl_tweet_num/tweet_num))