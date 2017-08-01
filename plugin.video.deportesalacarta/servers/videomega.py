# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videomega
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import jsunpack
from core import logger
from core import scrapertools


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("pelisalacarta.servers.videomega get_video_url(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)
    video_urls = []

    patron = r"(eval.function.p,a,c,k,e,.*?)\s*</script>"
    data = scrapertools.find_single_match(data, patron)
    if data != '':
        data = jsunpack.unpack(data)
        location = scrapertools.find_single_match(data, r'"src"\s*,\s*"([^"]+)')
        video_urls.append([scrapertools.get_filename_from_url(location)[-4:] + " [videomega]", location])

    for video_url in video_urls:
        logger.info("pelisalacarta.servers.videomega %s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

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

    return devuelve
