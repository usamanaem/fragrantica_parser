import datetime
import requests
import urllib.request
from bs4 import BeautifulSoup

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()
response = opener.open('https://www.fragrantica.com/perfume/Jean-Paul-Gaultier/Le-Male-430.html')

bsoup = BeautifulSoup(response, 'html.parser')

ratingValue=bsoup.find(itemprop="ratingValue").get_text()
ratingCount=bsoup.find(itemprop="ratingCount").get_text()
PerfumeReviews=bsoup.find_all('div', class_="revND")
longtivityTable=bsoup.find('table', class_="voteLS long")
longValuesList=list(longtivityTable)
longValuesCells=longValuesList[3::2]
for row in longValuesCells:
    cells= row.find_all("td")
    Cat= cells[0].get_text()
    Val=cells[1].get_text()
    print(Cat," ",Val)
ReviewsCount=len(PerfumeReviews)
