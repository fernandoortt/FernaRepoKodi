# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vodbeast
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re

from core import logger
from core import scrapertools

def test_video_exists( page_url ):
    logger.info("pelisalacarta.servers.vodbeast test_video_exists(page_url='%s')" % page_url)
    
    data = scrapertools.cache_page( page_url )
    if ("File was deleted" or "Not Found") in data: return False, "[Vodbeast] El archivo no existe o ha sido borrado"

    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("pelisalacarta.servers.vodbeast url="+page_url)
    
    data = scrapertools.cache_page( page_url )

    media_urls = scrapertools.find_multiple_matches(data,',{file:\s+"([^"]+)"')
    video_urls = []
    for media_url in media_urls:
        video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [vodbeast]",media_url])

    for video_url in video_urls:
        logger.info("pelisalacarta.servers.vodbeast %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://vodbeast.com/jdfscsa5uoy4
    patronvideos  = "vodbeast.com/(?:embed-|)([a-z0-9]+)"
    logger.info("pelisalacarta.servers.vodbeast find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vodbeast]"
        url = "http://vodbeast.com/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vodbeast' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve