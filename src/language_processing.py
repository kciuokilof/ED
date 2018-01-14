import csv
import codecs
import os
from langdetect import detect
import subprocess
from builtins import print
import xml.etree.ElementTree as et

path_to_taikip = 'C:\\Users\\Kamil\\Desktop\\studia\\ED\\TaKIPI18\\TaKIPI18\\Windows'
file_path = "C:\\Users\\Kamil\\Desktop\\studia\\ED\\TaKIPI18\\TaKIPI18\\Windows\\in.txt"
file = codecs.open("C:\\Users\\Kamil\\Desktop\\studia\\ED\\TaKIPI18\\TaKIPI18\\Windows\\in.txt", "w", "utf-8")
#string = u"Bardzo zdrowo się odżywiam, a Ty kurwiszonie qweqweds?"
path_to_skigram ="C:\\Users\\Kamil\\Desktop\\studia\\ED\\skipgram\\skip_gram_v100m8.w2v.txt"
os.chdir(path_to_taikip)
tree = et.parse('out.xml')
root = tree.getroot()


def tweet_to_vec(tweet):
    file = codecs.open("C:\\Users\\Kamil\\Desktop\\studia\\ED\\TaKIPI18\\TaKIPI18\\Windows\\in.txt", "w", "utf-8")
    file.write(tweet) #u'\ufeff')
    file.close()
    subprocess.call("takipi.exe -it TXT -i in.txt -o out.xml -force one -old")
    tree = et.parse('out.xml')
    root = tree.getroot()
    lemm_words_list = []
    for lemm_word in root.iter('lex'):
        if len(lemm_word.attrib) == 1:
            lemm_words_list.append(lemm_word[0].text)
            print("slowo do znalezienia")
            print(lemm_word[0].text)
            print ("grupa leksykalna ")
            print (lemm_word[1].text)

    with open(path_to_skigram, encoding="utf-8") as fp:
        for line in fp:
        #    print(line)
            if line.split(" ")[0] in lemm_words_list:
                print(line)

with open('C:\\Users\\Kamil\\Desktop\\studia\\ED\\1000\\tweets.csv', 'r',
          encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        if line[2][0:2] != 'RT':
            tweet = line[2]
            try:
                if detect(tweet) == 'pl':
                    print('tweet:')
                    print(tweet)

                    tweet_to_vec(tweet)
            except Exception as e:
                print('Lang detect ERROR!')


file.close()
