import csv
import codecs
import os
from langdetect import detect
import subprocess
from builtins import print
import xml.etree.ElementTree as et
import re

path_to_train_data = 'C:\\Users\\Kamil\\PycharmProjects\\ED\\files\\train.csv'
path_to_taikip = 'C:\\Users\\Kamil\\Desktop\\studia\\ED\\TaKIPI18\\TaKIPI18\\Windows'
file_path = "C:\\Users\\Kamil\\Desktop\\studia\\ED\\TaKIPI18\\TaKIPI18\\Windows\\in.txt"
file = codecs.open("C:\\Users\\Kamil\\Desktop\\studia\\ED\\TaKIPI18\\TaKIPI18\\Windows\\in.txt", "w", "utf-8")
#string = u"Bardzo zdrowo się odżywiam, a Ty kurwiszonie qweqweds?"
path_to_skigram ="C:\\Users\\Kamil\\Desktop\\studia\\ED\\skipgram\\skip_gram_v100m8.w2v.txt"
os.chdir(path_to_taikip)




def tweet_to_vec(tweet):
    csv_file_processed = open(path_to_train_data, 'a', encoding='utf-8', newline='')
    file = codecs.open("C:\\Users\\Kamil\\Desktop\\studia\\ED\\TaKIPI18\\TaKIPI18\\Windows\\in.txt", "w", "utf-8")
    tweet = re.sub(r'^https?:\/\/.*[\r\n]*', '', tweet, flags=re.MULTILINE)
    tweet = re.sub(r'^http?:\/\/.*[\r\n]*', '', tweet, flags=re.MULTILINE)
    file.write(tweet) #u'\ufeff')
    file.close()
    subprocess.call("takipi.exe -it TXT -i in.txt -o out.xml -force one -old")
    tree = et.parse('out.xml')
    root = tree.getroot()
    lemm_words_list = []
    leksykal_tag_list = []
    for lemm_word in root.iter('lex'):

        if len(lemm_word.attrib) == 1:
            slow = lemm_word[0]
            if ("subst" or "ppron") in lemm_word[1].text:
                leksykal_tag = 'noun'
                leksykal_tag_list.append(leksykal_tag)
                lemm_words_list.append(lemm_word[0].text+"::"+leksykal_tag)
            elif "perf" in lemm_word[1].text:
                leksykal_tag = 'verb'
                leksykal_tag_list.append(leksykal_tag)
                lemm_words_list.append(lemm_word[0].text+"::"+leksykal_tag)
            elif "ign" in lemm_word[1].text:
                leksykal_tag = ''
                leksykal_tag_list.append(leksykal_tag)
                lemm_words_list.append(lemm_word[0].text+"::"+leksykal_tag)
            elif "interp" in lemm_word[1].text:
                pass
            else: #prep adj
                leksykal_tag = lemm_word[1].text.split(":")[0]
                leksykal_tag_list.append(leksykal_tag)
                lemm_words_list.append(lemm_word[0].text+"::"+leksykal_tag)


            print("slowo do znalezienia")
            print(lemm_word[0].text)
            print ("grupa leksykalna ")
            print (lemm_word[1].text)
    word2vec_list = []
    with open(path_to_skigram, encoding="utf-8") as fp:
        for line in fp:
            for word_plus_lex in lemm_words_list:
                if line.split(" ")[0].startswith(word_plus_lex):
                    word2vec_list.append(line.split(" ")[1:])
    if lemm_words_list.__sizeof__() == word2vec_list.__sizeof__():
        writer = csv.writer(csv_file_processed, delimiter=',')
        writer.writerow([word2vec_list])

# with open('C:\\Users\\Kamil\\Desktop\\studia\\ED\\1000\\tweets.csv', 'r',
#           encoding='utf-8') as csvfile:
#     reader = csv.reader(csvfile)
#     for line in reader:
#         if line[2][0:2] != 'RT':
#             tweet = line[2]
#             if line[20] == 'pl' == detect(tweet):
#                 print('tweet:')
#                 print(tweet)
#                 detect(tweet)
#                 tweet_to_vec(tweet)
#
#
# file.close()


with open(path_to_skigram, encoding="utf-8") as fp:
    for line in fp:
        if  line.startswith('dzień::'):
        # if '::qub' in line:
            print(line)
        # if line.split(" ")[0] in lemm_words_list:
        #     print(line)
