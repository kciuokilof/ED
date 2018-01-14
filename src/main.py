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
book = xlrd.open_workbook('C:\\Users\\Kamil\\Desktop\\studia\\ED\\user_names_utf-8.xlsx', 'r', encoding_override= 'utf-8')
sheet = book.sheet_by_index(0)
uids = []
names = []
comagnes = []
private = []
for rownum in range(sheet.nrows):
    rows = sheet.row_values(rownum)
    uids.append(rows[0])
    names.append(rows[1])
    human_name_tag = ed_lib.check_if_polish_name(rows[1])
    if human_name_tag:
        famous_person_tag = ed_lib.check_if_famous_person_name(rows[1])
    else:
        print(rows[1])