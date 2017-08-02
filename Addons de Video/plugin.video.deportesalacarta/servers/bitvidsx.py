# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para bitvidsx ex videoweed
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re

from core import logger
from core import scrapertools


# Returns an array of possible video url's from the page_url
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

    # http://www.videoweed.es/api/player.api.php?cid=undefined&cid2=undefined&file=31f8c26a80d23&cid3=undefined&key=88%2E0%2E189%2E203%2Dd3cb0515a1ed66e5b297da999ed23b42%2D&numOfErrors=0&user=undefined&pass=undefined 
    parameters="cid=undefined&cid2=undefined&file="+file_parameter+"&cid3=undefined&key="+filekey_parameter+"&numOfErrors=0&user=undefined&pass=undefined"
    url = "http://www.bitvid.sx/api/player.api.php?"+parameters
    headers.append(["Referer",page_url])
    data = scrapertools.cache_page(url,headers=headers)
    logger.info(data)
    patron = 'url=(.*?)&title='
    matches = re.compile(patron).findall(data)
    scrapertools.printMatches(matches)
    
    video_urls = []
    logger.info(matches[0])
    video_urls.append( [".flv [bitvidsx]",matches[0]])
    
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []    
    data = data.replace('videoweed.es','bitvid.sx')
    
    patronvideos  = '(http://www.bitvid.[a-z]+/file/[a-zA-Z0-9]+)'
    logger.info("[bitvidsx.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[bitvidsx]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'bitvidsx' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #logger.info("1) Videoweed formato islapeliculas") #http://embed.videoweed.com/embed.php?v=h56ts9bh1vat8
    patronvideos  = "(http://embed.bitvid.*?)&"
    logger.info("[bitvidsx.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[bitvidsx]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'bitvidsx' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
           
    #rep="/rep2.php?vw=wuogenrzatq40&t=18&c=13"
    patronvideos  = 'src="" rep="([^"]+)" width="([^"]+)" height="([^"]+)"'
    logger.info("[bitvidsx.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[bitvidsx]"
        url = match[0]
        url = url.replace("/rep2.php?vw=","http://www.bitvid.sx/file/")
        
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'bitvidsx' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
