#-*- coding: utf-8 -*-
import urllib,urllib2,re,cookielib,urlresolver,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main

#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
from universal import playbackengine, watchhistory
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art
wh = watchhistory.WatchHistory('plugin.video.movie25')


def LISTINT3(url):
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Source Data,10000)")
        urllist=main.OPENURL('http://www.cinevip.org/')+main.OPENURL('http://www.cinevip.org/page/2')+main.OPENURL('http://www.cinevip.org/page/3')+main.OPENURL('http://www.cinevip.org/page/4')+main.OPENURL('http://www.cinevip.org/page/5')+main.OPENURL('http://www.cinevip.org/page/6')+main.OPENURL('http://www.cinevip.org/page/7')+main.OPENURL('http://www.cinevip.org/page/8')+main.OPENURL('http://www.cinevip.org/page/9')+main.OPENURL('http://www.cinevip.org/page/10')        
        if urllist:
                urllist=urllist.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
                match=re.compile('<div class="thumbnail"><a href="(.+?)"><img alt="(.+?)" title=".+?" height=".+?" width=".+?" src="(.+?)"></a>').findall(urllist)
                dialogWait = xbmcgui.DialogProgress()
                ret = dialogWait.create('Please wait until Movie list is cached.')
                totalLinks = len(match)
                loadedLinks = 0
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
                for url,name,thumb in match:
                        name=name.replace('ver online','').replace('Ver ','').replace(' Online','')
                        main.addPlayM(name,url,67,thumb,'','','','','')
                        loadedLinks = loadedLinks + 1
                        percent = (loadedLinks * 100)/totalLinks
                        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                        if (dialogWait.iscanceled()):
                            return False   
        dialogWait.close()
        del dialogWait
        main.GA("INT","Cinevip")


def LINKINT3(name,murl,thumb):
        sources = []
        main.GA("Cinevip","Watched")
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Hosts,3000)")
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        ok=True
        infoLabels =main.GETMETAT(name,'','',thumb)
        video_type='movie'
        season=''
        episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        match=re.compile('class=".+?">([^<]+)</span></td><td>([^<]+)</td><td>([^<]+)</td>.+?adf.ly/.+?/(.+?)"').findall(link)
        if len(match) == 0:
                match=re.compile('<td><span class=".+?">.+?</span></td><td><span class=".+?">(.+?)</span></td><td>(.+?)</td><td>(.+?)</td>.+?<a .+?href=(.+?)>.+?</a>').findall(link)
        for host, lang, qua, url in match:
                print url
                url=url.replace('target="_blank"','').replace('"','')
                hosted_media = urlresolver.HostedMediaFile(url=url, title=host+' [COLOR red]'+lang+'[/COLOR] '+qua)
                sources.append(hosted_media)
        if (len(sources)==0):
                xbmc.executebuiltin("XBMC.Notification(Sorry!,Show doesn't have playable links,5000)")
      
        else:
                source = urlresolver.choose_source(sources)
        try:
                xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
                stream_url = main.resolve_url(source.get_url())
                if(stream_url == False):
                    return
                
                listitem = xbmcgui.ListItem(thumbnailImage=thumb)
                listitem.setInfo('video', {'Title': name, 'Year': ''} )         
                
                infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                # play with bookmark
                player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=infoLabels['title'],season=season, episode=episode, year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                #WatchHistory
                if selfAddon.getSetting("whistory") == "true":
                    wh.add_item(name+' '+'[COLOR green]Cinevip[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
                player.KeepAlive()
                return ok
        except Exception, e:
                if stream_url != False:
                        main.ErrorReport(e)
                return ok
