from time import strftime, gmtime, strptime, mktime
from datetime import datetime
import cherrypy
import os
import ConfigParser
import GamezServer.GamezServerDao
import GamezServer.RiveuServer
import GamezServer.GamesDBReader
import GamezServer.PostProcessor
import GamezServer.Logger
import GamezServer.GameSearcher
import sys
from GamezServer import Constants
from cherrypy.process.plugins import Monitor
from GamezServer import GamezServerUpdater
import thread


class RunWebServer(object):
    def __init__(self):
        cherrypy.engine.subscribe('start', self.start)
        cherrypy.engine.subscribe('stop', self.stop)

    @cherrypy.expose
    def index(self, redirect=None, *args, **kwargs):
        updater = GamezServerUpdater.GamezServerUpdater(dbfile)
        gamesList = dao.GetGames(dbfile)
        content = ""
        content += "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\">"
        content += "<html>"
        content += "   <head>"
        content += "       <title>Gamez Server :: Home</title>"
        content += "       <link rel=\"shortcut icon\" href=\"/images/favicon.ico\" type=\"image/x-icon\">"
        content += "       <link rel=\"icon\" href=\"/images/favicon.ico\" type=\"image/x-icon\">"
        content += "       <link href=\"css/excite-bike/jquery-ui-1.10.3.custom.css\" type=\"text/css\" rel=\"stylesheet\">"
        content += "       <link href=\"css/styles.css\" type=\"text/css\" rel=\"stylesheet\">"
        content += "       <link href=\"css/demo_table_jui.css\" type=\"text/css\" rel=\"stylesheet\">"
        content += "       <script src=\"js/jquery-1.9.1.js\" type=\"text/javascript\"></script>"
        content += "       <script src=\"js/jquery-ui-1.10.3.custom.js\" type=\"text/javascript\"></script>"
        content += "       <script src=\"js/jquery.dataTables.js\" type=\"text/javascript\"></script>"
        content += "       <script src=\"js/jqueryshorten.js\" type=\"text/javascript\"></script>"
        content += "       <script type=\"text/javascript\">"
        content += "       $(document).ready(function() {"
        content += "       $(\".comment\").shorten();"
        content += "       });"
        content += "       </script>"
        content += "   </head>"
        content += "   <body style=\"background: url(/images/bgnoise_lg.png) repeat left top;width:100%\">"
        content += "   <form method=\"post\" action=\"https://www.paypal.com/cgi-bin/webscr\">"
        content += "       <div id=\"container\" style=\"width: 100%; margin: 0px auto 0;\">"
        content += "           <table width=\"100%\" style=\"padding:15px\">"
        content += "               <tr width=\"100%\"><td width=\"100%\"><table width=\"100%\"><tr width=\"100%\"><td width=\"80px\"><img src=\"images/logo.png\" alt=\"Riveu Logo\" /></td><td><div style=\"color:Orange;font-family: Lucida Handwriting;font-size: XX-Large\">Gamez Server</div></td><td><div style=\"float:right;\"><input type=\"hidden\" name=\"cmd\" value=\"_s-xclick\"><input type=\"hidden\" name=\"hosted_button_id\" value=\"SPK7EYG47DHZ4\"><input type=\"image\" src=\"https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif\" border=\"0\" name=\"submit\" alt=\"Donate\"><img alt=\"\" border=\"0\" src=\"https://www.paypalobjects.com/en_US/i/scr/pixel.gif\" width=\"1\" height=\"1\"></div></td></tr></table></td></tr>"
        content += "               <tr width=\"100%\"><td><div id='cssmenu'><ul>   <li class='active'><a href='/'><span>Home</span></a></li><li><a href='/addgame'><span>Add Game</span></a></li><li><a href='/bulkaddgame'><span>Bulk Add Game</span></a></li> <li><a href='/mastergames'><span>Master Game List</span></a></li>  <li><a href='/settings'><span>Settings</span></a></li><li class='last'><a href='/log'><span>Log</span></a></li><li class='last'><a href='http://www.riveu.com/support.aspx' target='_blank'><span>Support</span></a></li><div style=\"text-align:right;padding: 15px 20px;color: #ffffff;text-shadow: 0 -1px 1px #5c2800;font-size: 14px;font-family: Helvetica;\">Version: " + str(
            version) + "</div></ul></div></td></tr>"
        content += "               <tr>";
        content += "                   <td>"
        content += "                       <table id=\"logGrid\" width=\"100%\" class=\"display\"><thead><tr><th>Cover</th><th>Game Title</th><th>Game ID</th><th>Game Description</th><th>Console</th><th>Release Date</th><th>Status</th><th>Location</th><th>Commands</th></tr></thead><tbody>"
        for row in gamesList:
            gameId = row[8]
            statusValue = row[6]
            statusDropDown = "<select onchange=\"window.location = '/updatestatus?game_id=" + str(
                gameId) + "&filePath=&status=' + this.value;\"><option value=\"Downloaded\">Downloaded</option><option value=\"Snatched\">Snatched</option><option value=\"Wanted\" selected>Wanted</option></select>"
            if (statusValue == 'Snatched'):
                statusDropDown = "<select onchange=\"window.location = '/updatestatus?game_id=" + str(
                    gameId) + "&filePath=&status=' + this.value;\"><option value=\"Downloaded\">Downloaded</option><option value=\"Snatched\" selected>Snatched</option><option value=\"Wanted\">Wanted</option></select>"
            if (statusValue == 'Downloaded'):
                statusDropDown = "<select onchange=\"window.location = '/updatestatus?game_id=" + str(
                    gameId) + "&filePath=&status=' + this.value;\"><option value=\"Downloaded\" selected>Downloaded</option><option value=\"Snatched\">Snatched</option><option value=\"Wanted\">Wanted</option></select>"
            content += "                       <tr><td><image  onError=\"this.onerror=null;this.src='images/noCoverArt.gif';\" style=\"width:125px;height:200px\" src=\"" + \
                       row[0] + "\" alt=\"Cover Image\" /></td><td>" + row[1] + "</td><td>" + row[
                           2] + "</td><td><div class=\"comment\">" + row[3] + "</div></td><td>" + row[4] + "</td><td>" + \
                       row[5] + "</td><td>" + statusDropDown + "</td><td>" + str(
                row[7]) + "</td><td><a href=\"/deletegame?game_id=" + str(gameId) + "\">Delete</a></td></tr>"
            # except:
            #logger.Log("Unable to show game because there is unicode error in description: " + str(row[1]))
        content += "                       </tbody></table>"
        content += "                   </td>"
        content += "               </tr>"
        content += "           </table>"
        content += "       </div>"
        content += "       <script>$(function() {$('#logGrid').dataTable({\"bJQueryUI\": true, \"sPaginationType\": \"full_numbers\"});});</script>"
        content += "       <div id=\"statusmessage\" style=\"position:fixed;bottom:0;padding:0 5px;line-height:25px;background-color:#eeee99;margin-bottom:-25px;font-weight:bold;left:0;right:0;\"></div>"
        content += "       <div id=\"versionstatusmessage\" style=\"position:fixed;bottom:0;padding:0 5px;line-height:25px;background-color:#eeee99;margin-bottom:-25px;font-weight:bold;left:0;right:0;\"><label>A new version of GamezServer is available</label>&nbsp;&nbsp;&nbsp;<button onclick=\"window.location='/updategamezserver';return false;\">Upgrade Now</button></div>"
        if (updater.CheckForNewVersion()):
            content += "<script>$('#versionstatusmessage').animate({'margin-bottom':0},200);setTimeout( function(){$('#versionstatusmessage').animate({'margin-bottom':-25},200);}, 500*1000);</script>"
        if (redirect == 'gameadded'):
            content += "<script>$('#statusmessage').text('Game Added to Wanted List...').animate({'margin-bottom':0},200);setTimeout( function(){$('#statusmessage').animate({'margin-bottom':-25},200);}, 5*1000);</script>"
        if (redirect == 'gamedeleted'):
            content += "<script>$('#statusmessage').text('Game Deleted From Wanted List...').animate({'margin-bottom':0},200);setTimeout( function(){$('#statusmessage').animate({'margin-bottom':-25},200);}, 5*1000);</script>"
        if (redirect == 'statusupdated'):
            content += "<script>$('#statusmessage').text('Game Status Updated...').animate({'margin-bottom':0},200);setTimeout( function(){$('#statusmessage').animate({'margin-bottom':-25},200);}, 5*1000);</script>"
        if (str(redirect).find("Successfully Upgraded to Version") <> -1):
            content += "<script>$('#statusmessage').text('" + str(
                redirect) + "').animate({'margin-bottom':0},200);setTimeout( function(){$('#statusmessage').animate({'margin-bottom':-25},200);}, 5*1000);</script>"
        dbReader = GamezServer.GamesDBReader.GamesDBReader(dbfile)
        if (dbReader.ReturnFullUpdate()):
            content += "<script>$('#statusmessage').text('There is a Full Update occuring! You might notice slow responses or games missing...').animate({'margin-bottom':0},200);</script>"
        content += "   </form>"
        content += "   </body>"
        content += "</html>"
        return content

    @cherrypy.expose
    def updategamezserver(self, *args, **kwargs):
        updater = GamezServerUpdater.GamezServerUpdater(dbfile)
        updateResult = updater.Update(app_path)
        raise cherrypy.HTTPRedirect("/?redirect=" + updateResult)
        return

    @cherrypy.expose
    def mastergames(self, *args, **kwargs):
        gamesList = dao.GetMasterGames(dbfile)
        content = ""
        content += "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\">"
        content += "<html>"
        content += "   <head>"
        content += "       <title>Gamez Server :: Master Games</title>"
        content += "       <link rel=\"shortcut icon\" href=\"/images/favicon.ico\" type=\"image/x-icon\">"
        content += "       <link rel=\"icon\" href=\"/images/favicon.ico\" type=\"image/x-icon\">"
        content += "       <link href=\"css/excite-bike/jquery-ui-1.10.3.custom.css\" type=\"text/css\" rel=\"stylesheet\">"
        content += "       <link href=\"css/styles.css\" type=\"text/css\" rel=\"stylesheet\">"
        content += "       <link href=\"css/demo_table_jui.css\" type=\"text/css\" rel=\"stylesheet\">"
        content += "       <script src=\"js/jquery-1.9.1.js\" type=\"text/javascript\"></script>"
        content += "       <script src=\"js/jquery-ui-1.10.3.custom.js\" type=\"text/javascript\"></script>"
        content += "       <script src=\"js/jquery.dataTables.js\" type=\"text/javascript\"></script>"
        content += "   </head>"
        content += "   <body style=\"background: url(/images/bgnoise_lg.png) repeat left top;width:100%\">"
        content += "   <form action=\"/clearlog\" method=\"post\">"
        content += "       <div id=\"container\" style=\"width: 100%; margin: 0px auto 0;\">"
        content += "           <table width=\"100%\" style=\"padding:15px\">"
        content += "               <tr><td><table><tr><td><img src=\"images/logo.png\" alt=\"Riveu Logo\" /></td><td><div style=\"color:Orange;font-family: Lucida Handwriting;font-size: XX-Large\">Gamez Server</div></td></tr></table></td></tr>"
        content += "               <tr width=\"100%\"><td><div id='cssmenu'><ul>   <li class='active'><a href='/'><span>Home</span></a></li><li><a href='/addgame'><span>Add Game</span></a></li> <li><a href='/bulkaddgame'><span>Bulk Add Game</span></a></li><li><a href='/mastergames'><span>Master Game List</span></a></li>  <li><a href='/settings'><span>Settings</span></a></li><li class='last'><a href='/log'><span>Log</span></a></li><li class='last'><a href='http://www.riveu.com/support.aspx' target='_blank'><span>Support</span></a></li><div style=\"text-align:right;padding: 15px 20px;color: #ffffff;text-shadow: 0 -1px 1px #5c2800;font-size: 14px;font-family: Helvetica;\">Version: " + str(
            version) + "</div></ul></div></td></tr>"
        content += "               <tr>";
        content += "                   <td>"
        content += "                       <table id=\"gamesGrid\" width=\"100%\" class=\"display\"><thead><tr><th>Cover</th><th>Game Title</th><th>Game ID</th><th>Game Description</th><th>Release Date</th><th>Console</th></tr></thead><tbody>"
        for row in gamesList:
            try:
                dateValue = str(row[4])
                if (dateValue == '//'):
                    dateValue = 'Unkown'
                content += "                       <tr><td><img src=\"" + str(row[
                    5]) + "\" onError=\"this.onerror=null;this.src='images/noCoverArt.gif';\" style=\"width:125px;height:200px\" /></td><td>" + str(
                    row[1]) + "</td><td>" + str(row[0]) + "</td><td>" + str(
                    row[2]) + "</td><td>" + dateValue + "</td><td>" + str(row[3]) + "</td></tr>"
            except:
                logger.Log("Unable to show game because there is unicode error in description: " + str(row[1]))
        content += "                       </tbody></table>"
        content += "                   </td>"
        content += "               </tr>"
        content += "           </table>"
        content += "       </div>"
        content += "       <script>$(function() {$('#gamesGrid').dataTable({\"bJQueryUI\": true, \"sPaginationType\": \"full_numbers\"});});</script>"
        content += "   </form>"
        content += "   </body>"
        content += "</html>"
        return content

    @cherrypy.expose
    def addgame(self, *args, **kwargs):
        gamelist = dao.GetMasterGames(dbfile)
        consolelist = dao.GetConsoles(dbfile)
        content = ""
        content += "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\">"
        content += "<html>"
        content += "   <head>"
        content += "       <title>Gamez Server :: Add Game</title>"
        content += "       <link rel=\"shortcut icon\" href=\"/images/favicon.ico\" type=\"image/x-icon\">"
        content += "       <link rel=\"icon\" href=\"/images/favicon.ico\" type=\"image/x-icon\">"
        content += "       <link href=\"css/excite-bike/jquery-ui-1.10.3.custom.css\" type=\"text/css\" rel=\"stylesheet\">"
        content += "       <link href=\"css/styles.css\" type=\"text/css\" rel=\"stylesheet\">"
        content += "       <script src=\"js/jquery-1.9.1.js\" type=\"text/javascript\"></script>"
        content += "       <script src=\"js/jquery-ui-1.10.3.custom.js\" type=\"text/javascript\"></script>"
        content += "       <script src=\"js/modernizr-2.0.6.min.js\" type=\"text/javascript\"></script> "
        content += "       <script src=\"js/jquery.horizontalNav.js\" type=\"text/javascript\"></script> "
        content += "   </head>"
        content += "   <body style=\"background: url(/images/bgnoise_lg.png) repeat left top;width:100%\">"
        content += "   <form action=\"processAddGame\" method=\"post\" onsubmit=\"return CheckValidation();\">"
        content += "       <div id=\"container\" style=\"width: 100%; margin: 0px auto 0;\">"
        content += "           <table width=\"100%\" style=\"padding:15px\">"
        content += "               <tr><td><table><tr><td><img src=\"images/logo.png\" alt=\"Riveu Logo\" /></td><td><div style=\"color:Orange;font-family: Lucida Handwriting;font-size: XX-Large\">Gamez Server</div></td></tr></table></td></tr>"
        content += "               <tr width=\"100%\"><td><div id='cssmenu'><ul>   <li class='active'><a href='/'><span>Home</span></a></li><li><a href='/addgame'><span>Add Game</span></a></li><li><a href='/bulkaddgame'><span>Bulk Add Game</span></a></li> <li><a href='/mastergames'><span>Master Game List</span></a></li>  <li><a href='/settings'><span>Settings</span></a></li><li class='last'><a href='/log'><span>Log</span></a></li><li class='last'><a href='http://www.riveu.com/support.aspx' target='_blank'><span>Support</span></a></li><div style=\"text-align:right;padding: 15px 20px;color: #ffffff;text-shadow: 0 -1px 1px #5c2800;font-size: 14px;font-family: Helvetica;\">Version: " + str(
            version) + "</div></ul></div></td></tr>"
        content += "               <tr>";
        content += "                   <td>"
        content += "                       <div id=\"addgame-tabs\"><ul><li><a href=\"#addgame-tab\">Add Game</a></li><li><a href=\"#bulkaddgame-tab\">Bulk Add</a></li></ul>"
        content += "                           <div id=\"addgame-tab\">"
        content += "                               <div>"
        content += "                                   <fieldset class=\"ui-widget ui-widget-content\">"
        content += "                                       <legend class=\"ui-widget-header ui-corner-all\">"
        content += "                                           <div>Game Information</div>"
        content += "                                       </legend>"
        content += "                                       <div class=\"ui-widget\"><table style=\"width:100%\"><tr style=\"width:100%\"><td style=\"width:100px\"><label for=\"game\">Game: </label></td><td style=\"width:95%\"><input name=\"game\" id=\"game\" style=\"width:60%;margin-left:20px\"></td></tr>"
        content += "                                       <tr><td style=\"width:100%;text-align:right;padding:15px\" colspan=\"2\"><button id=\"saveSettingsButton\" type=\"submit\">Add Game</button></td></tr></table></div>"
        content += "                                   </fieldset>"
        content += "                               </div>"
        content += "                           </div>"
        content += "                           <div id=\"bulkaddgame-tab\">"
        content += "                               <div>"
        content += "                                   <fieldset class=\"ui-widget ui-widget-content\">"
        content += "                                       <legend class=\"ui-widget-header ui-corner-all\">"
        content += "                                           <div>Add By Console</div>"
        content += "                                       </legend>"
        content += "                                       <div class=\"ui-widget\"><table style=\"width:100%\"><tr style=\"width:100%\"><td style=\"width:100px\"><label for=\"consoleselect\">Console: </label></td><td style=\"width:95%\"><select name=\"consoleselect\" style=\"width:60%;margin-left:20px\">"
        for row in consolelist:
            content += "<option value=\"" + str(row[0]) + "\">" + str(row[0]) + "</option>"
        content += "                                       </select></td></tr>"
        content += "                                       <tr><td style=\"width:100%;text-align:right;padding:15px\" colspan=\"2\"><button id=\"addGamesButton\" type=\"submit\">Add Games</button></td></tr></table></div>"
        content += "                                   </fieldset>"
        content += "                               </div>"
        content += "                           </div>"
        content += "                       </div>"
        content += "                   </td>"
        content += "               </tr>"
        content += "           </table>"
        content += "       </div>"
        content += "<script>"
        content += "var availableGames = ["
        for row in gamelist:
            content += '"' + row[1].replace("\r", "") + " - " + row[3] + '",'
        content += "];"

        content += "function CheckValidation(){var gameVal = availableGames.indexOf(document.getElementById('game').value);if(gameVal == -1){alert('Please Enter A Valid Game');return false;}else{return true;}}</script>"
        content += "       <script>$(function() {"
        content += "       $( \"#addgame-tabs\" ).tabs();$(\"#saveSettingsButton\").button();$(\"#game\").autocomplete({source: availableGames});});</script>"
        content += "   </form>"
        content += "   </body>"
        content += "</html>"
        return content

    @cherrypy.expose
    def bulkaddgame(self, *args, **kwargs):
        consolelist = dao.GetConsoles(dbfile)
        content = ""
        content += "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\">"
        content += "<html>"
        content += "   <head>"
        content += "       <title>Gamez Server :: Bulk Add</title>"
        content += "       <link rel=\"shortcut icon\" href=\"/images/favicon.ico\" type=\"image/x-icon\">"
        content += "       <link rel=\"icon\" href=\"/images/favicon.ico\" type=\"image/x-icon\">"
        content += "       <link href=\"css/excite-bike/jquery-ui-1.10.3.custom.css\" type=\"text/css\" rel=\"stylesheet\">"
        content += "       <link href=\"css/styles.css\" type=\"text/css\" rel=\"stylesheet\">"
        content += "       <script src=\"js/jquery-1.9.1.js\" type=\"text/javascript\"></script>"
        content += "       <script src=\"js/jquery-ui-1.10.3.custom.js\" type=\"text/javascript\"></script>"
        content += "       <script src=\"js/modernizr-2.0.6.min.js\" type=\"text/javascript\"></script> "
        content += "       <script src=\"js/jquery.horizontalNav.js\" type=\"text/javascript\"></script> "
        content += "   </head>"
        content += "   <body style=\"background: url(/images/bgnoise_lg.png) repeat left top;width:100%\">"
        content += "   <form action=\"processBulkAddGame\" method=\"post\" onsubmit=\"return CheckValidation();\">"
        content += "       <div id=\"container\" style=\"width: 100%; margin: 0px auto 0;\">"
        content += "           <table width=\"100%\" style=\"padding:15px\">"
        content += "               <tr><td><table><tr><td><img src=\"images/logo.png\" alt=\"Riveu Logo\" /></td><td><div style=\"color:Orange;font-family: Lucida Handwriting;font-size: XX-Large\">Gamez Server</div></td></tr></table></td></tr>"
        content += "               <tr width=\"100%\"><td><div id='cssmenu'><ul>   <li class='active'><a href='/'><span>Home</span></a></li><li><a href='/addgame'><span>Add Game</span></a></li><li><a href='/bulkaddgame'><span>Bulk Add Game</span></a></li> <li><a href='/mastergames'><span>Master Game List</span></a></li>  <li><a href='/settings'><span>Settings</span></a></li><li class='last'><a href='/log'><span>Log</span></a></li><li class='last'><a href='http://www.riveu.com/support.aspx' target='_blank'><span>Support</span></a></li><div style=\"text-align:right;padding: 15px 20px;color: #ffffff;text-shadow: 0 -1px 1px #5c2800;font-size: 14px;font-family: Helvetica;\">Version: " + str(
            version) + "</div></ul></div></td></tr>"
        content += "               <tr>";
        content += "                   <td>"
        content += "                       <div id=\"addgame-tabs\"><ul><li><a href=\"#bulkaddgame-tab\">Bulk Add</a></li></ul>"
        content += "                           <div id=\"bulkaddgame-tab\">"
        content += "                               <div>"
        content += "                                   <fieldset class=\"ui-widget ui-widget-content\">"
        content += "                                       <legend class=\"ui-widget-header ui-corner-all\">"
        content += "                                           <div>Add By Console</div>"
        content += "                                       </legend>"
        content += "                                       <div class=\"ui-widget\"><table style=\"width:100%\"><tr style=\"width:100%\"><td style=\"width:100px\"><label for=\"consoleselect\">Console: </label></td><td style=\"width:95%\"><select name=\"consoleselect\" style=\"width:60%;margin-left:20px\">"
        for row in consolelist:
            content += "<option value=\"" + str(row[0]) + "\">" + str(row[0]) + "</option>"
        content += "                                       </select></td></tr>"
        content += "                                       <tr><td style=\"width:100%;text-align:right;padding:15px\" colspan=\"2\"><button id=\"addGamesButton\" type=\"submit\">Add Games</button></td></tr></table></div>"
        content += "                                   </fieldset>"
        content += "                               </div>"
        content += "                           </div>"
        content += "                       </div>"
        content += "                   </td>"
        content += "               </tr>"
        content += "           </table>"
        content += "       </div>"
        content += "       <script>$(function() {"
        content += "       $( \"#addgame-tabs\" ).tabs();$(\"#addGamesButton\").button();});</script>"
        content += "   </form>"
        content += "   </body>"
        content += "</html>"
        return content

    @cherrypy.expose
    def processAddGame(self, game=None, **kwargs):
        consolelist = dao.GetConsoles(dbfile)
        gameArray = game.split(" - ")
        game = gameArray[0]
        console = gameArray[1]
        # console = dao.GetConsoleByGame(dbfile, game)
        logger.Log("Game: " + game + " Console: " + console)
        if (console <> ""):
            dao.AddWantedGame(dbfile, console, game)
            thread.start_new_thread(RunGameSearch, ())
        raise cherrypy.HTTPRedirect("/?redirect=gameadded")

    @cherrypy.expose
    def processBulkAddGame(self, consoleselect=None, *args, **kwargs):
        print(consoleselect)
        dao.BulkAddByConsole(dbfile, str(consoleselect))
        raise cherrypy.HTTPRedirect("/?redirect=gameadded")

    def stop(self):
        logger.Log("Shutting Down Web Server")

    def start(self):
        logger.Log("Web Server Started")

    @cherrypy.expose
    def log(self, redirect=None, *args, **kwargs):
        logResult = dao.GetLogMessages(dbfile)
        content = ""
        content += "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\">"
        content += "<html>"
        content += "   <head>"
        content += "       <title>Gamez Server :: Log</title>"
        content += "       <link rel=\"shortcut icon\" href=\"/images/favicon.ico\" type=\"image/x-icon\">"
        content += "       <link rel=\"icon\" href=\"/images/favicon.ico\" type=\"image/x-icon\">"
        content += "       <link href=\"css/excite-bike/jquery-ui-1.10.3.custom.css\" type=\"text/css\" rel=\"stylesheet\">"
        content += "       <link href=\"css/styles.css\" type=\"text/css\" rel=\"stylesheet\">"
        content += "       <link href=\"css/demo_table_jui.css\" type=\"text/css\" rel=\"stylesheet\">"
        content += "       <script src=\"js/jquery-1.9.1.js\" type=\"text/javascript\"></script>"
        content += "       <script src=\"js/jquery-ui-1.10.3.custom.js\" type=\"text/javascript\"></script>"
        content += "       <script src=\"js/jquery.dataTables.js\" type=\"text/javascript\"></script>"
        content += "   </head>"
        content += "   <body style=\"background: url(/images/bgnoise_lg.png) repeat left top;width:100%\">"
        content += "   <form action=\"/clearlog\" method=\"post\">"
        content += "       <div id=\"container\" style=\"width: 100%; margin: 0px auto 0;\">"
        content += "           <table width=\"100%\" style=\"padding:15px\">"
        content += "               <tr><td><table><tr><td><img src=\"images/logo.png\" alt=\"Riveu Logo\" /></td><td><div style=\"color:Orange;font-family: Lucida Handwriting;font-size: XX-Large\">Gamez Server</div></td></tr></table></td></tr>"
        content += "               <tr width=\"100%\"><td><div id='cssmenu'><ul>   <li class='active'><a href='/'><span>Home</span></a></li><li><a href='/addgame'><span>Add Game</span></a></li><li><a href='/bulkaddgame'><span>Bulk Add Game</span></a></li> <li><a href='/mastergames'><span>Master Game List</span></a></li>  <li><a href='/settings'><span>Settings</span></a></li><li class='last'><a href='/log'><span>Log</span></a></li><li class='last'><a href='http://www.riveu.com/support.aspx' target='_blank'><span>Support</span></a></li><div style=\"text-align:right;padding: 15px 20px;color: #ffffff;text-shadow: 0 -1px 1px #5c2800;font-size: 14px;font-family: Helvetica;\">Version: " + str(
            version) + "</div></ul></div></td></tr>"
        content += "               <tr>";
        content += "                   <td>"
        content += "                       <table id=\"logGrid\" width=\"100%\" class=\"display\"><thead><tr><th>Date/Time</th><th>Message</th></tr></thead><tbody>"
        for row in logResult:
            content += "                       <tr><td width=\"250px\">" + str(row[1]) + "</td><td>" + str(
                row[0]) + "</td></tr>"
        content += "                       </tbody></table>"
        content += "                   </td>"
        content += "               </tr>"
        content += "               <tr>"
        content += "                   </td>"
        content += "                   <td colspan=\"2\" style=\"text-align:right;padding:15px\">"
        content += "                       <button id=\"clearLogButton\" type=\"submit\">Clear Log</button>"
        content += "                   </td>"
        content += "               </tr>"
        content += "           </table>"
        content += "       </div>"
        content += "       <script>$(function() {$(\"#clearLogButton\").button();$('#logGrid').dataTable({\"bJQueryUI\": true, \"sPaginationType\": \"full_numbers\"});});</script>"
        content += "       <div id=\"statusmessage\" style=\"position:fixed;bottom:0;padding:0 5px;line-height:25px;background-color:#eeee99;margin-bottom:-25px;font-weight:bold;left:0;right:0;\"></div>"
        if (redirect == 'logcleared'):
            content += "<script>$('#statusmessage').text('Log Cleared..').animate({'margin-bottom':0},200);setTimeout( function(){$('#statusmessage').animate({'margin-bottom':-25},200);}, 5*1000);</script>"
        content += "   </form>"
        content += "   </body>"
        content += "</html>"
        return content

    @cherrypy.expose
    def settings(self, redirect=None, *args, **kwargs):
        config = ConfigParser.RawConfigParser()
        config.read(conffile)
        enableAuthChecked = ""
        enableUsenetCrawlerChecked = ""
        enableSabnzbdChecked = ""
        enableWiiPostProcessingChecked = ""
        enablePS3PostProcessingChecked = ""
        enableXBOX360PostProcessingChecked = ""
        enableNDSPostProcessingChecked = ""

        if (config.get('GamezServer', 'EnableAuth') == "1"):
            enableAuthChecked = "checked"
        if (config.get('UsenetCrawler', 'EnableUsenetCrawler') == "1"):
            enableUsenetCrawlerChecked = "checked"
        if (config.get('Sabnzbd', 'EnableSabnzbd') == "1"):
            enableSabnzbdChecked = "checked"
        if (config.get('PostProcessing', 'EnableWiiPostProcessing') == "1"):
            enableWiiPostProcessingChecked = "checked"
        if (config.get('PostProcessing', 'EnablePS3PostProcessing') == "1"):
            enablePS3PostProcessingChecked = "checked"
        if (config.get('PostProcessing', 'EnableXBOX360PostProcessing') == "1"):
            enableXBOX360PostProcessingChecked = "checked"
        if (config.get('PostProcessing', 'EnableNDSPostProcessing') == "1"):
            enableNDSPostProcessingChecked = "checked"

        content = ""
        content += "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\">"
        content += "<html>"
        content += "   <head>"
        content += "       <title>Gamez Server :: Settings</title>"
        content += "       <link rel=\"shortcut icon\" href=\"/images/favicon.ico\" type=\"image/x-icon\">"
        content += "       <link rel=\"icon\" href=\"/images/favicon.ico\" type=\"image/x-icon\">"
        content += "       <link href=\"css/excite-bike/jquery-ui-1.10.3.custom.css\" type=\"text/css\" rel=\"stylesheet\">"
        content += "       <link href=\"css/styles.css\" type=\"text/css\" rel=\"stylesheet\">"
        content += "       <script src=\"js/jquery-1.9.1.js\" type=\"text/javascript\"></script>"
        content += "       <script src=\"js/jquery-ui-1.10.3.custom.js\" type=\"text/javascript\"></script>"
        content += "       <script src=\"js/modernizr-2.0.6.min.js\" type=\"text/javascript\"></script> "
        content += "       <script src=\"js/jquery.horizontalNav.js\" type=\"text/javascript\"></script> "
        content += "   </head>"
        content += "   <body style=\"background: url(/images/bgnoise_lg.png) repeat left top;width:100%\">"
        content += "   <form action=\"saveSettings\" method=\"post\">"
        content += "       <div id=\"container\" style=\"width: 100%; margin: 0px auto 0;\">"
        content += "           <table width=\"100%\" style=\"padding:15px\">"
        content += "               <tr><td><table><tr><td><img src=\"images/logo.png\" alt=\"Riveu Logo\" /></td><td><div style=\"color:Orange;font-family: Lucida Handwriting;font-size: XX-Large\">Gamez Server</div></td></tr></table></td></tr>"+ version + "</div></ul></div></td></tr>"
        content += "               <tr>";
        content += "                   <td>"
        content += "                       <div id=\"settings-tabs\"><ul><li><a href=\"#general-tab\">General</a></li><li><a href=\"#downloaders-tab\">Downloaders</a></li><li><a href=\"#searchers-tab\">Search Providers</a></li><li><a href=\"#updateoptions-tab\">Database Update Options</a></li><li><a href=\"#postprocessing-tab\">Post Processing</a></li></ul>"
        content += "                           <div id=\"general-tab\">"
        content += "                               <h4>General Settings</h4>"
        content += "                               <div>"
        content += "                                   <fieldset class=\"ui-widget ui-widget-content\">"
        content += "                                       <legend class=\"ui-widget-header ui-corner-all\">"
        content += "                                           <div>Gamez Web Server</div>"
        content += "                                       </legend>"
        content += "                                       <table style=\"width:100%\">"
        content += "                                           <tr style=\"width:100%\"><td style=\"width:1o%\"><label>Host:</label></td><td style=\"width:90%\"><input name=\"host\" value=\"" + config.get(
            'global', 'server.socket_host').replace("'", "") + "\" type=\"text\" style=\"width:75%\"></td></tr>"
        content += "                                           <tr><td><div class=\"field\"><label>Port:</label></td><td><input name=\"port\" value=\"" + config.get(
            'global', 'server.socket_port') + "\" type=\"text\" style=\"width:75%\"></div></td></tr>"
        content += "                                           <tr><td><div class=\"field\"><label>Enable Authentication:</label></td><td><input name=\"enableAuth\" " + enableAuthChecked + " type=\"checkbox\"></div></td></tr>"
        content += "                                           <tr><td><div class=\"field\"><label>Username:</label></td><td><input name=\"authUsername\" value=\"" + config.get(
            'GamezServer', 'AuthUsername').replace("'", "") + "\" type=\"text\" style=\"width:75%\"></div></td></tr>"
        content += "                                           <tr><td><div class=\"field\"><label>Password:</label></td><td><input name=\"authPassword\" value=\"" + config.get(
            'GamezServer', 'AuthPassword').replace("'",
                                                   "") + "\" type=\"password\" style=\"width:75%\"></div></td></tr>"
        content += "                                       </table>"
        content += "                                   </fieldset>"
        content += "                               </div>"
        content += "                           </div>"
        content += "                           <div id=\"downloaders-tab\">"
        content += "                               <h4>Downloaders</h4>"
        content += "                               <div>"
        content += "                                   <fieldset class=\"ui-widget ui-widget-content\">"
        content += "                                       <legend class=\"ui-widget-header ui-corner-all\">"
        content += "                                           <div>Sabnzbd+</div>"
        content += "                                       </legend>"
        content += "                                       <table style=\"width:100%\">"
        content += "                                           <tr><td><div class=\"field\" style=\"width:10%\"><label>Enable</label></td><td style=\"width:90%\"><input name=\"enableSabnzbd\" " + enableSabnzbdChecked + " type=\"checkbox\"></div></td></tr>"
        content += "                                           <tr><td><div class=\"field\"><label>Sabnzbd+ URL:</label></td><td><input name=\"sabnzbdUrl\" value=\"" + config.get(
            'Sabnzbd', 'SabnzbdHostUrl').replace("'", "") + "\" type=\"text\" style=\"width:75%\"></div></td></tr>"
        content += "                                           <tr><td><div class=\"field\"><label>API Key:</label></td><td><input name=\"sabnzbdApiKey\" value=\"" + config.get(
            'Sabnzbd', 'SabnzbdApiKey').replace("'", "") + "\" type=\"text\" style=\"width:75%\"></div></td></tr>"
        content += "                                           <tr><td><div class=\"field\"><label>Category</label></td><td><input name=\"sabnzbdCategory\" value=\"" + config.get(
            'Sabnzbd', 'SabnzbdCategory').replace("'", "") + "\" type=\"text\" style=\"width:75%\"></div></td></tr>"
        content += "                                       </table>"
        content += "                                   </fieldset>"
        content += "                               </div>"
        content += "                           </div>"
        content += "                           <div id=\"searchers-tab\">"
        content += "                               <h4>Search Providers</h4>"
        content += "                               <div>"
        content += "                                   <fieldset class=\"ui-widget ui-widget-content\">"
        content += "                                       <legend class=\"ui-widget-header ui-corner-all\">"
        content += "                                           <div>Usenet-Crawler</div>"
        content += "                                       </legend>"
        content += "                                       <table style=\"width:100%\">"
        content += "                                           <tr><td><div class=\"field\" style=\"width:10%\"><label>Enable</label></td><td style=\"width:90%\"><input name=\"enableUsenetCrawler\" " + enableUsenetCrawlerChecked + " type=\"checkbox\"></div></td></tr>"
        content += "                                           <tr><td><div class=\"field\"><label>API Key:</label></td><td><input name=\"usenetCrawlerApi\" value=\"" + config.get(
            'UsenetCrawler', 'UsenetCrawlerApiKey').replace("'",
                                                            "") + "\" type=\"text\" style=\"width:75%\"></div></td></tr>"
        content += "                                       </table>"
        content += "                                   </fieldset>"
        content += "                               </div>"
        content += "                           </div>"
        content += "                           <div id=\"updateoptions-tab\">"
        content += "                               <h4>Database Update Options</h4>"
        content += "                               <div>"
        content += "                                   <fieldset class=\"ui-widget ui-widget-content\">"
        content += "                                       <legend class=\"ui-widget-header ui-corner-all\">"
        content += "                                           <div>Database Update Options</div>"
        content += "                                       </legend>"
        content += "                                       <table style=\"width:100%\">"
        content += "                                           <tr><td><div class=\"field\"><label>Time between full database updates (in hours)</label></td><td><input name=\"dbSearchTime\" value=\"" + config.get(
            'Games Database Update', 'Time between full database updates (in hours)').replace("'", "") + "\" type=\"text\" style=\"width:75%\"></div></td></tr>"
        content += "                                       </table>"
        content += "                                   </fieldset>"
        content += "                               </div>"
        content += "                           </div>"
        content += "                           <div id=\"postprocessing-tab\">"
        content += "                               <h4>Post Processing</h4>"
        content += "                               <div>"
        content += "                                   <fieldset class=\"ui-widget ui-widget-content\">"
        content += "                                       <legend class=\"ui-widget-header ui-corner-all\">"
        content += "                                           <div>Microsoft XBOX 360</div>"
        content += "                                       </legend>"
        content += "                                       <table style=\"width:100%\">"
        content += "                                           <tr><td><div class=\"field\" style=\"width:10%\"><label>Enable</label></td><td style=\"width:90%\"><input name=\"enableXBOX360PostProcessing\" " + enableXBOX360PostProcessingChecked + " type=\"checkbox\"></div></td></tr>"
        content += "                                           <tr><td><div class=\"field\"><label>Destination Path:</label></td><td><input name=\"xbox360DestinationPath\" value=\"" + config.get(
            'PostProcessing', 'XBOX360DestinationPath').replace("'", "").replace('\\\\',
                                                                                 '\\') + "\" type=\"text\" style=\"width:75%\"></div></td></tr>"
        content += "                                       </table>"
        content += "                                   </fieldset>"
        content += "                               </div>"
        content += "                               <br />"
        content += "                               <div>"
        content += "                                   <fieldset class=\"ui-widget ui-widget-content\">"
        content += "                                       <legend class=\"ui-widget-header ui-corner-all\">"
        content += "                                           <div>Nintendo DS</div>"
        content += "                                       </legend>"
        content += "                                       <table style=\"width:100%\">"
        content += "                                           <tr><td><div class=\"field\" style=\"width:10%\"><label>Enable</label></td><td style=\"width:90%\"><input name=\"enableNDSPostProcessing\" " + enableNDSPostProcessingChecked + " type=\"checkbox\"></div></td></tr>"
        content += "                                           <tr><td><div class=\"field\"><label>Destination Path:</label></td><td><input name=\"ndsDestinationPath\" value=\"" + config.get(
            'PostProcessing', 'NDSDestinationPath').replace("'", "").replace('\\\\',
                                                                             '\\') + "\" type=\"text\" style=\"width:75%\"></div></td></tr>"
        content += "                                       </table>"
        content += "                                   </fieldset>"
        content += "                               </div>"
        content += "                               <br />"
        content += "                               <div>"
        content += "                                   <fieldset class=\"ui-widget ui-widget-content\">"
        content += "                                       <legend class=\"ui-widget-header ui-corner-all\">"
        content += "                                           <div>Nintendo Wii</div>"
        content += "                                       </legend>"
        content += "                                       <table style=\"width:100%\">"
        content += "                                           <tr><td><div class=\"field\" style=\"width:10%\"><label>Enable</label></td><td style=\"width:90%\"><input name=\"enableWiiPostProcessing\" " + enableWiiPostProcessingChecked + " type=\"checkbox\"></div></td></tr>"
        content += "                                           <tr><td><div class=\"field\"><label>Destination Path:</label></td><td><input name=\"wiiDestinationPath\" value=\"" + config.get(
            'PostProcessing', 'WiiDestinationPath').replace("'", "").replace('\\\\',
                                                                             '\\') + "\" type=\"text\" style=\"width:75%\"></div></td></tr>"
        content += "                                       </table>"
        content += "                                   </fieldset>"
        content += "                               </div>"
        content += "                               <br />"
        content += "                               <div>"
        content += "                                   <fieldset class=\"ui-widget ui-widget-content\">"
        content += "                                       <legend class=\"ui-widget-header ui-corner-all\">"
        content += "                                           <div>Sony Playstation 3</div>"
        content += "                                       </legend>"
        content += "                                       <table style=\"width:100%\">"
        content += "                                           <tr><td><div class=\"field\" style=\"width:10%\"><label>Enable</label></td><td style=\"width:90%\"><input name=\"enablePS3PostProcessing\" " + enablePS3PostProcessingChecked + " type=\"checkbox\"></div></td></tr>"
        content += "                                           <tr><td><div class=\"field\"><label>Destination Path:</label></td><td><input name=\"ps3DestinationPath\" value=\"" + config.get(
            'PostProcessing', 'PS3DestinationPath').replace("'", "").replace('\\\\',
                                                                             '\\') + "\" type=\"text\" style=\"width:75%\"></div></td></tr>"
        content += "                                       </table>"
        content += "                                   </fieldset>"
        content += "                               </div>"
        content += "                           </div>"
        content += "                       </div>"
        content += ""
        content += "                   </td>"
        content += "               </tr>"
        content += "               <tr>"
        content += "                   </td>"
        content += "                   <td colspan=\"2\" style=\"text-align:right;padding:15px\">"
        content += "                       <button id=\"saveSettingsButton\" type=\"submit\">Save Settings</button>"
        content += "                   </td>"
        content += "               </tr>"
        content += "           </table>"
        content += "       </div>"
        content += "       <script>$(function() {$( \"#settings-tabs\" ).tabs();$(\"#saveSettingsButton\").button();});</script>"
        content += "       <div id=\"statusmessage\" style=\"position:fixed;bottom:0;padding:0 5px;line-height:25px;background-color:#eeee99;margin-bottom:-25px;font-weight:bold;left:0;right:0;\"></div>"
        if (redirect == 'settingssaved'):
            content += "<script>$('#statusmessage').text('Settings Saved..').animate({'margin-bottom':0},200);setTimeout( function(){$('#statusmessage').animate({'margin-bottom':-25},200);}, 5*1000);</script>"
        content += "   </form>"
        content += "   </body>"
        content += "</html>"
        return content

    @cherrypy.expose
    def saveSettings(self, host=None, port=None, enableAuth=None, authUsername=None, authPassword=None,
                     enableUsenetCrawler=None, usenetCrawlerApi=None, enableSabnzbd=None, sabnzbdUrl=None,
                     sabnzbdApiKey=None, sabnzbdCategory=None, dbSearchTime=None, enableWiiPostProcessing=None,
                     wiiDestinationPath=None, enablePS3PostProcessing=None, ps3DestinationPath=None,
                     enableXBOX360PostProcessing=None, xbox360DestinationPath=None, enableNDSPostProcessing=None,
                     ndsDestinationPath=None):
        if (enableAuth == 'on'):
            enableAuth = '1'
        else:
            enableAuth = '0'

        if (enableUsenetCrawler == 'on'):
            enableUsenetCrawler = '1'
        else:
            enableUsenetCrawler = '0'

        if (enableSabnzbd == 'on'):
            enableSabnzbd = '1'
        else:
            enableSabnzbd = '0'

        if (enableWiiPostProcessing == 'on'):
            enableWiiPostProcessing = '1'
        else:
            enableWiiPostProcessing = '0'

        if (enablePS3PostProcessing == 'on'):
            enablePS3PostProcessing = '1'
        else:
            enablePS3PostProcessing = '0'

        if (enableXBOX360PostProcessing == 'on'):
            enableXBOX360PostProcessing = '1'
        else:
            enableXBOX360PostProcessing = '0'

        if (enableNDSPostProcessing == 'on'):
            enableNDSPostProcessing = '1'
        else:
            enableNDSPostProcessing = '0'

        config = ConfigParser.RawConfigParser()
        config.add_section('global')
        config.set('global', 'server.socket_host', "'" + host + "'")
        config.set('global', 'server.socket_port', port)
        config.add_section('GamezServer')
        config.set('GamezServer', 'EnableAuth', enableAuth)
        config.set('GamezServer', 'AuthUsername', "'" + authUsername + "'")
        config.set('GamezServer', 'AuthPassword', "'" + authPassword + "'")
        config.add_section('UsenetCrawler')
        config.set('UsenetCrawler', 'EnableUsenetCrawler', enableUsenetCrawler)
        config.set('UsenetCrawler', 'UsenetCrawlerApiKey', "'" + usenetCrawlerApi + "'")
        config.add_section('Sabnzbd')
        config.set('Sabnzbd', 'EnableSabnzbd', enableSabnzbd)
        config.set('Sabnzbd', 'SabnzbdHostUrl', "'" + sabnzbdUrl + "'")
        config.set('Sabnzbd', 'SabnzbdApiKey', "'" + sabnzbdApiKey + "'")
        config.set('Sabnzbd', 'SabnzbdCategory', "'" + sabnzbdCategory + "'")
        config.add_section('Games Database Update')
        config.set('Games Database Update', 'Time between full database updates (in hours)', dbSearchTime)
        config.add_section('PostProcessing')
        config.set('PostProcessing', 'EnableWiiPostProcessing', enableWiiPostProcessing)
        config.set('PostProcessing', 'WiiDestinationPath', "'" + str(wiiDestinationPath).replace('\\', '\\\\') + "'")
        config.set('PostProcessing', 'EnablePS3PostProcessing', enablePS3PostProcessing)
        config.set('PostProcessing', 'PS3DestinationPath', "'" + str(ps3DestinationPath).replace('\\', '\\\\') + "'")
        config.set('PostProcessing', 'EnableXBOX360PostProcessing', enableXBOX360PostProcessing)
        config.set('PostProcessing', 'XBOX360DestinationPath',
                   "'" + str(xbox360DestinationPath).replace('\\', '\\\\') + "'")
        config.set('PostProcessing', 'EnableNDSPostProcessing', enableNDSPostProcessing)
        config.set('PostProcessing', 'NDSDestinationPath', "'" + str(ndsDestinationPath).replace('\\', '\\\\') + "'")
        with open(conffile, 'wb') as configfile:
            config.write(configfile)
        raise cherrypy.HTTPRedirect("/settings?redirect=settingssaved")

    @cherrypy.expose
    def clearlog(self, logGrid_length):
        logger.ClearLog()
        raise cherrypy.HTTPRedirect("/log?redirect=logcleared")

    @cherrypy.expose
    def deletegame(self, game_id, *args, **kwargs):
        dao.DeleteGame(dbfile, game_id)
        raise cherrypy.InternalRedirect('/?redirect=gamedeleted')

    @cherrypy.expose
    def updatestatus(self, game_id='', status='', filePath='', *args, **kwargs):
        logger.Log('Updating Game Status')
        dao.UpdateGameStatus(dbfile, game_id, status)
        if (status == 'Downloaded'):
            postProcessor = GamezServer.PostProcessor.PostProcessor(conffile, game_id, dbfile)
            if (filePath <> ''):
                logger.Log('Calling Post Processing')
                postProcessResult = postProcessor.start(filePath)
                logger.Log('Post Processing Complete')
                if (postProcessResult <> ''):
                    filePath = postProcessResult
                else:
                    filePath = ''
                    logger.Log('Updating game status to wanted since there were no valid game files')
                    raise cherrypy.InternalRedirect('/updatestatus?game_id=' + game_id + '&status=Wanted&filePath=')
        if (status == 'Wanted'):
            dao.UpdateGameLocation(dbfile, game_id, '')
            RunGameSearch()
        if (filePath <> ''):
            dao.UpdateGameLocation(dbfile, game_id, filePath)
        raise cherrypy.InternalRedirect('/?redirect=statusupdated')


def RunGameSearch():
    logger.Log('Running Game Search')
    searcher = GamezServer.GameSearcher.GameSearcher(dbfile, conffile)
    searcher.start()
    return


def RunGameDBUpdater():
    dbReader = GamezServer.GamesDBReader.GamesDBReader(dbfile)
    currentTime = datetime.fromtimestamp(mktime(strptime(strftime("%Y-%m-%d %H:%M:%S", gmtime()), "%Y-%m-%d %H:%M:%S")))
    lastUpdate = datetime.fromtimestamp(mktime(strptime(dao.GetLastUpdateTime(dbfile), "%Y-%m-%d %H:%M:%S")))
    tdelta = currentTime - lastUpdate
    secondDifference = tdelta.total_seconds()
    logger.Log('Time since last update (in seconds): ' + str(secondDifference))
    config = ConfigParser.RawConfigParser()
    config.read(conffile)
    fullUpdateTime = float(config.get('Games Database Update', 'Time between full database updates (in hours)')) * 60 * 60
    if secondDifference >= fullUpdateTime:
        logger.Log('Running full update.')
        logger.Log('Updating Console List')
        dbReader.RetrievePlatformList()
        logger.Log('Updating Games List')
        dbReader.RetrieveGameList()
    else:
        logger.Log('Not long enough to run a full update, running incremental update.')
        # riveuServer.UpdateGames()


def GenerateSabPostProcessScript():
    config = ConfigParser.RawConfigParser()
    config.read(conffile)
    gamezWebHost = config.get('global', 'server.socket_host').replace("'", "")
    gamezWebport = config.get('global', 'server.socket_port').replace("'", "")
    gamezBaseUrl = "http://" + gamezWebHost + ":" + gamezWebport + "/"
    postProcessPath = os.path.join(app_path, 'GamezServer')
    postProcessPath = os.path.join(postProcessPath, 'postprocess')
    postProcessScript = os.path.join(postProcessPath, 'gamezPostProcess.py')
    file = open(postProcessScript, 'w')
    file.write('#!/usr/bin/env python')
    file.write("\n")
    file.write('import sys')
    file.write("\n")
    file.write('import urllib')
    file.write("\n")
    file.write("filePath = str(sys.argv[1])")
    file.write("\n")
    file.write('fields = str(sys.argv[3]).split("-")')
    file.write("\n")
    file.write('gamezID = fields[0].replace("[","").replace("]","").replace(" ","")')
    file.write("\n")
    file.write("status = str(sys.argv[7])")
    file.write("\n")
    file.write("downloadStatus = 'Wanted'")
    file.write("\n")
    file.write("if(status == '0'):")
    file.write("\n")
    file.write("    downloadStatus = 'Downloaded'")
    file.write("\n")
    file.write(
        'url = "' + gamezBaseUrl + 'updatestatus?game_id=" + gamezID + "&filePath=" + urllib.quote(filePath) + "&status=" + downloadStatus')
    file.write("\n")
    file.write('responseObject = urllib.FancyURLopener({}).open(url)')
    file.write("\n")
    file.write('responseObject.read()')
    file.write("\n")
    file.write('responseObject.close()')
    file.write("\n")
    file.write('print("Processing Completed Successfully")')
    file.close
    logger.Log('Setting permissions on post process script')
    cmd = "chmod +x '" + postProcessScript + "'"
    os.system(cmd)


def CheckConfig():
    config = ConfigParser.RawConfigParser()
    config.read(conffile)
    if not config.has_section("global"):
        config.add_section('global')
        config.set('global', 'server.socket_host', "'127.0.0.1'")
        config.set('global', 'server.socket_port', '5000')
    else:
        if not config.has_option('global', 'server.socket_host'):
            config.set('global', 'server.socket_host', "'127.0.0.1'")
        if not config.has_option('global', 'server.socket_port'):
            config.set('global', 'server.socket_port', '5000')
    if not config.has_section("GamezServer"):
        config.add_section('GamezServer')
        config.set('GamezServer', 'EnableAuth', '0')
        config.set('GamezServer', 'AuthUsername', "''")
        config.set('GamezServer', 'AuthPassword', "''")
    else:
        if not config.has_option('GamezServer', 'EnableAuth'):
            config.set('GamezServer', 'EnableAuth', '0')
        if not config.has_option('GamezServer', 'AuthUsername'):
            config.set('GamezServer', 'AuthUsername', "''")
        if not config.has_option('GamezServer', 'AuthPassword'):
            config.set('GamezServer', 'AuthPassword', "''")
    if not config.has_section('UsenetCrawler'):
        config.add_section('UsenetCrawler')
        config.set('UsenetCrawler', 'EnableUsenetCrawler', "0")
        config.set('UsenetCrawler', 'UsenetCrawlerApiKey', "''")
    else:
        if not config.has_option('UsenetCrawler', 'EnableUsenetCrawler'):
            config.set('UsenetCrawler', 'EnableUsenetCrawler', '0')
        if not config.has_option('UsenetCrawler', 'UsenetCrawlerApiKey'):
            config.set('UsenetCrawler', 'UsenetCrawlerApiKey', "''")
    if not config.has_section('Sabnzbd'):
        config.add_section('Sabnzbd')
        config.set('Sabnzbd', 'EnableSabnzbd', "0")
        config.set('Sabnzbd', 'SabnzbdHostUrl', "''")
        config.set('Sabnzbd', 'SabnzbdApiKey', "''")
        config.set('Sabnzbd', 'SabnzbdCategory', "''")
    else:
        if not config.has_option('Sabnzbd', 'EnableSabnzbd'):
            config.set('Sabnzbd', 'EnableSabnzbd', '0')
        if not config.has_option('Sabnzbd', 'SabnzbdHostUrl'):
            config.set('Sabnzbd', 'SabnzbdHostUrl', "''")
        if not config.has_option('Sabnzbd', 'SabnzbdApiKey'):
            config.set('Sabnzbd', 'SabnzbdApiKey', "''")
        if not config.has_option('Sabnzbd', 'SabnzbdCategory'):
            config.set('Sabnzbd', 'SabnzbdCategory', "''")
    if not config.has_section('Games Database Update'):
        config.add_section('Games Database Update')
        config.set('Games Database Update', 'Time between full database updates (in hours)', "72")
    else:
        if not config.has_option('Games Database Update', 'Time between full database updates (in hours)'):
            config.set('Games Database Update', 'Time between full database updates (in hours)', "72")

    if not config.has_section('PostProcessing'):
        config.add_section('PostProcessing')
        config.set('PostProcessing', 'EnableWiiPostProcessing', "0")
        config.set('PostProcessing', 'WiiDestinationPath', "''")
        config.set('PostProcessing', 'EnablePS3PostProcessing', "0")
        config.set('PostProcessing', 'PS3DestinationPath', "''")
    else:
        if not config.has_option('PostProcessing', 'EnableWiiPostProcessing'):
            config.set('PostProcessing', 'EnableWiiPostProcessing', '0')
        if not config.has_option('PostProcessing', 'WiiDestinationPath'):
            config.set('PostProcessing', 'WiiDestinationPath', "''")
        if not config.has_option('PostProcessing', 'EnablePS3PostProcessing'):
            config.set('PostProcessing', 'EnablePS3PostProcessing', '0')
        if not config.has_option('PostProcessing', 'PS3DestinationPath'):
            config.set('PostProcessing', 'PS3DestinationPath', "''")
        if not config.has_option('PostProcessing', 'EnableXBOX360PostProcessing'):
            config.set('PostProcessing', 'EnableXBOX360PostProcessing', '0')
        if not config.has_option('PostProcessing', 'XBOX360DestinationPath'):
            config.set('PostProcessing', 'XBOX360DestinationPath', "''")
        if not config.has_option('PostProcessing', 'EnableNDSPostProcessing'):
            config.set('PostProcessing', 'EnableNDSPostProcessing', '0')
        if not config.has_option('PostProcessing', 'NDSDestinationPath'):
            config.set('PostProcessing', 'NDSDestinationPath', "''")

    with open(conffile, 'wb') as configfile:
        config.write(configfile)


version = Constants.VersionNumber()
app_path = os.path.join(os.path.dirname(__file__))
conffile = os.path.join(app_path, 'GamezServer.ini')
dbfile = os.path.join(app_path, 'Gamez.db')
logger = GamezServer.Logger.Logger(dbfile)
css_path = os.path.join(app_path, 'web_resources')
css_path = os.path.join(css_path, 'css')
images_path = os.path.join(app_path, 'web_resources')
images_path = os.path.join(images_path, 'images')
js_path = os.path.join(app_path, 'web_resources')
js_path = os.path.join(js_path, 'js')
CheckConfig()
config = ConfigParser.RawConfigParser()
config.read(conffile)
enableAuthentication = False
if (config.get('GamezServer', 'EnableAuth') == "1"):
    enableAuthentication = True
username = str(config.get('GamezServer', 'authusername')).replace("'", "")
password = str(config.get('GamezServer', 'authpassword')).replace("'", "")
validation = cherrypy.lib.auth_basic.checkpassword_dict({username: password})
conf = {
    '/': {'tools.auth_basic.on': enableAuthentication, 'tools.auth_basic.realm': 'GamezServer',
          'tools.auth_basic.checkpassword': validation},
    '/css': {'tools.staticdir.on': True, 'tools.staticdir.dir': css_path},
    '/js': {'tools.staticdir.on': True, 'tools.staticdir.dir': js_path},
    '/images': {'tools.staticdir.on': True, 'tools.staticdir.dir': images_path}
}

dao = GamezServer.GamezServerDao.GamezServerDao()
if (os.path.exists(dbfile) == False):
    dao.InitializeDB(dbfile)
    RunGameDBUpdater()
GenerateSabPostProcessScript()
logger.Log('Configuring Web Server')
cherrypy.config.update(conffile)
cherrypy.config.update(conf)
cherrypy.config["tools.encode.on"] = True
cherrypy.config["tools.encode.encoding"] = "utf-8"
app = cherrypy.tree.mount(RunWebServer(), '/', conffile)
app.merge(conf)
if hasattr(cherrypy.engine, "signal_handler"):
    cherrypy.engine.signal_handler.subscribe()
if hasattr(cherrypy.engine, "console_control_handler"):
    cherrypy.engine.console_control_handler.subscribe()
logger.Log("Starting Web Server")
Monitor(cherrypy.engine, RunGameSearch, 3600).subscribe()
Monitor(cherrypy.engine, RunGameDBUpdater, 86400).subscribe()
cherrypy.engine.start()
thread.start_new_thread(RunGameDBUpdater, ())
thread.start_new_thread(RunGameSearch, ())
cherrypy.engine.block()