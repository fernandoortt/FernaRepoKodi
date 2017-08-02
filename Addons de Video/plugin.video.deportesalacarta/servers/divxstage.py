# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para divxstage
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

from core import scrapertools
from core import logger

host = "http://www.cloudtime.to"
api = host + "/api/player.api.php"

def test_video_exists( page_url ):
    logger.info("[divxstage.py] test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url.replace('/embed/?v=','/video/'))

    if "This file no longer exists" in data:
        return False, "El archivo no existe<br/>en divxstage o ha sido borrado."

    return True, ""

def get_video_url(page_url, premium = False, user="", password="", video_password=""):
    logger.info("[divxstage.py] get_video_url(page_url='%s')" % page_url)

    if "divxstage.net" in page_url:
        page_url = page_url.replace("divxstage.net","cloudtime.to")

    data = scrapertools.cache_page(page_url)

    filekey = scrapertools.find_single_match(data, 'flashvars.filekey=([^;]+);')
    file = scrapertools.find_single_match(data, 'flashvars.file="([^"]+)";')
    key = scrapertools.find_single_match(data, 'var %s="([^"]+)";' % filekey)

    data = api + '?cid2=undefined&pass=undefined&key=%s&cid=0&numOfErrors=0&user=undefined&file=%s&cid3=undefined' % (key, file)
    data = scrapertools.cache_page(data)

    errorUrl = scrapertools.find_single_match(data, 'url=(.+?)&title')

    data = api + '?errorUrl=%s&cid2=undefined&pass=undefined&errorCode=404&key=%s&cid=0&numOfErrors=1&user=undefined&file=%s&cid3=undefined' % (errorUrl, key, file)
    data = scrapertools.cache_page(data)

    media_url = scrapertools.find_single_match(data, 'url=(.+?)&title')

    video_urls = []
    if media_url != "":
        video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [divxstage]", media_url])

    for video_url in video_urls:
        logger.info("[divxstage.py] %s - %s" % (video_url[0], video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # divxstage http://www.divxstage.net/video/of7ww1tdv62gf"
    patronvideos  = 'divxstage[^/]+/video/(\w+)$'
    logger.info("[divxstage.py] find_videos #" + patronvideos + "#")
    matches = scrapertools.find_multiple_matches(data, patronvideos)

    for match in matches:
        titulo = "[Divxstage]"
        url = host + "/embed/?v=" + match
        if url not in encontrados:
            logger.info("url=" + url)
            devuelve.append([titulo, url, 'divxstage'])
            encontrados.add(url)
        else:
            logger.info("url duplicada=" + url)

    # divxstage http://www.cloudtime.to/video/of7ww1tdv62gf"
    patronvideos  = 'cloudtime[^/]+/video/(\w+)$'
    logger.info("[divxstage.py] find_videos #" + patronvideos + "#")
    matches = scrapertools.find_multiple_matches(data, patronvideos)

    for match in matches:
        titulo = "[Divxstage]"
        url = host + "/embed/?v=" + match
        if url not in encontrados:
            logger.info("url=" + url)
            devuelve.append([titulo, url, 'divxstage'])
            encontrados.add(url)
        else:
            logger.info("url duplicada=" + url)

    return devuelve

def test():
    video_urls = get_video_url(host + "/video/of7ww1tdv62gf")
    return len(video_urls)>0
