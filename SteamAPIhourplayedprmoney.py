import csv
import requests
import os

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    steamAPI = input('Input Steam API:\n')
    steamID64 = input('SteamID64 of user:\n')
    os.system('cls' if os.name == 'nt' else 'clear')


    #For JSON of owned game with appid & name
    hostApi = 'https://api.steampowered.com'
    pathApi = '/IPlayerService/GetOwnedGames/v0001/'

    #For JSON of price and other information about appid game
    hostStore = 'https://store.steampowered.com'
    pathStore = '/api/appdetails/'

    #Contains   !!! Steam API !!!   and steamID64 for steamuser 
    requestQueryApi = {
        'key': f'{steamAPI}',
        'steamid': f'{steamID64}',
        'format': 'json',
        'include_appinfo': '1'
    }

    respondApi = requests.get(hostApi+pathApi,requestQueryApi)

    appIDs = []
    appNames = []
    playTimes = []
    respondApiJSON = respondApi.json()

    respondApiGamesLength = len(respondApiJSON['response']['games']) #Length for gameIndex iterable

    #Appends app names, play time and app ids for game with game index corresponding to eachother
    for gameIndex in range(respondApiGamesLength):
        appNames.append(respondApiJSON['response']['games'][gameIndex]['name'])
        playTimes.append(respondApiJSON['response']['games'][gameIndex]['playtime_forever']) #In minutes
        appIDs.append(respondApiJSON['response']['games'][gameIndex]['appid'])

    #Make list to CSV
    csvAppIDs = str(appIDs)[1:-1].replace(' ','')

    #Gets appid from other request and add basic information and price overview
    requestQueryStore = {
        'appids': f'{csvAppIDs}',
        'filters': 'price_overview'
    }

    #Price request
    respondGame = requests.get(hostStore+pathStore,requestQueryStore)
    respondGameJSON = respondGame.json()

    gamePrices = []
    respondGameJsonPriceCurrency = respondGameJSON[str(appIDs[0])]['data']['price_overview']['currency'] #Assuming it will be same currency for all games

    #Appends prices data for corresponding game index
    for i in range(respondApiGamesLength):
        if respondGameJSON[str(appIDs[i])]['success'] and respondGameJSON[str(appIDs[i])]['data']:
            gamePrices.append(respondGameJSON[str(appIDs[i])]['data']['price_overview']['initial'])
        else:
            gamePrices.append(0)

    #New lists for sorting
    relevantAppIDs = []
    relevantAppNames = []
    relevantGamePrice = []
    relevantAppPlayedHrs = []
    relevantAppPlayedHrsPrPrice = []

    #Appends relevant data
    for i in range(respondApiGamesLength):
        if gamePrices[i] != 0:
            relevantAppIDs.append(appIDs[i])
            relevantAppNames.append(appNames[i])
            relevantGamePrice.append(gamePrices[i]/100)
            relevantAppPlayedHrs.append(round(playTimes[i]/60,2))
            relevantAppPlayedHrsPrPrice.append((playTimes[i]/60)/(gamePrices[i]/100))

    #Sorts for hours played
    relevantZip = zip(relevantAppIDs,relevantAppNames,relevantGamePrice,relevantAppPlayedHrs,relevantAppPlayedHrsPrPrice)
    relevantList = list(relevantZip)
    relevantSortedList = sorted(relevantList, key=lambda row:row[3])


    #Prints in console for debugging/showing
    for i in range(len(relevantSortedList)):
        print(relevantSortedList[i][1]+ ": "+ str(relevantSortedList[i][0]))
        print("Price: "+ str(relevantSortedList[i][2])+str(respondGameJsonPriceCurrency))
        print("Hours played: "+ str(relevantSortedList[i][3]))
        print("Hours played pr "+ str(respondGameJsonPriceCurrency) + ": "+ str(relevantSortedList[i][4])+"\n")

    #Asking user if they wanna save the data
    if input('Wanna save to CSV? [Y,n]\n') == 'Y':
        #Writes to CSV
        with open('SteamAppsHrsPr'+respondGameJsonPriceCurrency+".csv","w",newline='')as f:
            writer = csv.writer(f)
            headerForCSV = ['appID','name','price' + f'{respondGameJsonPriceCurrency}','hours','HRsPr'+respondGameJsonPriceCurrency]
            writer.writerow(headerForCSV)
            writer.writerows(relevantSortedList[::-1])
            f.close()

    input('Press any key to close.')
main()