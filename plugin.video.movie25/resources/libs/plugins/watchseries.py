# -*- coding: cp1252 -*-
import urllib,re,string,sys,os
import xbmc,xbmcgui,xbmcaddon,xbmcplugin
from resources.libs import main

#Mash Up - by Mash2k3 2012.

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art

def MAINWATCHS():
        main.addDir('Search','s',581,art+'/wfs/searchws.png')
        main.addDir('A-Z','s',577,art+'/wfs/azws.png')
        main.addDir('Yesterdays Episodes','http://watchseries.lt/tvschedule/-2',573,art+'/wfs/yesepi.png')
        main.addDir('Todays Episodes','http://watchseries.lt/tvschedule/-1',573,art+'/wfs/toepi2.png')
        main.addDir('Popular Shows','http://watchseries.lt/',580,art+'/wfs/popshowsws.png')
        main.addDir('This Weeks Popular Episodes','http://watchseries.lt/new',573,art+'/wfs/thisweek.png')
        main.addDir('Newest Episodes Added','http://watchseries.lt/latest',573,art+'/wfs/newadd.png')
        main.addDir('By Genre','genre',583,art+'/wfs/genrews.png')
        main.GA("Plugin","Watchseries")
        main.VIEWSB()

def POPULARWATCHS(murl):
        main.GA("Watchseries","PopularShows")
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<span style=".+?">.+?;</span><a href="([^<]+)" title="watch online (.+?)">.+?</a><br/>').findall(link)
        main.addLink('[COLOR red]Most Popular Series[/COLOR]','',art+'/link.png')
        for url, name in match[0:12]:
            main.addDirT(name,'http://watchseries.lt'+url,578,'','','','','','')
        main.addLink('[COLOR red]Most Popular Cartoons[/COLOR]','',art+'/link.png')
        for url, name in match[12:24]:
            main.addDirT(name,'http://watchseries.lt'+url,578,'','','','','','')
        main.addLink('[COLOR red]Most Popular Documentaries[/COLOR]','',art+'/link.png')
        for url, name in match[24:36]:
            main.addDirT(name,'http://watchseries.lt'+url,578,'','','','','','')
        main.addLink('[COLOR red]Most Popular Shows[/COLOR]','',art+'/link.png')
        for url, name in match[36:48]:
            main.addDirT(name,'http://watchseries.lt'+url,578,'','','','','','')
        main.addLink('[COLOR red]Most Popular Sports[/COLOR]','',art+'/link.png')
        for url, name in match[48:60]:
            main.addDirT(name,'http://watchseries.lt'+url,578,'','','','','','')

            
def GENREWATCHS():
        main.addDir('Action','http://watchseries.lt/genres/action',576,art+'/wfs/act.png')
        main.addDir('Adventure','http://watchseries.lt/genres/adventure',576,art+'/wfs/adv.png')
        main.addDir('Animation','http://watchseries.lt/genres/animation',576,art+'/wfs/ani.png')
        main.addDir('Comedy','http://watchseries.lt/genres/comedy',576,art+'/wfs/com.png')
        main.addDir('Crime','http://watchseries.lt/genres/crime',576,art+'/wfs/cri.png')
        main.addDir('Documentary','http://watchseries.lt/genres/documentary',576,art+'/wfs/doc.png')
        main.addDir('Drama','http://watchseries.lt/genres/drama',576,art+'/wfs/dra.png')
        main.addDir('Family','http://watchseries.lt/genres/family',576,art+'/wfs/fam.png')
        main.addDir('Fantasy','http://watchseries.lt/genres/fantasy',576,art+'/wfs/fan.png')
        main.addDir('History','http://watchseries.lt/genres/history',576,art+'/wfs/his.png')
        main.addDir('Horror','http://watchseries.lt/genres/horror',576,art+'/wfs/hor.png')
        main.addDir('Music','http://watchseries.lt/genres/music',576,art+'/wfs/mus.png')
        main.addDir('Mystery','http://watchseries.lt/genres/mystery',576,art+'/wfs/mys.png')
        main.addDir('Reality','http://watchseries.lt/genres/reality-tv',576,art+'/wfs/rea.png')
        main.addDir('Sci-Fi','http://watchseries.lt/genres/sci-fi',576,art+'/wfs/sci.png')
        main.addDir('Sport','http://watchseries.lt/genres/sport',576,art+'/wfs/spo.png')
        main.addDir('Talk Show','http://watchseries.lt/genres/talk-show',576,art+'/wfs/tals.png')
        main.addDir('Thriller','http://watchseries.lt/genres/thriller',576,art+'/wfs/thr.png')
        main.addDir('War','http://watchseries.lt/genres/war',576,art+'/wfs/war.png')
        main.GA("Watchseries","Genre")
        main.VIEWSB()

def AtoZWATCHS():
    main.addDir('0-9','http://watchseries.lt/letters/09',576,art+'/wfs/09.png')
    for i in string.ascii_uppercase:
            main.addDir(i,'http://watchseries.lt/letters/'+i.lower()+'/list-type/a_z',576,art+'/wfs/'+i+'.png')
    main.GA("Watchseries","A-Z")
    main.VIEWSB()

def LISTWATCHS(murl):
        main.GA("Watchseries","List")
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        match=re.compile('<a title=".+?" href="(.+?)">(.+?)</a>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for url, name in match:
            name=re.sub('\((\d+)x(\d+)\)','',name,re.I)
            episode = re.search('Seas(on)?\.? (\d+).*?Ep(isode)?\.? (\d+)',name, re.I)
            if(episode):
                e = str(episode.group(4))
                if(len(e)==1): e = "0" + e
                s = episode.group(2)
                if(len(s)==1): s = "0" + s
                name = re.sub('Seas(on)?\.? (\d+).*?Ep(isode)?\.? (\d+)','',name,re.I)
                name = name.strip() + " " + "S" + s + "E" + e
            main.addDirTE(name,'http://watchseries.lt'+url,575,'','','','','','')
            loadedLinks = loadedLinks + 1
            percent = (loadedLinks * 100)/totalLinks
            remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
            if (dialogWait.iscanceled()):
                return False   
        dialogWait.close()
        del dialogWait

def LISTSHOWWATCHS(murl):
        main.GA("Watchseries","List")
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        match=re.compile('<a title="(.+?)" href="(.+?)">.+?<span class="epnum">(.+?)</span></a>').findall(link)
        for name, url, year in match:
            main.addDirT(name,'http://watchseries.lt'+url,578,'','','','','','')

def LISTWATCHSEASON(mname, murl):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        thumb=art+'/folder.png'
        match=re.compile('<a class="null" href="(.+?)">(.+?)</a>').findall(link)
        for url, name in reversed(match):
            main.addDir(mname+' [COLOR red]'+name+'[/COLOR]','http://watchseries.lt'+url,579,thumb)


def LISTWATCHEPISODE(mname, murl):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace("&nbsp;&nbsp;&nbsp;"," ")
        match=re.compile('<a href="([^<]+)"><span class="" >([^<]+)</span>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        season = re.search('Seas(on)?\.? (\d+)',main.removeColorTags(mname),re.I)
        for url, episode in reversed(match):
            name = mname
            epi= re.search('Ep(isode)?\.? (\d+)(.*)',episode, re.I)
            if(epi):
                e = str(epi.group(2))
                if(len(e)==1): e = "0" + e
                if(season):
                    s = season.group(2)
                    if(len(s)==1): s = "0" + s
                    name = main.removeColoredText(mname).strip()
                    name = name + " " + "S" + s + "E" + e
                    episode = epi.group(3).strip()
            main.addDirTE(name + ' [COLOR red]'+str(episode)+'[/COLOR]','http://watchseries.lt'+url,575,'','','','','','')
            loadedLinks = loadedLinks + 1
            percent = (loadedLinks * 100)/totalLinks
            remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
            if (dialogWait.iscanceled()):
                return False   
        dialogWait.close()
        del dialogWait
        if selfAddon.getSetting('auto-view') == 'true':
                xbmc.executebuiltin("Container.SetViewMode(%s)" % selfAddon.getSetting('episodes-view'))

def SearchhistoryWS():
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTv')
        if not os.path.exists(SeaFile):
            url='ws'
            SEARCHWS(url)
        else:
            main.addDir('Search','ws',582,art+'/search.png')
            main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
            thumb=art+'/link.png'
            searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
            for seahis in reversed(searchis):
                    url=seahis
                    seahis=seahis.replace('%20',' ')
                    main.addDir(seahis,url,582,thumb)
            
            


def SEARCHWS(murl):
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTv')
        try:
            os.makedirs(seapath)
        except:
            pass
        if murl == 'ws':
            keyb = xbmc.Keyboard('', 'Search For Shows or Episodes')
            keyb.doModal()
            if (keyb.isConfirmed()):
                    search = keyb.getText()
                    encode=urllib.quote(search)
                    surl='http://watchseries.lt/search/'+encode
                    if not os.path.exists(SeaFile) and encode != '':
                        open(SeaFile,'w').write('search="%s",'%encode)
                    else:
                        if encode != '':
                            open(SeaFile,'a').write('search="%s",'%encode)
                    searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
                    for seahis in reversed(searchis):
                        continue
                    if len(searchis)>=10:
                        searchis.remove(searchis[0])
                        os.remove(SeaFile)
                        for seahis in searchis:
                            try:
                                open(SeaFile,'a').write('search="%s",'%seahis)
                            except:
                                pass


        else:
            encode = murl
            surl='http://watchseries.lt/search/'+encode
        link=main.OPENURL(surl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        match=re.compile('</a></td><td valign=".+?">    <a title="watch serie (.+?)" href="(.+?)">').findall(link)
        for name,url in match:
                main.addDirT(name,'http://watchseries.lt'+url,578,'','','','','','')
        main.GA("Watchseries","Search")


def LISTHOST(name,murl):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        if selfAddon.getSetting("hide-download-instructions") != "true":
            main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
        putlocker=re.compile('<span>putlocker.com</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(putlocker) > 0:
            for url in putlocker:
                main.addDown2(name+"[COLOR blue] : Putlocker[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/putlocker.png',art+'/hosts/putlocker.png')
        sockshare=re.compile('<span>sockshare.com</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(sockshare) > 0:
            for url in sockshare:
                main.addDown2(name+"[COLOR blue] : Sockshare[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/sockshare.png',art+'/hosts/sockshare.png')
        nowvideo=re.compile('<span>nowvideo.co</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(nowvideo) > 0:
            for url in nowvideo:
                main.addDown2(name+"[COLOR blue] : Nowvideo[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/nowvideo.png',art+'/hosts/nowvideo.png')
        oeupload=re.compile('<span>180upload.com/span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(oeupload) > 0:
            for url in oeupload:
                main.addDown2(name+"[COLOR blue] : 180upload[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/180upload.png',art+'/hosts/180upload.png')
        filenuke=re.compile('<span>filenuke.com</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(filenuke) > 0:
            for url in filenuke:
                main.addDown2(name+"[COLOR blue] : Filenuke[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/filenuke.png',art+'/hosts/filenuke.png')
        flashx=re.compile('<span>flashx.tv</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(flashx) > 0:
            for url in flashx:
                main.addDown2(name+"[COLOR blue] : Flashx[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/flashx.png',art+'/hosts/flashx.png')
        novamov=re.compile('<span>novamov.com</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(novamov) > 0:
            for url in novamov:
                main.addDown2(name+"[COLOR blue] : Novamov[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/novamov.png',art+'/hosts/novamov.png')
        uploadc=re.compile('<span>uploadc.com</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(uploadc) > 0:
            for url in uploadc:
                main.addDown2(name+"[COLOR blue] : Uploadc[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/uploadc.png',art+'/hosts/uploadc.png')
        xvidstage=re.compile('<span>xvidstage.com</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(xvidstage) > 0:
            for url in xvidstage:
                main.addDown2(name+"[COLOR blue] : Xvidstage[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/xvidstage.png',art+'/hosts/xvidstage.png')
        stagevu=re.compile('<span>stagevu.com</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(stagevu) > 0:
            for url in stagevu:
                main.addDown2(name+"[COLOR blue] : StageVu[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/stagevu.png',art+'/hosts/stagevu.png')        
        gorillavid=re.compile('<span>gorillavid.in</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(gorillavid)==0:
                gorillavid=re.compile('<span>gorillavid.com</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(gorillavid) > 0:
            for url in gorillavid:
                main.addDown2(name+"[COLOR blue] : Gorillavid[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/gorillavid.png',art+'/hosts/gorillavid.png')
        divxstage=re.compile('<span>divxstage.eu</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(divxstage) > 0:
            for url in divxstage:
                main.addDown2(name+"[COLOR blue] : Divxstage[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/divxstage.png',art+'/hosts/divxstage.png')
        moveshare=re.compile('<span>moveshare.net</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(moveshare) > 0:
            for url in moveshare:
                main.addDown2(name+"[COLOR blue] : Moveshare[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/moveshare.png',art+'/hosts/moveshare.png')
        sharesix=re.compile('<span>sharesix.com</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(sharesix) > 0:
            for url in sharesix:
                main.addDown2(name+"[COLOR blue] : Sharesix[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/sharesix.png',art+'/hosts/sharesix.png')
        movpod=re.compile('<span>movpod.in</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(movpod)==0:
                movpod=re.compile('<span>movpod.net</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(movpod) > 0:
            for url in movpod:
                main.addDown2(name+"[COLOR blue] : Movpod[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/movpod.png',art+'/hosts/movpod.png')
        daclips=re.compile('<span>daclips.in</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(daclips)==0:
                daclips=re.compile('<span>daclips.com</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(daclips) > 0:
            for url in daclips:
                main.addDown2(name+"[COLOR blue] : Daclips[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/daclips.png',art+'/hosts/daclips.png')
        videoweed=re.compile('<span>videoweed.es</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(videoweed) > 0:
            for url in videoweed:
                main.addDown2(name+"[COLOR blue] : Videoweed[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/videoweed.png',art+'/hosts/videoweed.png')        
        zooupload=re.compile('<span>zooupload.com</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(zooupload) > 0:
            for url in zooupload:
                main.addDown2(name+"[COLOR blue] : Zooupload[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/zooupload.png',art+'/hosts/zooupload.png')
        zalaa=re.compile('<span>zalaa.com</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(zalaa) > 0:
            for url in zalaa:
                main.addDown2(name+"[COLOR blue] : Zalaa[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/zalaa.png',art+'/hosts/zalaa.png')
        vidxden=re.compile('<span>vidxden.com</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(vidxden) > 0:
            for url in vidxden:
                main.addDown2(name+"[COLOR blue] : Vidxden[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/vidxden.png',art+'/hosts/vidxden.png')
        vidbux=re.compile('<span>vidbux.com</span></td><td> <a target=".+?" href="(.+?)"').findall(link)
        if len(vidbux) > 0:
            for url in vidbux:
                main.addDown2(name+"[COLOR blue] : Vidbux[/COLOR]",url+'xocx'+murl+'xocx',574,art+'/hosts/vidbux.png',art+'/hosts/vidbux.png')

def geturl(murl):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        match=re.compile('<a class="myButton" href="(.+?)">Click Here to Play</a>').findall(link)
        if len(match)==0:
                match=re.compile('<a class="myButton" href="(.+?)">Click Here to Play Part1</a><a class="myButton" href="(.+?)">Click Here to Play Part2</a>').findall(link)
                return match[0]
        else:
                return match[0]

def LINKWATCHS(mname,murl):
        main.GA("Watchseries","Watched")
        ok=True
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        match=re.compile('(.+?)xocx(.+?)xocx').findall(murl)
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Checking Link,3000)")
        for hurl, durl in match:
                furl=geturl('http://watchseries.lt'+hurl)
        link=main.OPENURL(durl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match2=re.compile('<h1 class=".+?"><a href=".+?">.+?</a> - <a href="(.+?)" title=".+?">.+?</a>').findall(link)
        for xurl in match2:
                link2=main.OPENURL('http://watchseries.lt'+xurl)
                link2=link2.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        descr=re.compile('<b>Description :</b>(.+?)<').findall(link2)
        if len(descr)>0:
                desc=descr[0]
        else:
                desc=''
        thumbs=re.compile('<td style=".+?"><a href=".+?"><img src="(.+?)"').findall(link2)
        if len(thumbs)>0:
                thumb=thumbs[0]
        else:
                thumb=''
        genres=re.compile('<b>Genre: <a href=.+?>(.+?)</a>').findall(link2)
        if len(genres)>0:
                genre=genres[0]
        else:
                genre=''
        infoLabels =main.GETMETAEpiT(mname,thumb,desc)
        video_type='episode'
        season=infoLabels['season']
        episode=infoLabels['episode']
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        try:
                xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
                stream_url = main.resolve_url(furl)

                infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                # play with bookmark
                from universal import playbackengine
                player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                #WatchHistory
                if selfAddon.getSetting("whistory") == "true":
                    from universal import watchhistory
                    wh = watchhistory.WatchHistory('plugin.video.movie25')
                    wh.add_item(mname+' '+'[COLOR green]WatchSeries[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
                player.KeepAlive()
                return ok
        except Exception, e:
                if stream_url != False:
                        main.ErrorReport(e)
                return ok
