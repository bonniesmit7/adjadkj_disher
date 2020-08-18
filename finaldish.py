import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import schedule 
import random
from telegraph import Telegraph
from html_telegraph_poster import upload_image
import pymongo
from pymongo import MongoClient
from time import sleep

cluster = MongoClient('mongodb+srv://lynda:0909@py.jnv5r.mongodb.net/<dbname>?retryWrites=true&w=majority')
db = cluster['telegram']
collection = db['dish']

def postlink():
    print("Collection link....",end='  ')
    urls = ['https://porndish.com/','https://www.porndish.com/page/2/']
    linklist  = []
    proxyDict = {
        "http": "http://13.234.165.48:80"
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
        }
    for url in urls:
        
        html = requests.get(url,headers = headers,proxies=proxyDict) # ,headers = {'user-agent':user_agent.chrome}
        soup = BeautifulSoup(html.text,'lxml')
        link = soup.find_all("li", class_ = 'g1-collection-item g1-collection-item-1of3' )
        for postlink in link:
            # print(postlink.figure.a['href'])
            linklist.append(postlink.figure.a['href'])
    print("Collected links....Comparing with DATABAsE....",end=' ')

    flist = []
    no = 0
    for i in linklist:
        con = True
        results = collection.find({'_id':i})
        for result in results:
            if result['_id'] == i:
                con = False
        if con:
            flist.append(i)
            # print('Checked ',no)
            no += 1
    
    print("Process Done")
    # print(flist)
    return flist


def content():
    page = postlink()
    print("Cooking Post Now...",end='')
    newsDictionary = []
    post = []
    coverimg = carbon()
    post.append(f'<img src="{coverimg}">')
    posturl = []
    no = 1
    print("Entering page")
    for url in page:
        print("Entered")
        print(no,end=' ')
        
        proxyDict = {
        "http": "http://13.234.165.48:80"
        }
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
        }

        html = requests.get(url,headers = headers,proxies=proxyDict)   
        soup = BeautifulSoup(html.text,'lxml')

        # Fetching Image Url
        image = soup.find_all('figure', class_ = 'entry-featured-media entry-featured-media-main')
        for pic in image:
            picLink = upload_image(pic.img['src'])
        
        
        # Fectching Title
        name = soup.find('h1', class_ = 'g1-mega g1-mega-1st entry-title')
        tcondition = True
        for t in name:
            title = name.text.split('(')[1].split(')')[0].strip()
            for t in title:
                if t.isdigit():
                    tcondition = False
                    break
            if tcondition:
                newtitle = title
            else:
                title = name.text.split(']')[1].split('(')[0].replace(",",'').strip()
                newtitle = title
        
        
        # Fetching Video Url
        video = soup.find_all('iframe')
        vidLink = video[0]['src']
        # post.append(vidLink)
        # print(video[0]['src'])
        
        # Merging Title and Image
        gplink = 'https://gplinks.in/api?api=786898fc840232b8d4e7f1e6ce51faa2695852dd&url='
        gpgo = requests.get(gplink + vidLink).json()
        titleimg = f"""<figure><img src="{picLink}"><figcaption>{newtitle}</figcaption></figure><blockquote><a href="{gpgo['shortenedUrl']}">  🔗 Click here to Watch Online </a></blockquote><hr></hr><br>"""
        post.append(titleimg)
        posturl.append(url)


        if no == 4:
            # print(post)
            break
        no += 1
    for url in page:
        print("Cooked...",end='')
        telegraph(listToString(post))
        print("Yummy...")
        # for p in posturl:
        #     collection.insert_one({'_id':p})
        break
    

def carbon():
    print("Carbon CAlled")
    postno = 0
    result = collection.find({'_id': 'postid'})
    for r in result:    
        if str(r['no']).isdigit:
            postno = int(r['no'])
    r = random.randint(150,255)
    g = random.randint(150,255)
    b = random.randint(150,255)
    a = random.randint(100,155)
    defaulturl = f"https://carbonnowsh.herokuapp.com/?code=UpdateID%20{postno}%20\U0001F44C%250Awww.xDot.in%20\U0001F4F2%250A%250ABraz%20on%20Fire%20\U0001F525&theme=darcula&backgroundColor=rgba({r},%20{g},%20{b},%20{a})"
    return upload_image(defaulturl)

def listToString(s):  
    print("ListToString CAlled")
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    
    # return string   
    return str1  


def telegraph(s):
    print("Telegraph CAlled")
    result = collection.find({'_id': 'postid'})
    for r in result:    
        if str(r['no']).isdigit:
            postno = int(r['no']) + 1

    telegraph = Telegraph(access_token = '0bd0b1a153ac5b330c5c4537a5155f2fa50cc7735f247cf81c9b729aaee1')
    response = telegraph.create_page(
        f'Braz on Fire🔥 UpdateID {postno}',
        html_content=f'{s}'
    )
    turl = 'https://telegra.ph/{}'.format(response['path'])
    t = 'https://api.telegram.org/bot1142419177:AAFch7I4vQJggmsiQOSxQPcubHdkj3ZDfvc/sendMessage?chat_id=-1001200427937&text='
    requests.get(t + turl)
    # collection.update_one({'_id': 'postid'},{"$set": {'no': postno}})
    sleep(1)



def setid():
    collection.update_one({'_id': 'postid'},{"$set": {'no': 1}})
    result = collection.find({'_id': 'postid'})
    for r in result:    
        if str(r['no']).isdigit:
            print(r['no'])
    # print(result['no'])


print("Mission Start juSt :) Wait and Watch")
# schedule.every(10).minutes.do(postlink)
# while True: 
#     # Checks whether a scheduled task  
#     # is pending to run or not 
#     schedule.run_pending() 
#     sleep(1) 

content()
