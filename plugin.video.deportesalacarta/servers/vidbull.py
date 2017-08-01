# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidbull
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re

from core import logger
from core import scrapertools

headers = [['User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25']]

def test_video_exists( page_url ):
    logger.info("pelisalacarta.servers.vidbull test_video_exists(page_url='%s')" % page_url)
    
    data = scrapertools.cache_page( page_url )
    if "The file was removed by administrator" in data:
        return False,"El archivo ya no está disponible<br/>en vidbull (ha sido borrado)"
    else:
        return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("pelisalacarta.servers.vidbull url="+page_url)
        
    data = scrapertools.cache_page( page_url , headers=headers )
    
    # Extrae la URL
    media_url = scrapertools.get_match(data,'<source\s+src="([^"]+)"')
    
    video_urls = []
    
    if len(media_url)>0:
        video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [vidbull]",media_url])

    for video_url in video_urls:
        logger.info("pelisalacarta.servers.vidbull %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://www.vidbull.com/3360qika02mo
    # http://vidbull.com/6efa0ns1dpxc.html
    patronvideos  = 'vidbull.com/(?:embed-|)([A-Z0-9a-z]+)'
    logger.info("pelisalacarta.servers.vidbull find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[vidbull]"
        url = "http://vidbull.com/"+match+".html"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vidbull' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
