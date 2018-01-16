from lxml import etree
import lxml.html
import time
import wikipedia
import unidecode
import re
import csv
from langdetect import detect


with open("../files/names_eng.txt", 'rb') as f:
    eng_names_list = f.read().splitlines()
with open("../files/names_pl.txt", 'rb') as f:
    names_list = f.read().splitlines()
with open("../files/surnames_pl.txt", 'rb') as f:
    surnames_list = f.read().splitlines()


def private_famous_user_validaton_and_save():
    with open('C:\\Users\\Kamil\\Desktop\\studia\\ED\\ed-twitter-2017-10-27\\users.csv', 'r',
              encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        private_business_tag_list = []
        famous_person_tag_list = []
        all = []
        for idx, row in enumerate(reader):
            human_name_tag = check_if_polish_name(row[1])
            row.append(human_name_tag)
            if human_name_tag:
                famous_person_tag = check_if_famous_person_name(row[1])
                row.append(famous_person_tag)
            else:
                row.append(None)
            all.append(row)
    with open('C:\\Users\\Kamil\\Desktop\\studia\\ED\\ed-twitter-2017-10-27\\users_withtag2.csv', "w", encoding='utf-8',
              newline='', ) as f:
        writer = csv.writer(f)
        writer.writerows(all)


def language_tagger():
    path = 'C:\\Users\\Kamil\\Desktop\\studia\\ED\\1000\\'
    with open(path + 'tweets.csv', 'r',
              encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        tweet_num = 0
        all = []
        for line in reader:
            if line[2][0:2] != 'RT':
                tweet = line[2]
                tweet_num = tweet_num + 1
                try:
                    tag = detect(tweet)
                except Exception as e:
                    tag = "Don't know"
            else:
                tag='RT'
            line.append(tag)
            all.append(line)
    with open(path + 'tweets_with_lang_tag.csv', "w", encoding='utf-8',
              newline='', ) as f:
        writer = csv.writer(f)
        writer.writerows(all)

def safe_surnames_to_file():
    first_letter_string = 'wertuiopasdfghjklzcbnm'
    webpage_url = 'http://genealogiapolska.pl/surnames-oneletter.php?firstchar='
    surnames = []
    for i in range(0, len(first_letter_string)):
        letter_webpage = first_letter_string[i].upper()
        surnames_webpage_url = webpage_url + letter_webpage
        tree = lxml.html.parse(surnames_webpage_url)
        xpatheval = etree.XPathDocumentEvaluator(tree)
        surnames.append(xpatheval('//table[@class="sntable"]//a[@href]/text()'))
        time.sleep(1)
    with open('../files/surnames_pl.txt', 'w', encoding='utf-8') as f:
        for surname_on_letter in surnames:
            for surname in surname_on_letter:
                if len(surname)>2:
                    f.write('%s\n' % unidecode.unidecode(surname.strip()))
    f.close()


def safe_eng_names_to_file():
    num_of_pages = 13
    webpage_url = 'http://www.behindthename.com/names/usage/english'
    names = []
    for i in range(1, num_of_pages):
        letter_webpage = '/'+str(i)
        surnames_webpage_url = webpage_url + letter_webpage

        tree = lxml.html.parse(surnames_webpage_url)
        xpatheval = etree.XPathDocumentEvaluator(tree)
        names.extend(xpatheval('//div[@class="browsename"]/a[@href]/text()'))
        time.sleep(1)
    names2 = names
    names = list(set(names))
    with open('../files/names_eng.txt', 'w', encoding='utf-8') as f:
        for name in names:
            if len(name) > 2:
                f.write('%s\n' % unidecode.unidecode(name.strip()))
    f.close()


def safe_names_to_file():
    first_letter_string = 'wertuiopasdfghjklzcbnm'
    names = []
    webpage_url = 'http://www.ksiegaimion.com/spis-imion'
    tree = lxml.html.parse(webpage_url)
    xpatheval = etree.XPathDocumentEvaluator(tree)
    names.append(xpatheval('//div[@class="table"]//a/text()'))
    time.sleep(1)
    with open('../files/names_pl.txt', 'w') as f:
        for name in names[0]:
            cos = name.strip()
            f.write('%s\n' % unidecode.unidecode(cos))
    f.close()


def check_if_compagny_name(name):
    wikipedia.set_lang("pl")
    search_result = wikipedia.search(name)
    for result_prompt in search_result:
        if -1 != result_prompt.lower().find(name.lower()):
            print(name + ' found: ' + result_prompt)

def check_if_famous_person_name(name):
    wikipedia.set_lang("pl")
    search_result = wikipedia.search(name)
    for search_prompt in search_result:
        if unidecode.unidecode(search_prompt.upper()) == unidecode.unidecode(name.upper()):
            return True
    return False


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def check_name_correct(name_component):
    name_component = unidecode.unidecode(name_component.upper())
    for tipical_name in names_list:
        if tipical_name.upper().decode('utf-8') == name_component:
            return True
    return False


def check_eng_name_correct(name_component):
    name_component = unidecode.unidecode(name_component.upper())
    for tipical_name in eng_names_list:
        if tipical_name.upper().decode('utf-8') == name_component:
            return True
    return False


def check_surname_correct(name_component):
    name_component = unidecode.unidecode(name_component.upper())
    for tipical_name in surnames_list:
        if tipical_name.upper().decode('utf-8') == name_component:
            return True
    return False


def check_if_polish_name(name):
    name_components = re.findall(r"[\w]+", str(name))
    surname_fetch_result_list = []
    for name_component in name_components:
        name_fetch_result = check_name_correct(name_component)
        surname_fetch_result = check_surname_correct(name_component)
        surname_fetch_result_list.append(surname_fetch_result)
        if not (name_fetch_result or surname_fetch_result):
            return False
    if True in surname_fetch_result_list:
        return True
    else:
        return False
