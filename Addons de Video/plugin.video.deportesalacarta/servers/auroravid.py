
# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para novamov
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# Credits:
# Unwise and main algorithm taken from Eldorado url resolver
# https://github.com/Eldorados/script.module.urlresolver/blob/master/lib/urlresolver/plugins/novamov.py

import re

from core import logger
from core import scrapertools


def test_video_exists( page_url ):
    logger.info("[auroravid.py] test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)
    
    if "This file no longer exists on our servers" in data:
        return False,"El fichero ha sido borrado de novamov"

    elif "is being converted" in data:
        return False,"El fichero está en proceso todavía"

    return True,""

def get_video_url( page_url , premium = False , user="" , password="" , video_password="" ):
    logger.info("[bitvidsx.py] get_video_url(page_url='%s')" % page_url)
    headers = []
    headers.append( [ "User-Agent" , "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36" ] )
    headers.append( [ "Accept-Encoding","gzip,deflate,sdch" ] )
    data = scrapertools.cache_page(page_url,headers=headers)
    stepkey = scrapertools.get_match(data,'name="stepkey" value="(.+?)"')
    logger.info("data="+stepkey)
    post = "stepkey="+stepkey
    data = scrapertools.downloadpage(page_url,headers=headers,post=post)
    logger.info("data="+data)

    file_parameter = scrapertools.find_single_match(data,'flashvars\.file="([^"]+)"')
    logger.info("file_parameter="+file_parameter)

    filekey_parameter = scrapertools.find_single_match(data,'flashvars.filekey\="([^"]+)"')
    logger.info("filekey_parameter="+filekey_parameter)
    if filekey_parameter=="":
        filekey_parameter = scrapertools.find_single_match(data,'fkz="([^"]+)"')
        logger.info("filekey_parameter="+filekey_parameter)
    #88%2E0%2E189%2E203%2Dd3cb0515a1ed66e5b297da999ed23b42%2D
    filekey_parameter = filekey_parameter.replace(".","%2E")
    filekey_parameter = filekey_parameter.replace("-","%2D")
    logger.info("filekey_parameter="+filekey_parameter)

    parameters="cid=undefined&cid2=undefined&file="+file_parameter+"&cid3=undefined&key="+filekey_parameter+"&numOfErrors=0&user=undefined&pass=undefined"
    url = "http://www.auroravid.to/api/player.api.php?"+parameters
    headers.append(["Referer",page_url])
    data = scrapertools.cache_page(url,headers=headers)
    logger.info(data)
    patron = 'url=(.*?)&title='
    matches = re.compile(patron).findall(data)
    scrapertools.printMatches(matches)
    
    video_urls = []
    logger.info(matches[0])
    video_urls.append( [".flv [auroravid]",matches[0]])

    return video_urls

def find_videos(data):
    encontrados = set()
    devuelve = []
    data = data.replace('novamov.com','auroravid.to')

    patronvideos = 'auroravid.to/video/([a-z0-9]{13})'
    logger.info("[auroravid.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[auroravid]"
        url = "http://www.auroravid.to/video/"+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'auroravid' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://embed.novamov.com/embed.php?width=568&height=340&v=zadsdfoc0pirx&px=1
    # http://embed.novamov.com/embed.php?width=620&amp;height=348&amp;v=4f21e91a1f2f7&amp;px=1&amp;px=1
    patronvideos = 'http://embed.auroravid.to/embed.php.*?v=([a-z0-9]{13})'
    logger.info("[auroravid.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[auroravid]"
        url = "http://www.auroravid.to/video/"+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'auroravid' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
