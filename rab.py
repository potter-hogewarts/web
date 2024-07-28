#!/usr/bin/env python3
from bs4 import BeautifulSoup
import sqlite3
import discord
from discord.ext import tasks
import time
import requests
import json
import os

#TOKEN
TOKEN = os.getenv('TOKEN')
intents=discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

conn1=sqlite3.connect("./xxxxx.db", check_same_thread=False)
c1=conn1.cursor()

c1.execute("CREATE TABLE IF NOT EXISTS game(target_url primary key, url_now)")


targeturl=['URL(https://...)']

channel_game = None

@client.event
async def on_ready():
    global channel_game

    await client.change_presence(activity=discord.Game(name="XXXXXXXXXX"))
    await tree.sync()

    #チャンネル(投稿したいチャンネルID)
    channel_pricone = client.get_channel("XXXXXXXXXXXXXXXXX")

    try:
        post_url.start()
    except Exception as e:
        print(e)
        pass

    print("起動")


@tasks.loop(seconds=900,reconnect=True)
#引数で与えられたURLからスクレイピング
async def post_url():
    global channel_game

    #url_now=""
    # スクレイピング対象の URL にリクエストを送り HTML を取得する
    for url in targeturl: 
        try:
            c1.execute("INSERT INTO game VALUES(?, ?)",(url,""))
            conn1.commit()
        except:
            pass

        res = requests.get(url)
        res.encoding = res.apparent_encoding # 日本語の文字化け防止
        #html = Scrape.scrape(url)
        # レスポンスの HTML から BeautifulSoup オブジェクトを作る
        soup = BeautifulSoup(res.content,"html.parser")
        
        try:
            c1.execute("SELECT url_now FROM game WHERE target_url =?", (url,))
            url_now = c1.fetchone()[0]
            url_now = json.loads(url_now)
        except:
            pass

        #URL投稿
        result_url=origin(soup,url,url_now)
        #更新分があれば投下する
        try:
            for result in result_url:
                await channel_game.send(result)
        except:
            pass
        


#情報取得元サイトの最新情報の取得をするスクレイピング
def origin(soup,url,url_now):
    result_url = []
    urlnew = []
    #情報取得元サイトの最新情報の取得をする(適宜Webページの構成はご自身で調査して、変えてください)
    for article in soup.find_all('div', {'class': 'news-list-contents'})[0].find_all('a'):
        urlnew.append(article.get('href'))
    
    result_url = list(set(urlnew) - set(url_now))

    if len(result_url) == 0:
        return

    try:
        c1.execute("UPDATE game set url_now=? WHERE target_url =?", (json.dumps(urlnew), url))
        conn1.commit()
    except:
        pass

    return result_url

client.run(TOKEN) #ボットのトークン
