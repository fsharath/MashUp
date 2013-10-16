# -*- coding: utf-8 -*-
import urllib,re,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,time,threading
from resources.libs import main

#Mash Up - by Mash2k3 2012.

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
smalllogo=art+'/smallicon.png'

user = selfAddon.getSetting('rlsusername')
passw = selfAddon.getSetting('rlspassword')
filters = ''
if selfAddon.getSetting('ddtv_pdtv') == 'true': filters += 'pdtv,'
if selfAddon.getSetting('ddtv_dsr') == 'true': filters += 'dsr,'
if selfAddon.getSetting('ddtv_hdtv480p') == 'true': filters += 'hdtv,'
if selfAddon.getSetting('ddtv_hdtv720p') == 'true': filters += 'realhd,'
if selfAddon.getSetting('ddtv_dvdrip') == 'true': filters += 'dvdrip,'
if selfAddon.getSetting('ddtv_webdl720p') == 'true': filters += 'webdl,'
if selfAddon.getSetting('ddtv_webdl1080p') == 'true': filters += 'webdl1080p,'
filters = filters.strip(',')
if user == '' and passw == '':
    dialog = xbmcgui.Dialog()
    dialog.ok("[COLOR=FF67cc33]MashUp[/COLOR]", "Please set your Rlsmix credentials", "in Addon settings under logins tab.", "For credentials register @ http://directdownload.tv/.")
    selfAddon.openSettings()
    user = selfAddon.getSetting('rlsusername')
    passw = selfAddon.getSetting('rlspassword')
           
def ListDirectDownloadTVItems(startpage):
    subpages = 4
    setCookie()
    main.addDir('Search Rlsmix','rlsmix',136,art+'/search.png')
    if 'TV' in startpage:
        startpage = 0
    try: page = int(startpage)
    except: page = 0
    urls = []
    for n in range(subpages):
        urls.append('http://directdownload.tv/index/search/keyword//qualities/'+filters+'/from/'+str(page)+'/search')
        page += 20
    html = getBatchUrl(urls)
    ShowDirectDownloadTVItems(html)
    strpage = str((int(startpage))/(20*subpages)+1)
    main.addDir('Page ' + strpage + ' [COLOR blue]Next Page >>>[/COLOR]',str(page),61,art+'/next2.png')
    main.GA("TV","DirectDownloadTV")
            
def setCookie():
    from t0mm0.common.net import Net as net
    cookie_file = os.path.join(os.path.join(xbmc.translatePath(selfAddon.getAddonInfo('profile')),'Cookies'), 'directdownload.cookies')
    s = time.time()
    cookieExpired = False
    if os.path.exists(cookie_file):
        try:
            cookie = open(cookie_file).read()
            expire = re.search('expires="(.*?)"',cookie, re.I)
            if expire:
                expire = str(expire.group(1))
                if time.time() > time.mktime(time.strptime(expire, '%Y-%m-%d %H:%M:%SZ')):
                   cookieExpired = True
        except: cookieExpired = True 
    if not os.path.exists(cookie_file) or cookieExpired:
        log_in = net().http_POST('http://directdownload.tv',{'username':user,'password':passw,'Login':'Login'}).content
        if "alert('Invalid login or password.')" in log_in:
                xbmcplugin.endOfDirectory(int(sys.argv[1]),False,False)
                xbmc.executebuiltin("XBMC.Notification(Sorry!,Username or Password Incorrect,10000,"+smalllogo+")")
                return
        net().save_cookies(cookie_file)
    else:
        net().set_cookies(cookie_file)
        
def getUrl(url, q = False):
    from t0mm0.common.net import Net as net
    content = net().http_GET(url).content
    if q: q.put(content)
    return content

def getBatchUrl(urls):
    try:
        import Queue as queue
    except ImportError:
        import queue
    max = len(urls)
    results = []
    for url in urls: 
        q = queue.Queue()
        threading.Thread(target=getUrl, args=(url,q)).start()
        results.append(q)
    content = ''
    for n in range(max):
        content += results[n].get()
    return content

def processTitle(title):
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
    isHD = re.compile('720p|1080p').findall(title)
    if isHD:
        title = title.split(isHD[0])[0].strip("- ")
    else:
        title = title.split('HDTV')[0].strip()
        title = title.split('PDTV')[0].strip()
        title = title.split('WEB DL')[0].strip()
    title = re.sub('(\d{4}\.\d{2}\.\d{2})(.*)','\\1[COLOR blue]\\2[/COLOR]',title)
    title = re.sub('([sS]\d+[eE]\d+.*?) (.*)','\\1 [COLOR blue]\\2[/COLOR]',title)
    if isHD:
        title += " [COLOR red]"+isHD[0]+"[/COLOR]"
    return title

def ShowDirectDownloadTVItems(html):
    html=main.unescapes(html)
    match=re.compile('{"release":"(.+?)","when":.+?,"size":".+?","links":(.+?),"idtvs".+?}').findall(html)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until Show list is cached.')
    totalLinks = len(match)
    if totalLinks:
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for title,url in match:
            title = processTitle(title)
            url=url.replace('\/','/')
            main.addDirTE(title,url,62,'','','','','','')
    
            loadedLinks = loadedLinks + 1
            percent = (loadedLinks * 100)/totalLinks
            remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
            if (dialogWait.iscanceled()):
                    return False   
        dialogWait.close()
        del dialogWait
    return totalLinks

def ListDirectDownloadTVLinks(mname,url):
    ok=True
    if selfAddon.getSetting("hide-download-instructions") != "true":
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    match=re.compile('{"url":"(.+?)","hostname":"(.+?)"}').findall(url)
#     import urlresolver
    for url,host in match:
        thumb=host.lower()
        urlExceptions = re.compile('rar').findall(url)
        hostExceptions = re.compile('fileom|oteupload').findall(host)
        if not urlExceptions and not hostExceptions:
#             hosted_media = urlresolver.HostedMediaFile(url=url, title=host)
#             match2=re.compile("{'url': '(.+?)', 'host': '(.+?)', 'media_id': '.+?'}").findall(str(hosted_media))
#             for murl,name in match2:
            main.addDown2(mname+' [COLOR blue]'+host.upper()+'[/COLOR]',url,210,art+"/hosts/"+thumb+".png",art+"/hosts/"+thumb+".png")     
        
def PlayDirectDownloadTVLink(mname,murl):
    main.GA("DirectDownloadTV","Watched")
    ok=True
    infoLabels =main.GETMETAEpiT(mname,'','')
    video_type='episode'
    season=infoLabels['season']
    episode=infoLabels['episode']
    img=infoLabels['cover_url']
    fanart =infoLabels['backdrop_url']
    imdb_id=infoLabels['imdb_id']
    infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
    try:
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
        stream_url = main.resolve_url(murl)
        
        infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
        # play with bookmark
        from universal import playbackengine
        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=infoLabels['title'],season=str(season), episode=(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            from universal import  watchhistory
            wh = watchhistory.WatchHistory('plugin.video.movie25')
            wh.add_item(mname+' '+'[COLOR green]Rlsmix[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
        player.KeepAlive()
        return ok
    except Exception, e:
        if stream_url != False:
                main.ErrorReport(e)
        return ok

def StartDirectDownloadTVSearch():
    searchpath=os.path.join(main.datapath,'Search')
    SearchFile=os.path.join(searchpath,'SearchHistoryTv')
    if not os.path.exists(SearchFile):
        SEARCHRlsmix('rlsmix')
    else:
        main.addDir('Search','rlsmix',137,art+'/search.png')
        main.addDir('Clear History',SearchFile,128,art+'/cleahis.png')
        thumb=art+'/link.png'
        searchitems=re.compile('search="(.+?)",').findall(open(SearchFile,'r').read())
        for searchitem in reversed(searchitems):
            searchitem=searchitem.replace('%20',' ')
            main.addDir(searchitem,searchitem,137,thumb)
            
def SearchDirectDownloadTV(searchQuery):
    setCookie()
    addToSearchHistory = True
    searchpath=os.path.join(main.datapath,'Search')
    searchHistoryFile = "SearchHistoryTv"
    try:
        params = searchQuery.split('#@#', 1 );
        page = int(params[1])
        searchQuery = params[0]
    except: page = 0
    SearchFile=os.path.join(searchpath,searchHistoryFile)
    searchQuery=urllib.unquote(searchQuery)
    if searchQuery == 'rlsmix' :
        searchQuery = ''
        try:
            os.makedirs(searchpath)
        except:
            pass
        keyb = xbmc.Keyboard('', 'Search For Shows or Movies' )
        keyb.doModal()
        if (keyb.isConfirmed()):
            searchQuery = keyb.getText()
        else:
            xbmcplugin.endOfDirectory(int(sys.argv[1]),False,False)
    else:
        addToSearchHistory = False
    searchQuery=urllib.quote(searchQuery)
    if addToSearchHistory:
        if not os.path.exists(SearchFile) and searchQuery != '':
            open(SearchFile,'w').write('search="%s",'%searchQuery)
        elif searchQuery != '':
                open(SearchFile,'a').write('search="%s",'%searchQuery)
        else: return False
        searchitems=re.compile('search="(.+?)",').findall(open(SearchFile,'r').read())
        if len(searchitems)>=10:
            searchitems.remove(searchitems[0])
            os.remove(SearchFile)
            for searchitem in searchitems:
                try: open(SearchFile,'a').write('search="%s",'%searchitem)
                except: pass
    
    searchUrl='http://directdownload.tv/index/search/keyword/'+searchQuery+'/qualities/pdtv,dsr,realhd,dvdrip,webdl,webdl1080p/from/'+str(page)+'/search'
    from t0mm0.common.net import Net as net
    html = net().http_GET(searchUrl).content
    if html:
        totalLinks = ShowDirectDownloadTVItems(html)
        if not totalLinks:
            xbmc.executebuiltin("XBMC.Notification(DirectDownloadTV,No Results Found,3000)") 
            return False
        if page == 0: strpage = "1"
        else: strpage = str(page/20+1)
        page += 20
        if not totalLinks % 20:
            main.addDir('Page ' + strpage + ' [COLOR blue]Next Page >>>[/COLOR]',searchQuery + '#@#' + str(page),137,art+'/next2.png')
    else:
        xbmcplugin.endOfDirectory(int(sys.argv[1]), False, False)
        xbmc.executebuiltin("XBMC.Notification(Sorry,Could not connect to DirectDownloadTV,3000)") 
    main.GA("DirectDownloadTV","Search")