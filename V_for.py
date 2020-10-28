# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 17:34:31 2020

@author: muki
"""
#%%
import discord
from discord.ext import commands
import random
import requests #web bağlantısı için
from bs4 import BeautifulSoup #html parçalamak için


TOKEN = open("VfMuki.txt","r").readline()
client = commands.Bot(command_prefix='*', description="Bu muki tarafından kişisel çıkarlar için oluşturulmuş bir bottur!")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
site = requests.get("https://bayart.org/anime-quotes/", headers=headers)
soup = BeautifulSoup(site.content, "html.parser")
#%%

@client.event
async def on_ready():
    print('{0.user} olarak giriş yaptık, güzel günler dilerim!'.format(client))
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('.selamlar'):
        await message.channel.send('Selamlar! Nasıl görünüyorum ')

    if message.content.startswith("V "):
        await message.channel.send(f'Bana mesaj attığını görüyorum ama ne yazdığını pek anlamıyorum, {client.user} üzgün:/')

#   Sembolik bir komut /Vfor yaz bunu dönsün
@client.command()
async def Vfor(ctx):
    await ctx.send("V for Muki!")


#   Çok güzel anime quote'lerini /quote komutuyla random verme
@client.command()
async def quote(ctx):

    quotes_block = soup.find("div",{"class":"entry-content"})
    #top_10 = quotes_block.find_all("blockquote",{"class":"wp-block-quote"})
    best_quotes_block = quotes_block.find("ul") #ul bloğunun li elementlerinin içinde
    best_quotes = best_quotes_block.find("li")
    best_quotes = best_quotes.get_text().split('“') 
    """Tüm sözler tek bir elemente
    toplanmıştı. Tek elementteki sözleri “ 'den split ile 
    ayırdım. Böylece tüm sözler ayrı ayrı elime düştü. Son olarak bu sözlerdeki
    diğer işareti replace ile alırım ve söyleyen kişiyi de ayrı göstermek için
    yine split ile söz sahibi ve sözü ayrı ayrı yere koyarım! """
    quote = random.choice(best_quotes) #Söz seçildi
    quote = quote.replace("”"," ") #Gereksiz işaret kaldırıldı
    quote = quote.split("  – ") #Söz sahibi ve söz ayrıldı
    embed = discord.Embed(color=discord.Color.red())
    embed.add_field(name='"',value=f"{quote[0]}", inline= False)
    embed.add_field(name=">", value=f"{quote[1]}", inline= False)
    #embed.set_thumbnail(f"{ctx.guild.icon}")
    #embed.set_thumbnail(url="https://pluralsight.imgix.net/paths/python-7be70baaac.png")

    await ctx.send(embed=embed)

@client.command()
async def avatar(ctx,member:discord.Member): #argument olarak memberi discord.membere eşitledik ki member diyince direkt dicord member algılasın
    #await ctx.send(f"{member.display_name} {member.avatar_url} {member.public_flags} {member.raw_status} {member.desktop_status}")
    show_Avatar = discord.Embed(color = discord.Color.dark_purple())
    show_Avatar.add_field(name= "👻",value=f"{member.display_name}") #koyu altın rengi seçtik
    show_Avatar.set_image(url="{}".format(member.avatar_url))
    await ctx.send(embed=show_Avatar)

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
   # await ctx.send(f"Here your news!\n\n**{baslik}** \nÖZET:\n```{ozet}```\nFoto Linki: {foto} \nHaber:{link}")

@client.command()
async def temizle(ctx,*,amount=5):
    await ctx.channel.purge(limit=amount)

client.run(TOKEN)
