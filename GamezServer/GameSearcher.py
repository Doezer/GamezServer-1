import GamezServerDao
import Logger
import urllib2
import json
import urllib
import ConfigParser
import unicodedata

class GameSearcher(object):
    """description of class"""

    def __init__(self, dbfile, conffile):
        self.dbfile = dbfile
        self.conffile = conffile

    def start(self):
        logger = Logger.Logger(self.dbfile)
        if(self.DownloaderEnabled()):
            logger.Log("Starting Search")
            dao = GamezServerDao.GamezServerDao()
            for row in dao.GetWantedGames(self.dbfile):
                gameTitle = row[1]
                console = str(row[4])
                gameId = str(row[8])
                logger.Log("Searching for game: " + gameTitle + " - " + console)
                self.SearchUsenetCrawler(gameTitle,console,gameId)
        else:
            logger.Log("No Downloaders Enabled. Terminating Search.")

    def DownloaderEnabled(self):
        return self.UseSabnzbd()


    def UseSabnzbd(self):
        enable = False
        config = ConfigParser.RawConfigParser()
        config.read(self.conffile)
        apiKey = config.get('Sabnzbd','SabnzbdApiKey')
        if(config.get('Sabnzbd','EnableSabnzbd') == "1"):
            enable = True
        if(enable and len(apiKey) > 0):
            return True
        else:
            return False

    def SendToSab(self, url, nzbName, gameId):
        config = ConfigParser.RawConfigParser()
        apikey = "96febf6555fbcb72fdee5c0f63a294f8"
        config.read(self.conffile)
        category = str(config.get('Sabnzbd','SabnzbdCategory')).replace("'","")
        if(category <> ''):
            category = '&cat=' + category
        sabUrl = "http://127.0.0.1:8080/sabnzbd/api?apikey=" + apikey + "&mode=addurl&name=" + urllib.quote_plus(url) + "&script=gamezPostProcess.py&nzbname=[" + gameId + "] - " + nzbName + category
        responseObject = urllib.FancyURLopener({}).open(sabUrl)
        responseObject.read()
        responseObject.close()
        return

    def SearchUsenetCrawler(self, gameTitle, console,gameId):
        logger = Logger.Logger(self.dbfile)
        enable = False
        config = ConfigParser.RawConfigParser()
        config.read(self.conffile)
        print gameTitle
        gameTitle = unicodedata.normalize('NFKD', gameTitle).encode('ascii','ignore')
        print gameTitle
        apiKey = str(config.get('UsenetCrawler','UsenetCrawlerApiKey')).replace("'","")
        if(config.get('UsenetCrawler','EnableUsenetCrawler') == "1"):
            enable = True
        if(enable and len(apiKey) > 0):
            cat = "1000"
            if(console == "Nintendo Wii"):
                cat = "1030"
            if(console == "Microsoft XBOX 360"):
                cat = "1050"
            if(console == "Sony Playstation 3"):
                cat = "1080"
            if(console == "Nintendo DS"):
                cat = "1010"
            downloadGuid = ""
            nzbName = ""
            isGameFound = False
            url = "http://www.usenet-crawler.com/api?apikey=" + apiKey + "&t=search&cat=" + cat + "&o=json&q=" + gameTitle
            try:
                jsonData = urllib2.urlopen(url).read()
                resultDict = json.loads(jsonData)
                for entry in resultDict["channel"]["item"]:
                    nzbName = json.loads(json.dumps(entry))["title"]
                    try:
                        if(isGameFound == False):
                            attributes = entry["attr"]
                            for attr in attributes:
                                attributeName = json.loads(json.dumps(attr))["@attributes"]["name"]
                                if(attributeName == "guid"):
                                    downloadGuid = json.loads(json.dumps(attr))["@attributes"]["value"]
                                    isGameFound = True
                    except:
                        continue
            except:
                print("Unable to Search Usenet-Crawler")
            if(len(downloadGuid) > 0):
                logger.Log("Game Found on Usenet-Crawler. Attempting to Download.")
                if(self.UseSabnzbd()):
                    url = "http://www.usenet-crawler.com/api?apikey=" + apiKey + "&t=get&id=" + downloadGuid
                    logger.Log("Sending Game to Sabnzbd+")
                    self.SendToSab(url,nzbName,gameId)
                    dao = GamezServerDao.GamezServerDao()
                    logger.Log("Updating Game Status to Snatched")
                    dao.UpdateGameStatus(self.dbfile, gameId, "Snatched")
            else:
                logger.Log("Game Not Found on Usenet-Crawler")
