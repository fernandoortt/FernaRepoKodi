# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para aliez.me|aliez.tv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import re
from core import scrapertools
from core import logger


def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("pelisalacarta.servers.aliez get_video_url(page_url='%s')" % page_url)

    data = scrapertools.cachePage(page_url)

    video_urls = []
    matches = scrapertools.find_multiple_matches(data, 'file(?:"\s*|\'\s*|\s*):(?:\s*"|\s*\')([^"\']+)')
    for media_url in matches:
        video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [aliez]", media_url] )

    for video_url in video_urls:
        logger.info("pelisalacarta.servers.aliez %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://emb.aliez.me/player/video.php?id=338080&s=djk5r59yj&w=590&h=332xrva9o
    # http://aliez.me/video/33911/np0ug91t3/
    patronvideos  = 'aliez.(?:me|tv)/(?:player/video.php\?id=|video/)([0-9]+)(?:&s=|/)([A-z0-9]+)'
    logger.info("pelisalacarta.servers.aliez find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for id, s in matches:
        titulo = "[aliez]"
        url = "http://emb.aliez.me/player/video.php?id=%s&s=%s&w=590&h=332" % (id, s)
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'aliez' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():
    video_urls = get_video_url("http://aliez.me/video/33911/np0ug91t/")
    if len(video_urls)==0:
        return false


    return True
