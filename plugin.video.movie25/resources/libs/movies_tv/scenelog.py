import re,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main

#Mash Up - by Mash2k3 2012.

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
    
def ListSceneLogItems(murl,quality='all'):
    if murl.startswith('Movies'):
            subpages = 5
            category = "movies"
    elif murl.startswith('TV'):
            subpages = 5
            category = "tv-shows"
    parts = murl.split('-', 1 );
    max = subpages
    try:
        pages = parts[1].split(',', 1 );
        page = int(pages[0])
        max = int(pages[1])
        murl = parts[0]
    except:
        page = 0
    page = page * subpages;
    html = ''
    urls = []
    for n in range(subpages):
        if page + n + 1 > max: break
        urls.append('http://scenelog.eu/'+category+'/page/'+str(page+n+1)+'/')
    html = main.batchOPENURL(urls)            
    hasNextPage = re.compile('<strong>&raquo;</strong>').findall(html)
    if len(hasNextPage) < subpages:
        page = None
    hasMax = re.compile('page/(\d+)/">Last &raquo;').findall(html)
    if hasMax:
        max = hasMax[0]
    if html:
        html = main.unescapes(html)
        match = re.compile('<h1>.*?href="(.+?)".*?title="(.+?)"').findall(html)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies/Episodes Cached :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        if match:
            for url,title in match:
                isHD = re.compile('720p|1080p').findall(title)
                title = title.replace("."," ").replace("_"," ")
                episode = re.search('(\d+)x(\d\d+)',title, re.I)
                if(episode):
                    e = str(episode.group(2))
                    s = str(episode.group(1))
                    if len(s)==1: s = "0" + s
                    episode = "S" + s + "E" + e
                    title = re.sub('(\d+)x(\d\d+)',episode,title,re.I)
                else:
                    title = re.sub('(\d{4}) (\d{2}) (\d{2})','\\1.\\2.\\3',title,re.I)
                if isHD:
                    title = title.split(isHD[0])[0].strip()
                else:
                    title = title.split('HDTV')[0].strip()
                title = re.sub('(\d{4}\.\d{2}\.\d{2})(.*)','\\1[COLOR blue]\\2[/COLOR]',title,re.I)
                title = re.sub('(S\d+E\d+)(.*)','\\1[COLOR blue]\\2[/COLOR]',title,re.I)
                if isHD:
                    title += " [COLOR red]HD[/COLOR]"
                if (isHD or quality != 'HD'):
                    if murl=='TV':
                        main.addDirTE(title,url,656,'','','','','','')
                    else:
                        main.addDirM(title,url,656,'','','','','','')
                        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies/Episodes Cached :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                    return False
        if not page is None:
            main.addDir('Page ' + str(page/subpages+1) + ', Next Page >>>',murl + "-" + str(page/subpages+1) + "," + max,657,art+'/next2.png')

    dialogWait.close()
    del dialogWait
    main.GA("Movies-TV","SceneLog")
    main.VIEWS()
            
def ListSceneLogLinks(mname,url):
    link=main.OPENURL(url)
    link=main.unescapes(link)
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    match=re.compile('<p><a href="(.*?)"').findall(link)
    import urlresolver
    for url in match:
#                 thumb=name.lower()
#                 murl='h'+murl
        hosted_media = urlresolver.HostedMediaFile(url=url)
        match2=re.compile("{'url': '(.+?)', 'host': '(.+?)', 'media_id': '.+?'}").findall(str(hosted_media))
        host = ''
        for murl,host in match2:
            host = re.sub('^([aA-zZ]*?\.)?(.*?)\.[aA-zZ].*','\\2',host).title()
            main.addDown2(mname+' [COLOR blue]'+host+'[/COLOR]',murl,658,'','')

def PlaySceneLogLink(mname,murl):
    main.GA("SceneLog","Watched") 
    ok=True
    r = re.findall('s(\d+)e(\d\d+)',mname,re.I)
    if r:
        infoLabels =main.GETMETAEpiT(mname,'','')
        video_type='episode'
        season=infoLabels['season']
        episode=infoLabels['episode']
    else:
        infoLabels =main.GETMETAT(mname,'','','')
        video_type='movie'
        season=''
        episode=''
    img=infoLabels['cover_url']
    fanart =infoLabels['backdrop_url']
    imdb_id=infoLabels['imdb_id']
    infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    try :
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
        stream_url = main.resolve_url(murl)
        infoLabels['title'] = main.removeColoredText(infoLabels['title'])
        infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
        if not video_type is 'episode': infoL['originalTitle']=main.removeColoredText(infoLabels['metaName']) 
        # play with bookmark
        from universal import playbackengine
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=infoLabels['title'],season=season, episode=episode, year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            from universal import watchhistory
            wh = watchhistory.WatchHistory(addon_id)
            wh.add_item(mname+' '+'[COLOR green]SceneLog[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=infoLabels['cover_url'], fanart=infoLabels['backdrop_url'], is_folder=False)
        player.KeepAlive()
        return ok
    except Exception, e:
        if stream_url != False:
                main.ErrorReport(e)
        return ok