import wikipedia as wiki
import requests
from lxml import etree
import lxml.html
import time
import csv
import sys
sys.path.append('../lib')
import ed_lib
import xlrd
import re

with open('C:\\Users\\Kamil\\Desktop\\studia\\ED\\ed-twitter-2017-10-27\\users.csv', 'r',
          encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    private_business_tag_list = []
    famous_person_tag_list = []
    all = []
    count = 0
    start_tag = False
    with open('../files/others.txt', 'r', encoding='utf-8') as others_file:
        lines = others_file.readlines()
        if lines:
            last_line = lines[-1]
        else:
            last_line = "0"
            start_tag = True
    for idx, row in enumerate(reader):
        if row[0] == last_line[:-1]:
            start_tag = True

        if start_tag:
            name_components = re.findall(r"[\w]+", str(row[1]))
            for name_component in name_components:
                surname_tag = ed_lib.check_surname_correct(name_component)
                name_tag = ed_lib.check_name_correct(name_component)
                eng_name_tag = ed_lib.check_eng_name_correct(name_component)
                if name_tag or surname_tag or eng_name_tag:
                    break
            if not(name_tag or surname_tag or eng_name_tag):
                if ed_lib.RepresentsInt(row[9]):
                    if int(row[9]) > 500:
                        print("\n\n")
                        print("Nazwa            " + row[1])
                        print("Screen name      "+row[-1])
                        print("Folowers_num     " +row[9])
                        print("Tweety           " + row[-3])
                        print("Opis             " +row[12])
                        to_do = input("Press W to approve as company, press other to disapprove...")
                        if to_do == 'w':
                            with open('../files/compagnes.txt', 'a', encoding='utf-8') as company_file:
                                company_file.write(row[0]+'\n')
                        else:
                            with open('../files/others.txt', 'a', encoding='utf-8') as others_file:
                                others_file.write(row[0]+'\n')
                        count = count+1
