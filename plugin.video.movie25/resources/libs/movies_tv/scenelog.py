import urllib,urllib2,re,cookielib,urlresolver,os,sys
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
    print murl
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
    for url in match:
#                 thumb=name.lower()
#                 murl='h'+murl
        hosted_media = urlresolver.HostedMediaFile(url=url)
        match2=re.compile("{'url': '(.+?)', 'host': '(.+?)', 'media_id': '.+?'}").findall(str(hosted_media))
        host = ''
        for murl,host in match2:
            host = re.sub('^([aA-zZ]*?\.)?(.*?)\.[aA-zZ].*','\\2',host).title()
            main.addDown2(mname+' [COLOR blue]'+host+'[/COLOR]',murl,209,'','')

