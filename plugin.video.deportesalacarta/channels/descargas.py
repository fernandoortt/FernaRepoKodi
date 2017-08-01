# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta 4
# Copyright 2015 tvalacarta@gmail.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#
# Distributed under the terms of GNU General Public License v3 (GPLv3)
# http://www.gnu.org/licenses/gpl-3.0.html
# ------------------------------------------------------------
# This file is part of pelisalacarta 4.
#
# pelisalacarta 4 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pelisalacarta 4 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pelisalacarta 4.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------
# Lista de vídeos descargados
# ------------------------------------------------------------
import os
import sys

from core import config
from core import downloadtools
from core import logger
from core import servertools
from core.item import Item
from lib.sambatools import libsmb as samba
from core import filetools

import favoritos
import xbmc

CHANNELNAME = "descargas"
DEBUG = config.get_setting("debug")
DOWNLOAD_LIST_PATH = config.get_setting("downloadlistpath")
downloadpath = config.get_setting("downloadpath")


# if DOWNLOAD_LIST_PATH.startswith("special://") or downloadpath.startswith("special://"):
#     logger.info("channels.descargas Se esta usando el protocolo 'special'")
# else:
#     logger.info("channels.descargas Se esta usando una ruta convencional")
if DOWNLOAD_LIST_PATH.startswith("special://"):
    DOWNLOAD_LIST_PATH = xbmc.translatePath(config.get_setting("downloadlistpath"))
    # logger.info("channels.descargas DOWNLOAD_LIST_PATH convertido= " +
    #             DOWNLOAD_LIST_PATH)
else:
    DOWNLOAD_LIST_PATH = config.get_setting("downloadlistpath")
    # logger.info("channels.descargas DOWNLOAD_LIST_PATH= " +
    #             DOWNLOAD_LIST_PATH)
# Lee la ruta de descargas
if downloadpath.startswith("special://"):
    downloadpath = xbmc.translatePath(config.get_setting("downloadpath"))
    # logger.info("channels.descargas downloadpath convertido= " + downloadpath)
else:
    downloadpath = config.get_setting("downloadpath")
    # logger.info("channels.descargas downloadpath= " + downloadpath)


IMAGES_PATH = filetools.join(config.get_runtime_path(), 'resources', 'images')
ERROR_PATH = filetools.join(DOWNLOAD_LIST_PATH, 'error')
usingsamba = samba.usingsamba(DOWNLOAD_LIST_PATH)


def mainlist(item):
    logger.info("[descargas.py] mainlist")
    itemlist = []

    # Lee la ruta de descargas
    downloadpath = config.get_setting("downloadpath")

    logger.info("[descargas.py] downloadpath=" + downloadpath)

    itemlist.append(Item(channel="descargas", action="pendientes", title="Descargas pendientes"))
    itemlist.append(Item(channel="descargas", action="errores", title="Descargas con error"))

    # Añade al listado de XBMC
    try:
        ficheros = os.listdir(downloadpath)
        for fichero in ficheros:
            logger.info("[descargas.py] fichero=" + fichero)
            if fichero != "lista" and fichero != "error" and fichero != ".DS_Store" and not fichero.endswith(".nfo") \
                    and not fichero.endswith(".tbn") \
                    and os.path.join(downloadpath, fichero) != config.get_setting("downloadlistpath"):
                url = os.path.join(downloadpath, fichero)
                if not os.path.isdir(url):
                    itemlist.append(Item(channel="descargas", action="play", title=fichero, fulltitle=fichero, url=url,
                                         server="local", folder=False))

    except:
        logger.info("[descargas.py] exception on mainlist")
        pass

    return itemlist


def pendientes(item):
    logger.info("[descargas.py] pendientes")
    itemlist = []

    # Crea un listado con las entradas de favoritos
    if usingsamba:
        ficheros = samba.get_files(DOWNLOAD_LIST_PATH)
    else:
        ficheros = os.listdir(DOWNLOAD_LIST_PATH)

    # Ordena el listado por orden de incorporación
    ficheros.sort()

    # Crea un listado con las entradas de la lista de descargas
    for fichero in ficheros:
        logger.info("fichero="+fichero)
        try:
            # Lee el bookmark
            canal, titulo, thumbnail, plot, server, url, fulltitle = favoritos.readbookmark(fichero, DOWNLOAD_LIST_PATH)
            if canal == "":
                canal = "descargas"

            logger.info("canal="+canal+", titulo="+titulo+", thumbnail="+thumbnail+", server="+server+", url="+url +
                        ", fulltitle="+fulltitle+", plot="+plot)

            # Crea la entrada
            # En la categoría va el nombre del fichero para poder borrarlo
            itemlist.append(Item(channel=canal, action="play", url=url, server=server, title=titulo,
                                 fulltitle=fulltitle, thumbnail=thumbnail, plot=plot, fanart=thumbnail,
                                 extra=os.path.join(DOWNLOAD_LIST_PATH, fichero), folder=False))

        except:
            pass
            logger.info("[descargas.py] error al leer bookmark")
            for line in sys.exc_info():
                logger.error("%s" % line)

    itemlist.append(Item(channel=CHANNELNAME, action="downloadall", title="(Empezar la descarga de la lista)",
                         thumbnail=os.path.join(IMAGES_PATH, "Crystal_Clear_action_db_update.png"), folder=False))

    return itemlist


def errores(item):
    logger.info("[descargas.py] errores")
    itemlist = []

    # Crea un listado con las entradas de favoritos
    if usingsamba:
        ficheros = samba.get_files(ERROR_PATH)
    else:
        ficheros = os.listdir(ERROR_PATH)

    # Ordena el listado por orden de incorporación
    ficheros.sort()

    # Crea un listado con las entradas de la lista de descargas
    for fichero in ficheros:
        logger.info("[descargas.py] fichero="+fichero)
        try:
            # Lee el bookmark
            canal, titulo, thumbnail, plot, server, url, fulltitle = favoritos.readbookmark(fichero, ERROR_PATH)
            if canal == "":
                canal = "descargas"

            # Crea la entrada
            # En la categoría va el nombre del fichero para poder borrarlo
            itemlist.append(Item(channel=canal, action="play", url=url, server=server, title=titulo,
                                 fulltitle=fulltitle, thumbnail=thumbnail, plot=plot, fanart=thumbnail,
                                 category="errores", extra=os.path.join(ERROR_PATH, fichero), folder=False))

        except:
            pass
            logger.info("[descargas.py] error al leer bookmark")
            for line in sys.exc_info():
                logger.error("%s" % line)

    return itemlist


def downloadall(item):
    logger.info("[descargas.py] downloadall")

    # Lee la lista de ficheros
    if usingsamba:
        ficheros = samba.get_files(DOWNLOAD_LIST_PATH)
    else:
        ficheros = os.listdir(DOWNLOAD_LIST_PATH)

    logger.info("[descargas.py] numero de ficheros=%d" % len(ficheros))

    # La ordena
    ficheros.sort()

    # Crea un listado con las entradas de favoritos
    for fichero in ficheros:
        # El primer video de la lista
        logger.info("[descargas.py] fichero="+fichero)

        if fichero != "error" and fichero != ".DS_Store":
            # Descarga el vídeo
            try:
                # Lee el bookmark
                canal, titulo, thumbnail, plot, server, url, fulltitle = \
                    favoritos.readbookmark(fichero, DOWNLOAD_LIST_PATH)
                logger.info("[descargas.py] url="+url)

                # Averigua la URL del vídeo
                video_urls, puedes, motivo = servertools.resolve_video_urls_for_playing(server, url, "", False)

                # La última es la de mayor calidad, lo mejor para la descarga
                mediaurl = video_urls[len(video_urls)-1][1]
                logger.info("[descargas.py] mediaurl="+mediaurl)

                # Genera el NFO
                nfofilepath = downloadtools.getfilefromtitle("sample.nfo", fulltitle)
                outfile = open(nfofilepath, "w")
                outfile.write("<movie>\n")
                outfile.write("<title>("+fulltitle+")</title>\n")
                outfile.write("<originaltitle></originaltitle>\n")
                outfile.write("<rating>0.000000</rating>\n")
                outfile.write("<year>2009</year>\n")
                outfile.write("<top250>0</top250>\n")
                outfile.write("<votes>0</votes>\n")
                outfile.write("<outline></outline>\n")
                outfile.write("<plot>"+plot+"</plot>\n")
                outfile.write("<tagline></tagline>\n")
                outfile.write("<runtime></runtime>\n")
                outfile.write("<thumb></thumb>\n")
                outfile.write("<mpaa>Not available</mpaa>\n")
                outfile.write("<playcount>0</playcount>\n")
                outfile.write("<watched>false</watched>\n")
                outfile.write("<id>tt0432337</id>\n")
                outfile.write("<filenameandpath></filenameandpath>\n")
                outfile.write("<trailer></trailer>\n")
                outfile.write("<genre></genre>\n")
                outfile.write("<credits></credits>\n")
                outfile.write("<director></director>\n")
                outfile.write("<actor>\n")
                outfile.write("<name></name>\n")
                outfile.write("<role></role>\n")
                outfile.write("</actor>\n")
                outfile.write("</movie>")
                outfile.flush()
                outfile.close()
                logger.info("[descargas.py] Creado fichero NFO")

                # Descarga el thumbnail
                if thumbnail != "":
                    logger.info("[descargas.py] thumbnail="+thumbnail)
                    thumbnailfile = downloadtools.getfilefromtitle(thumbnail, fulltitle)
                    thumbnailfile = thumbnailfile[:-4] + ".tbn"
                    logger.info("[descargas.py] thumbnailfile="+thumbnailfile)
                    try:
                        downloadtools.downloadfile(thumbnail, thumbnailfile)
                        logger.info("[descargas.py] Thumbnail descargado")
                    except:
                        logger.info("[descargas.py] error al descargar thumbnail")
                        for line in sys.exc_info():
                            logger.error("%s" % line)

                # Descarga el video
                dev = downloadtools.downloadbest(video_urls, fulltitle)
                if dev == -1:
                    # El usuario ha cancelado la descarga
                    logger.info("[descargas.py] Descarga cancelada")
                    return
                elif dev == -2:
                    # Error en la descarga, lo mueve a ERROR y continua con el siguiente
                    logger.info("[descargas.py] ERROR EN DESCARGA DE "+fichero)
                    if not usingsamba:
                        origen = os.path.join(DOWNLOAD_LIST_PATH, fichero)
                        destino = os.path.join(ERROR_PATH, fichero)
                        import shutil
                        shutil.move(origen, destino)
                    else:
                        favoritos.savebookmark(canal, titulo, url, thumbnail, server, plot, fulltitle, ERROR_PATH)
                        favoritos.deletebookmark(fichero, DOWNLOAD_LIST_PATH)
                else:
                    logger.info("[descargas.py] Video descargado")
                    # Borra el bookmark e itera para obtener el siguiente video
                    filepath = os.path.join(DOWNLOAD_LIST_PATH, fichero)
                    if usingsamba:
                        os.remove(filepath)
                    else:
                        favoritos.deletebookmark(fichero, DOWNLOAD_LIST_PATH)
                    logger.info("[descargas.py] "+fichero+" borrado")
            except:
                logger.info("[descargas.py] ERROR EN DESCARGA DE "+fichero)
                import sys
                for line in sys.exc_info():
                    logger.error("%s" % line)
                if not usingsamba:
                    origen = os.path.join(DOWNLOAD_LIST_PATH, fichero)
                    destino = os.path.join(ERROR_PATH, fichero)
                    import shutil
                    shutil.move(origen, destino)
                else:
                    favoritos.savebookmark(canal, titulo, url, thumbnail, server, plot, fulltitle, ERROR_PATH)
                    favoritos.deletebookmark(fichero, DOWNLOAD_LIST_PATH)


def savebookmark(canal=CHANNELNAME, titulo="", url="", thumbnail="", server="", plot="", fulltitle="",
                 savepath=DOWNLOAD_LIST_PATH):
    favoritos.savebookmark(canal, titulo, url, thumbnail, server, plot, fulltitle, savepath)


def deletebookmark(fullfilename, deletepath=DOWNLOAD_LIST_PATH):
    favoritos.deletebookmark(fullfilename, deletepath)


def delete_error_bookmark(fullfilename, deletepath=ERROR_PATH):
    favoritos.deletebookmark(fullfilename, deletepath)


def mover_descarga_error_a_pendiente(fullfilename):
    # La categoría es el nombre del fichero en favoritos, así que lee el fichero
    canal, titulo, thumbnail, plot, server, url, fulltitle = favoritos.readbookmark(fullfilename, "")
    # Lo añade a la lista de descargas
    savebookmark(canal, titulo, url, thumbnail, server, plot, fulltitle)
    # Y lo borra de la lista de errores
    os.remove(fullfilename)
