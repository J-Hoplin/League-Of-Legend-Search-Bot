'''
KR Riot API End Point

-> 	kr.api.riotgames.com

quote() : url to encode
'''

# encid : 5ClrZV6I5PMUl6byGJ7MVejLfW2YfGxylkY999B6q1zbf4w
# puuid : Fy50ddrXuPpwZMInrRrZPsT2tCAHlQFrI5G9NI_-Lu9R91L4i7S09sbB0tquRcr-ST3u3NJdEJCi9A

import requests
import json
from urllib.parse import quote
from typing import MutableSequence, Any
from reProcessChampion import reProcessChampionLists

with open('championInfo.json') as f:
    champInfo = json.load(f)

mapRankName = {
    'RANKED_FLEX_SR' : "Flex 5:5 Rank",
    'RANKED_SOLO_5x5' : "Personal/Duo Rank"
}

class riotAPIRequest(object):
    def __init__(self, riotapikey) -> None:
        self.KRRegionAPIEndPoint='https://kr.api.riotgames.com'
        self.puuidEnd = "/lol/summoner/v4/summoners/by-name/"# /lol/summoner/v4/summoners/by-name/{summonerName}
        self.personalInfoEnd = "/lol/league/v4/entries/by-summoner/"  #/lol/league/v4/entries/by-summoner/{encryptedSummonerId}
        self.personalChampionMastery = "/lol/champion-mastery/v4/champion-masteries/by-summoner/"#/lol/champion-mastery/v4/champion-masteries/by-summoner/{encryptedSummonerId}
        self.req_header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.96 Safari/537.36",
            "Accept-Language": "ko-KR",
            "X-Riot-Token": riotapikey
        }
    
    def reOpenJSON(self):
        with open('championInfo.json') as f:
            champInfo = json.load(f)
    
    def update_CInfo(self):
        if requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0] != champInfo["Version"]:
            reProcessChampionLists()
            self.reOpenJSON()
        else:
            pass
    
    def get_puuid_and_encryptedID(self,name) -> bool:
        getResponseJSON = requests.get(self.KRRegionAPIEndPoint + self.puuidEnd + quote(name),headers=self.req_header).json()
        summonerKeyBox = {
            'encid' : getResponseJSON['id'],
            'puuid' : getResponseJSON['puuid']
        }
        return summonerKeyBox
        
    def getPersonalChampionMastery(self,name) -> bool:
        self.update_CInfo()
        try:
            keybox = self.get_puuid_and_encryptedID(name)
            mastery = requests.get(self.KRRegionAPIEndPoint + self.personalChampionMastery + keybox['encid'], headers=self.req_header).json()[0]
            chid = mastery['championId']
            chlv = mastery['championLevel']
            chpoint = mastery['championPoints']
            reProcessMastery = {
                'championname' : champInfo[str(chid)]["name"],
                'championlevel' : chlv,
                'championpoint' : chpoint,
                'championImage' : champInfo[str(chid)]["image"]    
            }
            return reProcessMastery
        except KeyError as e: #For not-Existing ID
            return  False
    
    def getPersonalChampionMasteries(self,name) -> bool:
        self.update_CInfo()
        try:
            keybox = self.get_puuid_and_encryptedID(name)
            mastery = requests.get(self.KRRegionAPIEndPoint + self.personalChampionMastery + keybox['encid'], headers=self.req_header).json()
            reprocessmastery = dict()
            if len(mastery) > 3:
                mastery = mastery[0:3]
                for i in mastery:
                    chid = i['championId']
                    chlv = i['championLevel']
                    chpoint = i['championPoints']
                    reprocessmastery[champInfo[str(chid)]["name"]] = {
                        'championlevel' : chlv,
                        'championpoint' : chpoint,
                        'championImage' : champInfo[str(chid)]["image"]
                    }
            else:
                for i in mastery:
                    chid = i['championId']
                    chlv = i['championLevel']
                    chpoint = i['championPoints']
                    reprocessmastery[champInfo[str(chid)]["name"]] = {
                        'championlevel' : chlv,
                        'championpoint' : chpoint,
                        'championImage' : champInfo[str(chid)]["image"]
                    }
            return reprocessmastery
        except KeyError as e: #For not-Existing ID
            return  False
        
    def getPersonalGameRecord(self,name) -> bool:
        self.update_CInfo()
        try:
            keybox = self.get_puuid_and_encryptedID(name)
            getMastery = self.getPersonalChampionMastery(name)
            getResponseJSON = requests.get(self.KRRegionAPIEndPoint + self.personalInfoEnd + keybox['encid'], headers=self.req_header).json()
            reProcessRecord = dict()
            for i in getResponseJSON:
                reProcessRecord[mapRankName[i['queueType']]] = {
                    'tier' : f"{i['tier']}",
                    'rank' : f"{i['rank']}",
                    'leaguepoint' : i['leaguePoints'],
                    'win' : i['wins'],
                    'loss' : i['losses']
                }
            summary = {
                "Record" : reProcessRecord,
                "ChampionMastery" : getMastery
            }
            return summary
        except KeyError as e: #For not-Existing ID
            return  False
