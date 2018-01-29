import datetime
import requests
import urllib.request
from bs4 import BeautifulSoup

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()
response = opener.open('https://www.fragrantica.com/designers/')

#pageContent = requests.get('https://www.fragrantica.com/designers/')
#soup = BeautifulSoup(pageContent.content, 'html.parser')

soup = BeautifulSoup(response, 'html.parser')
designers = soup.find_all('div', class_="nduList")

listDesigners = list(designers)
i = 0
j = 0

now = datetime.datetime.now()
fileName=now.strftime("frag-%Y%m%d-%H%M.csv")
f = open(fileName, "w")
ShortListDesigner=listDesigners#[:5]
for designer in ShortListDesigner:
    i = i + 1
    # f.write(str(i) + ' | '+ designer.text+ ' | '+ 'https://www.fragrantica.com'+designer.a['href']+',')
    print(str(i) + ' | ' + designer.text, ' | ' + 'https://www.fragrantica.com' + designer.a['href'])
    #designerPage = requests.get('https://www.fragrantica.com' + designer.a['href'])
    #designersoup = BeautifulSoup(designerPage.content, 'html.parser')

    designerPage = opener.open('https://www.fragrantica.com' + designer.a['href'])
    designersoup = BeautifulSoup(designerPage, 'html.parser')
    perfumes = designersoup.find_all('div', class_="perfumeslist")
    listperfumes =list(perfumes)
    SamplePerfumeList=listperfumes#[:5]
    for perfume in SamplePerfumeList:
        j = j + 1
        print(str(j) + ' ' + perfume.text)

        PerfumePage = opener.open('https://www.fragrantica.com' + perfume.a['href'])
        PerfumePagesoup = BeautifulSoup(PerfumePage, 'html.parser')
        ratingValue=PerfumePagesoup.find(itemprop="ratingValue").get_text()
        ratingCount=PerfumePagesoup.find(itemprop="ratingCount").get_text()
        PerfumeReviews=PerfumePagesoup.find_all('div', class_="revND")
        ratingCount=PerfumePagesoup.find(itemprop="ratingCount").get_text()
        
        reviwsCount=len(PerfumeReviews)
        print(ratingValue)
        print(ratingCount)

        info = (str(j).zfill(5) + ' | ' + designer.text + ' | ' + perfume.text + ' | ' + ratingValue+ ' | ' + ratingCount + ' | ' + str(reviwsCount)  + ' | ' + 'https://www.fragrantica.com' + perfume.a['href'] + '>').encode("utf-8")
        f.write(str(info))

f.close()
