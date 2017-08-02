# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para nosvideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re, os

from core import config
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("deportesalacarta.servers.nosvideo.py test_video_exists(page_url='%s')" % page_url)


    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("deportesalacarta.servers.gdrive.py get_video_url(page_url='%s')" % page_url)
    video_urls = []

    # Lee la URL
    #page_url = "https://drive.google.com/file/d/0B8_IF8XF7tZDSkdmR05Jbks4R00/preview"
    data = scrapertools.downloadpage(page_url)
    logger.info(data)
    data = data.decode('unicode-escape')
    
    fmt_stream_map = scrapertools.find_single_match(data, '"fmt_stream_map"\s*,\s*"([^"]+)').split(',')
    
    for stream in fmt_stream_map:
        logger.info(stream)
        fmt_id, video_url = stream.split('|')
        video_urls.append([" [gdrive]", video_url])

    for video_url in video_urls:
        logger.info("deportesalacarta.servers.gdrive.py %s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # https://drive.google.com/file/d/0B8_IF8XF7tZDSkdmR05Jbks4R00/preview
    patronvideos = 'drive.google.com/(file/d/.../preview)'
    logger.info("deportesalacarta.servers.gdrive.py find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[gdrive]"
        url = "https://drive.google.com/%s" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'gdrive'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)


    return devuelve
