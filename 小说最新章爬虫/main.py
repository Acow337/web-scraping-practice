import re
from Fiction import *
import requests
from lxml import etree

if __name__ == "__main__":
    url='https://www.laiyexs.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77'
    }
    page= requests.get(url=url, headers=headers)
    page.encoding="gbk"
    tree = etree.HTML(page.text)
    tags=tree.xpath('//*[@id="wrap"]/div[6]/dl/dd')[1:-1]
    fictions=[]

    for tag in tags:
        type=tag.xpath('span[1]/a/text()')[0]
        title=tag.xpath('span[2]/a/text()')[0]
        author=tag.xpath('span[3]/a/text()')[0]
        chapter=tag.xpath('span[4]/a/text()')[0]
        update_time=tag.xpath('span[5]/text()')[0]
        url='https://www.laiyexs.com'+tag.xpath('span[4]/a/@href')[0]
        fiction=Fiction(type, title, author, chapter, update_time, url)
        fictions.append(fiction)

    for fiction in fictions:
        url=fiction.url
        page = requests.get(url=url, headers=headers)
        page.encoding = "gbk"
        tree = etree.HTML(page.text)

        title=tree.xpath('//*[@id="wrap"]/div[4]/h1/text()')[0]
        pattern=re.compile('[0-9]')
        index=int(pattern.findall(title)[-1])
        content=[]

        for num in range(1,index+1):
            pattern=re.compile(r'(?<=).*?(?=\.html)')
            url=pattern.findall(fiction.url)[0]+'_'+str(num)+'.html'
            print(url)
            page=requests.get(url=url,headers=headers)
            page.encoding = "gbk"
            tree = etree.HTML(page.text)
            content=content+tree.xpath('//*[@id="dx"]/p//text()')
            if num==index:
                with open('./'+fiction.title+'.txt', 'w', encoding='utf-8') as fp:
                    for item in content:
                        fp.write(item)





