# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 17:34:31 2020

@author: muki
Geliştirici: Mustafa
Keyfimin kaçtığı şu günlerde başına oturup saatlerce uğraşabildiğim tek şey buydu sanırım.

"""#%%
import discord
from discord.ext import commands
import random
import requests #web bağlantısı için
from bs4 import BeautifulSoup #html parçalamak için
import os
import praw
path = os.path.dirname(os.path.abspath(__file__))+"/"
reddit = praw.Reddit(client_id="aOJkDPW0KXsXjQ",client_secret="Mq5wxnbMyXQ6OaBN2CJorBZUX2U8Mg" ,user_agent="vfor")
#%%
TOKEN = open(path+"VfMuki.txt","r").readline()
client = commands.Bot(command_prefix = '+', description = "Bu bot muki tarafından kişisel çıkarlar için oluşturulmuştur!")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

#%%

@client.command()
async def test(ctx,*args):
    await ctx.channel.purge(limit=1)
    await ctx.send(f"{args[1]}, {args[2]}")

@client.command()
async def mana(ctx,*args):
    kelime = args[0]
    link = "https://tureng.com/en/turkish-english/" + kelime
    site = requests.get(link, headers=headers)
    soup = BeautifulSoup(site.content, "html.parser")
    #Olası bir yazım hatası için "bunu mu demek istediniz sayfası"
    
    try:
        suggestion_list = soup.find("ul",{"class":"suggestion-list"})
        suggestios = suggestion_list.find_all("li")
        maybe_ = "Maybe the correct one is..."
        embed = discord.Embed(title = f"I could'nt find it :/ {maybe_}", color = discord.Color.dark_red())
        sabit=0
        for sug in suggestios:
            sug_link = "https://tureng.com" +sug.find('a').get('href')
            embed.add_field(name = f"{sug.get_text()}", value = f"{sug_link}", inline=True)
            sabit = sabit + 1
            if sabit == 5:
                break
    #Kelime doru yazıldıysa veya eşleşti ise>>>
    except:
        
        ses = soup.find("audio", {"id" : "turengVoiceENTRENus"})
        ses_link = "http:" + ses.find("source").get("src")
        table = soup.find("table", {"class" : "table table-hover table-striped searchResultsTable"})
        kelimeler = table.find_all("tr")
        bosluk = " "*20
        embed = discord.Embed(title = f"*{kelime}* via. Tureng Dict.{bosluk}", url = f"{link}", color = discord.Color.dark_red())
        embed.add_field(name = "How to pronounce in US", value=f"{ses_link}", inline= False)
        sabit = 0
        for tr in kelimeler:
            
            try:
                eng_word_type = tr.find("td", {"class":"en tm"}).find("i").get_text()
                tr_word = tr.find("td", {"class":"tr ts"}).get_text()
                #embed mesajda add field  yapıp isim ve value diyerekten yapılabilir
                try:
                    embed.add_field(name = f"{eng_word_type}", value = f"{tr_word}", inline=True)
                    sabit = sabit + 1
                    if sabit > 5:
                        break
                except:
                    pass
            except:
                pass
    await ctx.send(embed=embed)

#print(reddit.read_only)  # Output: True
@client.command()
async def redd(ctx):
    embed = discord.Embed(color=discord.Color.red())
    for submission in reddit.subreddit("learnpython").hot(limit=5):
        embed.add_field(name=f'{submission.title}',value=f"{submission.url}", inline= False)
        #embed.add_field(name='Permalink',value=f"{submission.permalink}", inline= False)
    #embed.add_field(name="^^", value=f"~~{quote[1]}", inline= False)
    #embed.set_thumbnail(f"{ctx.guild.icon}")
    #embed.set_thumbnail(url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")
    await ctx.send(embed=embed)
    #print(submission.content)
#%%
@client.event
async def on_ready():
    print('{0.user} olarak giriş yaptık, güzel günler dilerim!'.format(client))

#   Sembolik bir komut /Vfor yaz bunu dönsün
@client.command()
async def Vfor(ctx):
    await ctx.send("V for Muki!")
#   Random Emoji!
@client.command()
async def face(ctx):
    with open(path+"emoji_faces.txt",encoding="utf-8") as f:
        lines = f.readlines()
        face = random.choice(lines)
    await ctx.channel.purge(limit=1)
    await ctx.send(f"{face}")  
#   Çok güzel anime quote'lerini /quote komutuyla random verme
@client.command()
async def quote(ctx):
    with open(path+"quotes.txt",encoding="utf-8") as f:
        lines = f.readlines()
        quote = random.choice(lines)
    quote = quote.split(" – ") #Söz sahibi ve söz ayrıldı
    embed = discord.Embed(color=discord.Color.red())
    embed.add_field(name=f'{quote[0]}',value=f"~{quote[1]}", inline= False)
    #embed.add_field(name="^^", value=f"~~{quote[1]}", inline= False)
    #embed.set_thumbnail(f"{ctx.guild.icon}")
    #embed.set_thumbnail(url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")
    await ctx.send(embed=embed)
#Etiketlenen kişinin avatarını atar, pp'sini yani
@client.command()
async def avatar(ctx,member:discord.Member): #argument olarak memberi discord.membere eşitledik ki member diyince direkt dicord member algılasın
    #await ctx.send(f"{member.display_name} {member.avatar_url} {member.public_flags} {member.raw_status} {member.desktop_status}")
    show_Avatar = discord.Embed(color = discord.Color.dark_purple())
    show_Avatar.add_field(name= "👻",value=f"{member.display_name}") #koyu altın rengi seçtik
    show_Avatar.set_image(url="{}".format(member.avatar_url))
    await ctx.send(embed=show_Avatar)

@client.command()
async def dolar(ctx):
    site = requests.get("https://www.google.com/search?q=dolar+kuru&oq=dolar+kuru&aqs=chrome..69i57j0i20i263j0l6.1700j1j7&sourceid=chrome&ie=UTF-8", headers=headers)
    soup = BeautifulSoup(site.content, "html.parser")
    soup = soup.find("div",{"class":"dDoNo vk_bk gsrt gzfeS"})
    dolar = soup.get_text()
    embed = discord.Embed(color = discord.Color.green())
    embed.add_field(name = '1 Dolar>>',value = f"{dolar}", inline = False)
    #embed.add_field(name="^^", value=f"~~{quote[1]}", inline= False)
    try:
        embed.set_image(url = "https://www.webtekno.com/images/editor/default/0002/88/1688b681b45fa466bfbfb820c0d6ae125c90fcec.jpeg")
    except:
        pass
    #embed.set_thumbnail(url="/dolar_17.jpg")
    #await message.channel.purge(limit=1)
    await ctx.channel.send(embed = embed)

@client.command()
async def gbhaber(ctx,*,a=5):
    #   GEREKLİ KÜTÜPHANELER
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    site = requests.get("https://gelecekbilimde.net/", headers=headers)
    soup = BeautifulSoup(site.content, "html.parser")
    #   FOTOYU ÖZETİ BAŞLIĞI ÇEKME YERİ
    a1 = soup.find("div",{"class":"containerblock_252"})
    a2 = a1.find("div",{"class":"tie-slick-slider"})
    a3 = a2.find("div")
    foto = a3.get("style")
    foto = foto.replace("background-image: url","").replace("(","").replace(")","")
    print("foto linki",foto)
    #   HABERİN SAYFASINDAN ÖZET VE BAŞLIK ÇEKME VAKTİ
    link = "https://gelecekbilimde.net/"+a3.find("a",{"class":"all-over-thumb-link"}).get("href")
    print("haber linki:",link)
    site = requests.get(link, headers=headers)
    soup = BeautifulSoup(site.content, "html.parser")
    baslik = soup.find("h1",{"class":"post-title entry-title"}).get_text()
    a1 = soup.find("div",{"class":"entry-content entry clearfix"})
    a2 = a1.find_all("p")
    a3 = a2[1]
    ozet = a3.get_text().replace("Özet:","").strip()
    embed = discord.Embed()
    embed = discord.Embed(title = f"{baslik}", url = f"{link}", color = discord.Color.blue())
    embed.add_field(name = "Özet", value=f"{ozet}", inline= False)
    embed.add_field(name = "Haber Resmi", value = f"{foto}", inline=True)
    embed.add_field(name = "Haber Linki", value = f"{link}", inline= True)
    embed.set_thumbnail(url=foto)
    await ctx.send(embed=embed)
    #await ctx.send(f"Here your news!\n\n**{baslik}** \nÖZET:\n```{ozet}```\nFoto Linki: {foto} \nHaber:{link}")

@client.command()
async def temizle(ctx,*,amount=5):
    await ctx.channel.purge(limit=amount)

client.run(TOKEN)
