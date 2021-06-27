import json
import requests

'''
Riot API Data Dragon Champion 정보 전처리
'''

getFullChampionJSON = requests.get('http://ddragon.leagueoflegends.com/cdn/11.13.1/data/en_US/champion.json').json()
reJSON = dict()

for i in getFullChampionJSON['data'].keys():
    ckey = getFullChampionJSON['data'][i]['key']
    cid = getFullChampionJSON['data'][i]['id']
    tags = getFullChampionJSON['data'][i]['tags']
    imageli = getFullChampionJSON['data'][i]['image']['full']
    reJSON[ckey] = {
        'name' : cid,
        'tags' : tags,
        'image' : imageli
    }
with open('championInfo.json','w') as f:
    json.dump(reJSON,f, indent = 4, sort_keys=True)