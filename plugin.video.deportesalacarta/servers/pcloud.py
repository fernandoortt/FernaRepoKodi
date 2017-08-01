# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para pCloud
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re

from core import config
from core import httptools
from core import logger
from core import scrapertools
from platformcode import platformtools


def test_video_exists( page_url ):
    logger.info("pelisalacarta.servers.pCloud test_video_exists(page_url='%s')" % page_url)
    
    data = httptools.downloadpage(page_url).data
    if "Invalid link" in data:
        return False, "[pCloud] El archivo no existe o ha sido borrado"
    elif '"overtraffic": true' in data and config.get_setting("pcloud") == "false":
        return False, "[pCloud] El acceso está limitado, se necesita una cuenta en pCloud. " \
                      "Puedes introducir una en la configuración del addon"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("pelisalacarta.servers.pCloud url="+page_url)

    data = httptools.downloadpage(page_url).data

    fileid = scrapertools.find_single_match(data, '"fileid":\s*(\d+)')
    size = float(scrapertools.find_single_match(data, '"size":\s*(\d+)'))
    code = scrapertools.find_single_match(data, '"code":\s*"([^"]+)"')
    usuario = config.get_setting("pclouduser")
    password = config.get_setting("pcloudpassword")
    if config.get_setting("pcloud") == "true" and usuario and password:
        from core import jsontools
        if '"overtraffic": true' in data:
            data_info = jsontools.load_json(httptools.downloadpage("https://api.pcloud.com/userinfo?username=%s&password=%s" % (usuario, password), hide=True).data)
            size_available = float(data_info['quota']- data_info['usedquota'])
            size_f = size/(1024**3)
            size_available_f = size_available/(1024**3)
            if size > size_available:
                platformtools.dialog_ok("Para continuar es necesario copiar el archivo a tu cuenta",
                                        "No dispones del espacio disponible suficiente para la copia",
                                        "Tamaño del archivo: %.3f GB" % size_f,
                                        "Espacio libre en tu cuenta: %.3f GB" % size_available_f)
                return []
            else:
                dialog = platformtools.dialog_yesno("Es necesario copiar el archivo a tu cuenta",
                                       "¿Quieres guardar el archivo en tu cuenta para reproducirlo?",
                                       "Tamaño del archivo: %.3f GB" % size_f,
                                       "Espacio libre en tu cuenta: %.3f GB" % size_available_f)
                if dialog:
                    url = "https://api.pcloud.com/copypubfile?code=%s&fileid=%s&tofolderid=0&username=%s&password=%s" % (code, fileid, usuario, password)
                    data_copy = jsontools.load_json(httptools.downloadpage(url, hide=True).data)
                    logger.debug("data=" + data_copy)
                    if data_copy.get("metadata", {}).get("fileid"):
                        fileid = data_copy["metadata"]["fileid"]
                else:
                    return []
        url = "https://api.pcloud.com/getfilelink?fileid=%s&tofolderid=0&username=%s&password=%s" % (fileid, usuario, password)
        data_link = jsontools.load_json(httptools.downloadpage(url, hide=True).data)
        logger.debug("data=" + data_link)
        video_urls = []
        for h in data_link["hosts"]:
            media_url = "http://%s%s" % (h, data_link["path"])
            ext = scrapertools.get_filename_from_url(media_url)[-4:]
            video_urls.append(["%s [pCloud]" % ext, media_url])
    else:        
        media_url = scrapertools.find_single_match(data,'"downloadlink":.*?"([^"]+)"')
        media_url = media_url.replace("\\","")

        video_urls = []
        video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:]+" [pCloud]", media_url])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0],video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # https://my.pcloud.com/publink/show?code=XZhKu7Z49dTa1sEfLX9Tjgk8tESFGfXTjk
    patronvideos  = "(my.pcloud.com/publink/show\?code=[A-z0-9]+)"
    logger.info("pelisalacarta.servers.pCloud find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[pCloud]"
        url = "https://%s" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'pCloud' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
