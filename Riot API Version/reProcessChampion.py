import json
import requests

'''
Riot API Data Dragon Champion 정보 전처리
'''


def reProcessChampionLists():
    #Get Latest Version of Patch Note
    getPatchVersions = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()
    latestVersion = getPatchVersions[0]
    
    getFullChampionJSON = requests.get(f'http://ddragon.leagueoflegends.com/cdn/{latestVersion}/data/en_US/champion.json').json()
    reJSON = dict()

    reJSON["Version"] = latestVersion

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

if __name__=="__main__":
    reProcessChampionLists()