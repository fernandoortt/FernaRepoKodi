# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidzi
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools
from lib import jsunpack


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)
    if "embed" not in page_url:
        page_url = page_url.replace("http://vidzi.tv/", "http://vidzi.tv/embed-") + ".html"

    data = scrapertools.cache_page(page_url)
    logger.info("data=" + data)

    data = scrapertools.find_single_match(data,
                                          "<script type='text/javascript'>(eval\(function\(p,a,c,k,e,d.*?)</script>")
    logger.info("data=" + data)

    data = jsunpack.unpack(data)
    logger.info("data=" + data)

    video_urls = []
    media_urls = scrapertools.find_multiple_matches(data, 'file:"([^"]+)"')
    for media_url in media_urls:

        if not media_url.endswith("vtt"):
            video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [vidzi]", media_url])

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    devuelve = []

    patronvideos = 'vidzi.tv/embed-([a-z0-9A-Z]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vidzi]"
        url = "http://vidzi.tv/embed-" + match + ".html"
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'vidzi'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    patronvideos = 'vidzi.tv/([a-z0-9A-Z]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vidzi]"
        url = "http://vidzi.tv/embed-" + match + ".html"
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'vidzi'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)
    return devuelve
