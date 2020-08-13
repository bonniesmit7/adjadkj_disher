from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
from telegram import MessageEntity
import urllib.request,json
import requests
import os
from bs4 import BeautifulSoup
# from fake_useragent import UserAgent
import re
from html_telegraph_poster.upload_images import upload_image
import time

TOKEN = '1142419177:AAFch7I4vQJggmsiQOSxQPcubHdkj3ZDfvc'

def postlink():
    url = 'https://porndish.com/'
    linklist  = []
    # user_agent = UserAgent()
    html = requests.get(url)  #,headers = {'user-agent':user_agent.chrome}
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
        # user_agent = UserAgent()
        html = requests.get(url) #,headers = {'user-agent':user_agent.chrome}
        soup = BeautifulSoup(html.text,'lxml')
        print("Started : ",no,end = '   .....  ')
        
        no += 1
        # print(url)
        try:
            vidLink = soup.find('iframe')['src']
        except:
            vidLink = 'https://gounlimited.to/embed-rvjc9b6lk6x8.html'
        # vidLink = video[0]['src']
        # print(video[0]['src'])
        # print(video)

        image = soup.find_all('figure', class_ = 'entry-featured-media entry-featured-media-main')
       
        for pic in image:
            # picLink = pic.img['src']
            picLink = upload_image(pic.img['src'])
            # print(pic.img['src'])
        
        name = soup.find_all('h1', class_ = 'g1-mega g1-mega-1st entry-title')

        for t in name:
            title = t.text

        print("Fetched PoST")

        newObj = {
            'title' : title,
            'post' : url ,
            'pic' : picLink,
            'vid' : vidLink
        }
        newsDictionary.append(newObj)

    return newsDictionary


def setx(update,context):
    listt = postlink()
    print(listt)
    f = open("recent.txt",'w')
    f.write(listt[11])
    f.close()

    
def start(update,context):
    Msg = f"'Status Code' : '200' OK"
    context.bot.sendMessage(chat_id=update.effective_chat.id,text = Msg)
    


def send(update,context):
    # image = 'https://www.porndish.com/wp-content/uploads/2020/08/FakeHostel-Sybil-Kailena-Stuck-In-A-Ladder.jpg'
    # context.bot.send_photo(chat_id ='-1001266419000',photo = upload_image(image) , caption = "Working") 
    i = 1
    while True:
        
        print("While True : ",i)
        i += 1
        f = open("recent.txt",'r')
        condition = f.readline()
        print("FILE READ : ",condition)
        f.close()
        results = content()
        changeLine = results[0]['post']
        print("ChangeLink : ",changeLine)
        for result in results:
            POSTMSG = f"{result['title']}\n\n{result['vid']}"
            if condition == result['post']:
                os.remove("recent.txt")
                f = open('recent.txt','w')
                f.write(changeLine)
                f.close()
                break                
            else:
                IMAGE = result['pic']
                # try:
                context.bot.send_photo(chat_id ='-1001266419000',photo = IMAGE, caption = POSTMSG) 
                # except:
                    # continue

        print("Break; ")
        time.sleep(30)
        
    # Msg = f"Hello {update.effective_user.first_name}\nThanks for trying RoMusic Downloader !\n\nSend me link of JioSaavn song and I'll send the song on Telegram \n\nMade with ❤️ by @truroshan"
        # context.bot.sendPhoto(chat_id=update.effective_chat.id,photo = result['pic'])

updater = Updater(TOKEN, use_context = True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start',start))
dispatcher.add_handler(CommandHandler('send',send))
dispatcher.add_handler(CommandHandler('setx', setx))


updater.start_polling()
updater.idle()
