# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta 4
# Copyright 2015 tvalacarta@gmail.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#
# Distributed under the terms of GNU General Public License v3 (GPLv3)
# http://www.gnu.org/licenses/gpl-3.0.html
# ------------------------------------------------------------
# This file is part of pelisalacarta 4.
#
# pelisalacarta 4 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pelisalacarta 4 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pelisalacarta 4.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------
# Server management
#------------------------------------------------------------

import re, urllib, mechanize


from core import logger
from core import scrapertools


def find_videos(data, servers):
    encontrados = set()
    devuelve = []
    for serverid in servers:
        try:
            globals()[serverid](data, encontrados, devuelve)
        except:
            import traceback
            logger.info(traceback.format_exc())

    return devuelve

def adnstream(data, encontrados, devuelve):
    # http://www.adnstream.com/video/jvaRziGkoP/
    patronvideos  = 'adnstream.com/video/([a-zA-Z]+)'
    logger.info("[adnstream.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[adnstream]"

        url = "http://www.adnstream.com/video/"+match+"/"

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'adnstream' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

def allmyvideos(data, encontrados, devuelve):
    # Añade manualmente algunos erróneos para evitarlos

    encontrados.add("http://allmyvideos.net/embed-theme.html")
    encontrados.add("http://allmyvideos.net/embed-jquery.html")
    encontrados.add("http://allmyvideos.net/embed-s.html")
    encontrados.add("http://allmyvideos.net/embed-images.html")
    encontrados.add("http://allmyvideos.net/embed-faq.html")
    encontrados.add("http://allmyvideos.net/embed-embed.html")
    encontrados.add("http://allmyvideos.net/embed-ri.html")
    encontrados.add("http://allmyvideos.net/embed-d.html")
    encontrados.add("http://allmyvideos.net/embed-css.html")
    encontrados.add("http://allmyvideos.net/embed-js.html")
    encontrados.add("http://allmyvideos.net/embed-player.html")
    encontrados.add("http://allmyvideos.net/embed-cgi.html")
    encontrados.add("http://allmyvideos.net/embed-i.html")
    encontrados.add("http://allmyvideos.net/images")
    encontrados.add("http://allmyvideos.net/theme")
    encontrados.add("http://allmyvideos.net/xupload")
    encontrados.add("http://allmyvideos.net/s")
    encontrados.add("http://allmyvideos.net/js")
    encontrados.add("http://allmyvideos.net/jquery")
    encontrados.add("http://allmyvideos.net/login")
    encontrados.add("http://allmyvideos.net/make")
    encontrados.add("http://allmyvideos.net/i")
    encontrados.add("http://allmyvideos.net/faq")
    encontrados.add("http://allmyvideos.net/tos")
    encontrados.add("http://allmyvideos.net/premium")
    encontrados.add("http://allmyvideos.net/checkfiles")
    encontrados.add("http://allmyvideos.net/privacy")
    encontrados.add("http://allmyvideos.net/refund")
    encontrados.add("http://allmyvideos.net/links")
    encontrados.add("http://allmyvideos.net/contact")



    # http://allmyvideos.net/3sw6tewl21sn
    # http://allmyvideos.net/embed-3sw6tewl21sn.html
    # http://www.cinetux.org/video/allmyvideos.php?id=3sw6tewl21sn
    patronvideos = 'allmyvideos.(?:net/|php\?id=)(?:embed-|)([a-z0-9]+)'
    logger.info("deportesalacarta.servers.allmyvideos find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    if len(matches) > 0:
        for match in matches:
            titulo = "[allmyvideos]"
            url = "http://allmyvideos.net/" + match
            if url not in encontrados:
                logger.info("  url=" + url)
                devuelve.append([titulo, url, 'allmyvideos'])
                encontrados.add(url)
            else:
                logger.info("  url duplicada=" + url)

    


def allvid(data, encontrados, devuelve):
    # http://allvid.ch/jdfscsa5uoy4
    patronvideos  = "allvid.ch/(?:embed-|)([a-z0-9]+)"
    logger.info("deportesalacarta.servers.allvid find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[allvid]"
        url = "http://allvid.ch/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'allvid' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    logger.info("encontradooos "+str(encontrados))
    

def auroravid(data, encontrados, devuelve):
    data = data.replace('novamov.com','auroravid.to')

    patronvideos = 'auroravid.to/video/([a-z0-9]{13})'
    logger.info("[auroravid.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[auroravid]"
        url = "http://www.auroravid.to/video/"+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'auroravid' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://embed.novamov.com/embed.php?width=568&height=340&v=zadsdfoc0pirx&px=1
    # http://embed.novamov.com/embed.php?width=620&amp;height=348&amp;v=4f21e91a1f2f7&amp;px=1&amp;px=1
    patronvideos = 'http://embed.auroravid.to/embed.php.*?v=([a-z0-9]{13})'
    logger.info("[auroravid.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[auroravid]"
        url = "http://www.auroravid.to/video/"+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'auroravid' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

def backin(data, encontrados, devuelve):
	
	#http://backin.net/iwbe6genso37
    patronvideos  = '(?:backin).net/([A-Z0-9]+)'
    logger.info("[backin.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[backin]"
        url = "http://backin.net/s/generating.php?code="+match
        if url not in encontrados and id != "":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'backin' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)        
					
	
	#http://cineblog01.pw/HR/go.php?id=6475
    temp  = data.split('<strong>Streaming')
    if (len(temp)>1):
        tem = temp[1].split('Download')
        patronvideos  = '(?:HR)/go.php\?id\=([A-Z0-9]+)'
        logger.info("[backin.py] find_videos #"+patronvideos+"#")
        matches = re.compile(patronvideos,re.DOTALL).findall(tem[0])
    else:
        matches=[]
    page = scrapertools.find_single_match(data,'rel="canonical" href="([^"]+)"')

    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_handle_robots(False)

    for match in matches:
        titulo = "[backin]"
        url = "http://cineblog01.pw/HR/go.php?id="+match
        r = br.open(page)
        req = br.click_link(url=url)
        data = br.open(req)
        data= data.read()
        id = scrapertools.find_single_match(data,'http://backin.net/([^"]+)"')
        url = "http://backin.net/s/generating.php?code="+id
        if url not in encontrados and id != "":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'backin' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


    #http://vcrypt.net/sb/0a8hqibleus5
        #Filmpertutti.eu
    tem = data.split('<p><strong>Download:<br />')
    patronvideos  = 'http://vcrypt.net/sb/([^"]+)'
    matches = re.compile(patronvideos,re.DOTALL).findall(tem[0])
    page = scrapertools.find_single_match(data,'rel="canonical" href="([^"]+)"')

    for match in matches:
        titulo = "[backin]"
        url = "http://vcrypt.net/sb/"+match
        r = br.open(url)
        data= r.read()
        id = scrapertools.find_single_match(data,'/streams-([^"]+)-')
        url = "http://backin.net/s/generating.php?code="+id
        if url not in encontrados and id != "":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'backin' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


def bigfile(data, encontrados, devuelve):
    # https://www.bigfile.to/file/cKMCXrm7gZqv
    patronvideos  = 'bigfile.to/((?:list/|file/)[\w]+)'
    logger.info("deportesalacarta.servers.bigfile find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[bigfile]"
        url = "https://www.bigfile.to/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'bigfile' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

def bitshare(data, encontrados, devuelve):
    # http://bitshare.com/files/##/####.rar
    patronvideos  = '(bitshare.com/files/[^/]+/.*?\.rar)'
    logger.info("[bitshare.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[bitshare]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'bitshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    # http://bitshare.com/files/tn74w9tm/Rio.2011.DVDRip.LATiNO.XviD.by.Glad31.avi.html
    patronvideos  = '(bitshare.com/files/[^/]+/.*?\.html)'
    logger.info("[bitshare.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[bitshare]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'bitshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.bitshare.com/files/agax5te5
    patronvideos  = '(bitshare.com/files/[a-z0-9]+)'
    logger.info("[bitshare.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[bitshare]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'bitshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://bitshare.com/?f=idwml58s
    patronvideos  = '(bitshare.com/\?f=[\w+]+)'
    logger.info("[bitshare.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[bitshare]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'bitshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def bitvid(data, encontrados, devuelve):
    data = data.replace('videoweed.es','bitvid.sx')
    
    patronvideos  = '(http://www.bitvid.[a-z]+/file/[a-zA-Z0-9]+)'
    logger.info("[bitvidsx.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[bitvidsx]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'bitvidsx' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #logger.info("1) Videoweed formato islapeliculas") #http://embed.videoweed.com/embed.php?v=h56ts9bh1vat8
    patronvideos  = "(http://embed.bitvid.*?)&"
    logger.info("[bitvidsx.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[bitvidsx]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'bitvidsx' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
           
    #rep="/rep2.php?vw=wuogenrzatq40&t=18&c=13"
    patronvideos  = 'src="" rep="([^"]+)" width="([^"]+)" height="([^"]+)"'
    logger.info("[bitvidsx.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[bitvidsx]"
        url = match[0]
        url = url.replace("/rep2.php?vw=","http://www.bitvid.sx/file/")
        
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'bitvidsx' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

def clicknupload(data, encontrados, devuelve):

    # http://clicknupload.me/jdfscsa5uoy4
    patronvideos  = "clicknupload.(?:me|com)/([a-z0-9]+)"
    logger.info("deportesalacarta.servers.clicknupload find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[clicknupload]"
        url = "http://clicknupload.me/%s" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'clicknupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    
def cloudsix(data, encontrados, devuelve):
    # http://cloudsix.me/users/abc/123/BlaBlaBla.cas
    patronvideos  = 'cloudsix.me/users/([^\/]+/\d+)'
    logger.info("deportesalacarta.servers.cloudsix find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[cloudsix]"
        url = "http://cloudsix.me/users/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'cloudsix' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


    patronvideos  = 'https://www.cloudy.ec/embed.php\?id=(.*?&width=.*?&height=\d\d\d)'
    logger.info("deportesalacarta.servers.cloudy find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[cloudy]"
        url = "https://www.cloudy.ec/embed.php?id="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'cloudy' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

def cloudzilla(data, encontrados, devuelve):
    patronvideos  = 'http://www.cloudzilla.to/embed/([a-z0-9A-Z]+)/'
    logger.info("[cloudzilla.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[cloudzilla]"
        url = "http://www.cloudzilla.to/embed/"+match+"/"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'cloudzilla' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

def cnubis(data, encontrados, devuelve):
    # https://cnubis.com/plugins/mediaplayer/site/_1embed.php?u=9mk&w=640&h=320
    # http://cnubis.com/plugins/mediaplayer/site/_2embed.php?u=2aZD
    # http://cnubis.com/plugins/mediaplayer/embed/_2embed.php?u=U6w
    patronvideos  = 'cnubis.com/plugins/mediaplayer/(.*?/[^.]+.php\?u\=[A-Za-z0-9]+)'
    logger.info("deportesalacarta.servers.cnubis find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[cnubis]"
        url = "http://cnubis.com/plugins/mediaplayer/%s" % (match)
        if url not in encontrados and id != "":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'cnubis' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)        


def cumlouder(data, encontrados, devuelve):
    patronvideos  = 'http://es.cumlouder.com/embed/([a-z0-9A-Z]+)/'
    logger.info("[cumlouder.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[cumlouder]"
        url = "http://es.cumlouder.com/embed/"+match+"/"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'cumlouder' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


def dailymotion(data, encontrados, devuelve):
    # http://www.dailymotion.com/embed/video/xrva9o
    # http://www.dailymotion.com/swf/video/xocczx
    # http://www.dailymotion.com/swf/x17idxo&related=0
    # http://www.dailymotion.com/video/xrva9o
    patronvideos = 'dailymotion.com/(?:video/|swf/(?:video/|)|)(?:embed/video/|)([A-z0-9]+)'
    logger.info("deportesalacarta.servers.dailymotion find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[dailymotion]"
        url = "http://www.dailymotion.com/embed/video/" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'dailymotion'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)
    

def datoporn(data, encontrados, devuelve):
    patronvideos  = 'datoporn.com/(?:embed-|)([A-z0-9]+)'
    logger.info("deportesalacarta.servers.datoporn find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[datoporn]"
        url = "http://datoporn.com/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'datoporn' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

def depositfiles(data, encontrados, devuelve):
    # http://depositfiles.com/files/jdxpu4cze
    # http://www.depositfiles.com/files/zqeggnpa6
    patronvideos  = '(depositfiles.com/files/[a-z0-9]+)'
    logger.info("[depositfiles.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[depositfiles]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'depositfiles' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

def directo(data, encontrados, devuelve):
    # mysites.com
    patronvideos  = "(http://[a-zA-Z0-9]+\.mysites\.com\/get_file\/.*?\.mp4)"
    logger.info("[directo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        partes = match.split("/")
        filename = partes[len(partes)-1]
        titulo = "[Directo]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'directo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = 'flashvars="file=(http://[^\.]+.myspacecdn[^\&]+)&'
    logger.info("[directo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Directo]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Directo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = '(http://[^\.]+\.myspacecdn.*?\.flv)'
    logger.info("[directo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Directo]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Directo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = '(http://api.ning.com.*?\.flv)'
    logger.info("[directo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Directo]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'Directo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #file=http://es.video.netlogstatic.com//v/oo/004/398/4398830.flv&
    #http://es.video.netlogstatic.com//v/oo/004/398/4398830.flv
    patronvideos  = "file\=(http\:\/\/es.video.netlogstatic[^\&]+)\&"
    logger.info("[directo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Directo]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'directo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = "file=http.*?mangaid.com(.*?)&amp;backcolor="
    logger.info("[directo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    cont = 0
    for match in matches:
        cont = cont + 1 
        titulo = " Parte %s [Directo]" % (cont)
        url = "http://mangaid.com"+match
        url = url.replace('%2F','/').replace('%3F','?').replace('%23','#')
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'directo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://peliculasid.net/plugins/rip-google.php?id=8dpjvXV7bq05QjAnl93yu9MTjNZETYmyPJy0liipFm0#.mp4
    patronvideos = "so\.addVariable\(\’file\’,\’(http\://peliculasid[^\']+)"
    logger.info("[directo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    cont = 0
    for match in matches:
        cont = cont + 1 
        titulo = "[Directo]" % (cont)
        url = match
        url = url.replace('%2F','/').replace('%3F','?').replace('%23','#')
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'directo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    
def divxstage(data, encontrados, devuelve):
    # divxstage http://www.divxstage.net/video/of7ww1tdv62gf"
    patronvideos  = 'divxstage[^/]+/video/(\w+)$'
    logger.info("[divxstage.py] find_videos #" + patronvideos + "#")
    matches = scrapertools.find_multiple_matches(data, patronvideos)

    for match in matches:
        titulo = "[Divxstage]"
        url = host + "/embed/?v=" + match
        if url not in encontrados:
            logger.info("url=" + url)
            devuelve.append([titulo, url, 'divxstage'])
            encontrados.add(url)
        else:
            logger.info("url duplicada=" + url)

    # divxstage http://www.cloudtime.to/video/of7ww1tdv62gf"
    patronvideos  = 'cloudtime[^/]+/video/(\w+)$'
    logger.info("[divxstage.py] find_videos #" + patronvideos + "#")
    matches = scrapertools.find_multiple_matches(data, patronvideos)

    for match in matches:
        titulo = "[Divxstage]"
        url = host + "/embed/?v=" + match
        if url not in encontrados:
            logger.info("url=" + url)
            devuelve.append([titulo, url, 'divxstage'])
            encontrados.add(url)
        else:
            logger.info("url duplicada=" + url)


def documentary(data, encontrados, devuelve):
    # <iframe src="http://documentary.es/2321-mundos-invisibles-1x02-mas-alla-de-nuestra-vision-720p?embed"
    patronvideos  = 'http://documentary.es/(\d+[a-z0-9\-]+)'
    logger.info("documentary find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[documentary.es]"
        url = "http://documentary.es/"+match+"?embed"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'documentary' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

def extabit(data, encontrados, devuelve):
    # http://extabit.com/file/1haty8nt
    patronvideos  = '(extabit.com/file/[a-zA-Z0-9]+)'
    logger.info("[extabit.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[extabit.com]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'extabit' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

def facebook(data, encontrados, devuelve):
    # Facebook para AnimeID    src="http://www.facebook.com/v/194008590634623" type="application/x-shockwave-flash"
    # Facebook para Buena isla src='http://www.facebook.com/v/134004263282552_44773.mp4&amp;video_title=Vid&amp;v=1337'type='application/x-shockwave-flash'
    patronvideos  = 'http://www.facebook.com/v/([\d]+)'
    logger.info("[facebook.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Facebook]"
        url = "http://www.facebook.com/video/external_video.php?v="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'facebook' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    # Estos vídeos son en realidad enlaces directos
    #http://video.ak.facebook.com/cfs-ak-ash2/33066/239/133241463372257_27745.mp4
    patronvideos  = '(http://video.ak.facebook.com/.*?\.mp4)'
    logger.info("[facebook.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[facebook]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'directo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    
def fakingstv(data, encontrados, devuelve):
    patronvideos  = 'http://tv.fakings.com/embed/([a-z0-9A-Z]+)/'
    logger.info("[fakingstv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[fakingstv]"
        url = "http://tv.fakings.com/embed/"+match+"/"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'fakingstv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

def filebox(data, encontrados, devuelve):
    # http://www.filebox.com/embed-wa5p8wzh7tlq-700x385.html
    patronvideos  = 'filebox.com/embed-([0-9a-zA-Z]+)'
    logger.info("[filebox.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[filebox]"
        url = "http://www.filebox.com/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'filebox' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://www.filebox.com/729x1eo9zrx1
    patronvideos  = 'filebox.com/([0-9a-zA-Z]+)'
    logger.info("[filebox.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[filebox]"
        url = "http://www.filebox.com/"+match
        if url!="http://www.filebox.com/embed" and url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'filebox' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

def filefactory(data, encontrados, devuelve):
    patronvideos = "(www.filefactory.com/file.*?\.mkv)"
    logger.info("[filefactory.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for match in matches:
        titulo = "[filefactory]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'filefactory' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    patronvideos = "(www.filefactory.com/file.*?\.mp4)"
    logger.info("[filefactory.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for match in matches:
        titulo = "[filefactory]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'filefactory' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    #http://www.filefactory.com/file/35ip193vzp1f/n/HMD-5x19-ESP.avi
    patronvideos = "(www.filefactory.com/file.*?\.avi)"
    logger.info("[filefactory.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for match in matches:
        titulo = "[filefactory]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'filefactory' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    patronvideos = "(www.filefactory.com/file.*?\.rar)"
    logger.info("[filefactory.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for match in matches:
        titulo = "[filefactory]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'filefactory' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
            
    #http://filefactory.com/file/15437757
    patronvideos  = '(filefactory.com/file/[a-z0-9]+)'
    logger.info("[filefactory.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[filefactory]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'filefactory' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)      

    

def fileflyer(data, encontrados, devuelve):
    # http://www.fileflyer.com/view/fioZRBu
    patronvideos  = '(fileflyer.com/view/[a-zA-Z0-9]+)'
    logger.info("[fileflyer.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[fileflyer]"
        url = "http://www."+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'fileflyer' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


def filemonster(data, encontrados, devuelve):
    # http://uploaz.com/file/
    patronvideos  = '"filesmonster.com/download(.*?)"'
    logger.info("[filemonster.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[filesmonster]"
        url = "http://filesmonster.com/download"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'filemonster' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

def flashx(data, encontrados, devuelve):
    # http://flashx.tv/z3nnqbspjyne
    # http://www.flashx.tv/embed-li5ydvxhg514.html
    patronvideos = 'flashx.(?:tv|pw)/(?:embed.php\?c=|embed-|playvid-|)([A-z0-9]+)'
    logger.info("deportesalacarta.servers.flashx find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[flashx]"
        url = "http://www.flashx.tv/playvid-%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'flashx'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    
def fourshared(data, encontrados, devuelve):
    patronvideos  = "(http://www.4shared.com/embed/[A-Z0-9a-z]+/[A-Z0-9a-z]+)"
    logger.info("[fourshared.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[4shared]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'fourshared' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


    patronvideos  = 'file=(http\://[a-z0-9]+.4shared.com/img/.*?\.flv)'
    logger.info("[fourshared.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[4shared]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'fourshared' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = '"(http://www.4shared.com.*?)"'
    logger.info("[fourshared.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[4shared]"
        url = match

        if url not in encontrados and url!="http://www.4shared.com/flash/player.swf":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'fourshared' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = "'(http://www.4shared.com.*?)'"
    logger.info("[fourshared.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[4shared]"
        url = match

        if url not in encontrados and url!="http://www.4shared.com/flash/player.swf":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'fourshared' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    
def freakshare(data, encontrados, devuelve):
    #http://freakshare.com/files/##/###.rar
    patronvideos  = '(freakshare.com/files/.*?\.rar)'
    logger.info("[freakshare.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[freakshare]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'freakshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://freakshare.com/files/wy6vs8zu/4x01-mundo-primitivo.avi.html
    patronvideos  = '(freakshare.com/files/.*?\.html)'
    logger.info("[freakshare.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[freakshare]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'freakshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


def gamovideo(data, encontrados, devuelve):
    # http://gamovideo.com/auoxxtvyoy
    # http://gamovideo.com/h1gvpjarjv88
    # http://gamovideo.com/embed-sbb9ptsfqca2-588x360.html
    patronvideos  = 'gamovideo.com/(?:embed-|)([a-z0-9]+)'
    logger.info("deportesalacarta.servers.gamovideo find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[gamovideo]"
        url = "http://gamovideo.com/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'gamovideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


def gigasize(data, encontrados, devuelve):
    # http://www.gigasize.com/get/097f9cgh7pf
    patronvideos  = '(gigasize.com/get/[a-z0-9]+)'
    logger.info("[gigasize.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[gigasize]"
        url = "http://www."+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'gigasize' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://www.gigasize.com/get.php?d=097f9cgh7pf
    patronvideos  = 'gigasize.com/get.php\?d\=([a-z0-9]+)'
    logger.info("[gigasize.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[gigasize]"
        url = "http://www.gigasize.com/get/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'gigasize' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    
def googlevideo(data, encontrados, devuelve):
    patronvideos = 'http://video.google.com/googleplayer.swf.*?docid=([0-9]+)'
    logger.info("[googlevideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[googlevideo]"
        if match.count("&")>0:
            primera = match.find("&")
            url = match[:primera]
        else:
            url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'googlevideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    
def hugefiles(data, encontrados, devuelve):
    #http://www.hugefiles.net/m23qtxy5bnlw
    patronvideos  = 'hugefiles.net/([a-z0-9]+)'
    logger.info("hugefiles find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[hugefiles]"
        url = "http://www.hugefiles.net/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'hugefiles' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def idowatch(data, encontrados, devuelve):
    # http://idowatch.net/m5k9s1g7il01.html
    patronvideos  = 'idowatch.net/(?:embed-|)([a-z0-9]+)'
    logger.info("deportesalacarta.servers.idowatch find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[idowatch]"
        url = "http://idowatch.net/%s.html" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'idowatch' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


def letitbit(data, encontrados, devuelve):
    #http://letitbit.net/download/12300.151ef074afcb8f56a43d97bd64ef/Nikita.S02E15.HDTV.XviD-ASAP.avi.html
    #http://www.letitbit.net/download/33293.34678a8198db5c640085f0386d60/kells.part2.rar.html
    #http://letitbit.net/download/83307.84ab4737dc0fd6d7ee90d0458d0c/legion.avi.html
    patronvideos  = '(letitbit.net/download/.*?\.html)'
    logger.info("[letitbit.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[letitbit]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'letitbit' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)



def letwatch(data, encontrados, devuelve):
    # letwatch.us/embed-e47krmd6vqo1
    patronvideos = 'letwatch.(?:us|to)/(?:embed-|)([a-z0-9A-Z]+)(?:.html|)'
    logger.info("deportesalacarta.servers.letwatch find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[letwatch]"
        url = "http://letwatch.to/embed-" + match + ".html"
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'letwatch'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

   

def mailru(data, encontrados, devuelve): 
    logger.info("[mailru.py] find_videos")
    # http://videoapi.my.mail.ru/videos/embed/mail/bartos1100/_myvideo/1136.html
    patronvideos  = 'videoapi.my.mail.ru/(?:videos|video)/embed/(mail|inbox)/([\w]+)/.*?/(\d+).html'
    logger.info("[mailru.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mail.ru]"
        url = "http://videoapi.my.mail.ru/videos/embed/"+match[0]+"/"+match[1]+"/_myvideo/"+match[2]+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'mailru' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://my.mail.ru/videos/embed/9sadas5d14fe4ae2
    patronvideos  = 'my.mail.ru/(?:videos|video)/embed/([\w]+)'
    logger.info("[mailru.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mail.ru]"
        url = "http://my.mail.ru/+/video/meta/%s?ver=0.2.130&ext=1" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'mailru' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

def mediafire(data, encontrados, devuelve):
    #http://www.mediafire.com/download.php?pkpnzadbp2qp893
    patronvideos  = 'mediafire.com/download.php\?([a-z0-9]+)'
    logger.info("[mediafire.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mediafire]"
        url = 'http://www.mediafire.com/?'+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'mediafire' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.mediafire.com/?4ckgjozbfid
    patronvideos  = 'http://www.mediafire.com/\?([a-z0-9]+)'
    logger.info("[mediafire.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mediafire]"
        url = 'http://www.mediafire.com/?'+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'mediafire' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.mediafire.com/file/c0ama0jzxk6pbjl
    patronvideos  = 'http://www.mediafire.com/file/([a-z0-9]+)'
    logger.info("[mediafire.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mediafire]"
        url = 'http://www.mediafire.com/?'+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'mediafire' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Encontrado en animeflv
    #s=mediafire.com%2F%3F7fsmmq2144fx6t4|-|wupload.com%2Ffile%2F2653904582
    patronvideos  = 'mediafire.com\%2F\%3F([a-z0-9]+)'
    logger.info("[mediafire.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mediafire]"
        url = "http://www.mediafire.com/?"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'mediafire' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    
def mega(data, encontrados, devuelve):
    patronvideos  = '(mega.co.nz/\#\![A-Za-z0-9\-\_]+\![A-Za-z0-9\-\_]+)'
    logger.info("[mega.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mega]"
        url = "https://"+match
        if url not in encontrados:
            logger.info(" url="+url)
            devuelve.append( [ titulo , url , 'mega' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)    

    patronvideos  = '(mega.co.nz/\#F\![A-Za-z0-9\-\_]+\![A-Za-z0-9\-\_]+)'
    logger.info("[mega.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mega]"
        url = "https://"+match
        if url not in encontrados:
            logger.info(" url="+url)
            devuelve.append( [ titulo , url , 'mega' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)   

    patronvideos  = '(mega.nz/\#\![A-Za-z0-9\-\_]+\![A-Za-z0-9\-\_]+)'
    logger.info("[mega.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mega]"
        url = "https://"+match
        if url not in encontrados:
            logger.info(" url="+url)
            devuelve.append( [ titulo , url , 'mega' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)    

    patronvideos  = '(mega.nz/\#F\![A-Za-z0-9\-\_]+\![A-Za-z0-9\-\_]+)'
    logger.info("[mega.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mega]"
        url = "https://"+match
        if url not in encontrados:
            logger.info(" url="+url)
            devuelve.append( [ titulo , url , 'mega' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url) 

    

def moevideos(data, encontrados, devuelve):
    # http://www.moevideos.net/online/18998
    patronvideos  = 'moevideos.net/online/(\d+)'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[moevideos]"
        url = "http://www.moevideos.net/online/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://www.moevideos.net/view/30086
    patronvideos  = 'moevideos.net/view/(\d+)'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[moevideos]"
        url = "http://www.moevideos.net/online/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://moevideo.net/video.php?file=71845.7a9a6d72d6133bb7860375b63f0e&width=600&height=450
    patronvideos  = 'moevideo.net/video.php\?file\=([a-z0-9\.]+)'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[moevideos]"
        url = "http://moevideo.net/?page=video&uid="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www2.cinetux.org/moevideo.php?id=20671.29b19bfe3cfcf1c203816a78d1e8
    patronvideos  = 'cinetux.org/moevideo.php\?id\=([a-z0-9\.]+)'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[moevideos]"
        url = "http://moevideo.net/?page=video&uid="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    #http://moevideo.net/?page=video&uid=81492.8c7b6086f4942341aa1b78fb92df
    patronvideos  = 'moevideo.net/\?page\=video\&uid=([a-z0-9\.]+)'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[moevideos]"
        url = "http://moevideo.net/?page=video&uid="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://moevideo.net/framevideo/95250.9c5a5f9faea7207a842d609e4913
    patronvideos  = 'moevideo.net/framevideo/([a-z0-9\.]+)'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:

        titulo = "[moevideos]"
        url = "http://moevideo.net/?page=video&uid="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://moevideo.net/framevideo/95250.9c5a5f9faea7207a842d609e4913
    patronvideos  = 'moevideo.net/video/([a-z0-9\.]+)'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[moevideos]"
        url = "http://moevideo.net/?page=video&uid="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://moevideo.net/swf/letplayerflx3.swf?file=23885.2b0a98945f7aa37acd1d6a0e9713
    patronvideos  = 'moevideo.net/swf/letplayerflx3.swf\?file\=([a-z0-9\.]+)'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[moevideos]"
        url = "http://moevideo.net/?page=video&uid="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    


def moviecloud(data, encontrados, devuelve):
    ## Patrones
    #http://moviecloud.to/<id>
    #http://moviecloud.to/<id>/<name>.<ext>
    #http://moviecloud.to/plugins/mediaplayer/site/_embed.php?u=<id>&w=600&h=330
    patterns = [
        'moviecloud.to/([A-Za-z0-9]+)$',
        'moviecloud.to/([A-Za-z0-9]+)/',
        'moviecloud.to/plugins/mediaplayer/site/_embed.php?u=([A-Za-z0-9]+)&'
    ]

    for pattern in patterns:

        logger.info("[moviecloudto.py] find_videos #"+pattern+"#")
        matches = re.compile(pattern,re.DOTALL).findall(data)

        url = "http://moviecloud.to/plugins/mediaplayer/site/_embed.php?u=%s&w=600&h=330"

        for match in matches:
            titulo = "[moviecloud.to]"
            url = url % match
            if url not in encontrados:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'moviecloudto' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)

    
def movshare(data, encontrados, devuelve):
    #http://www.movshare.net/video/deg0ofnrnm8nq
    patronvideos  = 'movshare.net/video/([a-z0-9]+)'
    logger.info("[movshare.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[movshare]"
        url = "http://www.movshare.net/video/"+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'movshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #
    patronvideos  = "movshare.net/embed/([a-z0-9]+)"
    logger.info("[movshare.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[movshare]"
        url = "http://www.movshare.net/video/"+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'movshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://embed.movshare.net/embed.php?v=xepscujccuor7&width=1000&height=450
    patronvideos  = "movshare.net/embed.php\?v\=([a-z0-9]+)"
    logger.info("[movshare.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[movshare]"
        url = "http://www.movshare.net/video/"+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'movshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    
def mp4upload(data, encontrados, devuelve):
    encontrados.add("http://www.mp4upload.com/embed/embed")
    # http://www.mp4upload.com/embed-g4vrsasad9iu.html
    patronvideos = 'mp4upload.com/embed-([A-Za-z0-9]+)'
    logger.info("deportesalacarta.servers.mp4upload find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mp4upload]"
        url = "http://www.mp4upload.com/embed-" + match + ".html"
        if url not in encontrados and match != "embed":
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'mp4upload'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    

def netload(data, encontrados, devuelve):
    # http://netload.in/dateiroqHV0QNJg/Salmon.Fishing.in.the.Yemen.2012.720p.UNSOLOCLIC.INFO.mkv.htm
    patronvideos  = '(netload.in/[a-zA-Z0-9]+/.*?.htm)'
    logger.info("[netload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data+'"')

    for match in matches:
        titulo = "[netload]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'netload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://netload.in/datei2OuYAjcVGq.htm
    patronvideos  = '(netload.in/[a-zA-Z0-9]+.htm)'
    logger.info("[netload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data+'"')

    for match in matches:
        titulo = "[netload]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'netload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    
def netutv(data, encontrados, devuelve):
    ## Patrones
    # http://www.yaske.net/archivos/netu/tv/embed_54b15d2d41641.html
    # http://www.yaske.net/archivos/netu/tv/embed_54b15d2d41641.html?1
    # http://hqq.tv/player/embed_player.php?vid=498OYGN19D65&autoplay=no
    # http://hqq.tv/watch_video.php?v=498OYGN19D65
    # http://netu.tv/player/embed_player.php?vid=82U4BRSOB4UU&autoplay=no
    # http://netu.tv/watch_video.php?v=96WDAAA71A8K
    # http://waaw.tv/player/embed_player.php?vid=82U4BRSOB4UU&autoplay=no
    # http://waaw.tv/watch_video.php?v=96WDAAA71A8K
    patterns = [
        '/netu/tv/embed_(.*?$)',
        'hqq.tv/[^=]+=([a-zA-Z0-9]+)',
        'netu.tv/[^=]+=([a-zA-Z0-9]+)',
        'waaw.tv/[^=]+=([a-zA-Z0-9]+)',
        'netu.php\?nt=([a-zA-Z0-9]+)'
    ]

    if '/netu/tv/embed_' in data:
        url = "http://www.yaske.net/archivos/netu/tv/embed_%s"
    else:
        url = "http://netu.tv/watch_video.php?v=%s"

    for pattern in patterns:

        logger.info("[netutv.py] find_videos #"+pattern+"#")
        matches = re.compile(pattern,re.DOTALL).findall(data)

        for match in matches:
            titulo = "[netu.tv]"
            url = url % match
            if url not in encontrados:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'netutv' ] )
                encontrados.add(url)
                break
            else:
                logger.info("  url duplicada="+url)

    


def nosvideo(data, encontrados, devuelve):
    # http://nosvideo.com/?v=iij5rw25kh4c
    # http://nosvideo.com/vj/video.php?u=27cafd27ce64900d&w=640&h=380
    patronvideos = 'nosvideo.com/(?:\?v=|vj/video.php\?u=|)([a-z0-9]+)'
    logger.info("deportesalacarta.servers.nosvideo.py find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nosvideo]"
        url = "http://nosvideo.com/vj/videomain.php?u=%s&w=&h=530" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'nosvideo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # http://nosupload.com/?v=iij5rw25kh4c
    patronvideos = 'nosupload.com(/\?v\=[a-z0-9]+)'
    logger.info("deportesalacarta.servers.nosvideo.py find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nosvideo]"
        url = "http://nosvideo.com" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'nosvideo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    


def nowdownload(data, encontrados, devuelve):
    #http://www.nowdownload.co/dl/9gwahc3577hj9
    #http://www.nowdownload.eu/dl/srv4g94wk6j7b
    patronvideos  = '(nowdownload.\w{2}/dl/[a-z0-9]+)'
    logger.info("[nowdownload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nowdownload]"
        url = "http://www."+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'nowdownload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def nowvideo(data, encontrados, devuelve):
    #http://www.nowvideo.eu/video/4fd0757fd4592
    #serie tv cineblog
    page = scrapertools.find_single_match(data,'canonical" href="http://www.cb01.tv/serietv/([^"]+)"')
    page2 = scrapertools.find_single_match(data,'title">Telef([^"]+)</span>')
    page3 = scrapertools.find_single_match(data,'content="http://www.piratestreaming.../serietv/([^"]+)"')
    patronvideos  = 'nowvideo.../video/([a-z0-9]+)'
    logger.info("[nowvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nowvideo]"
        url = "http://www.nowvideo.sx/video/"+match
        d = scrapertools.cache_page(url)
        ma = scrapertools.find_single_match(d,'(?<=<h4>)([^<]+)(?=</h4>)')
        ma=titulo+" "+ma
        if url not in encontrados:
            logger.info("  url="+url)
            if page != "" or page2 != "" or page3 != "":
                devuelve.append( [ ma , url , 'nowvideo' ] )
            else:
                devuelve.append( [ titulo , url , 'nowvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.player3k.info/nowvideo/?id=t1hkrf1bnf2ek
    patronvideos  = 'player3k.info/nowvideo/\?id\=([a-z0-9]+)'
    logger.info("[nowvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nowvideo]"
        url = "http://www.nowvideo.sx/video/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'nowvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://embed.nowvideo.eu/embed.php?v=obkqt27q712s9&amp;width=600&amp;height=480
    #http://embed.nowvideo.eu/embed.php?v=4grxvdgzh9fdw&width=568&height=340
    patronvideos  = 'nowvideo.../embed.php\?v\=([a-z0-9]+)'
    logger.info("[nowvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nowvideo]"
        url = "http://www.nowvideo.sx/video/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'nowvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://embed.nowvideo.eu/embed.php?width=600&amp;height=480&amp;v=9fb588463b2c8
    patronvideos  = 'nowvideo.../embed.php\?.+?v\=([a-z0-9]+)'
    logger.info("[nowvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nowvideo]"
        url = "http://www.nowvideo.sx/video/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'nowvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

#Cineblog by be4t5
    patronvideos  = '<a href="http://cineblog01.../NV/go.php\?id\=([0-9]+)'
    logger.info("[nowvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    page = scrapertools.find_single_match(data,'rel="canonical" href="([^"]+)"')

    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_handle_robots(False)

    for match in matches:
        titulo = "[nowvideo]"
        url = "http://cineblog01.pw/NV/go.php?id="+match
        r = br.open(page)
        req = br.click_link(url=url)
        data = br.open(req)
        data= data.read()
        data = scrapertools.find_single_match(data,'www.nowvideo.../video/([^"]+)"?')
        url = "http://www.nowvideo.sx/video/"+data
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'nowvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    


def oboom(data, encontrados, devuelve):    
    patronvideos  = '(oboom.com/[a-zA-Z0-9]+)'
    logger.info("[oboom.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[oboom]"
        url = "https://www."+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'oboom' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def okru(data, encontrados, devuelve):
    patronvideos = '//(?:www.)?ok.../(?:videoembed|video)/(\d+)'
    logger.info("[okru.py] find_videos #" + patronvideos + "#")

    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for media_id in matches:
        titulo = "[okru]"
        url = 'http://ok.ru/dk?cmd=videoPlayerMetadata&mid=%s|http://ok.ru/videoembed/%s' % (media_id, media_id)
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'okru'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)


def onefichier(data, encontrados, devuelve):
    #http://kzu0y3.1fichier.com/
    patronvideos  = '([a-z0-9]+\.1fichier.com)'
    logger.info("deportesalacarta.servers.onefichier find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[onefichier]"
        url = "https://1fichier.com/?"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'onefichier' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # https://1fichier.com/?s6gdceia9y
    patronvideos  = '1fichier.com/\?([a-z0-9]+)'
    logger.info("deportesalacarta.servers.onefichier find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[onefichier]"
        url = "https://1fichier.com/?"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'onefichier' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def openload(data, encontrados, devuelve):
    patronvideos = '(?:openload|oload).../(?:embed|f)/([0-9a-zA-Z-_]+)'
    logger.info("deportesalacarta.servers.openload find_videos #" + patronvideos + "#")

    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for media_id in matches:
        titulo = "[Openload]"
        url = 'https://openload.co/embed/%s/' % media_id
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'openload'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)


def pcloud(data, encontrados, devuelve):
    # https://my.pcloud.com/publink/show?code=XZhKu7Z49dTa1sEfLX9Tjgk8tESFGfXTjk
    patronvideos  = "(my.pcloud.com/publink/show\?code=[A-z0-9]+)"
    logger.info("deportesalacarta.servers.pCloud find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[pCloud]"
        url = "https://%s" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'pCloud' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def playwire(data, encontrados, devuelve):
    # http://config.playwire.com/18542/videos/v2/3154852/zeus.json
    # http://cdn.playwire.com/54884/embed/12487.html
    patronvideos  = '(?:cdn|config).playwire.com(?:/v2|)/(\d+)/(?:embed|videos/v2|config)/(\d+)'
    logger.info("deportesalacarta.servers.playwire find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[playwire]"
        url = "http://config.playwire.com/%s/videos/v2/%s/zeus.json" % (match[0], match[1])
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'playwire' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


def powvideo(data, encontrados, devuelve):
    # http://powvideo.net/sbb9ptsfqca2
    # http://powvideo.net/embed-sbb9ptsfqca2
    # http://powvideo.net/iframe-sbb9ptsfqca2
    # http://powvideo.net/preview-sbb9ptsfqca2
    patronvideos  = 'powvideo.net/(?:embed-|iframe-|preview-|)([a-z0-9]+)'
    logger.info("deportesalacarta.servers.powvideo find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[powvideo]"
        url = "http://powvideo.net/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'powvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    
def rapidgator(data, encontrados, devuelve):
    #http://rapidgator.net/file/10126555/ElBatallon-byjerobien.avi.html
    #http://rapidgator.net/file/15437757
    patronvideos  = '(rapidgator.net/file/.*?(?:\.html)?$)'
    logger.info("[rapidgator.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[rapidgator]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'rapidgator' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

def rapidvideo(data, encontrados, devuelve):
    #http://www.rapidvideo.com/view/YK7A0L7FU3A
    patronvideos  = 'rapidvideo.org/([A-Za-z0-9]+)/'
    logger.info("[rapidvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[rapidvideo]"
        url = "http://www.rapidvideo.org/"+match
        d = scrapertools.cache_page(url)
        ma = scrapertools.find_single_match(d,'"fname" value="([^<]+)"')
        ma=titulo+" "+ma
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ ma , url , 'rapidvideo' ] )

            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


def redirects(data, encontrados, devuelve):    
    patronvideos  = '(https://animeflv.net/embed_izanagi.php\?key=.+?),'
    logger.info("[redirects.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    titulo = "[izanagi]"
    for match in matches:
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'redirects' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = "(http://animeflv.net/embed_yotta.php\?key=.+?)\\\\"
    logger.info("[redirects.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[yotta]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'redirects' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    
    patronvideos  = "(http://www.animeid..{2,3}/embed/.+?/)"
    logger.info("[redirects.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    titulo = "[animeimoe]"
    for match in matches:
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'redirects' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    patronvideos  = "(https://jkanime.net/jk.php\?u=stream/jkmedia.+?)\s"
    logger.info("[redirects.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    titulo = "[jkanime]"
    for match in matches:
        url = match.replace('"','')

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'redirects' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


def rutube(data, encontrados, devuelve):
    # http://rutube.ru/video/dbfe808a8828dfcfb8c6b2ed6457eef/
    # http://rutube.ru/play/embed/78451
    patronvideos  = 'rutube.ru\/(?:video\/([\da-zA-Z]{32})|play\/embed\/([\d]+))'
    logger.info("deportesalacarta.servers.rutube find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[rutube]"
        if len (match[0]) == 32:
            url = "http://rutube.ru/api/play/options/%s/?format=json" % match[0]
        else:
            url = "http://rutube.ru/video/embed/%s" % match[1]
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'rutube' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


def sendvid(data, encontrados, devuelve):
    #sendvid.com/embed/1v0chsus
    patronvideos  = 'sendvid.com/embed/([a-zA-Z0-9]+)'
    logger.info("deportesalacarta.servers.sendvid find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[sendvid]"
        url = "http://sendvid.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'sendvid' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    
def sharpfile(data, encontrados, devuelve):
    #http://www.sharpfile.com/8fgbj6dtq4xc/house.05x19.pionnerdj.avi.html
    patronvideos = "http://(www.sharpfile.com/.*?\.html)"
    logger.info("[sharpfile.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for match in matches:
        titulo = "[sharpfile]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'sharpfile' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


def speedplay(data, encontrados, devuelve):
    #http://speedplay.us/kgcldj6y8l8t.html
    #http://speedplay.pw/embed-kgcldj6y8l8t.html
    patronvideos  = 'speedplay.(?:us|pw|xyz)/(?:embed-|)([A-Z0-9a-z]+)'
    logger.info("deportesalacarta.servers.speedplay find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[speedplay]"
        url = "http://speedplay.pw/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'speedplay' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    
    
def speedvideo(data, encontrados, devuelve):
    #http://speedvideo.net/embed-fmbvopi1381q-530x302.html	
    #http://speedvideo.net/hs7djap7jwrw/Tekken.Kazuyas.Revenge.2014.iTALiAN.Subbed.DVDRiP.XViD.NeWZoNe.avi.html
    patronvideos  = 'speedvideo.net/(?:embed-|)([A-Z0-9a-z]+)'
    logger.info("deportesalacarta.servers.speedvideo find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[speedvideo]"
        url = "http://speedvideo.net/embed-%s.html" % match
        if url not in encontrados and url != "http://speedvideo.net/embed":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'speedvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #Cineblog by be4t5
    patronvideos  = 'cineblog01.../HR/go.php\?id\=([0-9]+)'
    logger.info("deportesalacarta.servers.speedvideo find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    page = scrapertools.find_single_match(data,'rel="canonical" href="([^"]+)"')

    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_handle_robots(False)

    for match in matches:
        
        titulo = "[speedvideo]"
        url = "http://cineblog01.pw/HR/go.php?id="+match
        r = br.open(page)
        req = br.click_link(url=url)
        data = br.open(req)
        data= data.read()
        data = scrapertools.find_single_match(data,'speedvideo.net/([^"]+)"?')
        if data=="":
            continue
        d = data.split('-')
        if len(d)>1:
            data = d[1]
            
        url = "http://speedvideo.net/"+data
        d = scrapertools.cache_page(url)
        ma = scrapertools.find_single_match(d,'<title>Watch ([^<]+)</title>')
        ma=titulo+" "+ma

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ ma , url , 'speedvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

					
    
def spruto(data, encontrados, devuelve):
    # http://www.spruto.tv/iframe_embed.php?video_id=141593
    patronvideos = 'spruto.tv/iframe_embed.php\?video_id=(\d+)'
    logger.info("deportesalacarta.servers.spruto find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[spruto]"
        url = "http://spruto.tv/iframe_embed.php?video_id=" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'spruto'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

def stagevu(data, encontrados, devuelve):
    patronvideos  = '(http://stagevu.com/video/[A-Z0-9a-z]+)'
    logger.info("[stagevu.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[stagevu]"
        url = match
    
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'stagevu' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = 'http://stagevu.com.*?uid\=([A-Z0-9a-z]+)'
    logger.info("[stagevu.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[stagevu]"
        url = "http://stagevu.com/video/"+match
    
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'stagevu' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = 'http://[^\.]+\.stagevu.com/v/[^/]+/(.*?).avi'
    logger.info("[stagevu.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[stagevu]"
        url = "http://stagevu.com/video/"+match
    
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'stagevu' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    
def stormo(data, encontrados, devuelve):
    # http://www.stormo.tv/embed/84575
    patronvideos  = "stormo.tv/(?:videos/|embed/)([0-9]+)"
    logger.info("deportesalacarta.servers.stormo find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[stormo]"
        url = "http://stormo.tv/embed/%s" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'stormo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def streamable(data, encontrados, devuelve):
    # http://powvideo.net/embed-sbb9ptsfqca2
    patronvideos  = 'http://www.streamable.ch/video/([a-zA-Z0-9]+)'
    logger.info("streamable find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[streamable]"
        url = "http://www.streamable.ch/video/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'streamable' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    
def streamcloud(data, encontrados, devuelve):
    encontrados.add("http://streamcloud.eu/stylesheets")
    encontrados.add("http://streamcloud.eu/control")
    encontrados.add("http://streamcloud.eu/xupload")
    encontrados.add("http://streamcloud.eu/js")
    encontrados.add("http://streamcloud.eu/favicon")
    encontrados.add("http://streamcloud.eu/reward")
    encontrados.add("http://streamcloud.eu/login")
    encontrados.add("http://streamcloud.eu/deliver")
    encontrados.add("http://streamcloud.eu/faq")
    encontrados.add("http://streamcloud.eu/tos")
    encontrados.add("http://streamcloud.eu/checkfiles")
    encontrados.add("http://streamcloud.eu/contact")
    encontrados.add("http://streamcloud.eu/serve")

    # http://streamcloud.eu/cwvhcluep67i
    patronvideos  = '(streamcloud.eu/[a-z0-9]+)'
    logger.info("[streamcloud.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[streamcloud]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'streamcloud' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def streame(data, encontrados, devuelve):
    # http://streame.net/jdfscsa5uoy4
    patronvideos  = "streame.net/(?:embed-|)([a-z0-9]+)"
    logger.info("deportesalacarta.servers.streame find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[streame]"
        url = "http://streame.net/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'streame' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    
def streaminto(data, encontrados, devuelve):
    encontrados.add("http://streamin.to/embed-theme.html")
    encontrados.add("http://streamin.to/embed-jquery.html")
    encontrados.add("http://streamin.to/embed-s.html")
    encontrados.add("http://streamin.to/embed-images.html")
    encontrados.add("http://streamin.to/embed-faq.html")
    encontrados.add("http://streamin.to/embed-embed.html")
    encontrados.add("http://streamin.to/embed-ri.html")
    encontrados.add("http://streamin.to/embed-d.html")
    encontrados.add("http://streamin.to/embed-css.html")
    encontrados.add("http://streamin.to/embed-js.html")
    encontrados.add("http://streamin.to/embed-player.html")
    encontrados.add("http://streamin.to/embed-cgi.html")


    # http://streamin.to/z3nnqbspjyne
    patronvideos = 'streamin.to/([a-z0-9A-Z]+)'
    logger.info("deportesalacarta.servers.streaminto find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[streaminto]"
        url = "http://streamin.to/embed-" + match + ".html"
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'streaminto'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # http://streamin.to/embed-z3nnqbspjyne.html
    patronvideos = 'streamin.to/embed-([a-z0-9A-Z]+)'
    logger.info("deportesalacarta.servers.streaminto find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[streaminto]"
        url = "http://streamin.to/embed-" + match + ".html"
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'streaminto'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    


def streamplay(data, encontrados, devuelve):
    # http://streamplay.to/ubhrqw1drwlx
    patronvideos  = "streamplay.to/(?:embed-|)([a-z0-9]+)(?:.html|)"
    logger.info("deportesalacarta.streamplay find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[streamplay]"
        url = "http://streamplay.to/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'streamplay' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)



def thevideome(data, encontrados, devuelve):
    patronvideos  = 'thevideo.me/embed-([a-z0-9A-Z]+)'
    logger.info("deportesalacarta.servers.thevideome find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[thevideo.me]"
        url = "http://thevideo.me/embed-"+match+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'thevideome' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    patronvideos  = 'thevideo.me/([a-z0-9A-Z]+)'
    logger.info("deportesalacarta.servers.thevideome find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[thevideo.me]"
        url = "http://thevideo.me/embed-"+match+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'thevideome' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    

def thevideos(data, encontrados, devuelve):
    #http://thevideos.tv/fxp1ffutzw2y.html
    #http://thevideos.tv/embed-fxp1ffutzw2y.html
    patronvideos  = 'thevideos.tv/(?:embed-|)([a-z0-9A-Z]+)'
    logger.info("deportesalacarta.servers.thevideos find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[thevideos]"
        url = "http://thevideos.tv/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'thevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def torrent(data, encontrados, devuelve):
    patronvideos  = '(http:\/\/(?:.*?)\.torrent)'
    logger.info("[torrent.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[torrent]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'torrent' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    patronvideos  = '(magnet:\?xt=urn:[^"]+)'
    logger.info("[torrent.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    for match in matches:
        titulo = "[torrent]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'torrent' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    


def tunepk(data, encontrados, devuelve):
    # Código embed
    patronvideos  = 'tune.pk/player/embed_player.php\?vid\=(\d+)'
    logger.info("deportesalacarta.tunepk find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[tune.pk]"
        url = "http://embed.tune.pk/play/"+match+"?autoplay=no"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'tunepk' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def turbobit(data, encontrados, devuelve):
    # http://turbobit.net/scz8lxrrgllr.html
    # http://www.turbobit.net/uzo3gcyfmt4b.html
    # http://turbobit.net/eaz9ha3gop65/deadliest.catch.s08e09-killers.mp4.html
    patronvideos  = '(turbobit.net/[0-9a-z]+)'
    logger.info("[turbobit.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[turbobit]"
        url = "http://"+match+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'turbobit' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def turbovideos(data, encontrados, devuelve):
    patronvideos  = 'turbovideos.net/embed-([a-z0-9A-Z]+)'
    logger.info("deportesalacarta.servers.turbovideos find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[turbovideos]"
        url = "http://turbovideos.net/embed-"+match+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'turbovideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def tutv(data, encontrados, devuelve):
    patronvideos  = '<param name="movie" value="(http://tu.tv[^"]+)"'
    logger.info("[tutv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[tu.tv]"
        url = match
    
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'tutv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = '<param name="movie" value="(http://www.tu.tv[^"]+)"'
    logger.info("[tutv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[tu.tv]"
        url = match
    
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'tutv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = '<embed src="(http://tu.tv/[^"]+)"'
    logger.info("[tutv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[tu.tv]"
        url = match
    
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'tutv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://tu.tv/iframe/2593305
    patronvideos  = 'tu.tv/(iframe/\d+)'
    logger.info("[tutv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[tu.tv]"
        url = "http://tu.tv/"+match
    
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'tutv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def twitvid(data, encontrados, devuelve):
    #http://www.twitvid.com/embed.php?guid=ILHLI
    patronvideos  = 'twitvid.com/embed.php\?guid=([A-Z0-9]+)'
    logger.info("[twitvid.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[twitvid]"
        url = "http://www.telly.com/"+match+"?fromtwitvid=1"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'twitvid' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def uploadable(data, encontrados, devuelve):
    # https://www.uploadable.ch/list/cKMCXrm7gZqv
    patronvideos  = 'uploadable.ch/((?:list/|file/)[\w]+)'
    logger.info("deportesalacarta.servers.uploadable find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[uploadable]"
        url = "https://www.uploadable.ch/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'uploadable' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def uploadedto(data, encontrados, devuelve):
    # http://uploaded.net/file/1haty8nt
    patronvideos  = '(?:ul|uploaded).(?:net|to)\/(file/|f/|folder/|)([a-zA-Z0-9]+)'
    logger.info("[uploadedto.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for pre, match in matches:
        titulo = "[uploaded.to]"
        if pre == "folder/":
            url = "http://uploaded.net/folder/"+match
            data = scrapertools.cache_page(url)
            links = scrapertools.find_multiple_matches(data, '<tr id="([^"]+)">[\s\S]+?(?=onclick).*?>(.*?)</a>')
            for link, title in links:
                link = "http://uploaded.net/file/"+link
                logger.info("  url="+link)
                devuelve.append( [ title , link , 'uploadedto' ] )
                encontrados.add(link)
        else:
            url = "http://uploaded.net/file/"+match
            if url not in encontrados:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'uploadedto' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)

    

def uploading(data, encontrados, devuelve):
    # http://uploading.com/files/get/686bm1b2
    patronvideos  = '(uploading.com/files/get/[a-z0-9]+)'
    logger.info("[uploading.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[uploading]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'uploading' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


def uptobox(data, encontrados, devuelve):
    # http://uptobox.com/q7asuktfr84x
    # http://uptostream.com/q7asuktfr84x
    # http://uptostream.com/iframe/q7asuktfr84x
    patronvideos  = '(?:uptobox|uptostream).com(?:/iframe/|/)([a-z0-9]+)'
    logger.info("deportesalacarta.servers.uptobox find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[uptobox]"
        if "uptostream" in data:
            url = "http://uptostream.com/iframe/"+match
        else:
            url = "http://uptobox.com/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'uptobox' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def userporn(data, encontrados, devuelve):
    #Enlace estricto a userporn")
    #userporn tipo "http://www.userporn.com/f/szIwlZD8ewaH.swf"
    patronvideos = 'userporn.com\/f\/([A-Z0-9a-z]{12}).swf'
    logger.info("[userporn.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[userporn]"
        url = "http://www.userporn.com/video/"+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'userporn' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
           
    #logger.info ("1) Enlace estricto a userporn")
    #userporn tipo "http://www.userporn.com/video/ZIeb370iuHE4"
    patronvideos = 'userporn.com\/video\/([A-Z0-9a-z]{12})'
    logger.info("[userporn.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[userporn]"
        url = "http://www.userporn.com/video/"+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'userporn' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
           
    #logger.info ("2) Enlace estricto a userporn")
    #userporn tipo "http://www.userporn.com/e/LLqVzhw5ft7T"
    patronvideos = 'userporn.com\/e\/([A-Z0-9a-z]{12})'
    logger.info("[userporn.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[userporn]"
        url = "http://www.userporn.com/video/"+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'userporn' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = "http\:\/\/(?:www\.)?userporn.com\/(?:(?:e/|flash/)|(?:(?:video/|f/)))?([a-zA-Z0-9]{0,12})"
    logger.info("[userporn.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #print data
    for match in matches:
        titulo = "[Userporn]"
        url = "http://www.userporn.com/video/"+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'userporn' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


def veehd(data, encontrados, devuelve):
    #http://veehd.com/video/4623246#
    data = urllib.unquote(data)
    patronvideos  = '(veehd.com/video/\d+\#)'
    logger.info("[veehd.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[veehd]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'veehd' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


def veoh(data, encontrados, devuelve):
    patronvideos  = '"http://www.veoh.com/.*?permalinkId=([^"]+)"'
    logger.info("[veoh.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[veoh]"
        if match.count("&")>0:
            primera = match.find("&")
            url = match[:primera]
        else:
            url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'veoh' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos = 'var embed_code[^>]+>   <param name="movie" value="http://www.veoh.com/static/swf/webplayer/WebPlayer.swf.*?permalinkId=(.*?)&player=videodetailsembedded&videoAutoPlay=0&id=anonymous"></param>'
    logger.info("[veoh.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[veoh]"
        if match.count("&")>0:
            primera = match.find("&")
            url = match[:primera]
        else:
            url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'veoh' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


def vidbull(data, encontrados, devuelve):
    # http://www.vidbull.com/3360qika02mo
    # http://vidbull.com/6efa0ns1dpxc.html
    patronvideos  = 'vidbull.com/(?:embed-|)([A-Z0-9a-z]+)'
    logger.info("deportesalacarta.servers.vidbull find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vidbull]"
        url = "http://vidbull.com/"+match+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vidbull' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def videomega(data, encontrados, devuelve):
    pattern = r'//(?:www.)?videomega\.tv/(?:(?:iframe|cdn|validatehash|view)\.php)?\?(?:ref|hashkey)=([a-zA-Z0-9]+)'

    logger.info("[videomega.py] find_videos #" + pattern + "#")
    matches = re.compile(pattern, re.DOTALL).findall(data)

    for media_id in matches:
        titulo = "[videomega]"
        url = 'http://videomega.tv/view.php?ref=%s' % media_id
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'videomega'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)


def videott(data, encontrados, devuelve):
    # http://video.tt/e/vHDKmK32U
    patronvideos  = 'video.tt/e/([A-Za-z0-9]+)'
    logger.info("[videott.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[videott]"
        url = "http://video.tt/e/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videott' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            

def videowood(data, encontrados, devuelve):
    patronvideos = r"https?://(?:www.)?videowood.tv/(?:embed/|video/)[0-9a-z]+"
    logger.info("deportesalacarta.servers.videowood find_videos #" + patronvideos + "#")

    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for url in matches:
        titulo = "[Videowood]"
        url = url.replace('/video/', '/embed/')
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'videowood'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)



def videozed(data, encontrados, devuelve):
    # http://videozed.net/t9pxgc69j56f
    patronvideos  = '(videozed.net/[a-z0-9]+)'
    logger.info("[videozed.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[videozed]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videozed' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def vidgg(data, encontrados, devuelve):
    # http://vidgg.to/video/cf8ec93a67c45
    patronvideos  = "(?:vidgg.to|vid.gg)/(?:embed/|video/)([a-z0-9]+)"
    logger.info("deportesalacarta.servers.vidgg find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vidgg]"
        url = "http://vidgg.to/video/%s" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vidgg' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

def vidspot(data, encontrados, devuelve):    
    # Añade manualmente algunos erróneos para evitarlos

    encontrados.add("http://vidspot.net/embed-theme.html")
    encontrados.add("http://vidspot.net/embed-jquery.html")
    encontrados.add("http://vidspot.net/embed-s.html")
    encontrados.add("http://vidspot.net/embed-images.html")
    encontrados.add("http://vidspot.net/embed-faq.html")
    encontrados.add("http://vidspot.net/embed-embed.html")
    encontrados.add("http://vidspot.net/embed-ri.html")
    encontrados.add("http://vidspot.net/embed-d.html")
    encontrados.add("http://vidspot.net/embed-css.html")
    encontrados.add("http://vidspot.net/embed-js.html")
    encontrados.add("http://vidspot.net/embed-player.html")
    encontrados.add("http://vidspot.net/embed-cgi.html")
    encontrados.add("http://vidspot.net/embed-i.html")
    encontrados.add("http://vidspot.net/images")
    encontrados.add("http://vidspot.net/theme")
    encontrados.add("http://vidspot.net/xupload")
    encontrados.add("http://vidspot.net/s")
    encontrados.add("http://vidspot.net/js")
    encontrados.add("http://vidspot.net/jquery")
    encontrados.add("http://vidspot.net/login")
    encontrados.add("http://vidspot.net/make")
    encontrados.add("http://vidspot.net/i")
    encontrados.add("http://vidspot.net/faq")
    encontrados.add("http://vidspot.net/tos")
    encontrados.add("http://vidspot.net/premium")
    encontrados.add("http://vidspot.net/checkfiles")
    encontrados.add("http://vidspot.net/privacy")
    encontrados.add("http://vidspot.net/refund")
    encontrados.add("http://vidspot.net/links")
    encontrados.add("http://vidspot.net/contact")



    # http://vidspot.net/3sw6tewl21sn
    # http://vidspot.net/embed-3sw6tewl21sn.html
    # http://vidspot.net/embed-3sw6tewl21sn-728x400.html
    # http://www.cinetux.org/video/vidspot.php?id=3sw6tewl21sn
    patronvideos = 'vidspot.(?:net/|php\?id=)(?:embed-|)([a-z0-9]+)'
    logger.info("deportesalacarta.servers.vidspot find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    if len(matches) > 0:
        for match in matches:
            titulo = "[vidspot]"
            url = "http://vidspot.net/" + match
            if url not in encontrados:
                logger.info("  url=" + url)
                devuelve.append([titulo, url, 'vidspot'])
                encontrados.add(url)
            else:
                logger.info("  url duplicada=" + url)

    


def vidtome(data, encontrados, devuelve):
    #http://vidto.me/z3nnqbspjyne
    patronvideos  = 'vidto.me/([a-z0-9A-Z]+)'
    logger.info("deportesalacarta.servers.vidtome find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vidto.me]"
        url = "http://vidto.me/"+match+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vidtome' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://vidto.me/embed-z3nnqbspjyne
    patronvideos  = 'vidto.me/embed-([a-z0-9A-Z]+)'
    logger.info("deportesalacarta.servers.vidtome find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vidto.me]"
        url = "http://vidto.me/"+match+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vidtome' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


def vidzi(data, encontrados, devuelve):
    patronvideos  = 'vidzi.tv/embed-([a-z0-9A-Z]+)'
    logger.info("deportesalacarta.servers.vidzi find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vidzi]"
        url = "http://vidzi.tv/embed-"+match+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vidzi' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    patronvideos  = 'vidzi.tv/([a-z0-9A-Z]+)'
    logger.info("deportesalacarta.servers.vidzi find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vidzi]"
        url = "http://vidzi.tv/embed-"+match+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vidzi' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    


def vimeo(data, encontrados, devuelve):
    # http://player.vimeo.com/video/17555432?title=0&amp;byline=0&amp;portrait=0
    # http://vimeo.com/17555432
    patronvideos  = '(?:vimeo.com/|player.vimeo.com/video/)([0-9]+)'
    logger.info("deportesalacarta.servers.vimeo find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vimeo]"
        url = "https://player.vimeo.com/video/%s/config" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vimeo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    

def vimpleru(data, encontrados, devuelve):
    # http://player.vimple.ru/iframe/21ff2440e9174286ad8c22cd2efb94d2
    patronvideos  = 'vimple.ru/iframe/([a-f0-9]+)'
    logger.info("[vimple.ru] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vimpleru]"
        url = "http://player.vimple.ru/iframe/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vimpleru' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def vk(data, encontrados, devuelve):
    # http://vkontakte.ru/video_ext.php?oid=95855298&id=162902512&hash=4f0d023887f3648e
    # http://vk.com/video_ext.php?oid=70712020&amp;id=159787030&amp;hash=88899d94685174af&amp;hd=3"
    # http://vk.com/video_ext.php?oid=161288347&#038;id=162474656&#038;hash=3b4e73a2c282f9b4&#038;sd
    # http://vk.com/video_ext.php?oid=146263567&id=163818182&hash=2dafe3b87a4da653&sd
    # http://vk.com/video_ext.php?oid=146263567&id=163818182&hash=2dafe3b87a4da653
    # http://vk.com/video_ext.php?oid=-34450039&id=161977144&hash=0305047ffe3c55a8&hd=3
    data = data.replace("&amp;", "&")
    data = data.replace("&#038;", "&")
    patronvideos = '(/video_ext.php\?oid=[^&]+&id=[^&]+&hash=[a-z0-9]+)'
    logger.info("deportesalacarta.servers.vk find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[vk]"
        url = "http://vk.com" + match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'vk'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # http://vk.com/video97482389_161509127?section=all
    patronvideos = '(vk\.[a-z]+\/video[0-9]+_[0-9]+)'
    logger.info("deportesalacarta.servers.vk find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vk]"
        url = "http ://" + match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'vk'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    

def vkpass(data, encontrados, devuelve):
    patronvideos = r'//vkpass.com/token/([^/]+)/vkphash/([^"\']+)'
    logger.info("[vkpass.py] find_videos #" + patronvideos + "#")
    
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for media_id, vkphash in matches:
        titulo = "[vkpass]"
        url = 'http://vkpass.com/token/%s/vkphash/%s' % (media_id, vkphash)
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'vkpass'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)


def vodlocker(data, encontrados, devuelve):
    patronvideos  = 'vodlocker.com/embed-([a-z0-9A-Z]+)'
    logger.info("deportesalacarta.servers.vodlocker find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vodlocker]"
        url = "http://vodlocker.com/embed-"+match+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vodlocker' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    patronvideos  = 'vodlocker.com/([a-z0-9A-Z]+)'
    logger.info("deportesalacarta.servers.vodlocker find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vodlocker]"
        url = "http://vodlocker.com/embed-"+match+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vodlocker' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    


def watchfreeinhd(data, encontrados, devuelve):
    # http://www.watchfreeinhd.com/r0GUbN
    patronvideos  = '(http://www.watchfreeinhd.com/[A-Za-z0-9]+)'
    logger.info("[watchfreeinhd.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[watchfreeinhd]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'watchfreeinhd' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    
def xvideos(data, encontrados, devuelve):
    patronvideos  = 'src="http://flashservice.xvideos.com/embedframe/([0-9]+)" '
    logger.info("[xvideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for match in matches:
        url = "http://www.xvideos.com/video"+match
        titulo = "[xvideos]"
        devuelve.append( [ titulo , url , 'xvideos'] )
    

def yourupload(data, encontrados, devuelve):
    encontrados.add("http://www.yourupload.com/embed/embed")

    #http://www.yourupload.com/embed/2PU6jqindD1Q
    patronvideos  = 'yourupload.com/embed/([A-Za-z0-9]+)'
    logger.info("deportesalacarta.servers.yourupload find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[yourupload]"
        url = "http://www.yourupload.com/embed/"+match
        if url not in encontrados and match!="embed":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'yourupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://embed.yourupload.com/2PU6jqindD1Q
    patronvideos  = 'embed.yourupload.com/([A-Za-z0-9]+)'
    logger.info("deportesalacarta.servers.yourupload find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[yourupload]"
        url = "http://www.yourupload.com/embed/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'yourupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    
def youtube(data, encontrados, devuelve):
    patronvideos  = 'youtube(?:-nocookie)?\.com/(?:(?:(?:v/|embed/))|(?:(?:watch(?:_popup)?(?:\.php)?)?(?:\?|#!?)(?:.+&)?v=))?([0-9A-Za-z_-]{11})'#'"http://www.youtube.com/v/([^"]+)"'
    logger.info("[youtube.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[YouTube]"
        url = "http://www.youtube.com/watch?v="+match
        
        if url!='':
            if url not in encontrados:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'youtube' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)
    
    patronvideos  = 'www.youtube.*?v(?:=|%3D)([0-9A-Za-z_-]{11})'
    logger.info("[youtube.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[YouTube]"
        url = "http://www.youtube.com/watch?v="+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'youtube' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.youtube.com/v/AcbsMOMg2fQ
    patronvideos  = 'youtube.com/v/([0-9A-Za-z_-]{11})'
    logger.info("[youtube.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[YouTube]"
        url = "http://www.youtube.com/watch?v="+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'youtube' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

def youwatch(data, encontrados, devuelve):
    # http://chouhaa.info/embed-ihc21y2tqpnt.html
    # http://youwatch.org/ihc21y2tqpnt
    patronvideos = 'http://(?:youwatch.org|chouhaa.info)/(?:embed-|)([a-z0-9]+)'
    logger.info("deportesalacarta.servers.youwatch find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[youwatch]"
        url = "http://youwatch.org/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'youwatch'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    

def zippyshare(data, encontrados, devuelve):
    #http://www5.zippyshare.com/v/11178679/file.html
    #http://www52.zippyshare.com/v/hPYzJSWA/file.html
    patronvideos  = '([a-z0-9]+\.zippyshare.com/v/[a-zA-Z0-9]+/file.html)'
    logger.info("[zippyshare.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[zippyshare]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'zippyshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve