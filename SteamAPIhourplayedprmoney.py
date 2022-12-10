#https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=-----&steamid=76561198038062874&format=json&include_appinfo=1
#https://store.steampowered.com/api/appdetails/?appids=107410&filters=basic,price_overview
import requests

#For JSON of owned game with appid & name
hostApi = 'https://api.steampowered.com'
pathApi = '/IPlayerService/GetOwnedGames/v0001/'

#For JSON of price and other information about appid game
hostStore = 'https://store.steampowered.com'
pathStore = '/api/appdetails/'

#Contains   !!! Steam API !!!   and steamID64 for steamuser 
requestQueryApi = {
    'key': '***** INSERT STEAM API HERE *****',
    'steamid': '***** INSERT STEAMID64 HERE *****',
    'format': 'json',
    'include_appinfo': '1'
}

respondApi = requests.get(hostApi+pathApi,requestQueryApi)

gameIndex = 1 # Iterable from amount of games owned 'respondApiGamesLength'
appIDs = []
appNames = []
playTimes = []
respondApiJsonPlaytimeFEMin = []

respondApiJson = respondApi.json()
respondApiGamesLength = len(respondApiJson['response']['games']) #Length for gameIndex iterable
print(respondApiGamesLength)
#for gameIndex in range(respondApiGamesLength):
for gameIndex in range(respondApiGamesLength):
    respondApiJsonName = respondApiJson['response']['games'][gameIndex]['name']
    appNames.append(respondApiJsonName)
    print(respondApiJsonName)

    respondApiJsonAppId = respondApiJson['response']['games'][gameIndex]['appid']
    respondApiJsonPlaytimeFEMin.append(respondApiJson['response']['games'][gameIndex]['playtime_forever']) #In minutes

    playTimes.append(respondApiJsonPlaytimeFEMin)
    appIDs.append(respondApiJsonAppId)


csvAppIDs = str(appIDs)[1:-1].replace(' ','')
print(csvAppIDs)

print(respondApiGamesLength) #Checking amount of games owned

#Gets appid from other request and add basic information and price overview
requestQueryStore = {
    #'appids': f'{respondApiJsonAppId}',
    'appids': f'{csvAppIDs}',
    'filters': 'price_overview'
}

respondGame = requests.get(hostStore+pathStore,requestQueryStore)

respondGameJson = respondGame.json()
print(respondGameJson)
print(respondApiJsonPlaytimeFEMin) #Playtime in minutes

gamePrices = []

respondGameJsonPriceCurrency = respondGameJson[str(appIDs[0])]['data']['price_overview']['currency'] #Assuming it will be same currency for all games
for i in range(respondApiGamesLength):
    #respondGameJsonInitalPriceInCents = respondGameJson[str(appIDs[i])]['data']['price_overview']['initial']
    if respondGameJson[str(appIDs[i])]['success'] and respondGameJson[str(appIDs[i])]['data']:
        gamePrices.append(respondGameJson[str(appIDs[i])]['data']['price_overview']['initial'])
    else:
        gamePrices.append(0)

for i in range(respondApiGamesLength):
    if gamePrices[i] != 0:
        print(appNames[i])
        print(str(gamePrices[i]/100)+respondGameJsonPriceCurrency)
        print(str((respondApiJsonPlaytimeFEMin[i]/60)/(gamePrices[i]/100))+" Hr/"+respondGameJsonPriceCurrency+"\n") #Amount of hours played pr *Currency*(Eur)

    #Free games incl. as no data
    #     
    # print(appNames[i])
    # if gamePrices[i] != 0:
    #     print(str(gamePrices[i]/100)+respondGameJsonPriceCurrency)
    #     print(str((respondApiJsonPlaytimeFEMin[i]/60)/(gamePrices[i]/100))+" Hr/"+respondGameJsonPriceCurrency+"\n") #Amount of hours played pr *Currency*(Eur)
    # else:
    #     print("Game was/is free -> no data\n")
    



##### Write JSON to test.txt for JSON Viewer for analyzing #####
#
###SteamAPIJSON
##Playtime
# respond = requests.get(hostApi+pathApi,requestQueryApi)
# print(respond.json())
# with open('test.txt','w', encoding='utf-8') as f:
#     f.write(str(respond.text))
#     f.close()
#
###StoreJSON
##Price
# respond = requests.get(hostStore+pathStore,requestQueryStore)
# print(respond.json())
# with open('test.txt','w', encoding='utf-8') as f:
#     f.write(str(respond.text))
#     f.close()
###############################################################