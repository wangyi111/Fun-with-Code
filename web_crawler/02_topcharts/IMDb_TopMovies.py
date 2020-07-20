import random
import re
import requests
from openpyxl import Workbook
from time import sleep

# find all by pattern
def find_all_by_pat(pat,string):
    res = re.findall(pat,string)
    return res

def get_html_doc(url):
    pro = ['122.152.196.126','114.215.174.227','119.185.30.75']
    head = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    response = requests.get(url,proxies={'http':random.choice(pro)},headers = head)
    response.encoding = 'utf-8'
    html_doc = response.text
    return html_doc

def get_douban_html(query_name):
    url = 'https://www.douban.com/search?cat=1002&q=%s' % query_name
    douban_search_res = get_html_doc(url)
    return douban_search_res


def get_chinese_name(pat,doc):
    res_list = find_all_by_pat(pat,doc)
    try:
        return res_list[1]
    except:
        return ''

def get_director_name(pat,doc):
    res = find_all_by_pat(pat,doc)
    try:
        return res[0].split('/')[1]
    except:
        return ' '

if __name__ == "__main__":
    url = 'https://www.imdb.com/chart/top'
    imdb_doc = get_html_doc(url)
    pat = r'<td class="titleColumn">\s*(.*)..*\s*.*\s*title=".*" >(.*)</a>.*\s*<span class="secondaryInfo">\((.*)\)</span>'
    res = find_all_by_pat(pat,imdb_doc)

    pat2 = r'qcat.*\s*.*>(.*?)\s*</a>'
    pat3 = '<span\s*class="subject-cast">(.*)</span>'

    for i in range(len(res)):
        doc = get_douban_html(res[i][1])
        chinese_name = get_chinese_name(pat2,doc)
        director_name = get_director_name(pat3,doc)

        res[i] = list(res[i])
        res[i].insert(1,chinese_name)
        res[i].insert(3,director_name)
        print('writing %d movie' %(i+1),end='\r')
        sleep(random.random()*1.0)
    print()
        #print(res[i])
        #sleep(random.random()*1.2)

    wb = Workbook()
    sheet = wb.active
    sheet.column_dimensions['B'].width = 60
    sheet.column_dimensions['C'].width = 25
    for i in range(len(res)):
        for j in range(len(res[i])):
            sheet.cell(row=i+1,column=j+1).value = res[i][j]
        #print('writing %d movie' %i,end='\r')
    #print()
    wb.save('imdb.xlsx')
    
