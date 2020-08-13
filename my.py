import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re

def postlink():
    url = 'https://porndish.com/'
    linklist  = []
    user_agent = UserAgent()
    html = requests.get(url,headers = {'user-agent':user_agent.chrome})
    soup = BeautifulSoup(html.text,'lxml')
    link = soup.find_all("li", class_ = 'g1-collection-item g1-collection-item-1of3' )
    for postlink in link:
        # print(postlink.figure.a['href'])
        linklist.append(postlink.figure.a['href'])
    return linklist


def content(page = postlink()):
    newsDictionary = []

    no = 1
    for url in page:
        user_agent = UserAgent()
        html = requests.get(url,headers = {'user-agent':user_agent.chrome})
        soup = BeautifulSoup(html.text,'lxml')
        
        print("PoST ",no)
        no += 1
        # print(url)
        video = soup.find_all('iframe')
        vidLink = video[0]['src']
        # print(video[0]['src'])

        image = soup.find_all('figure', class_ = 'entry-featured-media entry-featured-media-main')
        for pic in image:
            picLink = pic.img['src']
            print(pic.img['src'])
        
        name = soup.find_all('h1', class_ = 'g1-mega g1-mega-1st entry-title')

        for t in name:
            title = t.text

        newObj = {
            'title' : title,
            'post' : url ,
            'pic' : picLink,
            'vid' : vidLink
        }
        newsDictionary.append(newObj)

    return newsDictionary

content()
