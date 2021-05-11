from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://news.naver.com/")

bsObject = BeautifulSoup(html,"html.parser")

for link in bsObject.find_all('a'):
    print(link.text.strip(), link.get('href'))
