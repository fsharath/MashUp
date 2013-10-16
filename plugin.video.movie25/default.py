#-*- coding: utf-8 -*-
import xbmc,xbmcgui, xbmcaddon, xbmcplugin
import urllib,re,string,os,time,threading

try:
    from resources.libs import main,settings    
except Exception, e:
    elogo = xbmc.translatePath('special://home/addons/plugin.video.movie25/resources/art/bigx.png')
    dialog = xbmcgui.Dialog()
    ok=dialog.ok('[B][COLOR=FF67cc33]Mash Up Import Error[/COLOR][/B]','Failed To Import Needed Modules',str(e),'Report missing Module at [COLOR=FF67cc33]Xbmctalk.com[/COLOR] to Fix')
    xbmc.log('Mash Up ERROR - Importing Modules: '+str(e), xbmc.LOGERROR)
    
#Mash Up - by Mash2k3 2012.

#################### Set Environment ######################
ENV = "Dev"  # "Prod" or "Dev"
############################################################

Mainurl ='http://www.movie25.so/movies/'
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art

################################################################################ Directories ##########################################################################################################
UpdatePath=os.path.join(main.datapath,'Update')
try: os.makedirs(UpdatePath)
except: pass
CachePath=os.path.join(main.datapath,'Cache')
try: os.makedirs(CachePath)
except: pass
CookiesPath=os.path.join(main.datapath,'Cookies')
try: os.makedirs(CookiesPath)
except: pass

def ShowAds():
    try:
        from xbmcads import ads
        ads.ADDON_ADVERTISE(addon_id)
    except:pass

def AtoZ():
        main.addDir('0-9','http://www.movie25.so/movies/0-9/',1,art+'/09.png')
        for i in string.ascii_uppercase:
                main.addDir(i,'http://www.movie25.so/movies/'+i.lower()+'/',1,art+'/'+i.lower()+'.png')
        main.GA("None","Movie25-A-Z")   
def MAIN():
        d = settings.getHomeItems()

        for index, value in sorted(enumerate(d), key=lambda x:x[1]):
            if value==None: continue
            if index==0:
                main.addDirHome('Search','http://www.movie25.so/',420,art+'/search2.png')
            elif index==1:
                main.addDirHome("All Fav's",'http://www.movie25.so/',639,art+'/favsu.png')
            elif index==2:
                main.addDirHome('A-Z','http://www.movie25.so/',6,art+'/AZ2.png')
            elif index==3:
                main.addDirHome('New Releases','http://www.movie25.so/movies/new-releases/',1,art+'/new2.png')
            elif index==4:
                main.addDirHome('Latest Added','http://www.movie25.so/movies/latest-added/',1,art+'/latest2.png')
            elif index==5:
                main.addDirHome('Featured Movies','http://www.movie25.so/movies/featured-movies/',1,art+'/feat2.png')
            elif index==6:
                main.addDirHome('Most Viewed','http://www.movie25.so/movies/most-viewed/',1,art+'/view2.png')
            elif index==7:
                main.addDirHome('Most Voted','http://www.movie25.so/movies/most-voted/',1,art+'/vote2.png')
            elif index==8:
                main.addDirHome('HD Releases','http://www.movie25.so/movies/latest-hd-movies/',1,art+'/dvd2hd.png')
            elif index==9:
                main.addDirHome('Genre','http://www.movie25.so/',2,art+'/genre2.png')
            elif index==10:
                main.addDirHome('By Year','http://www.movie25.so/',7,art+'/year2.png')
            elif index==11:
                main.addDirHome('Watch History','history',222,art+'/whistory.png')
            elif index==12:
                main.addDirHome('HD Movies','http://oneclickwatch.org/category/movies/',33,art+'/hd2.png')
            elif index==13:
                main.addDirHome('3D Movies','3D',223,art+'/3d.png')
            elif index==14:
                main.addDirHome('International','http://www.movie25.so/',36,art+'/intl.png')
            elif index==15:
                main.addDirHome('TV Latest','http://www.movie25.so/',27,art+'/tv2.png')
            elif index==16:
                main.addDirHome('Live Streams','http://www.movie25.so/',115,art+'/live.png')
            elif index==17:
                main.addDirHome('More TV Shows & Movies','http://www.movie25.so/',500,art+'/moretvmovies.png')
            elif index==18:
                main.addDirHome('Anime','http://www.movie25.so/',265,art+'/anime.png')
            elif index==19:
                main.addDirHome('[COLOR=FF67cc33]VIP[/COLOR]laylists','http://www.movie25.so/',234,art+'/vipp.png')
            elif index==20:
                main.addDirHome('Sports','http://www.movie25.so/',43,art+'/sportsec2.png')
            elif index==21:
                main.addDirHome('Adventure','http://www.movie25.so/',63,art+'/adv2.png')
            elif index==22:
                main.addDirHome('Kids Zone','http://www.movie25.so/',76,art+'/kidzone2.png')
            elif index==23:
                main.addDirHome('Documentaries','http://www.movie25.so/',85,art+'/docsec1.png')
            elif index==24:
                main.addDirHome("Mash Up How To's",'https://github.com/mash2k3/MashUpFixes/raw/master/HowToVid.xml',264,art+'/howto.png')
            elif index==25:
                main.addDirHome('Fixes','http://www.movie25.so/',784,art+'/fixes.png')
            elif index==26:
                main.addDirHome('HackerMils Stash','https://github.com/HackerMil/HackerMilsMovieStash/raw/master/Directory/HackerMil_Directory.xml',235,art+'/hackermil.png')
            elif index==27:
                main.addDirHome('The New Pirate Bay','https://github.com/mash2k3/MashUpTNPB/raw/master/TNPB_Directory.xml',235,'http://s20.postimg.org/jvq2l8xel/TNPB.png')
            elif index==28:
                main.addDirHome('MorePower','https://github.com/mash2k3/MashUpMorePower/raw/master/MorePower_Directory.xml',235,'https://dl.dropboxusercontent.com/u/35068738/icons/morepower.png')
            elif index==29:
                main.addDirHome('Staael 1982','https://github.com/mash2k3/Staael1982/raw/master/Staael_Directory.xml',235,'https://dl.dropboxusercontent.com/u/35068738/icons/staael.png')
            elif index==30:
                main.addDirHome('My XML Channels','nills',238,art+'/xml.png')
            elif index==31:
                main.addDirHome("K1M05's Streams",'https://github.com/mash2k3/MashUpK1m05/raw/master/k1m05_mashupDirectory.xml',181,art+'/k1m05.png')
            elif index==32:
                main.addDirHome('Mash Sports','https://github.com/mash2k3/MashSports/raw/master/Mashsprt.xml',182,art+'/mashsports.png')
            elif index==33:
                main.addDirHome('iLive Streams','ilive',119,art+'/ilive.png')
        main.addPlayc('Need Help?','http://www.movie25.com/',100,art+'/xbmctalk2.png','','','','','')
        main.addPlayc('XbmcTalk Maintenance','http://www.movie25.so/',156,art+'/talkmain.png','','','','','')
        main.addPlayc('Click Me!!!','https://github.com/mash2k3/MashupArtwork/raw/master/art/donation.png',244,art+'/paypalmash2.png','','','','','')
        main.addLink('@mashupxbmc','',art+'/twittermash.png')
        main.addPlayc('MashUp Settings','http://www.movie25.so/',1999,art+'/MashSettings.png','','','','','')
              
def Announcements():
        #Announcement Notifier from xml file
        
        try:
                link=main.OPENURL('https://github.com/mash2k3/MashUpNotifications/raw/master/Notifier.xml',verbose=False)
                link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')

        except:
                link='nill'

        r = re.findall(r'ANNOUNCEMENTWINDOW ="ON"',link)
        if r:
                match=re.compile('<item><new>(.+?)</new><message1>.+?</message1><message2>.+?</message2><message3>.+?</message3><ANNOUNCEMENT>(.+?)</ANNOUNCEMENT><old>(.+?)</old></item>').findall(link)
                if len(match)>0:
                        for new,anounce,old in match:
                                continue
                        if new != ' ':
                                runonce=os.path.join(main.datapath,'RunOnce')
                                notified=os.path.join(runonce,str(new))
                                if not os.path.exists(notified):
                                        open(notified,'w').write('version="%s",'%new)
                                        TextBoxes("[B][COLOR red]Mash Up Announcements[/B][/COLOR]",anounce)
                                if old != ' ':
                                        notified=os.path.join(runonce,str(old))
                                        if  os.path.exists(notified):
                                                os.remove(notified)
                        else:
                                print 'No Messages'
    
                else:
                    print 'Github Link Down'
                
        
        else:
                match=re.compile('<item><new>(.+?)</new><message1>(.+?)</message1><message2>(.+?)</message2><message3>(.+?)</message3><ANNOUNCEMENT>.+?</ANNOUNCEMENT><old>(.+?)</old></item>').findall(link)
                if len(match)>0:
                        for new,mes1,mes2,mes3,old in match:
                                continue
                        if new != ' ':
                                runonce=os.path.join(main.datapath,'RunOnce')
                                notified=os.path.join(runonce,str(new))
                                if not os.path.exists(notified):
                                        open(notified,'w').write('version="%s",'%new)
                                        dialog = xbmcgui.Dialog()
                                        ok=dialog.ok('[B]Important Announcement![/B]', str(mes1) ,str(mes2),str(mes3))
                                if old != ' ':
                                        notified=os.path.join(runonce,str(old))
                                        if  os.path.exists(notified):
                                                os.remove(notified)
                        else:
                                print 'No Messages'
    
                else:
                    print 'Github Link Down'
        
        match=re.compile('<vid><new>(.+?)</new><video>(.+?)</video><old>(.+?)</old></vid>').findall(link)
        if len(match)>0:
                for new,video,old in match:
                        continue
                if new != ' ':
                        runonce=os.path.join(main.datapath,'RunOnce')
                        notified=os.path.join(runonce,str(new))
                        if not os.path.exists(notified):
                                open(notified,'w').write('version="%s",'%new)
                                if '</mu>' in video:
                                    video=video.replace('</mu>','')
                                    from resources.libs.movies_tv import movieplaylist
                                    movieplaylist.MLink2('MashUp',video,'',muvideo=True)
                                else:
                                    from resources.libs import youtube
                                    youtube.YOULink('MashUp',video,'')
                        if old != ' ':
                                notified=os.path.join(runonce,str(old))
                                if  os.path.exists(notified):
                                        os.remove(notified)
                else:
                        print 'No Messages'
    
        else:
            print 'Github Link Down'


def CheckForAutoUpdate(force = False):
        GitHubRepo    = 'AutoUpdate'
        GitHubUser    = 'mash2k3'
        GitHubBranch  = 'master'
        UpdateVerFile = 'update'
        verCheck=main.CheckVersion()#Checks If Plugin Version is up to date
        if verCheck == True:
            from resources.libs import autoupdate
            try:
                print "Mashup auto update - started"
                html=main.OPENURL('https://github.com/'+GitHubUser+'/'+GitHubRepo+'?files=1', mobile=True, verbose=False)
            except: html=''
            m = re.search("View (\d+) commit",html,re.I)
            if m: gitver = int(m.group(1))
            else: gitver = 0
            UpdateVerPath = os.path.join(UpdatePath,UpdateVerFile)
            try: locver = int(autoupdate.getUpdateFile(UpdateVerPath))
            except: locver = 0
            if force: locver = 0
            if locver < gitver:
                UpdateUrl = 'https://github.com/'+GitHubUser+'/'+GitHubRepo+'/archive/'+GitHubBranch+'.zip'
                UpdateLocalName = GitHubRepo+'.zip'
                UpdateDirName   = GitHubRepo+'-'+GitHubBranch
                UpdateLocalFile = xbmc.translatePath(os.path.join(UpdatePath, UpdateLocalName))
            
                print "auto update - new update available ("+str(gitver)+")"
                xbmc.executebuiltin("XBMC.Notification(MashUp Update,New Update detected,3000,"+main.slogo+")")
                dialog = xbmcgui.Dialog()
                ret = dialog.yesno('Mash Up Update', 'There is a new update available.','Would you like to update now?','','No', 'Yes')
                if ret:
                    try:os.remove(UpdateLocalFile)
                    except:pass
                    try: urllib.urlretrieve(UpdateUrl,UpdateLocalFile)
                    except:pass
                    if os.path.isfile(UpdateLocalFile):
                        extractFolder = xbmc.translatePath('special://home/addons')
                        pluginsrc =  xbmc.translatePath(os.path.join(extractFolder,UpdateDirName))
                        if autoupdate.unzipAndMove(UpdateLocalFile,extractFolder,pluginsrc):
                            autoupdate.saveUpdateFile(UpdateVerPath,str(gitver))
                            main.GA("Autoupdate",str(gitver)+" Successful")
                            print "Mashup auto update - update install successful ("+str(gitver)+")"
                            xbmc.executebuiltin("XBMC.Notification(MashUp Update,Successful,5000,"+main.slogo+")")
                            xbmc.executebuiltin("XBMC.Container.Refresh")
                        else:
                            print "Mashup auto update - update install failed ("+str(gitver)+")"
                            xbmc.executebuiltin("XBMC.Notification(MashUp Update,Failed,3000,"+main.elogo+")")
                            main.GA("Autoupdate",str(gitver)+" Failed")
                    else:
                        print "Mashup auto update - cannot find downloaded update ("+str(gitver)+")"
                        xbmc.executebuiltin("XBMC.Notification(MashUp Update,Failed,3000,"+main.elogo+")")
                        main.GA("Autoupdate",str(gitver)+" Repo problem")
            else:
                if force: xbmc.executebuiltin("XBMC.Notification(MashUp Update,MashUp is up-to-date,3000,"+main.slogo+")")
                print "Mashup auto update - Mashup is up-to-date ("+str(locver)+")"
            return
        
def CheckForAutoUpdateDev(force = False):
        GitHubRepo    = 'MashUp'
        GitHubUser    = 'mash2k3'
        GitHubBranch  = 'master'
        UpdateVerFile = 'devupdate'
        from resources.libs import autoupdate
        try:
            print "Mashup DEV auto update - started"
            html=main.OPENURL('https://github.com/'+GitHubUser+'/'+GitHubRepo+'?files=1', mobile=True, verbose=False)
        except: html=''
        m = re.search("View (\d+) commit",html,re.I)
        if m: gitver = int(m.group(1))
        else: gitver = 0
        UpdateVerPath = os.path.join(UpdatePath,UpdateVerFile)
        try: locver = int(autoupdate.getUpdateFile(UpdateVerPath))
        except: locver = 0
        if force: locver = 0
        if locver < gitver:
            UpdateUrl = 'https://github.com/'+GitHubUser+'/'+GitHubRepo+'/archive/'+GitHubBranch+'.zip'
            UpdateLocalName = GitHubRepo+'.zip'
            UpdateDirName   = GitHubRepo+'-'+GitHubBranch
            UpdateLocalFile = xbmc.translatePath(os.path.join(UpdatePath, UpdateLocalName))
            print "Mashup DEV auto update - new update available ("+str(gitver)+")"
            xbmc.executebuiltin("XBMC.Notification(MashUp DEV Update,New Update detected,3000,"+main.slogo+")")
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno('Mash Up DEV Update', 'There is a new update available.','Would you like to update now?','','No', 'Yes')
            if ret:
                try:os.remove(UpdateLocalFile)
                except:pass
                try: urllib.urlretrieve(UpdateUrl,UpdateLocalFile)
                except:pass
                if os.path.isfile(UpdateLocalFile):
                    extractFolder = xbmc.translatePath('special://home/addons')
                    pluginsrc =  xbmc.translatePath(os.path.join(extractFolder,UpdateDirName))
                    if autoupdate.unzipAndMove(UpdateLocalFile,extractFolder,pluginsrc):
                        autoupdate.saveUpdateFile(UpdateVerPath,str(gitver))
                        print "Mashup DEV auto update - update install successful ("+str(gitver)+")"
                        xbmc.executebuiltin("XBMC.Notification(MashUp DEV Update,Successful,5000,"+main.slogo+")")
                        xbmc.executebuiltin("XBMC.Container.Refresh")
                    else:
                        print "Mashup DEV auto update - update install failed ("+str(gitver)+")"
                        xbmc.executebuiltin("XBMC.Notification(MashUp DEV Update,Failed,3000,"+main.elogo+")")
                else:
                    print "Mashup DEV auto update - cannot find downloaded update ("+str(gitver)+")"
                    xbmc.executebuiltin("XBMC.Notification(MashUp DEV Update,Failed,3000,"+main.elogo+")")
        else:
            if force: xbmc.executebuiltin("XBMC.Notification(MashUp DEV Update,MashUp is up-to-date,3000,"+main.slogo+")")
            print "Mashup auto update - Mashup DEV is up-to-date ("+str(locver)+")"
        return
    
def Notify():
        mashup=139
        runonce=os.path.join(main.datapath,'RunOnce')
        try:
            os.makedirs(runonce)
        except:
            pass
        notified=os.path.join(runonce,str(mashup))
        if not os.path.exists(notified):
            open(notified,'w').write('version="%s",'%mashup)
            dir = selfAddon.getAddonInfo('path')
            chlg = os.path.join(dir, 'changelog.txt')
            TextBoxes("[B][COLOR red]Mash Up Changelog[/B][/COLOR]",chlg)
            mashup=mashup-1
            notified=os.path.join(runonce,str(mashup))
            if  os.path.exists(notified):
                os.remove(notified)
        
        
def GENRE(url):
        main.addDir('Action','http://www.movie25.so/movies/action/',1,art+'/act.png')
        main.addDir('Adventure','http://www.movie25.so/movies/adventure/',1,art+'/adv.png')
        main.addDir('Animation','http://www.movie25.so/movies/animation/',1,art+'/ani.png')
        main.addDir('Biography','http://www.movie25.so/movies/biography/',1,art+'/bio.png')
        main.addDir('Comedy','http://www.movie25.so/movies/comedy/',1,art+'/com.png')
        main.addDir('Crime','http://www.movie25.so/movies/crime/',1,art+'/cri.png')
        main.addDir('Documentary','http://www.movie25.so/movies/documentary/',1,art+'/doc.png')
        main.addDir('Drama','http://www.movie25.so/movies/drama/',1,art+'/dra.png')
        main.addDir('Family','http://www.movie25.so/movies/family/',1,art+'/fam.png')
        main.addDir('Fantasy','http://www.movie25.so/movies/fantasy/',1,art+'/fant.png')
        main.addDir('History','http://www.movie25.so/movies/history/',1,art+'/his.png')
        main.addDir('Horror','http://www.movie25.so/movies/horror/',1,art+'/hor.png')
        main.addDir('Music','http://www.movie25.so/movies/music/',1,art+'/mus.png')
        main.addDir('Musical','http://www.movie25.so/movies/musical/',1,art+'/mucl.png')
        main.addDir('Mystery','http://www.movie25.so/movies/mystery/',1,art+'/mys.png')
        main.addDir('Romance','http://www.movie25.so/movies/romance/',1,art+'/rom.png')
        main.addDir('Sci-Fi','http://www.movie25.so/movies/sci-fi/',1,art+'/sci.png')
        main.addDir('Short','http://www.movie25.so/movies/short/',1,art+'/sho.png')
        main.addDir('Sport','http://www.movie25.so/movies/sport/',1,art+'/sport.png')
        main.addDir('Thriller','http://www.movie25.so/movies/thriller/',1,art+'/thr.png')
        main.addDir('War','http://www.movie25.so/movies/war/',1,art+'/war.png')
        main.addDir('Western','http://www.movie25.so/movies/western/',1,art+'/west.png')
        main.GA("None","Movie25-Genre")
        main.VIEWSB()
        
def YEAR():
        main.addDir('2013','http://www.movie25.so/search.php?year=2013/',8,art+'/year.png')
        main.addDir('2012','http://www.movie25.so/search.php?year=2012/',8,art+'/2012.png')
        main.addDir('2011','http://www.movie25.so/search.php?year=2011/',8,art+'/2011.png')
        main.addDir('2010','http://www.movie25.so/search.php?year=2010/',8,art+'/2010.png')
        main.addDir('2009','http://www.movie25.so/search.php?year=2009/',8,art+'/2009.png')
        main.addDir('2008','http://www.movie25.so/search.php?year=2008/',8,art+'/2008.png')
        main.addDir('2007','http://www.movie25.so/search.php?year=2007/',8,art+'/2007.png')
        main.addDir('2006','http://www.movie25.so/search.php?year=2006/',8,art+'/2006.png')
        main.addDir('2005','http://www.movie25.so/search.php?year=2005/',8,art+'/2005.png')
        main.addDir('2004','http://www.movie25.so/search.php?year=2004/',8,art+'/2004.png')
        main.addDir('2003','http://www.movie25.so/search.php?year=2003/',8,art+'/2003.png')
        main.addDir('Enter Year','http://www.movie25.com',23,art+'/enteryear.png')
        main.GA("None","Movie25-Year")
        main.VIEWSB()

def GlobalFav():
        if selfAddon.getSetting("groupfavs") == "true":
            ListglobalFavALL()
        else:
            main.addLink("[COLOR red]Mash Up Fav's can also be favorited under XBMC favorites[/COLOR]",'','')
            main.addDir("Downloaded Content",'Mash Up',241,art+'/downloadlog.png')
            main.addDir("Movie25 Fav's",'http://www.movie25.so/',10,art+'/fav2.png')
            main.addDir("iWatchOnline Fav's",'http://www.movie25.so/',655,art+'/fav2+.png')
            main.addDir("Movie Fav's",'http://www.movie25.so/',641,art+'/fav.png')
            main.addDir("TV Show Fav's",'http://www.movie25.so/',640,art+'/fav.png')
            main.addDir("TV Episode Fav's",'http://www.movie25.so/',651,art+'/fav.png')
            main.addDir("Live Fav's",'http://www.movie25.so/',648,art+'/fav.png')
            main.addDir("Misc. Fav's",'http://www.movie25.so/',650,art+'/fav.png')



    
def TV():
        main.addDir('Latest Episodes (Newmyvideolinks) True HD[COLOR red] DC[/COLOR]','TV',34,art+'/tvb.png')
        main.addDir('Latest Episodes (Rlsmix)[COLOR red](Debrid Only)[/COLOR] True HD[COLOR red] DC[/COLOR]','TV',61,art+'/tvb.png')
        main.addDir('Latest Episodes (Sceper)[COLOR red](Debrid Only)[/COLOR] True HD','http://sceper.ws/home/category/tv-shows',545,art+'/tvb.png')
        main.addDir('Latest Episodes (TvRelease) True HD[COLOR red] DC[/COLOR]','http://www.tv-release.net/category/tvshows/tv720p/',1001,art+'/tvb.png')
        main.addDir('Latest Episodes (SceneLog) True HD[COLOR red] DC[/COLOR]','TV',657,art+'/tvb.png')
        main.addDir('Latest Episodes (TubePlus)[COLOR red] DC[/COLOR]','http://www.tubeplus.me/browse/tv-shows/Last/ALL/',1041,art+'/tvb.png')
        main.addDir('Latest Episodes (Watchseries)','http://watchseries.lt/tvschedule/-1',573,art+'/tvb.png')
        main.addDir('Latest Episodes (iWatchonline)','http://www.iwatchonline.to/tv-schedule',592,art+'/tvb.png')
        main.addDir('Latest Episodes (Movie1k)','movintv',30,art+'/tvb.png')
        main.addDir('Latest Episodes (Oneclickwatch)','http://oneclickwatch.org',32,art+'/tvb.png')
        main.addDir('Latest Episodes (Seriesgate)','http://seriesgate.tv/latestepisodes/',602,art+'/tvb.png')
        main.addDir('Latest 150 Episodes (ChannelCut)','http://www.channelcut.me/last-150',546,art+'/tvb.png')
        main.addDir('Latest 100 Episodes (Tv4stream)','http://www.tv4stream.info/last-100-links/',546,art+'/tvb.png')
        main.GA("None","TV-Latest")


def ThreeDsec():
        main.addDir('3D Movies (Newmyvideolinks) True HD[COLOR red] DC[/COLOR]','3D',34,art+'/3d.png')
        link=getListFile('https://github.com/mash2k3/MashUpNotifications/raw/master/Directories/3D_Directory.xml', os.path.join(CachePath,'ThreeD'))
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode>').findall(link)
        for name,url,thumb,mode in match:
                if re.findall('http',thumb):
                    thumbs=thumb
                else:
                    thumbs=art+'/'+thumb+'.png'
                main.addDir(name,url,int(mode),thumbs)


def TVAll():
        main.addDir('Watchseries.lt[COLOR red] DC[/COLOR]','TV',572,art+'/wfs/watchseries.png')
        main.addDir('tubePLUS[COLOR red] DC[/COLOR]','tp+',1020,art+'/tubeplus.png')
        main.addDir('Series Gate','TV',601,art+'/wfs/sg.png')
        main.addDir('iWatchOnline [COLOR red] DC[/COLOR]','TV',584,art+'/iwatchonline.png')
        main.addDir('TV-Release[COLOR red] DC[/COLOR][COLOR blue] (Works Best With Debrid)[/COLOR]','tvr',1000,art+'/tvrelease.png')
        main.addDir('Movie25 [COLOR red]DC[/COLOR]','TV',267,art+'/movie25.png')
        main.addDir('Sceper [COLOR red](Debrid Only)[/COLOR]','TV',539,art+'/wfs/sceper.png')
        main.addDir('SominalTvFilms','TV',619,art+'/wfs/sominal.png')
        main.addDir('Dramania','TV',268,art+'/dramania.png')
        main.addDir('Extramina','TV',530,art+'/wfs/extramina.png')
        main.addDir('FMA','TV',567,art+'/wfs/fma.png')
        #main.addDir('Global BC','gbc',165,art+'/globalbc.png')       
        main.GA("None","Plugin")

def Movie25():
        main.addDirHome('Search','http://www.movie25.so/',420,art+'/search2.png')
        main.addDirHome('A-Z','http://www.movie25.so/',6,art+'/AZ2.png')
        main.addDirHome('New Releases','http://www.movie25.so/movies/new-releases/',1,art+'/new2.png')
        main.addDirHome('Latest Added','http://www.movie25.so/movies/latest-added/',1,art+'/latest2.png')
        main.addDirHome('Featured Movies','http://www.movie25.so/movies/featured-movies/',1,art+'/feat2.png')
        main.addDirHome('Most Viewed','http://www.movie25.so/movies/most-viewed/',1,art+'/view2.png')
        main.addDirHome('Most Voted','http://www.movie25.so/movies/most-voted/',1,art+'/vote2.png')
        main.addDirHome('HD Releases','http://www.movie25.so/movies/latest-hd-movies/',1,art+'/dvd2hd.png')
        main.addDirHome('Genre','http://www.movie25.so/',2,art+'/genre2.png')
        main.addDirHome('By Year','http://www.movie25.so/',7,art+'/year2.png')

def ANIME():
        main.addDir('dubzonline','TV',613,art+'/wfs/dubzonline.png')
        main.addDir('AnimeFreak TV','TV',625,art+'/animefreak.png')
        main.GA("None","Anime")
    

def HD():
        main.addDir('Latest HD Movies (Newmyvideolinks) True HD[COLOR red] DC[/COLOR]','http://newmyvideolinks.com',34,art+'/hd2.png')
        main.addDir('Latest HD Movies (Dailyflix) True HD','HD',53,art+'/hd2.png')
        main.addDir('Latest HD Movies (Starplay/[COLOR=FF67cc33]Noobroom7[/COLOR]) Direct MP4 True HD[COLOR red] DC[/COLOR]','http://noobroom7.com/latest.php',57,art+'/hd2.png')
        main.addDir('Latest HD Movies (Oneclickmovies)[COLOR red](Debrid Only)[/COLOR] True HD[COLOR red] DC[/COLOR]','www.scnsrc.me',55,art+'/hd2.png')
        main.addDir('Latest HD Movies (Sceper)[COLOR red](Debrid Only)[/COLOR] True HD','http://sceper.ws/category/movies/movies-bluray-rip',541,art+'/hd2.png')
        main.addDir('Latest HD Movies (Oneclickwatch)','http://oneclickwatch.org/category/movies/',25,art+'/hd2.png')
        main.addDir('HackerMil HD Movies','https://github.com/HackerMil/HackerMilsMovieStash/raw/master/Movies/5%20HD.xml',236,'https://github.com/mash2k3/MashupArtwork/raw/master/art/hd2.png')
        main.addDir('TNPB HD Movies','https://github.com/mash2k3/MashUpTNPB/raw/master/720p%20Movies.xml',236,'https://github.com/mash2k3/MashupArtwork/raw/master/art/hd2.png')
        main.addDir('MorePower HD Movies','https://github.com/mash2k3/MashUpMorePower/raw/master/Full1080P.xml',236,'https://github.com/mash2k3/MashupArtwork/raw/master/art/hd2.png')
        main.addDir('Staael1982 HD Movies','https://github.com/mash2k3/Staael1982/raw/master/veehdCollection.xml',236,'https://github.com/mash2k3/MashupArtwork/raw/master/art/hd2.png')
                
        main.GA("None","HD")
def INT():
        main.addDir('Latest Indian Subtitled Movies (einthusan)','http://www.einthusan.com',37,art+'/intl.png')
        main.addDir('Latest Hindi/Tamil/Telugu & more (sominaltv)','TV',619,art+'/intl.png')
        main.addDir('Latest Indian Movies (Movie1k)','movin',30,art+'/intl.png')
        main.addDir('Latest Indian Dubbed Movies (Movie1k)','movindub',30,art+'/intl.png')
        main.addDir('Latest Spanish Dubbed & Subtitled(ESP) Movies (cinevip)','http://www.cinevip.org/',66,art+'/intl.png')
        main.addDir("XcTech's Bollywood Playlist",'PLvNKtQkKaqg8IPssr3WG4-YkOEAe8TQ0j',205,art+'/intl.png')
        main.addDir('Staael1982 Danish Movies','https://github.com/mash2k3/Staael1982/raw/master/danish%20movies.xml',236,'https://github.com/mash2k3/MashupArtwork/raw/master/art/intl.png')
                
        main.GA("None","INT")

def SPORTS():
        main.addDir('ESPN','http:/espn.com',44,art+'/espn.png')
        main.addDir('TSN','http:/tsn.com',95,art+'/tsn.png')
        main.addDir('SkySports.com','www1.skysports.com',172,art+'/skysports.png')
        main.addDir('Fox Soccer  [COLOR red](US ONLY)[/COLOR]','http:/tsn.com',124,art+'/foxsoc.png')
        main.addDir('All MMA','mma',537,art+'/mma.png')
        main.addDir('Outdoor Channel','http://outdoorchannel.com/',50,art+'/OC.png')
        main.addDir('Wild TV','https://www.wildtv.ca/shows',92,art+'/wildtv.png')
        main.addDir('Workouts','https://www.wildtv.ca/shows',194,art+'/workout.png')
        main.addDir('The Golf Channel','golf',217,art+'/golfchannel.png')
        link=getListFile('https://github.com/mash2k3/MashUpNotifications/raw/master/Sport_Directory.xml', os.path.join(CachePath,'Sports'))
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode>').findall(link)
        for name,url,thumb,mode in match:
                if re.findall('http',thumb):
                    thumbs=thumb
                else:
                    thumbs=art+'/'+thumb+'.png'
                main.addDir(name,url,int(mode),thumbs)
        
        main.GA("None","Sports")

def MMA():
        main.addDir('UFC','ufc',59,art+'/ufc.png')
        main.addDir('Bellator','BellatorMMA',47,art+'/bellator.png')
        main.addDir('MMA Fighting.com','http://www.mmafighting.com/videos',113,art+'/mmafig.png')
        main.addDir('HackerMil Fight Club','https://github.com/HackerMil/HackerMilsMovieStash/raw/master/Fight%20Club/Fight%20Club.xml',236,'https://github.com/mash2k3/MashupArtwork/raw/master/art/mma.png')
                

def WorkoutMenu():
        main.addDir('Fitness Blender[COLOR red](Full Workouts)[/COLOR]','fb',198,art+'/fitnessblender.png')
        main.addDir('Insanity','http://watchseries.lt/serie/INSANITY_-_The_Asylum',578,art+'/insanity.png')
        main.addDir('P90X','http://watchseries.lt/serie/p90x',578,art+'/p90x.png')
        main.addDir('Body Building[COLOR red](Instructional Only)[/COLOR]','bb',195,art+'/bodybuilding.png')
        main.addDir('HackerMil Workouts','https://github.com/HackerMil/HackerMilsMovieStash/raw/master/Workouts/Workouts.xml',236,'https://github.com/mash2k3/MashupArtwork/raw/master/art/workout.png')
                
        

def UFC():
        main.addDir('UFC.com','ufc',47,art+'/ufc.png')
        main.addDir('UFC(Movie25)','ufc',60,art+'/ufc.png')
        main.addDir('UFC(Newmyvideolinks)','ufc',103,art+'/ufc.png')
        main.GA("None","UFC")

def ADVENTURE():
        main.addDir('Discovery Channel','http://dsc.discovery.com/videos',631,art+'/disco.png')
        main.addDir('National Geographic','ng',70,art+'/natgeo.png')
        main.addDir('Military Channel','http://military.discovery.com/videos',80,art+'/milcha.png')
        main.addDir('Science Channel','http://science.discovery.com/videos',81,art+'/scicha.png')
        main.addDir('Velocity Channel','http://velocity.discovery.com/videos',82,art+'/velo.png')
        main.addDir('Animal Planet','http://animal.discovery.com/videos',83,art+'/anip.png')
        main.GA("None","Adventure")
        


def KIDZone(murl):
        main.addDir('Disney Jr.','djk',107,art+'/disjr.png')
        main.addDir('National Geographic Kids','ngk',71,art+'/ngk.png')
        main.addDir('WB Kids','wbk',77,art+'/wb.png')
        main.addDir('Youtube Kids','wbk',84,art+'/youkids.png')
        main.addDir('TNPB KidsZone','https://github.com/mash2k3/MashUpTNPB/raw/master/kidszone.xml',236,'https://github.com/mash2k3/MashupArtwork/raw/master/art/kidzone2.png')
        main.addDir('MorePower Family and Kids shows and movies','https://github.com/mash2k3/MashUpMorePower/raw/master/KidsShowsMovies.xml',236,'https://github.com/mash2k3/MashupArtwork/raw/master/art/kidzone2.png')
        main.addDir('Staael1982 Animated Movies','https://github.com/mash2k3/Staael1982/raw/master/animated_movies.xml',236,'https://github.com/mash2k3/MashupArtwork/raw/master/art/kidzone2.png')
                
        main.GA("None","KidZone")
        main.VIEWSB()
    
def LiveStreams():
        threading.Thread(target=showLiveAnnouncements).start()
        main.addDir('Livestation News','http://mobile.livestation.com/',116,art+'/livestation.png')
        main.addDir('iLive Streams','ilive',119,art+'/ilive.png')
        main.addDir('Castalba Streams','castalgba',122,art+'/castalba.png')
        main.addDir('Misc. Music Streams','music',127,art+'/miscmusic.png')
        main.addDir('By Country','navi',143,art+'/countrysec.png')
        main.addDir('Arabic Streams','navi',231,art+'/arabicstream.png')
        link=getListFile('https://github.com/mash2k3/MashUpNotifications/raw/master/LiveDirectory(mash2k3Only).xml',os.path.join(CachePath,'LiveStreams'))
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('type=playlistname=Sorted by user-assigned order','').replace('name=Sorted [COLOR=FF00FF00]by user-assigned order[/COLOR]','').replace('name=Live Tv Channels Twothumb','')
        match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode>').findall(link)
        for name,url,thumb,mode in match:
                if re.findall('http',thumb):
                    thumbs=thumb
                else:
                    thumbs=art+'/'+thumb+'.png'
                main.addDir(name,url,int(mode),thumbs)
        if selfAddon.getSetting("customchannel") == "true":
                main.addDir('My XML Channels','nills',238,art+'/xml.png')
        main.addDir('TubTub.com','http://tubtub.com/',185,art+'/tubtub.png')
        main.addDir('181.FM Radio Streams','nills',191,art+'/181fm.png')
        
        main.GA("None","Live")

def DOCS():
        main.addDir('Vice','http://www.vice.com/shows',104,art+'/vice.png')
        main.addDir('Documentary Heaven','doc1',86,art+'/dh.png')
        main.addDir('Watch Documentary','doc1',159,art+'/watchdoc.png')
        main.addDir('Documentary Wire','doc1',226,art+'/docwire.png')
        main.addDir('Top Documentary Films','doc2',86,art+'/topdoc.png')
        main.addDir('Documentary Log','doc3',86,art+'/doclog.png')
        main.addDir('HackerMil Documentaries','https://github.com/HackerMil/HackerMilsMovieStash/raw/master/Misc/7%20DOCUMENTARY.xml',236,'https://github.com/mash2k3/MashupArtwork/raw/master/art/docsec1.png')
        main.addDir('MorePower Documentaries','https://github.com/mash2k3/MashUpMorePower/raw/master/Documentries.xml',236,'https://github.com/mash2k3/MashupArtwork/raw/master/art/docsec1.png')
                
        main.addDir('Documentaries (Movie25)','http://www.movie25.so/movies/documentary/',1,art+'/doc.png')
        main.GA("None","Documentary")


def PlaylistDir():
        link=getListFile('https://github.com/mash2k3/MashUpNotifications/raw/master/MoviePlaylist_Dir.xml',os.path.join(CachePath,'Playlist'))
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail><mode>(.+?)</mode>').findall(link)
        for name,url,thumb,mode in match:
                if re.findall('http',thumb):
                    thumbs=thumb
                else:
                    thumbs=art+'/'+thumb+'.png'
                main.addDir(name,url,int(mode),thumbs)
        main.GA("None","MoviePL")

def FIXES():
        main.addLink('[COLOR red]Apply fix only if your current one is broken[/COLOR]','','')
        try:
                link=main.OPENURL('https://github.com/mash2k3/MashUpFixes/raw/master/Fixes.xml')
        except:
                xbmc.executebuiltin("XBMC.Notification(Sorry!,Repo is Down,5000,"")")
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<item><name>([^<]+)</name.+?filename>([^<]+)</filename.+?location>([^<]+)</location.+?path>([^<]+)</path.+?thumbnail>([^<]+)</thumbnail></item>').findall(link)
        for name,filename,location,path,thumb in match:
                main.addDirFIX(name,filename,785,art+'/'+thumb+'.png',location,path)


def FIXDOWN(name,filename,location,path):
    main.GA("Fixes",name+"-Fix")
    url = 'https://github.com/mash2k3/MashUpFixes/raw/master/FIXES/'+filename
    print "#############  Downloading from "+ url+"  #####################"
    path = xbmc.translatePath(os.path.join(str(location),str(path)))
    lib=os.path.join(path, str(filename))
    DownloaderClass(url,lib)
    dialog = xbmcgui.Dialog()
    name  = name.split('[COLOR red]')[0]
    dialog.ok("Mash Up", "Thats It All Done", "[COLOR blue]Now "+name+" should be Fixed[/COLOR]")
    
def HTVList(murl):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<title>([^<]+)</title.+?link>(.+?)</link.+?thumbnail>([^<]+)</thumbnail>').findall(link)
        for name,url,thumb in match:
                main.addPlayc(name,url,259,thumb,'','','','','')
        main.GA("None","How To Videos")        
        
def showLiveAnnouncements():
                #Announcement Notifier from xml file
        try:
                link=main.OPENURL('https://github.com/mash2k3/MashUpNotifications/raw/master/NotifierLive.xml', verbose=False)
        except:
                link='nill'

        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<item><new>(.+?)</new><message1>(.+?)</message1><message2>(.+?)</message2><message3>(.+?)</message3><old>(.+?)</old></item>').findall(link)
        if len(match)>0:
                for new,mes1,mes2,mes3,old in match:
                        continue
                if new != ' ':
                        runonce=os.path.join(main.datapath,'RunOnce')
                        notified=os.path.join(runonce,str(new))
                        if not os.path.exists(notified):
                                open(notified,'w').write('version="%s",'%new)
                                dialog = xbmcgui.Dialog()
                                ok=dialog.ok('[B]Live Section Announcement![/B]', str(mes1) ,str(mes2),str(mes3))
                        if old != ' ':
                                notified=os.path.join(runonce,str(old))
                                if  os.path.exists(notified):
                                        os.remove(notified)
                else:
                        print 'No Messages'
    
        else:
            print 'Github Link Down'
def getListFile(url, path, excepturl = None ):
        link = ''
        t = threading.Thread(target=setListFile,args=(url,path,excepturl))
        t.start()
        if not os.path.exists(path):
            t.join()
        if os.path.exists(path):
            try: link = open(path).read()
            except: pass
        return link       
def setListFile(url, path, excepturl = None):
        content = None
        try:
            content=main.OPENURL(url, verbose=False)
        except:
            if excepturl:
                content=main.OPENURL(excepturl, verbose=False)
        if content:
            try:
                open(path,'w+').write(content)
            except: pass
        return
################################################################################ XBMCHUB Repo & Hub Maintenance Installer ##########################################################################################################


hubpath = xbmc.translatePath(os.path.join('special://home/addons', ''))
maintenance=os.path.join(hubpath, 'plugin.video.hubmaintenance')

def DownloaderClass2(url,dest):
        try:
            urllib.urlretrieve(url,dest)
        except Exception, e:
            dialog = xbmcgui.Dialog()
            main.ErrorReport(e)
            dialog.ok("Mash Up", "Report the error below at xbmctalk.com", str(e), "We will try our best to help you")


def DownloaderClass(url,dest):
        try:
            dp = xbmcgui.DialogProgress()
            dp.create("Mash Up","Downloading & Copying File",'')
            urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
        except Exception, e:
            dialog = xbmcgui.Dialog()
            main.ErrorReport(e)
            dialog.ok("Mash Up", "Report the error below at xbmctalk.com", str(e), "We will try our best to help you")
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
        try:
            percent = min((numblocks*blocksize*100)/filesize, 100)
            dp.update(percent)
        except:
            percent = 100
            dp.update(percent)
        if (dp.iscanceled()): 
            print "DOWNLOAD CANCELLED" # need to get this part working
            return False
        dp.close()
        del dp
def HubMain():
            ok=True
            cmd = 'plugin://plugin.video.hubmaintenance/'
            xbmc.executebuiltin('XBMC.Container.Update(%s)' % cmd)
            return ok


repopath = xbmc.translatePath(os.path.join('special://home/addons', 'repository.mash2k3'))
try: 
    if not os.path.exists(repopath):
        url = 'https://bitbucket.org/mash2k3/mash2k3-repository/src/a3be11dd1482e4b08fcc3905b9150971117e7955/zips/repository.mash2k3/repository.mash2k3-1.5.zip?at=master'
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        lib=os.path.join(path, 'repository.mash2k3-1.5.zip')
        DownloaderClass2(url,lib)
        print lib
        addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
        time.sleep(2)
        xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(lib,addonfolder))
except:
    pass

repopath = xbmc.translatePath(os.path.join('special://home/addons', 'repository.divingmule.addons'))
try: 
    if not os.path.exists(repopath):
        url = 'https://dl.dropboxusercontent.com/u/35068738/Mashup/repository.divingmule.addons.zip'
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        lib=os.path.join(path, 'repository.divingmule.addons.zip')
        DownloaderClass2(url,lib)
        print lib
        addonfolder = xbmc.translatePath(os.path.join('special://home/addons',''))
        time.sleep(2)
        xbmc.executebuiltin("XBMC.Extract(%s,%s)"%(lib,addonfolder))
except:
    pass
################################################################################ XBMCHUB POPUP ##########################################################################################################


class HUB( xbmcgui.WindowXMLDialog ):
    def __init__( self, *args, **kwargs ):
        self.shut = kwargs['close_time'] 
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
                                       
    def onInit( self ):
        xbmc.Player().play('%s/resources/skins/DefaultSkin/media/theme.mp3'%selfAddon.getAddonInfo('path'))# Music.
        while self.shut > 0:
            xbmc.sleep(1000)
            self.shut -= 1
        xbmc.Player().stop()
        self._close_dialog()
                
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ): 
        if controlID == 12:
            xbmc.Player().stop()
            self._close_dialog()
        if controlID == 7:
            xbmc.Player().stop()
            self._close_dialog()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            xbmc.Player().stop()
            self._close_dialog()

    def _close_dialog( self ):
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        time.sleep( .4 )
        self.close()
        
def pop():
    if xbmc.getCondVisibility('system.platform.ios'):
        if not xbmc.getCondVisibility('system.platform.atv'):
            popup = HUB('hub1.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    if xbmc.getCondVisibility('system.platform.android'):
        popup = HUB('hub1.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    else:
        popup = HUB('hub.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=34,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    popup.doModal()
    del popup
#######################################################################################

class HUBx( xbmcgui.WindowXMLDialog ):
        def __init__( self, *args, **kwargs ):
            self.shut = kwargs['close_time'] 
            xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
            xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
                                       
        def onInit( self ):
            xbmc.Player().play('%s/resources/skins/DefaultSkin/media/theme.mp3'%selfAddon.getAddonInfo('path'))# Music
            while self.shut > 0:
                xbmc.sleep(1000)
                self.shut -= 1
            xbmc.Player().stop()
            self._close_dialog()
                
        def onFocus( self, controlID ): pass
    
        def onClick( self, controlID ): 
            if controlID == 12:
                xbmc.Player().stop()
                self._close_dialog()
                
            if controlID == 7:
                xbmc.Player().stop()
                self._close_dialog()

        def onAction( self, action ):
            if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
                xbmc.Player().stop()
                self._close_dialog()

        def _close_dialog( self ):
            path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.movie25/resources/skins/DefaultSkin','media'))
            popimage=os.path.join(path, 'tempimage.jpg')
            xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
            time.sleep( .4 )
            self.close()
            os.remove(popimage)
        
def popVIP(image):
    path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.movie25/resources/skins/DefaultSkin','media'))
    popimage=os.path.join(path, 'tempimage.jpg')
    DownloaderClass2(image,popimage)
    if xbmc.getCondVisibility('system.platform.ios'):
        if not xbmc.getCondVisibility('system.platform.atv'):
            popup = HUBx('pop1.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=60,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'),)
    if xbmc.getCondVisibility('system.platform.android'):
        popup = HUBx('pop1.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=60,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    else:
        popup = HUBx('pop.xml',selfAddon.getAddonInfo('path'),'DefaultSkin',close_time=60,logo_path='%s/resources/skins/DefaultSkin/media/Logo/'%selfAddon.getAddonInfo('path'))
    popup.doModal()
    del popup
################################################################################ Favorites Function##############################################################################################################
def getFavorites(section_title = None):
        from universal import favorites
        fav = favorites.Favorites(addon_id, sys.argv)
 
        if(section_title):
            fav_items = fav.get_my_favorites(section_title=section_title, item_mode='addon')
        else:
            fav_items = fav.get_my_favorites(item_mode='addon')

        if len(fav_items) > 0 :

            for fav_item in fav_items:
                if (fav_item['isfolder'] == 'false'):
                    if (fav_item['section_addon_title'] == "iWatchOnline Fav's" or 
                        fav_item['section_addon_title'] == "Movie Fav's"):
                        main.addPlayM(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                            fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                            fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                            fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                            fav_item['infolabels'].get('year',''))
                    elif (fav_item['section_addon_title'] == "TV Show Fav's"):
                        main.addPlayT(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                            fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                            fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                            fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                            fav_item['infolabels'].get('year',''))
                    elif (fav_item['section_addon_title'] == "TV Episode Fav's"):
                        main.addPlayTE(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                            fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                            fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                            fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                            fav_item['infolabels'].get('year',''))
                    elif (fav_item['section_addon_title'] == "Misc. Fav's"):
                        main.addPlayMs(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                            fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                            fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                            fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                            fav_item['infolabels'].get('year',''))
                    elif (fav_item['section_addon_title'] == "Live Fav's"):
                        main.addPlayL(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                            fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                            fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                            fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                            fav_item['infolabels'].get('year',''))
                    elif (fav_item['section_addon_title'] == "Movie25 Fav's"):
                        main.addInfo(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                            fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                            fav_item['infolabels'].get('genre',''), fav_item['infolabels'].get('year',''))
                else:
                    if (fav_item['section_addon_title'] == "iWatchOnline Fav's" or 
                        fav_item['section_addon_title'] == "Movie Fav's"):
                        main.addDirM(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                            fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                            fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                            fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                            fav_item['infolabels'].get('year',''))
                    elif (fav_item['section_addon_title'] == "TV Show Fav's"):
                        main.addDirT(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                            fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                            fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                            fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                            fav_item['infolabels'].get('year',''))
                    elif (fav_item['section_addon_title'] == "TV Episode Fav's"):
                        main.addDirTE(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                            fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                            fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                            fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                            fav_item['infolabels'].get('year',''))
                    elif (fav_item['section_addon_title'] == "Misc. Fav's"):
                        main.addDirMs(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                            fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                            fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                            fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                            fav_item['infolabels'].get('year',''))
                    elif (fav_item['section_addon_title'] == "Live Fav's"):
                        main.addDirL(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                            fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                            fav_item['infolabels'].get('plot',''), fav_item['fanart_url'],
                            fav_item['infolabels'].get('duration',''), fav_item['infolabels'].get('genre',''),
                            fav_item['infolabels'].get('year',''))
                    elif (fav_item['section_addon_title'] == "Movie25 Fav's"):
                        main.addInfo(fav_item['title'],fav_item['infolabels'].get('item_url',''),  
                            fav_item['infolabels'].get('item_mode',''), fav_item['image_url'], 
                            fav_item['infolabels'].get('genre',''), fav_item['infolabels'].get('year',''))
                
        else:
                xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]Mash Up[/COLOR][/B],[B]You Have No Saved Favourites[/B],5000,"")")
        return
    
def ListglobalFavALL():
        getFavorites()
        main.GA("None","Grouped Fav's")
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

def ListglobalFavM25():
        getFavorites("Movie25 Fav's")
        main.GA("None","Movie25-Fav")
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        
def ListglobalFavIWO():
        getFavorites("iWatchOnline Fav's")
        main.GA("None","IWO-Fav")
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

def ListglobalFavT():
        getFavorites("TV Show Fav's")
        main.GA("None","TV-Fav")
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        
def ListglobalFavTE():
        getFavorites("TV Episode Fav's")
        main.GA("None","TVEPI-Fav")
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

def ListglobalFavM():
        getFavorites("Movie Fav's")
        main.GA("None","Movie-Fav")
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

def ListglobalFavMs():
        getFavorites("Misc. Fav's")
        main.GA("None","Misc-Fav")
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')

def ListglobalFavL():
        getFavorites("Live Fav's")
        main.GA("None","Live-Fav")
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    
################################################################################ Histroy ##########################################################################################################

def History():
    main.GA("None","WatchHistory")
    from universal import watchhistory
    wh = watchhistory.WatchHistory(addon_id)
    if selfAddon.getSetting("whistory") == "true":
        history_items = wh.get_my_watch_history()
        for item in history_items:
                item_title = item['title']
                item_url = item['url']
                item_image = item['image_url']
                item_fanart = item['fanart_url']
                item_infolabels = item['infolabels']
                item_isfolder = item['isfolder']
                if item_image =='':
                    item_image= art+'/noimage.png'
                item_title=item_title.replace('[COLOR green]','[COLOR=FF67cc33]')
                main.addLink(item_title,item_url,item_image)
    else:
        dialog = xbmcgui.Dialog()
        ok=dialog.ok('[B]Mash Up History[/B]', 'Watch history is disabled' ,'To enable go to addon settings','and enable Watch History')
        history_items = wh.get_my_watch_history()
        for item in history_items:
                item_title = item['title']
                item_url = item['url']
                item_image = item['image_url']
                item_fanart = item['fanart_url']
                item_infolabels = item['infolabels']
                item_isfolder = item['isfolder']
                item_title=item_title.replace('[COLOR green]','[COLOR=FF67cc33]')
                main.addLink(item_title,item_url,item_image)
    
        


    
################################################################################ Message ##########################################################################################################

def Message():
    help = SHOWMessage()
    help.doModal()
    main.GA("None","Mash2k3Info")
    del help


class SHOWMessage(xbmcgui.Window):
    def __init__(self):
        self.addControl(xbmcgui.ControlImage(0,0,1280,720,art+'/infoposter.png'))
    def onAction(self, action):
        if action == 92 or action == 10:
            xbmc.Player().stop()
            self.close()

def TextBoxes(heading,anounce):
        class TextBox():
            """Thanks to BSTRDMKR for this code:)"""
                # constants
            WINDOW = 10147
            CONTROL_LABEL = 1
            CONTROL_TEXTBOX = 5

            def __init__( self, *args, **kwargs):
                # activate the text viewer window
                xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
                # get window
                self.win = xbmcgui.Window( self.WINDOW )
                # give window time to initialize
                xbmc.sleep( 500 )
                self.setControls()


            def setControls( self ):
                # set heading
                self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
                try:
                        f = open(anounce)
                        text = f.read()
                except:
                        text=anounce
                self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
                return
        TextBox()
################################################################################ Modes ##########################################################################################################


def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
              
params=get_params()

url=None
name=None
mode=None
iconimage=None
fanart=None
plot=None
genre=None
title=None
season=None
episode=None
location=None
path=None


try:
        name=urllib.unquote_plus(params["name"])
except:
        pass

try:
        
        url=urllib.unquote_plus(params["url"])
        
except:
        pass

try:
        mode=int(params["mode"])
except:
        pass

try:
        iconimage=urllib.unquote_plus(params["iconimage"])
        iconimage = iconimage.replace(' ','%20')
except:
        pass
try:
        plot=urllib.unquote_plus(params["plot"])
except:
        pass
try:
        fanart=urllib.unquote_plus(params["fanart"])
        fanart = fanart.replace(' ','%20')
except:
        pass

try:
        genre=urllib.unquote_plus(params["genre"])
except:
        pass

try:
        title=urllib.unquote_plus(params["title"])
except:
        pass
try:
        episode=int(params["episode"])
except:
        pass
try:
        season=int(params["season"])
except:
        pass
try:
        location=urllib.unquote_plus(params["location"])
except:
        pass
try:
        path=urllib.unquote_plus(params["path"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Thumb: "+str(iconimage)

if mode==None or url==None or len(url)<1:
        if ENV is 'Prod':
            threading.Thread(target=CheckForAutoUpdate).start()
            threading.Thread(target=ShowAds).start()
        else:
            threading.Thread(target=CheckForAutoUpdateDev).start()
        threading.Thread(target=Notify).start()
        MAIN()
        threading.Thread(target=Announcements).start()
        main.VIEWSB()        
       
elif mode==1:
        from resources.libs import movie25
        movie25.LISTMOVIES(url)
        
elif mode==2:
        print ""+url
        GENRE(url)

elif mode==4:
        from resources.libs import movie25
        print ""+url
        movie25.SEARCH(url)
        
elif mode==420:
        from resources.libs import movie25
        print ""+url
        movie25.Searchhistory()

elif mode==3:
        from resources.libs import movie25
        print ""+url
        movie25.VIDEOLINKS(name,url)

elif mode==5:
        from resources.libs import movie25
        print ""+url
        movie25.PLAY(name,url)

elif mode==171:
        from resources.libs import movie25
        print ""+url
        movie25.PLAYB(name,url)
elif mode==6:
        AtoZ()

elif mode==7:
        YEAR()

elif mode==23:
        from resources.libs import movie25
        movie25.ENTYEAR()
        
elif mode==8:
        from resources.libs import movie25
        print ""+url
        movie25.YEARB(url)

elif mode==9:
        from resources.libs import movie25
        print ""+url
        movie25.NEXTPAGE(url)
        
elif mode==10:
        from resources.libs import movie25
        ListglobalFavM25()

elif mode==11:
        from resources.libs import movie25
        print ""+url
        movie25.PUTLINKS(name,url)

elif mode==12:
        from resources.libs import movie25
        print ""+url
        movie25.OELINKS(name,url)

elif mode==13:
        from resources.libs import movie25
        print ""+url
        movie25.FNLINKS(name,url)

elif mode==14:
        from resources.libs import movie25
        print ""+url
        movie25.VIDLINKS(name,url)

elif mode==15:
        from resources.libs import movie25
        print ""+url
        movie25.FLALINKS(name,url)

elif mode==16:
        from resources.libs import movie25
        print ""+url
        movie25.NOVLINKS(name,url)

elif mode==17:
        from resources.libs import movie25
        print ""+url
        movie25.UPLINKS(name,url)

elif mode==18:
        from resources.libs import movie25
        print ""+url
        movie25.XVLINKS(name,url)

elif mode==19:
        from resources.libs import movie25
        print ""+url
        movie25.ZOOLINKS(name,url)

elif mode==20:
        from resources.libs import movie25
        print ""+url
        movie25.ZALINKS(name,url)

elif mode==21:
        from resources.libs import movie25
        print ""+url
        movie25.VIDXLINKS(name,url)

elif mode==22:
        from resources.libs import movie25
        print ""+url
        movie25.SOCKLINKS(name,url)

elif mode==24:
        from resources.libs import movie25
        print ""+url
        movie25.NOWLINKS(name,url)

elif mode==25:
    from resources.libs.movies_tv import oneclickwatch
    print ""+url
    oneclickwatch.LISTSP(url)

elif mode==26:
    from resources.libs.movies_tv import oneclickwatch
    print ""+url
    oneclickwatch.LINKSP(name,url)
        
elif mode==27:
        print ""+url
        TV()

elif mode==28:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.LISTTV(url)
        
elif mode==29:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.VIDEOLINKST(name,url)

elif mode==30:
    from resources.libs.movies_tv import movie1k
    print ""+url
    movie1k.LISTTV2(url)

elif mode==31:
    from resources.libs.movies_tv import movie1k
    print ""+url
    movie1k.VIDEOLINKST2(name,url,iconimage)
        
elif mode==32:
    from resources.libs.movies_tv import oneclickwatch
    print ""+url
    oneclickwatch.LISTTV3(url)

elif mode==33:
        print ""+url
        HD()

elif mode==34:
    from resources.libs.movies_tv import newmyvideolinks
    print ""+url
    newmyvideolinks.LISTSP2(url)

elif mode==35:
    from resources.libs.movies_tv import newmyvideolinks
    print ""+url
    newmyvideolinks.LINKSP2(name,url)

elif mode==36:
        print ""+url
        INT()

elif mode==37:
    from resources.libs.international import  einthusan
    print ""+url
    einthusan.LISTINT(name,url)

elif mode==38:
    from resources.libs.international import  einthusan
    print ""+url
    einthusan.LINKINT(name,url)

######39-42 available
        
elif mode==43:
        print ""+url
        SPORTS()

elif mode==44:
    from resources.libs.sports import espn
    print ""+url
    espn.ESPN()
        
elif mode==45:
    from resources.libs.sports import espn
    print ""+url
    espn.ESPNList(url)

elif mode==46:
    from resources.libs.sports import espn
    print ""+url
    espn.ESPNLink(name,url,iconimage,plot)

elif mode==47:
    from resources.libs import youtube
    print ""+url
    youtube.YOUList(name,url)
        
elif mode==48:
    from resources.libs import youtube
    print ""+url
    youtube.YOULink(name,url,iconimage)

elif mode==50:
    from resources.libs.sports import outdoorch
    print ""+url
    outdoorch.OC()
        
elif mode==51:
    from resources.libs.sports import outdoorch
    print ""+url
    outdoorch.OCList(url)

elif mode==52:
    from resources.libs.sports import outdoorch
    print ""+url
    outdoorch.OCLink(name,url,iconimage)

elif mode==53:
    from resources.libs.movies_tv import dailyflix
    print ""+url
    dailyflix.LISTSP3(url)

elif mode==54:
    from resources.libs.movies_tv import dailyflix
    print ""+url
    dailyflix.LINKSP3(name,url)

elif mode==55:
    from resources.libs.movies_tv import oneclickmoviez
    print ""+url
    oneclickmoviez.LISTSP4(url)

elif mode==56:
    from resources.libs.movies_tv import oneclickmoviez
    print ""+url
    oneclickmoviez.LINKSP4(name,url)

elif mode==57:
    from resources.libs.movies_tv import starplay
    print ""+url
    starplay.LISTSP5(url)

elif mode==58:
    from resources.libs.movies_tv import starplay
    print ""+url
    starplay.LINKSP5(name,url)
        
elif mode==59:
        print ""+url
        UFC()
        
elif mode==60:
        from resources.libs import movie25
        print ""+url
        movie25.UFCMOVIE25()

elif mode==61:
    from resources.libs.movies_tv import rlsmix
    print ""+url
    rlsmix.LISTTV4(url)

elif mode==62:
    from resources.libs.movies_tv import rlsmix
    print ""+url
    rlsmix.LINKTV4(name,url)

elif mode==63:
        print ""+url
        ADVENTURE()
        
elif mode==631:
    from resources.libs.adventure import discovery
    print ""+url
    discovery.DISC(url)

elif mode==64:
    from resources.libs.adventure import discovery
    print ""+url
    discovery.LISTDISC(name,url)

elif mode==65:
    from resources.libs.adventure import discovery
    print ""+url
    discovery.LINKDISC(name,url)

elif mode==66:
    from resources.libs.international import cinevip
    print ""+url
    cinevip.LISTINT3(url)

elif mode==67:
    from resources.libs.international import cinevip
    print ""+url
    cinevip.LINKINT3(name,url,iconimage)

elif mode==68:
        print ""+url
        useme(url)

elif mode==69:
        print ""+url
        useMe(name,url)

elif mode==70:
    from resources.libs.adventure import nationalgeo
    print ""+url
    nationalgeo.NG()

elif mode==71:
    from resources.libs.adventure import nationalgeo
    print ""+url
    nationalgeo.NGDir(url)

elif mode==72:
    from resources.libs.adventure import nationalgeo
    print ""+url
    nationalgeo.LISTNG(url)

elif mode==73:
    from resources.libs.adventure import nationalgeo
    print ""+url
    nationalgeo.LISTNG2(url)

elif mode==74:
    from resources.libs.adventure import nationalgeo
    print ""+url
    nationalgeo.LINKNG(name,url)

elif mode==75:
    from resources.libs.adventure import nationalgeo
    print ""+url
    nationalgeo.LINKNG2(name,url)

elif mode==76:
        print ""+url
        KIDZone(url)
        
elif mode==77:
    from resources.libs.kids import wbkids
    print ""+url
    wbkids.WB()
        
elif mode==78:
    from resources.libs.kids import wbkids
    print ""+url
    wbkids.LISTWB(url)

elif mode==79:
    from resources.libs.kids import wbkids
    print ""+url
    wbkids.LINKWB(name,url)

elif mode==80:
    from resources.libs.adventure import discovery
    print ""+url
    discovery.MILIT(url)
        
elif mode==81:
    from resources.libs.adventure import discovery
    print ""+url
    discovery.SCI(url)

elif mode==82:
    from resources.libs.adventure import discovery
    print ""+url
    discovery.VELO(url)

elif mode==83:
    from resources.libs.adventure import discovery
    print ""+url
    discovery.ANIP(url)

elif mode==84:
    from resources.libs import youtube
    print ""+url
    youtube.YOUKIDS()

elif mode==85:
        print ""+url
        DOCS()        

elif mode==86:
    from resources.libs.documentaries import documentary
    print ""+url
    documentary.LISTDOC(url)
        
elif mode==87:
    from resources.libs.documentaries import documentary
    print ""+url
    documentary.LISTDOC2(url)

elif mode==88:
    from resources.libs.documentaries import documentary
    print ""+url
    documentary.LINKDOC(name,url,iconimage)
        
elif mode==89:
    from resources.libs.documentaries import documentary
    print ""+url
    documentary.LISTDOCPOP(url)

elif mode==90:
    from resources.libs.adventure import airaces
    print ""+url
    airaces.LISTAA()

elif mode==91:
    from resources.libs.adventure import airaces
    print ""+url
    airaces.PLAYAA(name,url,iconimage)

elif mode==92:
    from resources.libs.sports import wildtv
    print ""+url
    wildtv.WILDTV(url)        

elif mode==93:
    from resources.libs.sports import wildtv
    print ""+url
    wildtv.LISTWT(url)
        
elif mode==94:
    from resources.libs.sports import wildtv
    print ""+url
    wildtv.LINKWT(name,url)

elif mode==95:
    from resources.libs.sports import tsn
    print ""+url
    tsn.TSNDIR()

elif mode==96:
    from resources.libs.sports import tsn
    print ""+url
    tsn.TSNDIRLIST(url)        

elif mode==97:
    from resources.libs.sports import tsn
    print ""+url
    tsn.TSNLIST(url)
        
elif mode==98:
    from resources.libs.sports import tsn
    print ""+url
    tsn.TSNLINK(name,url,iconimage)
        
elif mode==100:
        pop()
        
elif mode==101:
    from resources.libs.movies_tv import newmyvideolinks
    newmyvideolinks.SEARCHNEW(name,url)

elif mode==102:
    from resources.libs.movies_tv import newmyvideolinks
    newmyvideolinks.SearchhistoryNEW(url)
        
elif mode==103:
    from resources.libs.movies_tv import newmyvideolinks
    newmyvideolinks.UFCNEW()
        
elif mode==104:
    from resources.libs.documentaries import vice
    vice.Vice(url)
        
elif mode==105:
    from resources.libs.documentaries import vice
    vice.ViceList(url)

elif mode==106:
    from resources.libs.documentaries import vice
    vice.ViceLink(name,url,iconimage)        

elif mode==107:
    from resources.libs.kids import disneyjr
    disneyjr.DISJR()
        
elif mode==108:
    from resources.libs.kids import disneyjr
    disneyjr.DISJRList(url)

elif mode==109:
    from resources.libs.kids import disneyjr
    disneyjr.DISJRList2(url)
        
elif mode==110:
    from resources.libs.kids import disneyjr
    disneyjr.DISJRLink(name,url,iconimage)       
        
elif mode==111:
        StrikeFList(url)

elif mode==112:        
        StrikeFLink(name,url)   

elif mode==113:
    from resources.libs.sports import mmafighting
    mmafighting.MMAFList(url)

elif mode==114:
    from resources.libs.sports import mmafighting
    mmafighting.MMAFLink(name,url,iconimage)
    
elif mode==115:
        LiveStreams()
elif mode==116:
    from resources.libs.live import livestation
    livestation.LivestationList(url)
elif mode==117:
    from resources.libs.live import livestation
    livestation.LivestationLink(name,url,iconimage)
elif mode==118:
    from resources.libs.live import livestation
    livestation.LivestationLink2(name,url,iconimage)

elif mode==119:
    from resources.libs.live import ilive
    ilive.iLive()
    
elif mode==120:
    from resources.libs.live import ilive
    ilive.iLiveList(url)
    
elif mode==121:
    from resources.libs.live import ilive
    ilive.iLiveLink(name,url,iconimage)

elif mode==122:
    from resources.libs.live import castalba
    castalba.CastalbaList(url)
    
elif mode==123:
    from resources.libs.live import castalba
    castalba.CastalbaLink(name,url,iconimage)

elif mode==124:
    from resources.libs.sports import foxsoccer
    foxsoccer.FOXSOC()
    
elif mode==125:
    from resources.libs.sports import foxsoccer
    foxsoccer.FOXSOCList(url)
    
elif mode==126:
    from resources.libs.sports import foxsoccer
    foxsoccer.FOXSOCLink(name,url)

elif mode==127:
    from resources.libs.live import musicstreams
    musicstreams.MUSICSTREAMS()
    
elif mode==128:
        main.Clearhistory(url)

elif mode==129:
    from resources.libs.live import desistreams
    desistreams.DESISTREAMS()
    
elif mode==130:
    from resources.libs.live import desistreams
    desistreams.DESISTREAMSList(url)
    
elif mode==131:
    from resources.libs.live import desistreams
    desistreams.DESISTREAMSLink(name,url)
        
elif mode==132:
    from resources.libs.movies_tv import movie1k
    movie1k.SearchhistoryMovie1k()
    
elif mode==133:
    from resources.libs.movies_tv import movie1k
    movie1k.SEARCHMovie1k(url)
    
elif mode==134:
    from resources.libs.movies_tv import oneclickwatch
    oneclickwatch.PLAYOCW(name,url)

elif mode==135:
    from resources.libs.movies_tv import oneclickwatch
    oneclickwatch.VIDEOLINKST3(name,url)

elif mode==136:
    from resources.libs.movies_tv import rlsmix
    rlsmix.SearchhistoryRlsmix()

elif mode==137:
    from resources.libs.movies_tv import rlsmix
    rlsmix.SEARCHRlsmix(url)


elif mode==138:
    from resources.libs.live import naviplaylists
    naviplaylists.playlists()

elif mode==139:
    from resources.libs.live import naviplaylists
    naviplaylists.playlistList(name,url)

elif mode==140:
    from resources.libs.live import naviplaylists
    naviplaylists.playlistList2(name,url)

elif mode==141:
    from resources.libs.live import naviplaylists
    naviplaylists.playlistList3(name,url)

elif mode==142:
    from resources.libs.live import naviplaylists
    naviplaylists.playlistList4(name,url)

elif mode==149:
    from resources.libs.live import naviplaylists
    naviplaylists.playlistList5(name,url)
        
elif mode==158:
    from resources.libs.live import naviplaylists
    naviplaylists.playlistList6(name,url)

elif mode==168:
    from resources.libs.live import naviplaylists
    naviplaylists.playlistList7(name,url)

elif mode==143:
    from resources.libs.live import countries
    countries.COUNTRIES()

elif mode==144:
    from resources.libs.live import countries
    countries.COUNTRIESList(name,url)

elif mode==204:
    from resources.libs.live import countries
    countries.COUNTRIESLink(name,url,iconimage)


elif mode==145:
        from resources.libs import movie25
        print ""+url
        movie25.MOVSHLINKS(name,url)

elif mode==146:
        from resources.libs import movie25
        print ""+url
        movie25.DIVXSLINKS(name,url)

elif mode==147:
        from resources.libs import movie25
        print ""+url
        movie25.SSIXLINKS(name,url)

elif mode==148:
        from resources.libs import movie25
        print ""+url
        movie25.GORLINKS(name,url)

elif mode==150:
        from resources.libs import movie25
        print ""+url
        movie25.MOVPLINKS(name,url)

elif mode==151:
        from resources.libs import movie25
        print ""+url
        movie25.DACLINKS(name,url)

elif mode==152:
        from resources.libs import movie25
        print ""+url
        movie25.VWEEDLINKS(name,url)

elif mode==153:
        from resources.libs import movie25
        print ""+url
        movie25.MOVDLINKS(name,url)

elif mode==154:
        from resources.libs import movie25
        print ""+url
        movie25.MOVRLINKS(name,url)

elif mode==155:
        from resources.libs import movie25
        print ""+url
        movie25.BUPLOADSLINKS(name,url)

elif mode==156:
        print ""+url
        HubMain()

elif mode==157:
        from resources.libs import movie25
        print ""+url
        movie25.PLAYEDLINKS(name,url)

elif mode==159:
    from resources.libs.documentaries import watchdocumentary
    print ""+url
    watchdocumentary.WATCHDOC()

elif mode==160:
    from resources.libs.documentaries import watchdocumentary
    print ""+url
    watchdocumentary.WATCHDOCList(url)

elif mode==161:
    from resources.libs.documentaries import watchdocumentary
    print ""+url
    watchdocumentary.WATCHDOCLink(name,url,iconimage)

elif mode==162:
    from resources.libs.documentaries import watchdocumentary
    print ""+url
    watchdocumentary.CATEGORIES()

elif mode==163:
    from resources.libs.documentaries import watchdocumentary
    print ""+url
    watchdocumentary.WATCHDOCList2(url)

elif mode==164:
    from resources.libs.documentaries import watchdocumentary
    print ""+url
    watchdocumentary.WATCHDOCSearch()

elif mode==165:
    from resources.libs.plugins import globalbc
    print ""+url
    globalbc.GLOBALBC()

elif mode==166:
    from resources.libs.plugins import globalbc
    print ""+url
    globalbc.GLOBALBCList(url)

elif mode==167:
    from resources.libs.plugins import globalbc
    print ""+url
    globalbc.GLOBALBCLink(name,url)

elif mode==169:
    from resources.libs.plugins import globalbc
    print ""+url
    globalbc.GLOBALBCList2(url)

elif mode==170:
    from resources.libs.plugins import globalbc
    print ""+url
    globalbc.GLOBALBCSearch()

#171 taken



elif mode==172:
    from resources.libs.sports import skysports
    print ""+url
    skysports.SKYSPORTS()

elif mode==173:
    from resources.libs.sports import skysports
    print ""+url
    skysports.SKYSPORTSList(url)

elif mode==174:
    from resources.libs.sports import skysports
    print ""+url
    skysports.SKYSPORTSLink(name,url)

elif mode==175:
    from resources.libs.sports import skysports
    print ""+url
    skysports.SKYSPORTSTV(url)

elif mode==176:
    from resources.libs.sports import skysports
    print ""+url
    skysports.SKYSPORTSList2(url)
        
elif mode==177:
        dialog = xbmcgui.Dialog()
        dialog.ok("Mash Up", "Sorry this video requires a SkySports Suscription.","Will add this feature in later Version.","Enjoy the rest of the videos ;).")

elif mode==178:
    from resources.libs.sports import skysports
    print ""+url
    skysports.SKYSPORTSCAT()

elif mode==179:
    from resources.libs.sports import skysports
    print ""+url
    skysports.SKYSPORTSCAT2(url)

elif mode==180:
    from resources.libs.sports import skysports
    print ""+url
    skysports.SKYSPORTSTEAMS(url)

elif mode==181:
    from resources.libs.live import vipplaylist
    print ""+url
    vipplaylist.VIPplaylists(url)

elif mode==182:
    from resources.libs.live import vipplaylist
    print ""+url
    vipplaylist.VIPList(name,url)

elif mode==183:
    from resources.libs.live import vipplaylist
    print ""+url
    vipplaylist.VIPLink(name,url,iconimage)


elif mode==184:
    from resources.libs.live import musicstreams
    print ""+url
    musicstreams.MUSICSTREAMSLink(name,url,iconimage)


elif mode==185:
    from resources.libs.live import tubtub
    print ""+url
    tubtub.TubTubMAIN(url)

elif mode==186:
    from resources.libs.live import tubtub
    print ""+url
    tubtub.TubTubLink(name,url)

elif mode==187:
        print ""+url
        arabic.ArabicMAIN(url)

elif mode==188:
        print ""+url
        arabic.ArabicLink(name,url)

elif mode==189:
        print ""+url
        arabic.ArabicList(url)

elif mode==190:
        print ""+url
        main.Download_Source(name,url)


elif mode==191:
    from resources.libs.live import oneeightone
    print ""+url
    oneeightone.MAINFM()

elif mode==192:
    from resources.libs.live import oneeightone
    print ""+url
    oneeightone.LISTFM(name,url)

elif mode==193:
    from resources.libs.live import oneeightone
    print ""+url
    oneeightone.LINKFM(name,url)

elif mode==194:
        print ""+url
        WorkoutMenu()

elif mode==195:
    from resources.libs.sports import bodybuilding
    print ""+url
    bodybuilding.MAINBB()

elif mode==196:
    from resources.libs.sports import bodybuilding
    print ""+url
    bodybuilding.LISTBB(url)

elif mode==197:
    from resources.libs.sports import bodybuilding
    print ""+url
    bodybuilding.LINKBB(name,url,iconimage)

elif mode==198:
    from resources.libs.sports import fitnessblender
    print ""+url
    fitnessblender.MAINFB()

elif mode==199:
    from resources.libs.sports import fitnessblender
    print ""+url
    fitnessblender.BODYFB()

elif mode==200:
    from resources.libs.sports import fitnessblender
    print ""+url
    fitnessblender.DIFFFB()

elif mode==201:
    from resources.libs.sports import fitnessblender
    print ""+url
    fitnessblender.TRAINFB()

elif mode==202:
    from resources.libs.sports import fitnessblender
    print ""+url
    fitnessblender.LISTBF(url)

elif mode==203:
    from resources.libs.sports import fitnessblender
    print ""+url
    fitnessblender.LINKBB(name,url,iconimage)

elif mode==205:
    from resources.libs import youplaylist
    print ""+url
    youplaylist.YOUList(name,url)

elif mode==206:
    from resources.libs import youplaylist
    print ""+url
    youplaylist.YOULink(name,url,iconimage)

elif mode==207:
        from resources.libs import movie25
        print ""+url
        movie25.GotoPage(url)

elif mode==208:
        from resources.libs import movie25
        print ""+url
        movie25.GotoPageB(url)

elif mode==209:
    from resources.libs.movies_tv import newmyvideolinks
    print ""+url
    newmyvideolinks.LINKSP2B(name,url)
        
elif mode==210:
    from resources.libs.movies_tv import rlsmix
    print ""+url
    rlsmix.LINKTV4B(name,url)

elif mode==211:
    from resources.libs.movies_tv import oneclickmoviez
    print ""+url
    oneclickmoviez.LINKSP4B(name,url)

elif mode==212:
        print ""+url
        main.Download_SourceB(name,url)
        
elif mode == 213 or mode == 214:
        if xbmc.Player().isPlayingAudio():
                info   = xbmc.Player().getMusicInfoTag()
                artist = info.getTitle().split(' - ')[0]
                track  = info.getTitle()
                track  = track.split(' (')[0]
                print track
                artist=artist.replace('f/','ft ')
                cmd = '%s?mode=%s&name=%s&artist=%s' % ('plugin://plugin.audio.xbmchubmusic/', str(mode), track, artist)
                xbmc.executebuiltin('XBMC.Container.Update(%s)' % cmd)



elif mode==217:
    from resources.libs.sports import golfchannel
    golfchannel.MAIN()
        
elif mode==218:
    from resources.libs.sports import golfchannel
    print ""+url
    golfchannel.LIST(url)

elif mode==219:
    from resources.libs.sports import golfchannel
    print ""+url
    golfchannel.LIST2(name,url,iconimage,plot)


elif mode==220:
    from resources.libs.sports import golfchannel
    print ""+url
    golfchannel.LINK(name,url,iconimage)

elif mode==221:
    from resources.libs.sports import golfchannel
    print ""+url
    golfchannel.LIST3(url)


elif mode==222:
        print ""+url
        History()

elif mode==223:
        print ""+url
        ThreeDsec()


elif mode==226:
    from resources.libs.documentaries import documentarywire
    documentarywire.MAIN()
        
elif mode==227:
    from resources.libs.documentaries import documentarywire
    print ""+url
    documentarywire.LIST(url)

elif mode==228:
    from resources.libs.documentaries import documentarywire
    print ""+url
    documentarywire.LINK(name,url,iconimage,plot)

elif mode==229:
    from resources.libs.documentaries import documentarywire
    print ""+url
    documentarywire.SEARCH(url)

elif mode==230:
    from resources.libs.documentaries import documentarywire
    print ""+url
    documentarywire.CATLIST(url)


elif mode==231:
    from resources.libs.live import hadynz
    print ""+url
    hadynz.MAIN()

elif mode==232:
    from resources.libs.live import hadynz
    print ""+url
    hadynz.LINK(name,url,iconimage)

elif mode==233:
        print ""+url
        


elif mode==234:
        print ""+url
        PlaylistDir()


elif mode==235:
    from resources.libs.movies_tv import movieplaylist
    print ""+url
    movieplaylist.Mplaylists(url)

elif mode==236:
    from resources.libs.movies_tv import movieplaylist
    print ""+url
    movieplaylist.MList(name,url)

elif mode==237:
    from resources.libs.movies_tv import movieplaylist
    print ""+url
    movieplaylist.MLink(name,url,iconimage)


elif mode==238:
    from resources.libs.live import customchannel
    print ""+url
    customchannel.MAIN()

elif mode==239:
    from resources.libs.live import customchannel
    print ""+url
    customchannel.LIST(name,url)

elif mode==240:
    from resources.libs.live import customchannel
    print ""+url
    customchannel.LINK(name,url,iconimage)

elif mode==241:
    from resources.libs import downloadedcontent
    print ""+url
    downloadedcontent.LIST()

elif mode==242:
    from resources.libs import downloadedcontent
    print ""+url
    downloadedcontent.LINK(name,url)

elif mode==243:
    from resources.libs import downloadedcontent
    print ""+url
    downloadedcontent.REMOVE(name,url)

elif mode==244:
        popVIP(url)


elif mode==245:
    from resources.libs.movies_tv import multilinkplaylist
    print ""+url
    multilinkplaylist.Mplaylists(url)

elif mode==246:
    from resources.libs.movies_tv import multilinkplaylist
    print ""+url
    multilinkplaylist.MList(name,url)

elif mode==247:
    from resources.libs.movies_tv import multilinkplaylist
    print ""+url
    multilinkplaylist.MLink(name,url,iconimage)

elif mode==248:
    from resources.libs.live import customchannel
    customchannel.XmlIns()

elif mode==249:
    from resources.libs.movies_tv import movieplaylist
    movieplaylist.subLink(name,url)

elif mode==250:
    from resources.libs.live import customchannel
    customchannel.addPlaylist(url)

elif mode==251:
    from resources.libs.live import customchannel
    customchannel.removePlaylist(name,url,iconimage)

elif mode==252:
    from resources.libs.live import customchannel
    customchannel.addFolder(url)

elif mode==253:
    from resources.libs.live import customchannel
    customchannel.openFolder(name,url)

elif mode==254:
    from resources.libs.live import customchannel
    customchannel.removeFolder(name,url)

elif mode==255:
    from resources.libs.live import customchannel
    customchannel.editPlaylist(name,url,iconimage)

elif mode==256:
    from resources.libs.live import customchannel
    customchannel.editFolder(name,url)

elif mode==257:
    from resources.libs.live import customchannel
    customchannel.listLS(name,url,fanart)

elif mode==259:
    from resources.libs.movies_tv import movieplaylist
    print ""+url
    movieplaylist.MLink2(name,url,iconimage)

elif mode==260:
    from resources.libs.movies_tv import viplus
    viplus.VIP(url)

elif mode==261:
    from resources.libs.movies_tv import viplus
    viplus.VIPList(url)

elif mode==262:
    from resources.libs.movies_tv import viplus
    viplus.subLink(name,url)

elif mode==263:
    from resources.libs.movies_tv import viplus
    viplus.MLink(name,url,iconimage)


elif mode==264:
    HTVList(url)

elif mode==265:
    ANIME()

elif mode==266:
    from resources.libs.live import customchannel
    print ""+url
    customchannel.subLink(name,url)

elif mode==267:
    Movie25()

elif mode==268:
    from resources.libs.plugins import dramania
    print ""+url
    dramania.MAIN()

elif mode==269:
    from resources.libs.plugins import dramania
    print ""+url
    dramania.MOVIES()

elif mode==270:
    from resources.libs.plugins import dramania
    print ""+url
    dramania.LISTMOVIES(url)

elif mode==271:
    from resources.libs.plugins import dramania
    print ""+url
    dramania.LISTHOSTS(name,url,iconimage)

elif mode==272:
    from resources.libs.plugins import dramania
    print ""+url
    dramania.PLAY(name,url,iconimage)

elif mode==273:
    from resources.libs.plugins import dramania
    print ""+url
    dramania.DRAMAS()

elif mode==274:
    from resources.libs.plugins import dramania
    print ""+url
    dramania.LISTDRAMAS(url)

elif mode==275:
    from resources.libs.plugins import dramania
    print ""+url
    dramania.LISTEPISODES(name,url,iconimage)

######################################################################################################
        ######################################################################################
        ######################################################################################
        ######################################################################################

        
elif mode==500:
        TVAll()        

elif mode==530:
    from resources.libs.plugins import extramina
    extramina.MAINEXTRA()

elif mode==531:
    from resources.libs.plugins import extramina
    print ""+url
    extramina.LISTEXgenre(url)

elif mode==532:
    from resources.libs.plugins import extramina
    print ""+url
    extramina.LISTEXrecent(url)


elif mode==533:
    from resources.libs.plugins import extramina
    print ""+url
    extramina.GENREEXTRA(url)

elif mode==534:
    from resources.libs.plugins import extramina
    print ""+url
    extramina.SEARCHEXTRA(url)
        
elif mode==535:
    from resources.libs.plugins import extramina
    print ""+url
    extramina.SearchhistoryEXTRA()

elif mode==536:
    from resources.libs.plugins import extramina
    print ""+url
    extramina.VIDEOLINKSEXTRA(name,url,iconimage,plot)
                
elif mode==538:
    from resources.libs.plugins import extramina
    print ""+url
    extramina.AtoZEXTRA()

elif mode==537:
        print ""+url
        MMA()        

elif mode==539:
    from resources.libs.plugins import sceper
    sceper.MAINSCEPER()
        
elif mode==540:
    from resources.libs.plugins import sceper
    sceper.MORTSCEPER(url)

elif mode==541:
    from resources.libs.plugins import sceper
    print ""+url
    sceper.LISTSCEPER(name,url)
        
elif mode==545:
    from resources.libs.plugins import sceper
    print ""+url
    sceper.LISTSCEPER2(name,url)

elif mode==542:
    from resources.libs.plugins import sceper
    print ""+url
    sceper.SEARCHSCEPER(url)
        
elif mode==543:
    from resources.libs.plugins import sceper
    print ""+url
    sceper.SearchhistorySCEPER()

elif mode==544:
    from resources.libs.plugins import sceper
    print ""+url
    sceper.VIDEOLINKSSCEPER(name,url,iconimage)

elif mode==546:
    from resources.libs.movies_tv import backuptv
    print ""+url
    backuptv.CHANNELCList(url)

elif mode==547:
    from resources.libs.movies_tv import backuptv
    print ""+url
    backuptv.CHANNELCLink(name,url)

elif mode==548:
    from resources.libs.movies_tv import newmyvideolinks
    print ""+url
    newmyvideolinks.LISTEtowns(url)

elif mode==549:
    from resources.libs.movies_tv import newmyvideolinks
    newmyvideolinks.SEARCHEtowns(url)

elif mode==550:
    from resources.libs.movies_tv import newmyvideolinks
    newmyvideolinks.SearchhistoryEtowns(url)


        

elif mode==567:
    from resources.libs.plugins import fma
    print ""+url
    fma.MAINFMA()

elif mode==568:
    from resources.libs.plugins import fma
    print ""+url
    fma.LISTFMA(url)
        
elif mode==569:
    from resources.libs.plugins import fma
    print ""+url
    fma.LINKFMA(name,url,iconimage,plot)
        
elif mode==570:
    from resources.libs.plugins import fma
    print ""+url
    fma.AtoZFMA()
        
elif mode==571:
    from resources.libs.plugins import fma
    print ""+url
    fma.GENREFMA(url)

elif mode==646:
    from resources.libs.plugins import fma
    print ""+url
    fma.SearchhistoryM()
        
elif mode==647:
    from resources.libs.plugins import fma
    print ""+url
    fma.SEARCHM(url)

elif mode==572:
    from resources.libs.plugins import watchseries
    print ""+url
    watchseries.MAINWATCHS()

elif mode==573:
    from resources.libs.plugins import watchseries
    print ""+url
    watchseries.LISTWATCHS(url)

elif mode==574:
    from resources.libs.plugins import watchseries
    print ""+url
    watchseries.LINKWATCHS(name,url)

elif mode==575:
    from resources.libs.plugins import watchseries
    print ""+url
    watchseries.LISTHOST(name,url)

elif mode==576:
    from resources.libs.plugins import watchseries
    print ""+url
    watchseries.LISTSHOWWATCHS(url)

elif mode==577:
    from resources.libs.plugins import watchseries
    print ""+url
    watchseries.AtoZWATCHS()
        
elif mode==578:
    from resources.libs.plugins import watchseries
    print ""+url
    watchseries.LISTWATCHSEASON(name, url)

elif mode==579:
    from resources.libs.plugins import watchseries
    print ""+url
    watchseries.LISTWATCHEPISODE(name, url)
        
elif mode==580:
    from resources.libs.plugins import watchseries
    print ""+url
    watchseries.POPULARWATCHS(url)

elif mode==581:
    from resources.libs.plugins import watchseries
    print ""+url
    watchseries.SearchhistoryWS()
        
elif mode==582:
    from resources.libs.plugins import watchseries
    print ""+url
    watchseries.SEARCHWS(url)

elif mode==583:
    from resources.libs.plugins import watchseries
    print ""+url
    watchseries.GENREWATCHS()

elif mode==584:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.iWatchMAIN()

elif mode==642:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.SearchhistoryTV()
        
elif mode==643:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.SEARCHTV(url)

elif mode==644:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.SearchhistoryM()
        
elif mode==645:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.SEARCHM(url)

elif mode==585:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.iWatchTV()

elif mode==586:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.iWatchMOVIES()

elif mode==587:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.iWatchLISTMOVIES(url)

elif mode==588:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.iWatchLINK(name,url)

elif mode==589:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.iWatchLISTSHOWS(url)

elif mode==590:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.iWatchSeason(name,url,iconimage)

elif mode==591:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.iWatchEpisode(name,url)

elif mode==592:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.iWatchToday(url)

elif mode==593:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.AtoZiWATCHtv()

elif mode==594:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.iWatchGenreTV()

elif mode==595:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.AtoZiWATCHm()

elif mode==596:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.iWatchGenreM()
      

elif mode==601:
    from resources.libs.plugins import seriesgate
    seriesgate.MAINSG()
        
elif mode==602:
    from resources.libs.plugins import seriesgate
    print ""+url
    seriesgate.LISTEpiSG(url)

elif mode==603:
    from resources.libs.plugins import seriesgate
    print ""+url
    seriesgate.LISTShowsSG(url)

elif mode==604:
    from resources.libs.plugins import seriesgate
    print ""+url
    seriesgate.LISTSeasonSG(name,url,iconimage)

elif mode==605:
    from resources.libs.plugins import seriesgate
    print ""+url
    seriesgate.LISTEpilistSG(name,url)

elif mode==606:
    from resources.libs.plugins import seriesgate
    print ""+url
    seriesgate.LISTPopSG(url)

elif mode==607:
    from resources.libs.plugins import seriesgate
    print ""+url
    seriesgate.GENRESG(url)

elif mode==608:
    from resources.libs.plugins import seriesgate
    print ""+url
    seriesgate.SEARCHSG(url)
        
elif mode==612:
    from resources.libs.plugins import seriesgate
    print ""+url
    seriesgate.SearchhistorySG()

elif mode==609:
    from resources.libs.plugins import seriesgate
    print ""+url
    seriesgate.VIDEOLINKSSG(name,url,iconimage)
       
elif mode==610:
    from resources.libs.plugins import seriesgate
    print ""+url
    seriesgate.AtoZSG()
        
elif mode==611:
    from resources.libs.plugins import seriesgate
    print ""+url
    seriesgate.AllShows(url)


elif mode==613:
    from resources.libs.plugins import dubzonline
    dubzonline.MAINdz()
        
elif mode==614:
    from resources.libs.plugins import dubzonline
    print ""+url
    dubzonline.AtoZdz()

elif mode==615:
    from resources.libs.plugins import dubzonline
    print ""+url
    dubzonline.AZLIST(name,url)

elif mode==616:
    from resources.libs.plugins import dubzonline
    print ""+url
    dubzonline.EPILIST(url)

elif mode==617:
    from resources.libs.plugins import dubzonline
    print ""+url
    dubzonline.LINK(name,url)

elif mode==618:
    from resources.libs.plugins import dubzonline
    print ""+url
    dubzonline.latestLIST(url)


elif mode==619:
    from resources.libs.plugins import sominaltvfilms
    sominaltvfilms.MAIN()
        
elif mode==620:
    from resources.libs.plugins import sominaltvfilms
    print ""+url
    sominaltvfilms.LIST(name,url)

elif mode==621:
    from resources.libs.plugins import sominaltvfilms
    print ""+url
    sominaltvfilms.LINK(name,url,iconimage,fanart,plot)

elif mode==622:
    from resources.libs.plugins import sominaltvfilms
    print ""+url
    sominaltvfilms.LINK2(name,url,iconimage,plot)

elif mode==623:
    from resources.libs.plugins import sominaltvfilms
    print ""+url
    sominaltvfilms.AtoZ(url)
        
elif mode==624:
    from resources.libs.plugins import sominaltvfilms
    print ""+url
    sominaltvfilms.SEARCH()

elif mode==625:
    from resources.libs.plugins import animefreak
    animefreak.MAIN()
        
elif mode==626:
    from resources.libs.plugins import animefreak
    print ""+url
    animefreak.LIST(name,url)

elif mode==627:
    from resources.libs.plugins import animefreak
    print ""+url
    animefreak.LINK(name,url,iconimage,plot)

elif mode==628:
    from resources.libs.plugins import animefreak
    print ""+url
    animefreak.AtoZ()

elif mode==629:
    from resources.libs.plugins import animefreak
    print ""+url
    animefreak.AZLIST(name,url)

elif mode==630:
    from resources.libs.plugins import animefreak
    print ""+url
    animefreak.LIST2(name,url,iconimage,plot)
        
elif mode==632:
    from resources.libs.plugins import animefreak
    print ""+url
    animefreak.LATESTE(name,url)

elif mode==633:
    from resources.libs.plugins import animefreak
    print ""+url
    animefreak.LATESTA(name,url)

elif mode==634:
    from resources.libs.plugins import animefreak
    print ""+url
    animefreak.GENRE(url)
        
elif mode==635:
    from resources.libs.plugins import animefreak
    print ""+url
    animefreak.GENRELIST(url)

elif mode==636:
    from resources.libs.plugins import animefreak
    print ""+url
    animefreak.LATESTA(name,url)

elif mode==637:
    from resources.libs.plugins import animefreak
    print ""+url
    animefreak.LISTPOP(url)

elif mode==638:
    from resources.libs.plugins import animefreak
    print ""+url
    animefreak.SEARCH()

elif mode==639:
        print ""+url
        GlobalFav()

elif mode==640:
        print ""+url
        ListglobalFavT()

elif mode==641:
        print ""+url
        ListglobalFavM()

#642-47 taken

elif mode==648:
        print ""+url
        ListglobalFavL()

elif mode==649:
    from resources.libs.plugins import iwatchonline
    print ""+url
    iwatchonline.iWatchLINKB(name,url)
elif mode==650:
        print ""+url
        ListglobalFavMs()
elif mode==651:
        print ""+url
        ListglobalFavTE()
elif mode==652:
    from resources.libs.plugins import iwatchonline
    iwatchonline.iWatchYearM()
elif mode==653:
    from resources.libs.plugins import iwatchonline
    iwatchonline.ENTYEAR()
elif mode==654:
    from resources.libs.plugins import iwatchonline
    iwatchonline.GotoPage(url)

elif mode==655:
        print ""+url
        ListglobalFavIWO()
elif mode==656:
    print ""+url
    from resources.libs.movies_tv import scenelog
    scenelog.ListSceneLogLinks(name,url)
elif mode==657:
    print ""+url
    from resources.libs.movies_tv import scenelog
    scenelog.ListSceneLogItems(url,'HD')
elif mode==658:
    print ""+url
    from resources.libs.movies_tv import scenelog
    scenelog.PlaySceneLogLink(name,url)
elif mode==659:
    print ""+url
    from resources.libs.movies_tv import scenelog
    scenelog.StartSceneLogSearch(url)
elif mode==660:
    print ""+url
    from resources.libs.movies_tv import scenelog
    scenelog.SearchSceneLog(name,url)

elif mode == 776:
        main.jDownloader(url)        
elif mode == 777:
        main.ChangeWatched(iconimage, url, name, '', '')

elif mode == 778:
        main.refresh_movie(name,iconimage)
        
elif mode == 779:
        main.ChangeWatched(iconimage, url, name, season, episode)
elif mode == 780:
        main.episode_refresh(name, iconimage, season, episode)
elif mode == 781:
        main.trailer(url)
elif mode == 782:
        main.TRAILERSEARCH(url, name, iconimage)
elif mode == 783:
        main.SwitchUp()
elif mode == 784:
        print ""+url
        FIXES()
elif mode == 785:
        print ""+url
        FIXDOWN(name,url,location,path)
        
elif mode == 1000:
    from resources.libs.plugins import tvrelease
    tvrelease.MAINMENU()
elif mode == 1001:
    from resources.libs.plugins import tvrelease
    tvrelease.INDEX(url)
elif mode == 1002:
    from resources.libs.plugins import tvrelease
    tvrelease.GOTOP(url)
elif mode == 1003:
    from resources.libs.plugins import tvrelease
    tvrelease.LISTHOSTERS(name,url)
elif mode == 1004:
    urlresolver.display_settings()
elif mode == 1005:
    from resources.libs.plugins import tvrelease
    tvrelease.PLAYMEDIA(name,url)
elif mode == 1006:
    from resources.libs.plugins import tvrelease
    tvrelease.SEARCHhistory()

elif mode == 1008:
    from resources.libs.plugins import tvrelease
    tvrelease.SEARCH(url)
    
elif mode == 1007:
    from resources.libs.plugins import tvrelease
    tvrelease.TVPACKS(url)

elif mode == 1020:
    from resources.libs.plugins import tubeplus
    tubeplus.MAINMENU()
elif mode == 1021:
    from resources.libs.plugins import tubeplus
    tubeplus.TVMENU()
elif mode == 1022:
    from resources.libs.plugins import tubeplus
    tubeplus.MOVIE_MENU()
elif mode == 1023:
    from resources.libs.plugins import tubeplus
    tubeplus.TUBE_CHARTS(url)
elif mode == 1024:
    from resources.libs.plugins import tubeplus
    tubeplus.SEARCHhistory()
elif mode == 1025:
    from resources.libs.plugins import tubeplus
    tubeplus.SEARCH(url)
elif mode == 1026:
    from resources.libs.plugins import tubeplus
    tubeplus.LINK(name,url)
elif mode == 1027:
    from resources.libs.plugins import tubeplus
    tubeplus.VIDEOLINKS(name,url)
elif mode == 1028:
    from resources.libs.plugins import tubeplus
    tubeplus.GOTOP(url)    
elif mode == 1040:
    from resources.libs.plugins import tubeplus
    tubeplus.MOVIES_SPECIAL(url)
elif mode == 1041:
    from resources.libs.plugins import tubeplus
    tubeplus.LATEST_TV(url)
elif mode == 1042:
    from resources.libs.plugins import tubeplus
    tubeplus.LAST_AIRED(url)
elif mode == 1043:
    from resources.libs.plugins import tubeplus
    tubeplus.TV_TOP10(url)
elif mode == 1044:
    from resources.libs.plugins import tubeplus
    tubeplus.GENRES(url)
elif mode == 1045:
    from resources.libs.plugins import tubeplus
    tubeplus.POPGENRES(url)
elif mode == 1046:
    from resources.libs.plugins import tubeplus
    tubeplus.INDEXONE(url)
elif mode == 1047:
    from resources.libs.plugins import tubeplus
    tubeplus.MOVIEAZ(url)
elif mode == 1048:
    from resources.libs.plugins import tubeplus
    tubeplus.INDEX2(url)
elif mode == 1049:
    from resources.libs.plugins import tubeplus
    tubeplus.SEASONS(name,url,iconimage)
elif mode == 1050:
    from resources.libs.plugins import tubeplus
    tubeplus.EPISODES(name,url,plot)        
elif mode == 1051:
    from resources.libs.plugins import tubeplus
    tubeplus.INDEXtv(url)   
    
    
    
    
    
    
                    
                    
    
    
    
elif mode == 1998:
    if ENV is 'Prod':
        CheckForAutoUpdate(True)
    else:
        CheckForAutoUpdateDev(True)

elif mode == 1999:
    settings.openSettings()

elif mode == 2000:
    xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
    xbmc.executebuiltin("XBMC.ActivateWindow(Home)")        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
