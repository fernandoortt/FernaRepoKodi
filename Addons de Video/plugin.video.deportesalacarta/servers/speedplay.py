# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para speedplay
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("pelisalacarta.servers.speedplay test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.downloadpage(page_url)
    if "File Not Found" in data:
        return False, "[Speedplay] El archivo no existe o ha sido borrado"
    
    return True,""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("pelisalacarta.servers.speedplay url="+page_url)
    video_urls = []

    data = scrapertools.downloadpage(page_url)
    
    matches = scrapertools.find_multiple_matches(data, 'file:"([^"]+)",label:"([^"]+)"')
    for media_url, calidad in matches:
        calidad = "."+media_url.rsplit('.',1)[1] + " " + calidad+"p"
        video_urls.append([ calidad+' [speedplay]',media_url ])
    
    return video_urls


# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []


    #http://speedplay.us/kgcldj6y8l8t.html
    #http://speedplay.pw/embed-kgcldj6y8l8t.html
    patronvideos  = 'speedplay.(?:us|pw|xyz)/(?:embed-|)([A-Z0-9a-z]+)'
    logger.info("pelisalacarta.servers.speedplay find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[speedplay]"
        url = "http://speedplay.pw/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'speedplay' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    
    return devuelve
