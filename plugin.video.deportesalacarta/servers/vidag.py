# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidag
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[vidag.py] url="+page_url)
    video_urls=[]
    
    data = scrapertools.cache_page(page_url)
    patron = '\|([^\|]{35,})\|'
    matches = re.compile(patron,re.DOTALL).findall(data)
    video="http://vid.ag/"+matches[0]+".m3u8"
    video_urls.append([scrapertools.get_filename_from_url(video)[-5:],video])
    
    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    
    devuelve = []

    # http://www.vidag.com/3360qika02mo/whale.wars.s04e10.hdtv.xvid-momentum.avi.html
    patronvideos  = '(http://vid.ag/embed-[A-Z0-9a-z]+\.html)'
    logger.info("[vidag.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[vidag]"
        url = match
        devuelve.append( [ titulo , url , 'vidag' ] )
        
            
    return devuelve
