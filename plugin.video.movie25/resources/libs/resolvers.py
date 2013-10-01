import urllib,urllib2,re,cookielib,string, urlparse,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import urlresolver
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net as net

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id)
datapath = addon.get_profile()
elogo = xbmc.translatePath('special://home/addons/plugin.video.movie25/resources/art/bigx.png')

class ResolverError(Exception):
    def __init__(self, value, value2):
        self.value = value
        self.value2 = value2
    def __str__(self):
        return repr(self.value,self.value2)

def resolve_url(url):
    stream_url = False
    if(url):
        try:
            match = re.search('xoxv(.+?)xoxe(.+?)xoxc',url)
            if(match):
                source = urlresolver.HostedMediaFile(host=match.group(1), media_id=match.group(2))
                if source:
                    stream_url = source.resolve()
            elif re.search('billionuploads',url,re.I):
                stream_url=resolve_billionuploads(url)
            elif re.search('180upload',url,re.I):
                stream_url=resolve_180upload(url)
            elif re.search('veehd',url,re.I):
                stream_url=resolve_veehd(url)
            elif re.search('vidto',url,re.I):
                stream_url=resolve_videto(url)
            elif re.search('epicshare',url,re.I):
                stream_url=resolve_epicshare(url)
            elif re.search('lemuploads',url,re.I):
                stream_url=resolve_lemupload(url)
            elif re.search('mightyupload',url,re.I):
                stream_url=resolve_mightyupload(url)               
            else:
                source = urlresolver.HostedMediaFile(url)
                if source:
                    stream_url = source.resolve()
                else:
                    stream_url=url
            try:
                stream_url=stream_url.split('referer')[0]
                stream_url=stream_url.replace('|','')
            except:
                pass
        except ResolverError as e:
            #addon.show_small_popup('[COLOR=FF67cc33]Mash Up URLresolver Error[/COLOR] ' + e.value2,'[B][COLOR red]'+e.value+'[/COLOR][/B]',5000, elogo)
            try:
                source = urlresolver.HostedMediaFile(url)
                if source:
                    stream_url = source.resolve()
            except Exception as e:
                addon.show_small_popup('[COLOR=FF67cc33]Mash Up URLresolver Error[/COLOR]','[B][COLOR red]'+str(e)+'[/COLOR][/B]',5000, elogo)   
        except Exception as e:
            addon.show_small_popup('[COLOR=FF67cc33]Mash Up URLresolver Error[/COLOR]','[B][COLOR red]'+str(e)+'[/COLOR][/B]',5000, elogo)
    else:
        addon.show_small_popup('[COLOR=FF67cc33]Mash Up URLresolver Error[/COLOR]','[B][COLOR red]video url not valid[/COLOR][/B]',5000, elogo)
    return stream_url
    
def grab_cloudflare(url):

    class NoRedirection(urllib2.HTTPErrorProcessor):
        # Stop Urllib2 from bypassing the 503 page.    
        def http_response(self, request, response):
            code, msg, hdrs = response.code, response.msg, response.info()

            return response
        https_response = http_response

    cj = cookielib.CookieJar()
    
    opener = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')]
    response = opener.open(url).read()
        
    jschl=re.compile('name="jschl_vc" value="(.+?)"/>').findall(response)
    if jschl:
        jschl = jschl[0]    
    
        maths=re.compile('value = (.+?);').findall(response)[0].replace('(','').replace(')','')

        domain_url = re.compile('(https?://.+?/)').findall(url)[0]
        domain = re.compile('https?://(.+?)/').findall(domain_url)[0]
        
        time.sleep(5)
        
        normal = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        normal.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')]
        final= normal.open(domain_url+'cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s'%(jschl,eval(maths)+len(domain))).read()
        
        response = normal.open(url).read()

    return response

def resolve_veehd(url):
        name = "veeHD"
        cookie_file = os.path.join(datapath, '%s.cookies' % name)
        user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
        from random import choice
        userName = ['mashup1', 'mashup3', 'mashup4', 'mashup5', 'mashup6', 'mashup7']
        try:
            loginurl = 'http://veehd.com/login'
            ref = 'http://veehd.com/'
            submit = 'Login'        
            terms = 'on'
            remember_me = 'on'
            data = {'ref': ref, 'uname': choice(userName), 'pword': 'xbmcisk00l', 'submit': submit, 'terms': terms, 'remember_me': remember_me}
            html = net(user_agent).http_POST(loginurl, data).content
            net().save_cookies(cookie_file)
            headers = {}
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'}
            net().set_cookies(cookie_file)
            print 'Mash Up VeeHD - Requesting GET URL: %s' % url
            html = net().http_GET(url, headers).content
            fragment = re.findall('playeriframe".+?attr.+?src : "(.+?)"', html)
            frag = 'http://%s%s'%('veehd.com',fragment[1])
            net().set_cookies(cookie_file)
            html = net().http_GET(frag, headers).content
            r = re.search('"video/divx" src="(.+?)"', html)
            if r:
                stream_url = r.group(1)
            if not r:
                message = name + '- 1st attempt at finding the stream_url failed probably an Mp4, finding Mp4'
                addon.log_debug(message)
                a = re.search('"url":"(.+?)"', html)
                if a:
                    r=urllib.unquote(a.group(1))
                    if r:
                        stream_url = r
                    else:
                        xbmc.executebuiltin("XBMC.Notification(File Not Found,VeeHD,2000)")
                        return False
                if not a:
                    a = re.findall('href="(.+?)">', html)
                    stream_url = a[1]
            return stream_url
        except Exception, e:
            print '**** Mash Up VeeHD Error occured: %s' % e
            #addon.show_small_popup('[B][COLOR green]Mash Up: VeeHD Resolver[/COLOR][/B]','Error, Check XBMC.log for Details',5000, error_logo)
            raise ResolverError(str(e),"VeeHD")

def resolve_billionuploads(url):
# UPDATED BY THE-ONE @ XBMCHUB - 09-09-2013
# UPDATED BY THE-ONE @ XBMCHUB - 08-27-2013

    try:
            #########
            dialog = xbmcgui.DialogProgress()
            dialog.create('Resolving', 'Resolving Mash Up BillionUploads Link...')       
            dialog.update(0)
                                                                      
            print 'Mash Up BillionUploads - Requesting GET URL: %s' % url
            
            cj = cookielib.CookieJar()
            normal = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            normal.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')]
            
            ########################################################
            ######## CLOUD FLARE STUFF
            #######################################################
            class NoRedirection(urllib2.HTTPErrorProcessor):
                # Stop Urllib2 from bypassing the 503 page.    
                def http_response(self, request, response):
                    code, msg, hdrs = response.code, response.msg, response.info()

                    return response
                https_response = http_response            
            
            opener = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cj))
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36')]
            response = opener.open(url).read()
                
            html = None
            jschl=re.compile('name="jschl_vc" value="(.+?)"/>').findall(response)
            if jschl:
                jschl = jschl[0]    
            
                maths=re.compile('value = (.+?);').findall(response)[0].replace('(','').replace(')','')

                domain_url = re.compile('(https?://.+?/)').findall(url)[0]
                domain = re.compile('https?://(.+?)/').findall(domain_url)[0]
                                
                final= normal.open(domain_url+'cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s'%(jschl,eval(maths)+len(domain))).read()
                
                html = normal.open(url).read()
            else:
                html = response
            ################################################################################
            #Check page for any error msgs
            if re.search('This server is in maintenance mode', html, re.I):
                print '***** BillionUploads - Site reported maintenance mode'
                xbmc.executebuiltin("XBMC.Notification(File is currently unavailable,BillionUploads in maintenance,2000)")                                
                return False
                
            #Check for File Not Found
            if re.search('File Not Found', html, re.I):
                print '***** BillionUploads - File Not Found'
                xbmc.executebuiltin("XBMC.Notification(File Not Found,BillionUploads,2000)")
                return False                                
            
            #NEW BILLIONUPLOADS
            #postid = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
            #video_src_url = 'http://new.billionuploads.com/embed-' + postid + '.html'
            #print video_src_url
            #html = normal.open(video_src_url).read()
            
            #dialog.close()
            
            # SOLVEMEDIA CAPTCHA
            #try:
            #    captcha_dir = os.path.join( datapath, 'resources')
            #    captcha_img = os.path.join(captcha_dir, 'billion_uploads_resolver.png')
            #    if not os.path.exists(captcha_dir):
            #        os.makedirs(captcha_dir)
            #    os.remove(captcha_img)
            #except: 
            #    pass
                
            #net1 = net()
            #noscript=re.compile('<iframe src="(.+?)"').findall(html)[0]
            #check = net1.http_GET(noscript).content
            #hugekey=re.compile('id="adcopy_challenge" value="(.+?)">').findall(check)[0]           
            #captcha_headers= {'User-Agent':'Mozilla/6.0 (Macintosh; I; Intel Mac OS X 11_7_9; de-LI; rv:1.9b4) Gecko/2012010317 Firefox/10.0a4',
            #     'Host':'api.solvemedia.com','Referer':video_src_url,'Accept':'image/png,image/*;q=0.8,*/*;q=0.5'}
            #open(captcha_img, 'wb').write( net1.http_GET("http://api.solvemedia.com%s"%re.compile('<img src="(.+?)"').findall(check)[0]).content)
            
            #img = xbmcgui.ControlImage(550,15,240,100,captcha_img)
            #wdlg = xbmcgui.WindowDialog()
            #wdlg.addControl(img)
            #wdlg.show()
        
            #Prompt keyboard for user input
            #kb = xbmc.Keyboard('', 'Type the letters in the image', False)
            #kb.doModal()
            #capcode = kb.getText()
        
            #Check input                             
            #if (kb.isConfirmed()):
            #    userInput = kb.getText()
            #    if userInput != '':
            #        capcode = kb.getText()
            #    elif userInput == '':
            #        Notify('big', 'No text entered', 'You must enter text in the image to access video', '')
            #        return False
            #else:
            #    return False 
            #wdlg.close()
                
            #print 'Mash Up BillionUploads - Requesting POST URL: %s' % video_src_url
            #data={'op':'video_embed','file_code':postid, 'adcopy_response':capcode,'adcopy_challenge':hugekey}
            #html = normal.open(video_src_url, urllib.urlencode(data)).read()
            
            ####
            #OLD BILLION UPLOADS
            data = {}
            r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)
            for name, value in r:
                data[name] = value
                
            captchaimg = re.search('<img src="((?:http://|www\.)?BillionUploads.com/captchas/.+?)"', html)
    
            if captchaimg:
                dialog.close()
                img = xbmcgui.ControlImage(550,15,240,100,captchaimg.group(1))
                wdlg = xbmcgui.WindowDialog()
                wdlg.addControl(img)
                wdlg.show()
        
                kb = xbmc.Keyboard('', 'Type the letters in the image', False)
                kb.doModal()
                capcode = kb.getText()
        
                if (kb.isConfirmed()):
                    userInput = kb.getText()
                    if userInput != '':
                        capcode = kb.getText()
                    elif userInput == '':
                        common.addon.show_error_dialog("You must enter the text from the image to access video")
                        return False
                else:
                    return False
                wdlg.close()
                dialog.close() 
                dialog.create('Resolving', 'Resolving Mash Up BillionUploads Link...')
                dialog.update(50)
                data.update({'code':capcode})

            else:  
                dialog.update(50)
            
            data.update({'submit_btn':''})
            data.update({'please':'yeahman'})
            
            print 'Mash Up BillionUploads - Requesting POST URL: %s' % url
            html = normal.open(url, urllib.urlencode(data)).read()
            
            dialog.update(100)
            
            def custom_range(start, end, step):
                while start <= end:
                    yield start
                    start += step

            def checkwmv(e):
                s = ""
                
                # Create an array containing A-Z,a-z,0-9,+,/
                i=[]
                u=[[65,91],[97,123],[48,58],[43,44],[47,48]]
                for z in range(0, len(u)):
                    for n in range(u[z][0],u[z][1]):
                        i.append(chr(n))
                #print i

                # Create a dict with A=0, B=1, ...
                t = {}
                for n in range(0, 64):
                    t[i[n]]=n
                #print t

                for n in custom_range(0, len(e), 72):

                    a=0
                    h=e[n:n+72]
                    c=0

                    #print h
                    for l in range(0, len(h)):            
                        
                        f = t.get(h[l], 'undefined')
                        if f == 'undefined':
                            continue
                            
                        a= (a<<6) + f
                        c = c + 6

                        while c >= 8:
                            c = c - 8
                            s = s + chr( (a >> c) % 256 )

                return s

        
            dll = re.compile('<input type="hidden" id="dl" value="(.+?)">').findall(html)[0]
            dl = dll.split('GvaZu')[1]
            dl = checkwmv(dl);
            dl = checkwmv(dl);
            print 'Mash Up BillionUploads Link Found: %s' % dl

            return dl

    except Exception, e:
        print '**** Mash Up BillionUploads Error occured: %s' % e
        raise ResolverError(str(e),"BillionUploads")
    finally:
        dialog.close()


def resolve_180upload(url):

    try:
        datapath = addon.get_profile()
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving Mash Up 180Upload Link...')
        dialog.update(0)
        
        puzzle_img = os.path.join(datapath, "180_puzzle.png")
        
        print 'Mash Up 180Upload - Requesting GET URL: %s' % url
        html = net().http_GET(url).content

        dialog.update(50)
                
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)

        if r:
            for name, value in r:
                data[name] = value
        else:
            raise Exception('Unable to resolve 180Upload Link')
        
        #Check for SolveMedia Captcha image
        solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)

        if solvemedia:
           dialog.close()
           html = net().http_GET(solvemedia.group(1)).content
           hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
           open(puzzle_img, 'wb').write(net().http_GET("http://api.solvemedia.com%s" % re.search('<img src="(.+?)"', html).group(1)).content)
           img = xbmcgui.ControlImage(450,15,400,130, puzzle_img)
           wdlg = xbmcgui.WindowDialog()
           wdlg.addControl(img)
           wdlg.show()
        
           kb = xbmc.Keyboard('', 'Type the letters in the image', False)
           kb.doModal()
           capcode = kb.getText()

           if (kb.isConfirmed()):
               userInput = kb.getText()
               if userInput != '':
                   solution = kb.getText()
               elif userInput == '':
                   Notify('big', 'No text entered', 'You must enter text in the image to access video', '')
                   return False
           else:
               return False
               
           wdlg.close()
           dialog.create('Resolving', 'Resolving Mash Up 180Upload Link...') 
           dialog.update(50)
           if solution:
               data.update({'adcopy_challenge': hugekey,'adcopy_response': solution})

        print 'Mash Up 180Upload - Requesting POST URL: %s' % url
        html = net().http_POST(url, data).content
        dialog.update(100)
        
        link = re.search('<a href="(.+?)" onclick="thanks\(\)">Download now!</a>', html)
        if link:
            print 'Mash Up 180Upload Link Found: %s' % link.group(1)
            return link.group(1)
        else:
            raise Exception('Unable to resolve 180Upload Link')

    except Exception, e:
        print '**** Mash Up 180Upload Error occured: %s' % e
        raise ResolverError(str(e),"180Upload") 
    finally:
        dialog.close()
        
def resolve_videto(url):
    user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    from resources.libs import jsunpack
    try:
        html = net(user_agent).http_GET(url).content
        addon.log_error('Mash Up: Resolve Vidto - Requesting GET URL: '+url)
        r = re.findall(r'<font class="err">File was removed</font>',html,re.I)
        if r:
            addon.log_error('Mash Up: Resolve Vidto - File Was Removed')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,Vidto,2000)")
            return False
        if not r:
            r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?flvplayer.+?)</script>'
                           ,html,re.M|re.DOTALL)
            if r:
                unpacked = jsunpack.unpack(r[0])#this is where it will error, not sure if resources,libs added to os path
                r = re.findall(r'label:"\d+p",file:"(.+?)"}',unpacked)
            if not r:
                r = re.findall('type="hidden" name="(.+?)" value="(.+?)">',html)
                post_data = {}
                for name, value in r:
                    post_data[name] = value
                post_data['usr_login'] = ''
                post_data['referer'] = url
                addon.show_countdown(7, 'Please Wait', 'Resolving')
                html = net(user_agent).http_POST(url,post_data).content
                r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?flvplayer.+?)</script>'
                               ,html,re.M|re.DOTALL)
                if r:
                    unpacked = jsunpack.unpack(r[0])
                    r = re.findall(r'label:"\d+p",file:"(.+?)"}',unpacked)
                if not r:
                    r = re.findall(r"var file_link = '(.+?)';",html)
        return r[0]
    except Exception, e:
        print 'Mash Up: Resolve Vidto Error - '+str(e)
        #addon.show_small_popup('[B][COLOR green]Mash Up: Vidto Resolver[/COLOR][/B]','Error, Check XBMC.log for Details',5000, error_logo)
        raise ResolverError(str(e),"Vidto") 

def resolve_epicshare(url):

    try:
        
        puzzle_img = os.path.join(datapath, "epicshare_puzzle.png")
        
        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving MashUp EpicShare Link...')
        dialog.update(0)
        
        print 'EpicShare - MashUp Requesting GET URL: %s' % url
        html = net().http_GET(url).content

        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('This server is in maintenance mode', html):
            print '***** EpicShare - Site reported maintenance mode'
            xbmc.executebuiltin("XBMC.Notification(File is currently unavailable,EpicShare in maintenance,2000)")  
            return False
        if re.search('<b>File Not Found</b>', html):
            print '***** EpicShare - File not found'
            xbmc.executebuiltin("XBMC.Notification(File Not Found,EpicShare,2000)")
            return False


        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)

        if r:
            for name, value in r:
                data[name] = value
        else:
            print '***** EpicShare - Cannot find data values'
            raise Exception('Unable to resolve EpicShare Link')
        
        #Check for SolveMedia Captcha image
        solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)

        if solvemedia:
           dialog.close()
           html = net().http_GET(solvemedia.group(1)).content
           hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
           open(puzzle_img, 'wb').write(net().http_GET("http://api.solvemedia.com%s" % re.search('<img src="(.+?)"', html).group(1)).content)
           img = xbmcgui.ControlImage(450,15,400,130, puzzle_img)
           wdlg = xbmcgui.WindowDialog()
           wdlg.addControl(img)
           wdlg.show()
        
           kb = xbmc.Keyboard('', 'Type the letters in the image', False)
           kb.doModal()
           capcode = kb.getText()
   
           if (kb.isConfirmed()):
               userInput = kb.getText()
               if userInput != '':
                   solution = kb.getText()
               elif userInput == '':
                   Notify('big', 'No text entered', 'You must enter text in the image to access video', '')
                   return False
           else:
               return False
               
           wdlg.close()
           dialog.create('Resolving', 'Resolving MashUp EpicShare Link...') 
           dialog.update(50)
           if solution:
               data.update({'adcopy_challenge': hugekey,'adcopy_response': solution})

        print 'EpicShare - MashUp Requesting POST URL: %s' % url
        html = net().http_POST(url, data).content
        dialog.update(100)
        
        link = re.search('<a id="lnk_download"  href=".+?product_download_url=(.+?)">', html)
        if link:
            print 'MashUp EpicShare Link Found: %s' % link.group(1)
            return link.group(1)
        else:
            print '***** EpicShare - Cannot find final link'
            raise Exception('Unable to resolve EpicShare Link')
        
    except Exception, e:
        print '**** EpicShare MashUp Error occured: %s' % e
        raise ResolverError(str(e),"EpicShare") 

    finally:
        dialog.close()


def resolve_lemupload(url):

    try:

        #Show dialog box so user knows something is happening
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving MashUp LemUpload Link...')       
        dialog.update(0)
        
        print 'LemUpload - MashUp Requesting GET URL: %s' % url
        html = net().http_GET(url).content
        
        dialog.update(50)
        
        #Check page for any error msgs
        if re.search('<b>File Not Found</b>', html):
            print '***** LemUpload - File Not Found'
            xbmc.executebuiltin("XBMC.Notification(File Not Found,LemUpload,2000)")
            return False

        #Set POST data values
        data = {}
        r = re.findall('type="hidden" name="(.+?)" value="(.+?)">', html)
        
        for name, value in r:
            data[name] = value

        captchaimg = re.search('<script type="text/javascript" src="(http://www.google.com.+?)">', html)
        
        if captchaimg:
            dialog.close()
            html = net().http_GET(captchaimg.group(1)).content
            part = re.search("challenge \: \\'(.+?)\\'", html)
            captchaimg = 'http://www.google.com/recaptcha/api/image?c='+part.group(1)
            img = xbmcgui.ControlImage(450,15,400,130,captchaimg)
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
    
            kb = xbmc.Keyboard('', 'Type the letters in the image', False)
            kb.doModal()
            capcode = kb.getText()
    
            if (kb.isConfirmed()):
                userInput = kb.getText()
                if userInput != '':
                    solution = kb.getText()
                elif userInput == '':
                    Notify('big', 'No text entered', 'You must enter text in the image to access video', '')
                    return False
            else:
                return False
            wdlg.close()
            dialog.close() 
            dialog.create('Resolving', 'Resolving MashUp LemUpload Link...') 
            dialog.update(50)
            data.update({'recaptcha_challenge_field':part.group(1),'recaptcha_response_field':solution})
        
        else:
            #Check for captcha
            captcha = re.compile("left:(\d+)px;padding-top:\d+px;'>&#(.+?);<").findall(html)
            if captcha:
                result = sorted(captcha, key=lambda ltr: int(ltr[0]))
                solution = ''.join(str(int(num[1])-48) for num in result)
            data.update({'code':solution})
                               
        print 'LemUpload - MashUp Requesting POST URL: %s DATA: %s' % (url, data)
        html = net().http_POST(url, data).content

        #Get download link
        dialog.update(100)

        link = re.search('<a href="(.+?)">Download', html)
        
        if link:
            print 'MashUp LemUpload Link Found: %s' % link.group(1)
            link = link.group(1) + "|referer=" + url
            return link
        else:
            print '***** LemUpload - Cannot find final link'
            raise Exception('Unable to resolve LemUpload Link')

    except Exception, e:
        print '**** LemUpload Error occured: %s' % e
        raise ResolverError(str(e),"LemUpload") 
    finally:
        dialog.close()
        
def resolve_mightyupload(url):
    from resources.libs import jsunpack
    try:
        html = net().http_GET(url).content
        addon.log_error('Mash Up: Resolve MightyUpload - Requesting GET URL: '+url)
        r = re.findall(r'name="(.+?)" value="?(.+?)"', html, re.I|re.M)
        if r:
            post_data = {}
            for name, value in r:
                post_data[name] = value
            post_data['referer'] = url
            html = net().http_POST(url, post_data).content
            r = re.findall(r'<a href=\"(.+?)(?=\">Download the file</a>)', html)
            return r[0]
        else:
            print '***** MightyUpload - File not found'
            xbmc.executebuiltin("XBMC.Notification(File Not Found,MightyUpload,2000,"+elogo+")")
            return False
    except Exception, e:
        print 'Mash Up: Resolve MightyUpload Error - '+str(e)
        addon.show_small_popup('[B][COLOR green]Mash Up: MightyUpload Resolver[/COLOR][/B]','Error, Check XBMC.log for Details',
                               5000, elogo)
        return
