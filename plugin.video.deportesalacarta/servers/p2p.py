# -*- coding: utf-8 -*-
#:-----------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para enlaces a sopcast y acestream
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re
from core import logger, config

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="" , video_password="" ):
    logger.info("pelisalacarta.servers.p2p server=p2p, la url es la buena " + page_url)

    if page_url.startswith("acestream") or ".acelive" in page_url:
        mode = "1"
        name = "acestream"
    elif page_url.startswith("sop"):
        mode = "2"
        name = "Sopcast"
    
    if "|" in page_url:
        name = page_url.split("|")[1]
        page_url = page_url.split("|")[0]

    video_data = {
        'plexus' : {
            'url' : "plugin://program.plexus/?url=%s&mode=%s&name=%s" % (page_url, mode, name)
        },
        'p2p-streams' : {
            'url' : "plugin://plugin.video.p2p-streams/?url=%s&mode=%s&name=%s" % (page_url, mode, name)
        }
    }

    
    video_urls = []
    
    order = True
    if config.get_setting("default_action") == "2":
        order = False

    for plugin, data in sorted(video_data.iteritems(), reverse=order):
        video_urls.append([ "[" + plugin + "] %s" % (name), data['url']])
    
    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos  = 'sop://(?:broker.sopcast.com|[\d.]+):3912/([\d]+)'
    logger.info("pelisalacarta.servers.p2p find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[sopcast]"
        url = "sop://broker.sopcast.com:3912/%s" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'sopcast' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = '(?:acestream://|http://avod.me/play/|loadPlayer\(["\']|url=player/|torrentstream.org/embed/)([a-z0-9]{40})'
    logger.info("pelisalacarta.servers.p2p find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[acestream]"
        url = "acestream://%s" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'acestream' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = '(http\S+.acelive)'
    logger.info("pelisalacarta.servers.p2p find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[acestream]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'acestream' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
