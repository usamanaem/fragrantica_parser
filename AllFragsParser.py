import datetime
import requests
import urllib.request
from bs4 import BeautifulSoup
import time
#class AppURLopener(urllib.request.FancyURLopener):
#    version = "Mozilla/5.0"

#opener = AppURLopener()
#response = opener.open('https://www.fragrantica.com/designers/')

#pageContent = requests.get('https://www.fragrantica.com/designers/')
#soup = BeautifulSoup(pageContent.content, 'html.parser')
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

url = "https://www.fragrantica.com/designers/"
headers={'User-Agent':user_agent,} 

request=urllib.request.Request(url,None,headers) #The assembled request
response = urllib.request.urlopen(request)


soup = BeautifulSoup(response, 'html.parser')
designers = soup.find_all('div', class_="nduList")

listDesigners = list(designers)
i = 0
j = 0

now = datetime.datetime.now()
fileName=now.strftime("frag-%Y%m%d-%H%M.csv")
f = open(fileName, "w")
ShortListDesigner=listDesigners#[:5]
f.write("Number | Designer | Perfume | rating | ratingCount | Comments | Poor | Week| moderate | long lasting | very long lasting | URL")
for designer in ShortListDesigner:
    i = i + 1
    # f.write(str(i) + ' | '+ designer.text+ ' | '+ 'https://www.fragrantica.com'+designer.a['href']+',')
    print(str(i) + ' | ' + designer.text, ' | ' + 'https://www.fragrantica.com' + designer.a['href'])
    #designerPage = requests.get('https://www.fragrantica.com' + designer.a['href'])
    #designersoup = BeautifulSoup(designerPage.content, 'html.parser')
    requestDesigner=urllib.request.Request('https://www.fragrantica.com' + designer.a['href'],None,headers) 
    designerPage = urllib.request.urlopen(requestDesigner)
    designersoup = BeautifulSoup(designerPage, 'html.parser')
    perfumes = designersoup.find_all('div', class_="perfumeslist")
    listperfumes =list(perfumes)
    SamplePerfumeList=listperfumes#[:5]
    for perfume in SamplePerfumeList:
        j = j + 1
        print(str(j).zfill(5) + ' ' + perfume.text, end='| ')
        requestPerfume=urllib.request.Request('https://www.fragrantica.com' + perfume.a['href'],None,headers) 
        PerfumePage = urllib.request.urlopen(requestPerfume)
        PerfumePagesoup = BeautifulSoup(PerfumePage, 'html.parser')
        ratingValue=" " if(PerfumePagesoup.find(itemprop="ratingValue") is None) else PerfumePagesoup.find(itemprop="ratingValue").get_text()
        ratingCount=" " if(PerfumePagesoup.find(itemprop="ratingCount") is None) else PerfumePagesoup.find(itemprop="ratingCount").get_text()
        PerfumeReviews=PerfumePagesoup.find_all('div', class_="revND")
        longtivityTable=PerfumePagesoup.find('table', class_="voteLS long")
        longValuesList=list(longtivityTable)
        longValuesCells=longValuesList[3::2]
        Silage=""
        for row in longValuesCells:
            cells= row.find_all("td")
            Cat= cells[0].get_text()
            Val=cells[1].get_text()
            Silage+=Val+ " | "
        
        reviwsCount=len(PerfumeReviews)
        print(ratingValue, end =' ')
        print(ratingCount)

        info = (str(j).zfill(5) + ' | ' + designer.text + ' | ' + perfume.text + ' | ' + ratingValue+ ' | ' + ratingCount + ' | ' + str(reviwsCount)  +' | ' +Silage + 'https://www.fragrantica.com' + perfume.a['href'] + '>').encode("utf-8")
        f.write(str(info))
        time.sleep(1)
f.close()
