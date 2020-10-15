# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 17:34:31 2020

@author: hp
"""
#       İLGİLİ KÜTÜPHANELER
from discord.ext import commands


#%%
client = commands.Bot(command_prefix="get")

@client.event
async def on_ready():
    print("Hai, I'm alive. Thank you for giving my soul.")
    
@client.command()
async def step(ctx):
    await ctx.send("One step forward!")

@client.command()
async def gbhaber(ctx):
    #       GEREKLİ KÜTÜPHANELER
    from PIL import Image, ImageDraw, ImageFont
    import requests #web bağlantısı için
    from bs4 import BeautifulSoup #html parçalamak için
    #%%
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    
    site = requests.get("https://gelecekbilimde.net/", headers=headers)
    soup = BeautifulSoup(site.content, "html.parser")
    #%%
          # FOTOYU ÖZETİ BAŞLIĞI ÇEKME YERİ

    a1 = soup.find("div",{"class":"containerblock_252"})
    a2 = a1.find("div",{"class":"tie-slick-slider"})
    a3 = a2.find("div")
    foto = a3.get("style")
    foto = foto.replace("background-image: url","").replace("(","").replace(")","")
    print("foto linki",foto)
    
    # #       HABERİN SAYFASINDAN ÖZET VE BAŞLIK ÇEKME VAKTİ
    link = "https://gelecekbilimde.net/"+a3.find("a",{"class":"all-over-thumb-link"}).get("href")
    print("haber linki:",link)
    site = requests.get(link, headers=headers)
    soup = BeautifulSoup(site.content, "html.parser")
    baslik = soup.find("h1",{"class":"post-title entry-title"}).get_text()
    a1 = soup.find("div",{"class":"entry-content entry clearfix"})
    a2 = a1.find_all("p")
    a3 = a2[1]
    ozet = a3.get_text().replace("Özet:","").strip()
    # print("```",ozet,"```")

    
    await ctx.send(f"Here your news!\n\n**{baslik}** \nÖZET:\n```{ozet}```\nFoto Linki: {foto} \nHaber:{link}")

client.run('NzY2MzA4NzAzMDA3Mjc3MDY3.X4hemA.EXKTiig6uz-WUIkYCrI47jSY1fo')

