import urllib2, urllib, xbmcgui, xbmcplugin, xbmc, re, sys, os, dandy
import xbmcaddon
from addon.common.addon import Addon
from md_request import open_url

addon_id='plugin.video.openloadmovies'
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addon = Addon(addon_id, sys.argv)
addon_name = selfAddon.getAddonInfo('name')
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'

SITE = selfAddon.getSetting('website')
SITE = SITE.replace('PopNow','http://getmypopcornnow.xyz/')
SITE = SITE.replace('Oload','http://openloadmovies.net/')
SITE = SITE.replace('PubOnline','http://pubfilmonline.net/')

BASEURL = SITE

def MENU():
    addDir('[B][COLOR cornflowerblue]Trending[/COLOR][/B]',BASEURL + 'trending/?get=movies',5,ART + 'trend.jpg',FANART,'')
    addDir('[B][COLOR cornflowerblue]Featured[/COLOR][/B]',BASEURL + 'genre/featured/',5,ART + 'feature.jpg',FANART,'')
    addDir('[B][COLOR cornflowerblue]All Movies[/COLOR][/B]',BASEURL + 'movies/',5,ART + 'all_mov.jpg',FANART,'')
    addDir('[B][COLOR cornflowerblue]Genres[/COLOR][/B]',BASEURL + 'ratings/',3,ART + 'genres.jpg',FANART,'')
    addDir('[B][COLOR cornflowerblue]Release Year[/COLOR][/B]',BASEURL + 'trending/',4,ART + 'release.jpg',FANART,'')
    addDir('[B][COLOR cornflowerblue]IMDB Top Movies[/COLOR][/B]',BASEURL + 'top-imdb/',7,ART + 'imdb.jpg',FANART,'')
    addDir('[B][COLOR cornflowerblue]TV Shows[/COLOR][/B]',BASEURL + 'tvseries/',8,ART + 'tv_shows.jpg',FANART,'')
    addDir('[B][COLOR cornflowerblue]IMDB Top TV[/COLOR][/B]',BASEURL + 'top-imdb/',2,ART + 'tv_imdb.jpg',FANART,'')
    addDir('[B][COLOR cornflowerblue]Search[/COLOR][/B]','url',6,ART + 'search.jpg',FANART,'')
    setView('tvshows', 'tvshows-view')

def Get_content(url):
    OPEN = open_url(url).content
    Regex = re.compile('item movies.+?href="(.+?)".+?img src="(.+?)" alt="(.+?)"',re.DOTALL).findall(OPEN)
    for url,icon,name in Regex:
            icon = icon.replace('w185','w300_and_h450_bestv2')
            name = name.replace('&#8217;','\'').replace('#038;','').replace('\\xc3\\xa9','e').replace('&#8211;','-')
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
    np = re.compile('class=.+?current.+?<a href=\'(.+?)\'',re.DOTALL).findall(OPEN)
    for url in np:
        addDir('[B][COLOR blue]Next Page>>>[/COLOR][/B]',url,5,ART + 'nextpage.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def Get_Genres(url):
    OPEN = open_url(url).content
    Regex = re.compile('<ul class="genres scrolling">(.+?)</ul>',re.DOTALL).findall(OPEN)
    Regex2 = re.compile('<a href="(.+?)"',re.DOTALL).findall(str(Regex))
    for url in Regex2:
        name = url.split('/')[4]
        name = name.split('/')[0].split('.')[0].title()
        addDir('[B][COLOR cornflowerblue]%s[/COLOR][/B]' %name,url,5,ART + 'genres.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def Get_Years(url):
    OPEN = open_url(url).content
    Regex = re.compile('<h2>Release (.+?)</ul>',re.DOTALL).findall(OPEN)
    Regex2 = re.compile('href="(.+?)">(.+?)</a></li>',re.DOTALL).findall(str(Regex))
    for url,name in Regex2:
            addDir('[B][COLOR cornflowerblue]%s[/COLOR][/B]' %name,url,5,ICON,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def Get_imdb(url):
    OPEN = open_url(url).content
    Regex = re.compile('Movies</h3>(.+?)TV Shows</h3>',re.DOTALL).findall(OPEN)
    Regex2 = re.compile('<div class="image">.+?<img src="(.+?)" /></a>.+?<a href="(.+?)">(.+?)</a></div>',re.DOTALL).findall(str(Regex))
    for icon,url,name in Regex2:
            icon = icon.replace('w90','w300_and_h450_bestv2')
            name = name.replace('&#8211;',':').replace('#038;','').replace('\\xc3\\xa9','e').replace('&#8217;','\'')
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def Get_tv_imdb(url):
    OPEN = open_url(url).content
    Regex = re.compile('TV Shows</h3>(.+?)<footer class="main">',re.DOTALL).findall(OPEN)
    Regex2 = re.compile('<img src="(.+?)".+?<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(str(Regex))
    for icon,url,name in Regex2:
            icon = icon.replace('w90','w300_and_h450_bestv2')
            name = name.replace('&#8217;','').replace('#038;','').replace('\\xc3\\xa9','e').replace('&#039;','\'')
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,9,icon,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
    
def Get_TV(url):
    OPEN = open_url(url).content
    Regex = re.compile('class="item tvshows".+?<a href="(.+?)"><img src="(.+?)" alt="(.+?)"',re.DOTALL).findall(OPEN)
    for url,icon,name in Regex:
            icon = icon.replace('w185','w300_and_h450_bestv2')
            name = name.replace('&#8217;','\'')
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,9,icon,FANART,'')
    np = re.compile('class="current".+?<a href=\'(.+?)\'',re.DOTALL).findall(OPEN)
    for url in np:
            addDir('[B][COLOR blue]Next Page>>>[/COLOR][/B]',url,8,ART + 'nextpage.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def Get_show_content(url):
    OPEN = open_url(url).content
    Regex = re.compile('<div class="imagen">.+?<div class="numerando">(.+?)</div>.+?<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(OPEN)
    for name1,url,name2 in Regex:
            name = name1+'   '+name2
            name = name.replace('&#039;','\'').replace('amp;','')
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,iconimage,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

# def Get_links(url):
    # OPEN = open_url(url).content
    # trailer = re.compile('<iframe.+?src="https://www.youtube.com/embed/(.+?)\?rel=0&amp;controls=1&amp;showinfo=0&autoplay=0"',re.DOTALL).findall(OPEN)
    # for url in trailer:
            # addDir('[B][COLOR red]Play Trailer[/COLOR][/B]','plugin://plugin.video.youtube/play/?video_id=%s'%url,100,iconimage,FANART,name)
    # Regex = re.compile('label":(.+?),.+?"file":"(.+?)"',re.DOTALL).findall(OPEN)
    # for name2,url in Regex:
            # addDir('[B][COLOR white]%s[/COLOR][/B]' %name2,url,100,iconimage,FANART,name)
    # xbmc.executebuiltin('Container.SetViewMode(50)')

def Search():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = BASEURL + '/?s=' + search
                search_res(url)
    
def search_res(url):
    OPEN = open_url(url).content
    Regex = re.compile('<div class="result-item">.+?<a href="(.+?)">.+?<img src="(.+?)" alt="(.+?)"',re.DOTALL).findall(OPEN)
    for url,icon,name in Regex:
            name = name.replace('&#8217;','').replace('#038;','')
            icon = icon.replace('w90','w300_and_h450_bestv2')
            if '/tvseries/' in url:
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,9,icon,FANART,'')    
            else:
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)') 

def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
	if addon.get_setting('auto-view') == 'true':
		xbmc.executebuiltin("Container.SetViewMode(%s)" % addon.get_setting(viewType) )

def RESOLVE(url):
    res_quality = []
    stream_url = []
    quality = ''
    if 'pubfilmonline' in url:
        OPEN = open_url(url).content
        try:
            match = re.compile('file.+?"(.+?)"').findall(OPEN)
            for link in match:
                if 'requiressl'in link:
                    if 'itag=37' in link:
                        label = '1080P'
                    elif 'itag=22' in link:
                        label = '720P'
                    elif 'itag=59' in link:
                        label = '480P'
                    else:
                        label = '360P'                        
                    quality = '[B][COLOR white]%s[/COLOR][/B]' %label
                    res_quality.append(quality)
                    stream_url.append(link)
            if len(match) >1:
                    dialog = xbmcgui.Dialog()
                    ret = dialog.select('Please Select Quality',res_quality)
                    if ret == -1:
                        return
                    elif ret > -1:
                            url = stream_url[ret]
            else:
                url = re.compile('file.+?"(.+?)"').findall(OPEN)[0]
    
        except:
            xbmc.executebuiltin("XBMC.Notification([COLOR cornflowerblue]Sorry[/COLOR],[COLOR cornflowerblue]Link Unavailable[/COLOR] ,2000)")
    else:
        OPEN = open_url(url).content
        try:
            match = re.compile('file.+?"(.+?)"').findall(OPEN)
            for link in match:
                if 'requiressl'in link:
                    if 'itag=37' in link:
                        label = '1080P'
                    elif 'itag=22' in link:
                        label = '720P'
                    elif 'itag=59' in link:
                        label = '480P'
                    else:
                        label = '360P'                        
                    quality = '[B][COLOR white]%s[/COLOR][/B]' %label
                    res_quality.append(quality)
                    stream_url.append(link)
            if len(match) >1:
                    dialog = xbmcgui.Dialog()
                    ret = dialog.select('Please Select Quality',res_quality)
                    if ret == -1:
                        return
                    elif ret > -1:
                            url = stream_url[ret]
            else:
                url = re.compile('file.+?"(.+?)"').findall(OPEN)[0]
    
        except:
            xbmc.executebuiltin("XBMC.Notification([COLOR cornflowerblue]Sorry[/COLOR],[COLOR cornflowerblue]Link Unavailable[/COLOR] ,2000)")    
    url = url.replace('\/','/')
    liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    liz.setInfo(type='Video', infoLabels={"Title": name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        
# def RESOLVE(url):
    # res_quality = []
    # stream_url = []
    # quality = ''
    # OPEN = Open_Url(url)
    # Regex = re.compile('"apiURL":"(.+?)"',re.DOTALL).findall(OPEN)[0]
    # Regex = 'http:' + Regex
    # source = Open_Url(Regex)
    # match = re.compile('"file":"(.+?)","label":"(.+?)"').findall(source)
    # for link,label in match:
            # quality = '[B][COLOR white]%s[/COLOR][/B]' %label
            # res_quality.append(quality)
            # stream_url.append(link)
    # if len(match) >1:
            # dialog = xbmcgui.Dialog()
            # ret = dialog.select('Please Select Quality',res_quality)
            # if ret == -1:
                # return
            # elif ret > -1:
                    # url = stream_url[ret]
    # else:
        # url = re.compile('"file":"(.+?)"').findall(Regex)[0]
    # url = 'http:' + url
    # liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
    # liz.setInfo(type='Video', infoLabels={"Title": name})
    # liz.setProperty("IsPlayable","true")
    # liz.setPath(url)
    # xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

# def Open_Url(url):
        # try:
                # net.set_cookies(cookie_file)
                # link = net.http_GET(url).content
                # link = cleanHex(link)
                # return link
        # except:
                # import cloudflare
                # cloudflare.createCookie(url,cookie_file,'Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0')
                # net.set_cookies(cookie_file)
                # link = net.http_GET(url).content
                # link = cleanHex(link)
                # return link

    
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


                
def addDir(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==100:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok


params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None




try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass
try:
	description=urllib.unquote_plus(params["description"])
except:
	pass

if mode==None or url==None or len(url)<1 : MENU()
elif mode == 2 : Get_tv_imdb(url)
elif mode == 3 : Get_Genres(url)
elif mode == 4 : Get_Years(url)
elif mode == 5 : Get_content(url) 
elif mode == 6 : Search()
elif mode == 7 : Get_imdb(url)
elif mode == 8 : Get_TV(url)
elif mode == 9 : Get_show_content(url)
elif mode == 10 : Get_links(url)
elif mode ==100: RESOLVE(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))

















