# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para cloudsix
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re

from core import logger


def test_video_exists( page_url ):
    logger.info("pelisalacarta.servers.cloudsix test_video_exists(page_url='%s')" % page_url)
    
    return False,"Este servidor no es compatible con pelisalacarta"

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("pelisalacarta.servers.cloudsix get_video_url(page_url='%s')" % page_url)
    video_urls = []
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://cloudsix.me/users/abc/123/BlaBlaBla.cas
    patronvideos  = 'cloudsix.me/users/([^\/]+/\d+)'
    logger.info("pelisalacarta.servers.cloudsix find_videos #"+patronvideos+"#")
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

    return devuelve
