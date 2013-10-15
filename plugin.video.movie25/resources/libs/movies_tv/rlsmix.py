# -*- coding: utf-8 -*-
import urllib,re,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,time
from resources.libs import main

#Mash Up - by Mash2k3 2012.

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
art = main.art
smalllogo=art+'/smallicon.png'

user = selfAddon.getSetting('rlsusername')
passw = selfAddon.getSetting('rlspassword')
if user == '' and passw == '':
        dialog = xbmcgui.Dialog()
        dialog.ok("[COLOR=FF67cc33]MashUp[/COLOR]", "Please set your Rlsmix credentials", "in Addon settings under logins tab.", "For credentials register @ http://directdownload.tv/.")
        selfAddon.openSettings()
        user = selfAddon.getSetting('rlsusername')
        passw = selfAddon.getSetting('rlspassword')
        
def setCookie(net):
    cookie_file = os.path.join(xbmc.translatePath(selfAddon.getAddonInfo('profile')), 'directdownload.cookies')
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

def LISTTV4(durl):
        from t0mm0.common.net import Net as net
        setCookie(net)
        main.addDir('Search Rlsmix','rlsmix',136,art+'/search.png')
        if 'http://directdownload.tv/' in durl:
                murl=durl
        else:
                murl='http://directdownload.tv/index/search/keyword//qualities/pdtv,dsr,realhd,dvdrip,webdl,webdl1080p/from/0/search'
        link = net().http_GET(murl).content
        link=main.unescapes(link)
        match=re.compile('{"release":"(.+?)","when":.+?,"size":".+?","links":(.+?),"idtvs".+?}').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for name,url in match:
                name=name.replace('.',' ')
                url=url.replace('\/','/')
                main.addDirTE(name,url,62,'','','','','','')
        
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait   
        paginate=re.compile('http://directdownload.tv/index/search/keyword//qualities/pdtv,dsr,realhd,dvdrip,webdl,webdl1080p/from/(.+?)/search').findall(murl)
        for page in paginate:
                i=int(page)+20
                purl='http://directdownload.tv/index/search/keyword//qualities/pdtv,dsr,realhd,dvdrip,webdl,webdl1080p/from/'+str(i)+'/search'
                main.addDir('[COLOR blue]Next[/COLOR]',purl,61,art+'/next2.png')
        main.GA("TV","Rlsmix")

def LINKTV4(mname,url):
        ok=True
        if selfAddon.getSetting("hide-download-instructions") != "true":
            main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
        match=re.compile('{"url":"(.+?)","hostname":"(.+?)"}').findall(url)
#         import urlresolver
        for url,host in match:
            thumb=host.lower()
            urlExceptions = re.compile('rar').findall(url)
            hostExceptions = re.compile('fileom|oteupload').findall(host)
            if not urlExceptions and not hostExceptions:
#                 hosted_media = urlresolver.HostedMediaFile(url=url, title=host)
#                 match2=re.compile("{'url': '(.+?)', 'host': '(.+?)', 'media_id': '.+?'}").findall(str(hosted_media))
#                 for murl,name in match2:
                main.addDown2(mname+' [COLOR blue]'+host.upper()+'[/COLOR] [COLOR red]HD[/COLOR]',url,210,art+"/hosts/"+thumb+".png",art+"/hosts/"+thumb+".png")     
        
def LINKTV4B(mname,murl):
        main.GA("RlsmixTV","Watched")
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

def SearchhistoryRlsmix():
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTv')
        if not os.path.exists(SeaFile):
            url='rlsmix'
            SEARCHRlsmix(url)
        else:
            main.addDir('Search','rlsmix',137,art+'/search.png')
            main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
            thumb=art+'/link.png'
            searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
            for seahis in reversed(searchis):
                    url=seahis
                    seahis=seahis.replace('%20',' ')
                    main.addDir(seahis,url,137,thumb)
            
def SEARCHRlsmix(murl):
        from t0mm0.common.net import Net as net
        setCookie(net)
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTv')
        try:
            os.makedirs(seapath)
        except:
            pass
        if murl == 'rlsmix':
                keyb = xbmc.Keyboard('', 'Search For Shows or Movies')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText()
                        encode=urllib.quote(search)
                        surl='http://directdownload.tv/index/search/keyword/'+encode+'/qualities/pdtv,dsr,realhd,dvdrip,webdl,webdl1080p/from/0/search'
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
                    xbmcplugin.endOfDirectory(int(sys.argv[1]),False,False)
                    return
        else:
                encode = murl
                surl='http://directdownload.tv/index/search/keyword/'+encode+'/qualities/pdtv,dsr,realhd,dvdrip,webdl,webdl1080p/from/0/search'
        link = net().http_GET(surl).content
        urllist=main.unescapes(link)
        match=re.compile('{"release":"(.+?)","when":.+?,"size":".+?","links":(.+?),"idtvs".+?}').findall(urllist)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for name,url in match:
                name=name.replace('.',' ')
                url=url.replace('\/','/')
                main.addDirTE(name,url,62,'','','','','','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        main.GA("Movie1k","Search")

