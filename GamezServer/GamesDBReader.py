import ConfigParser
import codecs
import urllib2
from xml.dom.minidom import parseString
from GamezServer import GamezServerDao
import Logger
import os


class GamesDBReader(object):
    global fullUpdate
    fullUpdate = False

    def __init__(self, dbFile):
        self.dbfile = dbFile


    def RetrievePlatformList(self):
        logger = Logger.Logger(self.dbfile)
        logger.Log('Retriving List of Platforms')
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        infile = opener.open('http://thegamesdb.net/api/GetPlatformsList.php')
        page = infile.read()
        opener.close()
        dom = parseString(page)
        platforms = dom.getElementsByTagName('Platform')
        dao = GamezServerDao.GamezServerDao()
        # dn = os.path.dirname(os.path.realpath(__file__))
        # fn = os.path.join(dn,"consoles.txt")
        # file = open(fn, "w")
        for platform in platforms:
            # id = platform.getElementsByTagName('id')[0].firstChild.data
            console = platform.getElementsByTagName('name')[0].firstChild.data
            # file.write("%s\n" % (console))
            dao.AddConsole(self.dbfile, console)
            # logger.Log("Name: %s, ID: %s" % (name, id))
        # file.close()
        return

    def RetrieveGameList(self):
        logger = Logger.Logger(self.dbfile)
        logger.Log('Retriving List of Games')
        global fullUpdate
        fullUpdate = True
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        infile = opener.open('http://thegamesdb.net/api/GetPlatformGames.php?platform=12')
        page = infile.read()
        opener.close()
        dom = parseString(page)
        games = dom.getElementsByTagName('Game')
        # dn = os.path.dirname(os.path.realpath(__file__))
        # fn = os.path.join(dn,"games.txt")
        # file = codecs.open(fn, "w", encoding='utf-8')
        dao = GamezServerDao.GamezServerDao()
        for game in games:
            gameId = game.getElementsByTagName('id')[0].firstChild.data
            try:
                gameTitle = game.getElementsByTagName('GameTitle')[0].firstChild.data
            except:
                break
            try:
                releaseDate = game.getElementsByTagName('ReleaseDate')[0].firstChild.data
            except:
                releaseDate = "No date given."
            infile = opener.open('http://thegamesdb.net/api/GetGame.php?id=' + str(gameId))
            page = infile.read()
            opener.close()
            dom2 = parseString(page)
            try:
                console = dom2.getElementsByTagName('Platform')[0].firstChild.data
            except:
                console = "Not provided"
            try:
                gameDescription = dom2.getElementsByTagName('Overview')[0].firstChild.data
            except:
                gameDescription = "No description given."
            try:
                boxarts = dom2.getElementsByTagName('boxart')
                for art in boxarts:
                    if art.attributes["side"].value == "front":
                        coverArt = 'http://thegamesdb.net/banners/' + art.firstChild.data
                    else:
                        coverArt = 'http://thegamesdb.net/images/common/placeholders/boxart_blank.png'
                        
            except:
                coverArt = 'http://thegamesdb.net/images/common/placeholders/boxart_blank.png'
            dao.AddGame(self.dbfile, gameId, gameTitle, gameDescription, releaseDate, coverArt, console)
            # file.write("%s::||::%s::||::%s::||::%s::||::%s::||::%s\n" % (id, name, description.replace('\n', ''), relDate, cover, console))
            # logger.Log("ID: %s, Name: %s, Cover: %s" % (gameId, gameTitle, coverArt))
        # file.close()
        global fullUpdate
        fullUpdate = False
        return

    def ReturnFullUpdate(self):
        return fullUpdate