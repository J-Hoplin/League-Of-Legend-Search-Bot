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

with open('championInfo.json') as f:
    champInfo = json.load(f)

mapRankName = {
    'RANKED_FLEX_SR' : "Flex 5:5 Rank",
    'RANKED_SOLO_5x5' : "Personal/Duo Rank"
}

class riotAPIRequest(object):
    apiKey = "RGAPI-2ca26509-17ab-4ff9-9224-1332d0df40b0"
    def __init__(self) -> None:
        self.KRRegionAPIEndPoint='https://kr.api.riotgames.com'
        self.puuidEnd = "/lol/summoner/v4/summoners/by-name/"# /lol/summoner/v4/summoners/by-name/{summonerName}
        self.personalInfoEnd = "/lol/league/v4/entries/by-summoner/"  #/lol/league/v4/entries/by-summoner/{encryptedSummonerId}
        self.personalChampionMastery = "/lol/champion-mastery/v4/champion-masteries/by-summoner/"#/lol/champion-mastery/v4/champion-masteries/by-summoner/{encryptedSummonerId}
        self.req_header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.96 Safari/537.36",
            "Accept-Language": "ko-KR",
            "X-Riot-Token": riotAPIRequest.apiKey
        }
    
    def get_puuid_and_encryptedID(self,name) -> bool:
        getResponseJSON = requests.get(self.KRRegionAPIEndPoint + self.puuidEnd + quote(name),headers=self.req_header).json()
        summonerKeyBox = {
            'encid' : getResponseJSON['id'],
            'puuid' : getResponseJSON['puuid']
        }
        return  summonerKeyBox
        
    def getPersonalChampionMastery(self,name) -> bool:  
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
        try:
            keybox = self.get_puuid_and_encryptedID(name)
            return requests.get(self.KRRegionAPIEndPoint + self.personalChampionMastery + keybox['encid'], headers=self.req_header).json()[0]
        except KeyError as e: #For not-Existing ID
            return  False
        
    def getPersonalGameRecord(self,name) -> bool:
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