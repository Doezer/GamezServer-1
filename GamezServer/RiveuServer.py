import ConfigParser
import urllib2
import urllib
import GamezServerDao
import Logger
import os

class RiveuServer(object):
    def __init__(self, dbFile, conffile):
        self.dbfile = dbFile

        config = ConfigParser.RawConfigParser()
        config.read(conffile)
        self.consoles = config.get('GamezServer','consoles')
        if self.consoles == '*':
            self.consoles = []

    def UpdateConsoles(self):
        logger = Logger.Logger(self.dbfile)
        logger.Log('Downloading Console List')
        dn = os.path.dirname(os.path.realpath(__file__))
        fn = os.path.join(dn,"consoles.txt")
        openConsoleFile = open(fn, 'r')
        consoleFile = openConsoleFile.read()
        dao = GamezServerDao.GamezServerDao()
        for console in consoleFile.split('\n'):
            if(len(console) > 0 and (not self.consoles or console.replace("\r","") in self.consoles)):
                dao.AddConsole(self.dbfile, console.replace("\r",""))
        return

    def UpdateGames(self):
        logger = Logger.Logger(self.dbfile)
        logger.Log('Downloading Games List')
        dn = os.path.dirname(os.path.realpath(__file__))
        fn = os.path.join(dn,"games.txt")
        openGamesFile = open(fn, 'r')
        gamesFile = openGamesFile.read()
        dao = GamezServerDao.GamezServerDao()
        for game in gamesFile.split('\n'):
            if(len(game) > 0):
                gameAttributes = game.split('::||::')
                gameId = gameAttributes[0].decode("utf-8").replace(u'\ufeff','').replace(u'\xa0',' ').replace(u'\xb7','').replace(u'\xb2','').replace(u'\u2161','').replace(u'\u2164','')
                logger.Log(gameId)
                gameTitle = str(gameAttributes[1]).decode("utf-8").replace(u'\ufeff','').replace(u'\xa0',' ').replace(u'\xb7','').replace(u'\xb2','').replace(u'\u2161','').replace(u'\u2164','')
                gameDescription = str(gameAttributes[2]).decode("utf-8").replace(u'\ufeff','').replace(u'\xa0',' ').replace(u'\xb7','').replace(u'\xb2','').replace(u'\u2161','').replace(u'\u2164','')
                releaseDate = str(gameAttributes[3]).decode("utf-8").replace(u'\ufeff','').replace(u'\xa0',' ').replace(u'\xb7','').replace(u'\xb2','').replace(u'\u2161','').replace(u'\u2164','')
                coverArt = str(gameAttributes[4]).decode("utf-8").replace(u'\ufeff','').replace(u'\xa0',' ').replace(u'\xb7','').replace(u'\xb2','').replace(u'\u2161','').replace(u'\u2164','')
                console = str(gameAttributes[5]).decode("utf-8").replace(u'\ufeff','').replace(u'\xa0',' ').replace(u'\xb7','').replace(u'\xb2','').replace(u'\u2161','').replace(u'\u2164','')
                if console.replace("\r","") in self.consoles or not self.consoles:
                    dao.AddGame(self.dbfile, gameId, gameTitle, gameDescription, releaseDate, coverArt, console.replace("\r",""))
        return

    def SendNotification(self, message, username, password):
        data = "CMD=SEND_NOTIFICATION&Username=" + username + "&Password=" + password + "&Message=" + urllib.quote_plus(message)
        url = 'http://riveu.com/API.aspx?' + data
        responseObject = urllib.FancyURLopener({}).open(url)
        responseObject.read()
        responseObject.close()
