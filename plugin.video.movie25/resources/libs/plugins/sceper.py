import urllib,urllib2,re,cookielib,string, urlparse,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,urlresolver
from t0mm0.common.net import Net as net
from resources.libs import main

#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
from universal import playbackengine, watchhistory
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art
wh = watchhistory.WatchHistory('plugin.video.movie25')

def MAINSCEPER():
        main.GA("Plugin","Sceper")
        main.addDir('Search Movies & TV Shows','s',543,art+'/search.png')
        main.addDir('Movies','movies',540,art+'/wfs/sceperm.png')
        main.addDir('Tv Shows','tvshows',540,art+'/wfs/scepert.png')
        main.VIEWSB2()
def MORTSCEPER(murl):
        if murl=='movies':
            main.GA("Sceper","Movies")
            main.addDir('All Movies','http://sceper.ws/home/category/movies',541,art+'/wfs/sceperm.png')
            main.addDir('Cartoons','http://sceper.ws/home/category/movies/cartoons',541,art+'/wfs/sceperm.png')
            main.addDir('Foreign Movies','http://sceper.ws/home/category/movies/movies-foreign',541,art+'/wfs/sceperm.png')
            main.addDir('HDTV 720p Movies','http://sceper.ws/home/category/movies/movies-hdtv-720p',541,art+'/wfs/sceperm.png')
            main.addDir('BluRay Rip Movies (BDRC,BDRip,BRRip)','http://sceper.ws/home/category/movies/movies-bluray-rip',541,art+'/wfs/sceperm.png')
            main.addDir('HDDVD Rip Movies','http://sceper.ws/home/category/movies/movies-hddvd-rip',541,art+'/wfs/sceperm.png')
            main.addDir('DVD Rip Movies','http://sceper.ws/home/category/movies/movies-dvd-rip',541,art+'/wfs/sceperm.png')
            main.addDir('DVD Screener Movies','http://sceper.ws/home/category/movies/movies-screener/movies-screener-dvd',531,art+'/wfs/sceperm.png')
            main.addDir('R5 Movies','http://sceper.ws/home/category/movies/movies-r5',541,art+'/wfs/sceperm.png')
        elif murl=='tvshows':
            main.GA("Sceper","Tv")
            main.addDir('All TV Shows','http://sceper.ws/home/category/tv-shows',545,art+'/wfs/scepert.png')
            main.addDir('Anime/Cartoon TV Shows','http://sceper.ws/home/category/tv-shows/animes',545,art+'/wfs/scepert.png')
            main.addDir('HDTV 720p TV Shows','http://sceper.ws/home/category/tv-shows/tv-shows-x264',545,art+'/wfs/scepert.png')
            main.addDir('Documentary TV Shows','http://sceper.ws/home/category/tv-shows/documentaries',545,art+'/wfs/scepert.png')
        main.VIEWSB2()
        
            
def LISTSCEPER(name,murl):
        main.GA("Sceper","List")
        link=main.OPENURL(murl)
        i=0
        audiolist=[]
        desclist=[]
        genrelist=[]
        link=link.replace('\xc2\xa0','').replace('\n','')
        audio=re.compile('>Audio:</.+?>(.+?)<b').findall(link)
        if len(audio)>0:
            for aud in audio:
                aud=aud.replace('</span><span style="font-family: arial"> ','').replace('<span style="color: #ff0000;">','').replace('</span>','').replace('<span style="color: #ff9900">','').replace('<span style="color: #ff6600">','').replace('<span style="color: #ff0000">','').replace('</span><span style="font-family: arial">','').replace('<span style="font-family: arial">','').replace('<span style="font-family: arial;">','')
                audiolist.append(aud)
        else:
            audiolist.append('Audio Unknown')
        descr=re.compile('>Release Description</div><p>(.+?)</p>').findall(link)
        if len(descr)>0:
            for desc in descr:
                desc=desc.replace('</span><span style="font-family: arial"> ','').replace('<span style="color: #ff0000;">','').replace('</span>','')
                desclist.append(desc)
        else:
            desclist.append('Description Unavailable')
        genre=re.compile('>Genre:</span>(.+?)<br').findall(link)
        if len(genre)>0:
            for gen in genre:
                gen=gen.replace('</span><span style="font-family: arial"> ','').replace('<span style="color: #ff0000;">','').replace('</span>','')
                genrelist.append(gen)
        else:
            genrelist.append('Genre Unknown')
        match=re.compile('<a href="([^<]+)">([^<]+)</a></h2>\t\t<div class=".+?">\t\t\t\t<div class=".+?">Release Info</div><p><a href="(.+?)"').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for url,name,thumb in match:
            
            if len(audiolist)<8:
                audiolist.append('Audio Unknown')
            if len(desclist)<8:
                desclist.append('Description Unavailable')
            if len(genrelist)<8:
                genrelist.append('Genre Unknown')
            main.addPlayM(name+' [COLOR red]'+audiolist[i]+'[/COLOR]',url,544,thumb,desclist[i],'','',genrelist[i],'')
            i=i+1
            loadedLinks = loadedLinks + 1
            percent = (loadedLinks * 100)/totalLinks
            remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
            if (dialogWait.iscanceled()):
                    return False
        dialogWait.close()
        del dialogWait
        paginate = re.compile('<a href=\'([^<]+)\' class=\'nextpostslink\'>').findall(link)
        if len(paginate)>0:
            main.addDir('Next',paginate[0],541,art+'/next2.png')
        


def LISTSCEPER2(name,murl):
        link=main.OPENURL(murl)
        link=link.replace('\xc2\xa0','').replace('\n','')
        match=re.compile('<a href="([^<]+)">([^<]+)</a></h2>\t\t<div class=".+?<img.+?src="(.+?)"').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for url,name,thumb in match:
            main.addPlayTE(name,url,544,thumb,'','','','','')
            loadedLinks = loadedLinks + 1
            percent = (loadedLinks * 100)/totalLinks
            remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
            if (dialogWait.iscanceled()):
                    return False
        dialogWait.close()
        del dialogWait
        paginate = re.compile('<a href=\'([^<]+)\' class=\'nextpostslink\'>').findall(link)
        if len(paginate)>0:
            main.addDir('Next',paginate[0],545,art+'/next2.png')
        
    


def SearchhistorySCEPER():
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistory25')
        if not os.path.exists(SeaFile):
            url='extra'
            SEARCHSCEPER(url)
        else:
            main.addDir('Search','extra',542,art+'/search.png')
            main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
            thumb=art+'/link.png'
            searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
            for seahis in reversed(searchis):
                    url=seahis
                    seahis=seahis.replace('%20',' ')
                    main.addDir(seahis,url,542,thumb)
        
            
            
        
def SEARCHSCEPER(murl):
        main.GA("Sceper","Search")
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistory25')
        try:
            os.makedirs(seapath)
        except:
            pass
        if murl == 'extra':
            keyb = xbmc.Keyboard('', 'Search Movies')
            keyb.doModal()
            if (keyb.isConfirmed()):
                    search = keyb.getText()
                    encode=urllib.quote(search)
                    surl='http://sceper.ws/home/search/'+encode+'/'
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
                surl='http://sceper.ws/home/search/'+encode+'/'
        link=main.OPENURL(surl)
        i=0
        link=link.replace('\xc2\xa0','').replace('\n','')
        match=re.compile('<a href="([^<]+)">([^<]+)</a></h2>').findall(link)
        for url,name in match:
            if re.findall('(.+?)\ss(\d+)e(\d+)\s',name,re.I):
                main.addPlayTE(name,url,544,'','','','','','')
            else:
                main.addPlayM(name,url,544,'','','','','','')
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        

def VIDEOLINKSSCEPER(mname,murl,thumb):
        main.GA("Sceper","Watched")
        msg = xbmcgui.DialogProgress()
        msg.create('Please Wait!','')
        msg.update(0,'Collecting hosts')
        link=main.OPENURL(murl)
        sources=[]
        ok=True
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        match=re.compile('<a href="([^<]+)">htt').findall(link)
        hostsmax = len(match)
        h = 0
        for url in match:
            h += 1
            percent = (h * 100)/hostsmax
            msg.update(percent,'Collecting hosts - ' + str(percent) + '%')
            if (msg.iscanceled()): break
            vlink=re.compile('rar').findall(url)
            if len(vlink)==0:
                match2=re.compile('http://(.+?)/.+?').findall(url)
                for host in sorted(match2):   
                    host = host.replace('www.','')
                    match3=re.compile('720p').findall(url)
                    match4=re.compile('mp4').findall(url)
                    if len(match3)>0:
                        host =host+' [COLOR red]HD[/COLOR]'
                    elif len(match4)>0:
                        host =host+' [COLOR green]SD MP4[/COLOR]'
                    else:
                        host =host+' [COLOR blue]SD[/COLOR]'
                        
                    hosted_media = urlresolver.HostedMediaFile(url=url, title=host)
                    sources.append(hosted_media)
        if (len(sources)==0):
                xbmc.executebuiltin("XBMC.Notification(Sorry!,Could not find a playable link,3000)")
                return
        else:
                source = urlresolver.choose_source(sources)
        msg.close()
        try:
                if not source:
                    if (len(sources)>0):
                        xbmc.executebuiltin("XBMC.Notification(Sorry!,Could not find a playable link,3000)")
                    main.CloseAllDialogs()
                    return
                xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
                stream_url = main.resolve_url(source.get_url())
                if(stream_url == False):
                    return
                
                if re.findall('(.+?)\ss(\d+)e(\d+)\s',mname,re.I):
                    mname=mname.split('&')[0]
                    infoLabels =main.GETMETAEpiT(mname,thumb,'')
                    video_type='episode'
                    season=infoLabels['season']
                    episode=infoLabels['episode']
                else:
                    infoLabels =main.GETMETAT(mname,'','',thumb)
                    video_type='movie'
                    season=''
                    episode=''
                img=infoLabels['cover_url']
                fanart =infoLabels['backdrop_url']
                imdb_id=infoLabels['imdb_id']
                infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
                
                infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                if not video_type is 'episode': infoL['originalTitle']=main.removeColoredText(infoLabels['metaName'])
                # play with bookmark
                player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                #WatchHistory
                if selfAddon.getSetting("whistory") == "true":
                    wh.add_item(mname+' '+'[COLOR green]Sceper[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
                player.KeepAlive()
                return ok
        except Exception, e:
                if stream_url != False:
                        main.ErrorReport(e)
                return ok
