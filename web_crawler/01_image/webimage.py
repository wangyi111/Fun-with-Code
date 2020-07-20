##################################################
# scrap images from a webpage


import requests
import re
import time
import os
## request web page
# in case the web blocks python/request 
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}
# identity of visitor: chrome 
response = requests.get('https://www.vmgirls.com/12945.html',headers = headers)
#print(response.request.headers)
html = response.text

## analyze the web page, get urls of the images
#re.findall('<a href="https://static.vmgirls.com/image/2019/12/2019122210300913-scaled.jpeg" alt="少女情怀总是诗" title="少女情怀总是诗">',html)
urls = re.findall('<a href="(.*?)" alt=".*?" title=".*?">',html)
#print(urls)

## save image
# create folder
dir_name = re.findall('<h1 class="post-title h3">(.*?)</h1>',html)[-1]
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

for url in urls:
    time.sleep(1)
    # name of images
    file_name = url.split('/')[-1]
    response = requests.get(url, headers = headers)
    with open(dir_name + '/' + file_name,'wb') as f:
        f.write(response.content)


