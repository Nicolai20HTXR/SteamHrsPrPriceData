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
    dataForCSV = []
    respondGameJsonPriceCurrency = respondGameJSON[str(appIDs[0])]['data']['price_overview']['currency'] #Assuming it will be same currency for all games

    #Appends prices data for corresponding game index
    for i in range(respondApiGamesLength):
        if respondGameJSON[str(appIDs[i])]['success'] and respondGameJSON[str(appIDs[i])]['data']:
            gamePrices.append(respondGameJSON[str(appIDs[i])]['data']['price_overview']['initial'])
        else:
            gamePrices.append(0)


    #Prints in console for debugging/showing
    for i in range(respondApiGamesLength):
        if gamePrices[i] != 0:
            print(appNames[i])
            print(str(gamePrices[i]/100)+respondGameJsonPriceCurrency)
            print(str(playTimes[i]/6))
            print(str((playTimes[i]/60)/(gamePrices[i]/100))+" Hr/"+respondGameJsonPriceCurrency+"\n") #Amount of hours played pr *Currency*(Eur)
            dataForCSV.append([appIDs[i],appNames[i],gamePrices[i]/100,round(playTimes[i]/60,2),round((playTimes[i]/60)/(gamePrices[i]/100),2)])

    #Writes to CSV
    with open('steamplayedgamesprice.csv',"w",newline='')as f:
        writer = csv.writer(f)
        headerForCSV = ['appID','name','priceEUR','hours','HRsPrPrice']
        writer.writerow(headerForCSV)
        writer.writerows(dataForCSV)
        f.close()


    #Sorting file for hours played

    with open('steamplayedgamesprice.csv',newline='') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        sortedlist = sorted(spamreader, key=lambda row:float(row['hours']), reverse=True)
        csvfile.close()


    with open('steamplayedgamesprice.csv', 'w',newline='') as f:
        fieldnames = ['appID','name','priceEUR','hours','HRsPrPrice']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in sortedlist:
            writer.writerow(row)
        f.close()

    input('Press any key to close.')
main()