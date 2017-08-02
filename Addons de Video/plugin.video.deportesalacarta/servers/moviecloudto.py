# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para moviecloudto
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

from core.scrapertools import *

def test_video_exists( page_url ):
    logger.info("[moviecloudto.py] test_video_exists(page_url='%s')" % page_url)

    data = cache_page( page_url )

    if "<title>Video Stream - Moviecloud.to</title>" not in data:
        return False, "El vídeo no existe en el servidor"

    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[moviecloudto.py] get_video_url(page_url='%s')" % page_url)

    data = cache_page( page_url )
    media_url = get_match(data,'file: "([^"]+)"')

    video_urls = [ [ get_filename_from_url(media_url)[-4:]+" [moviecloudto]" , media_url ] ]

    for video_url in video_urls:
        logger.info("[moviecloudto.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    ## Patrones
    #http://moviecloud.to/<id>
    #http://moviecloud.to/<id>/<name>.<ext>
    #http://moviecloud.to/plugins/mediaplayer/site/_embed.php?u=<id>&w=600&h=330
    patterns = [
        'moviecloud.to/([A-Za-z0-9]+)$',
        'moviecloud.to/([A-Za-z0-9]+)/',
        'moviecloud.to/plugins/mediaplayer/site/_embed.php?u=([A-Za-z0-9]+)&'
    ]

    for pattern in patterns:

        logger.info("[moviecloudto.py] find_videos #"+pattern+"#")
        matches = re.compile(pattern,re.DOTALL).findall(data)

        url = "http://moviecloud.to/plugins/mediaplayer/site/_embed.php?u=%s&w=600&h=330"

        for match in matches:
            titulo = "[moviecloud.to]"
            url = url % match
            if url not in encontrados:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'moviecloudto' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)

    return devuelve
