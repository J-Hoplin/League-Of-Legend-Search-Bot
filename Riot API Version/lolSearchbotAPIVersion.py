#-*- coding: utf-8 -*-
import discord
import asyncio
import os
import json
import yaml
from discord.ext import commands
from apiRequest import riotAPIRequest
import re # Regex for youtube link
import warnings


with open('config.yml') as f:
    keys = yaml.load(f, Loader=yaml.FullLoader)

####################################################
bottoken = keys['Keys']['discordAPIToken']
riotapiKey = keys['Keys']['riotAPIToken']
apiCall = riotAPIRequest(riotapiKey)
# for lolplayersearch
tierScore = {
    'default' : 0,
    'IRON' : 1,
    'BRONZE' : 2,
    'SILVER' : 3,
    'GOLD' : 4,
    'PLATINUM' : 5,
    'DIAMOND' : 6,
    'MASTER' : 7,
    'GRANDMASTER' : 8,
    'CHALLENGER' : 9
}

def tierCompare(solorank,flexrank):
    #solorank is higher
    if tierScore[solorank] > tierScore[flexrank]:
        return 0
    #flexrank is higher
    elif tierScore[solorank] < tierScore[flexrank]:
        return 1
    # same
    else:
        return 2

####################################################

client = discord.Client() # Create Instance of Client. This Client is discord server's connection to Discord Room
warnings.filterwarnings(action='ignore')
bot = commands.Bot(command_prefix='!')

@client.event # Use these decorator to register an event.
async def on_ready(): # on_ready() event : when the bot has finised logging in and setting things up
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Type !help or !도움말 for help"))
    print("New log in as {0.user}".format(client))


@bot.command()
async def test(ctx,arg):
    await ctx.send(arg)

@client.event
async def on_message(message): # on_message() event : when the bot has recieved a message
    #To user who sent message
    # await message.author.send(msg)
    
    if message.author == client.user:
        return

    if message.content.startswith("!help") or message.content.startswith("!도움말"):
        embed = discord.Embed(title="명령어 사용방법!", description="!전적 (소환사 이름 - 띄어쓰기 붙여쓰기 상관없습니다)", color=0x5CD1E5)
        embed.set_footer(text='Service provided by Hoplin.',
                         icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
        await message.channel.send("도움말!", embed=embed)

    if message.content.startswith("!롤전적"):
        try:
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="소환사 이름이 입력되지 않았습니다!", description="", color=0x5CD1E5)
                embed.add_field(name="Summoner name not entered",
                                value="To use command !롤전적 : !롤전적 (Summoner Nickname)", inline=False)
                embed.set_footer(text='Service provided by Hoplin.',
                                 icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                await message.channel.send("소환사 이름이 입력되지않았습니다!", embed=embed)
            else:
                playerNickname = ' '.join((message.content).split(' ')[1:])
                #Return false if summoner not exist
                getPersonalRecordBox = apiCall.getPersonalGameRecord(playerNickname)
                if not getPersonalRecordBox:
                    embed = discord.Embed(title="존재하지 않는 소환사", description="", color=0x5CD1E5)
                    embed.add_field(name="해당 닉네임의 소환사가 존재하지 않습니다.", value="소환사 이름을 확인해주세요", inline=False)
                    embed.set_footer(text='Service provided by Hoplin.',icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                    await message.channel.send("존재하지않는 소환사입니다!", embed=embed)
                else:
                    record = getPersonalRecordBox["Record"]
                    keys = record.keys()
                    mastery = getPersonalRecordBox["ChampionMastery"]
                    if len(record) == 2:
                        solowinRatio = int((record['Personal/Duo Rank']['win'] / (record['Personal/Duo Rank']['win'] + record['Personal/Duo Rank']['loss'])) * 100)
                        flexwinRatio = int((record['Flex 5:5 Rank']['win'] / (record['Flex 5:5 Rank']['win'] + record['Flex 5:5 Rank']['loss'])) * 100)
                        solotier = record['Personal/Duo Rank']['tier']
                        flextier = record['Flex 5:5 Rank']['tier']
                        tc = tierCompare(solotier,flextier)
                        thumbnail = "lorem ipsum"
                        # Compare tier
                        if tc == 0:
                            thumbnail = solotier
                        elif tc == 1:
                            thumbnail = flextier
                        else:
                            thumbnail = solotier
                        embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
                        embed.add_field(name="Data Source", value="Data by Official Riot API : https://developer.riotgames.com/",inline=False)
                        embed.add_field(name=f"Ranked Solo : {record['Personal/Duo Rank']['tier']} {record['Personal/Duo Rank']['rank']}", value=f"{record['Personal/Duo Rank']['leaguepoint']} LP / {record['Personal/Duo Rank']['win']}W {record['Personal/Duo Rank']['loss']}L / Win Ratio {solowinRatio}%", inline=False)
                        embed.add_field(name=f"Flex 5:5 Rank : {record['Flex 5:5 Rank']['tier']} {record['Flex 5:5 Rank']['rank']}", value=f"{record['Flex 5:5 Rank']['leaguepoint']} LP / {record['Flex 5:5 Rank']['win']}W {record['Flex 5:5 Rank']['loss']}L / Win Ratio {flexwinRatio}%", inline=False)
                        embed.add_field(name=f"Most Used Champion : {mastery['championname']}",value=f"Proficiency Level : {mastery['championlevel']}.Lv / Champion Point : {mastery['championpoint']}pt")
                        embed.set_thumbnail(url=f"https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/Riot%20API%20Version/ranked-emblems/Emblem_{thumbnail}.png?raw=true")
                        embed.set_footer(text='Service provided by Hoplin.',icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                        await message.channel.send("소환사 \"" + playerNickname + "\" 님의 전적", embed=embed)
                        
                    elif len(record) == 0:
                        embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
                        embed.add_field(name="Data Source", value="Data by Official Riot API : https://developer.riotgames.com/",inline=False)
                        embed.add_field(name="Ranked Solo : Unranked", value="Unranked", inline=False)
                        embed.add_field(name="Flex 5:5 Rank : Unranked", value="Unranked", inline=False)
                        embed.set_thumbnail(url="https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/Riot%20API%20Version/ranked-emblems/Emblem_DEFAULT.png?raw=true")
                        embed.set_footer(text='Service provided by Hoplin.',icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                        await message.channel.send("소환사 \"" + playerNickname + "\" 님의 전적", embed=embed)
                        
                    elif len(record) == 1 and "Personal/Duo Rank" not in keys:
                        flexwinRatio = int((record['Flex 5:5 Rank']['win'] / (record['Flex 5:5 Rank']['win'] + record['Flex 5:5 Rank']['loss'])) * 100)
                        embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
                        embed.add_field(name="Data Source", value="Data by Official Riot API : https://developer.riotgames.com/",inline=False)
                        embed.add_field(name="Ranked Solo : Unranked", value="Unranked", inline=False)
                        embed.add_field(name=f"Flex 5:5 Rank : {record['Flex 5:5 Rank']['tier']} {record['Flex 5:5 Rank']['rank']}", value=f"{record['Flex 5:5 Rank']['leaguepoint']} LP / {record['Flex 5:5 Rank']['win']}W {record['Flex 5:5 Rank']['loss']}L / Win Ratio {flexwinRatio}%", inline=False)
                        embed.add_field(name=f"Most Used Champion : {mastery['championname']}",value=f"Proficiency Level : {mastery['championlevel']}.Lv / Champion Point : {mastery['championpoint']}pt")
                        embed.set_thumbnail(url=f"https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/Riot%20API%20Version/ranked-emblems/Emblem_{record['Flex 5:5 Rank']['tier']}.png?raw=true")
                        embed.set_footer(text='Service provided by Hoplin.',icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                        await message.channel.send("소환사 \"" + playerNickname + "\" 님의 전적", embed=embed)
                        
                    elif len(record) == 1 and "Flex 5:5 Rank" not in keys:
                        solowinRatio = int((record['Personal/Duo Rank']['win'] / (record['Personal/Duo Rank']['win'] + record['Personal/Duo Rank']['loss'])) * 100)
                        embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
                        embed.add_field(name="Data Source", value="Data by Official Riot API : https://developer.riotgames.com/",inline=False)
                        embed.add_field(name=f"Ranked Solo : {record['Personal/Duo Rank']['tier']} {record['Personal/Duo Rank']['rank']}", value=f"{record['Personal/Duo Rank']['leaguepoint']} LP / {record['Personal/Duo Rank']['win']}W {record['Personal/Duo Rank']['loss']}L / Win Ratio {solowinRatio}%", inline=False)
                        embed.add_field(name="Flex 5:5 Rank : Unranked", value="Unranked", inline=False)
                        embed.add_field(name=f"Most Used Champion : {mastery['championname']}",value=f"Proficiency Level : {mastery['championlevel']}.Lv / Champion Point : {mastery['championpoint']}pt")
                        embed.set_thumbnail(url=f"https://github.com/J-hoplin1/League-Of-Legend-Search-Bot/blob/master/Riot%20API%20Version/ranked-emblems/Emblem_{record['Personal/Duo Rank']['tier']}.png?raw=true")
                        embed.set_footer(text='Service provided by Hoplin.',icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                        await message.channel.send("소환사 \"" + playerNickname + "\" 님의 전적", embed=embed)
                        
        except BaseException as e:
            print(e)
            embed = discord.Embed(title="봇 로직 내 버그발생!", description="", color=0x5CD1E5)
            embed.add_field(name="봇 로직에서 버그를 발견하였습니다!.", value="서버 운영자 혹은 개발자(jhoplin7259@gmail.com)으로 연락주세요!", inline=False)
            embed.set_footer(text='Service provided by Hoplin.',
                             icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
            await message.channel.send("Discord Bot Logic Error", embed=embed)
            
    if message.content.startswith("!롤모스트"):
        try:
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="소환사 이름이 입력되지 않았습니다!", description="", color=0x5CD1E5)
                embed.add_field(name="Summoner name not entered",
                                value="To use command !롤전적 : !롤전적 (Summoner Nickname)", inline=False)
                embed.set_footer(text='Service provided by Hoplin.',
                                 icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                await message.channel.send("소환사 이름이 입력되지않았습니다!", embed=embed)
            else:
                playerNickname = ' '.join((message.content).split(' ')[1:])
                getMasteryBox = apiCall.getPersonalChampionMasteries(playerNickname)
                keys = list(getMasteryBox.keys())
                if not getMasteryBox:
                    embed = discord.Embed(title="존재하지 않는 소환사", description="", color=0x5CD1E5)
                    embed.add_field(name="해당 닉네임의 소환사가 존재하지 않습니다.", value="소환사 이름을 확인해주세요", inline=False)
                    embed.set_footer(text='Service provided by Hoplin.',icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                    await message.channel.send("존재하지않는 소환사입니다!", embed=embed)
                else:
                    embed = discord.Embed(title=f"소환사 \"{playerNickname}\" 님의 Most Top 3", description="", color=0x5CD1E5)
                    embed.add_field(name="Data Source", value="Data by Official Riot API : https://developer.riotgames.com/",inline=False)
                    count = 1
                    thumbnail = 'lorem ipsum'
                    for i in getMasteryBox:
                        key = keys[count - 1]
                        p = getMasteryBox[key]
                        embed.add_field(name=f"Most{count} : {key}", value=f"Proficiency Level : {p['championlevel']}.Lv / Champion Point : {p['championpoint']}pt",inline=False)
                        if count == 1:
                            thumbnail = p['championImage']
                        else:
                            pass
                        count += 1
                    embed.set_thumbnail(url=f"http://ddragon.leagueoflegends.com/cdn/11.13.1/img/champion/{thumbnail}")
                    embed.set_footer(text='Service provided by Hoplin.',icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
                    await message.channel.send("소환사 \"" + playerNickname + "\" 님의 Most Top3", embed=embed)
        except BaseException as e:
            embed = discord.Embed(title="존재하지 않는 소환사", description="", color=0x5CD1E5)
            embed.add_field(name="해당 닉네임의 소환사가 존재하지 않습니다.", value="소환사 이름을 확인해주세요", inline=False)
            embed.set_footer(text='Service provided by Hoplin.',icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
            await message.channel.send("존재하지않는 소환사입니다!", embed=embed)
client.run(bottoken)
