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
# Configuracion
# ------------------------------------------------------------

from core import config
from core.item import Item
from core import logger
from platformcode import platformtools

CHANNELNAME = "configuracion"


def mainlist(item):
    logger.info("deportes.channels.configuracion mainlist")

    itemlist = []
    itemlist.append(Item(channel=CHANNELNAME, title="Preferencias", action="settings", folder=False))
    itemlist.append(Item(channel=CHANNELNAME, title="[COLOR indianred]Configuración Ventana \"Info del partido\"[/COLOR]", action="config_", thumbnail="http://s6.postimg.org/etyqbs3o1/miscelania.png",fanart="http://i.imgur.com/Bt9PHVR.jpg?1", folder=False))
    itemlist.append(Item(channel=CHANNELNAME, title="", action="", folder=False))

    itemlist.append(Item(channel=CHANNELNAME, title="Comprobar actualizaciones", action="check_for_updates", folder=False))
    itemlist.append(Item(channel=CHANNELNAME, title="Ver cambios entre versiones", action="show_changes", folder=False))

    return itemlist


def config_(item):
    from core import channeltools
    dialog = platformtools.dialog_yesno("Configuración Info Partido", "       Selecciona el modo de inicio", yeslabel="Ventana", nolabel="Pantalla Completa")
    if dialog == 1:
        channeltools.set_channel_setting("modo", False, "futbol_window")
    elif dialog == 0:
        channeltools.set_channel_setting("modo", True, "futbol_window")


def check_for_updates(item):
    from core import updater
  
    try:
        update, version_publicada, message, url_repo, server = updater.check()

        if update:
            yes_pressed = platformtools.dialog_yesno("¿Quieres instalarla?", "Versión "+version_publicada+" disponible",
                                    message)
      
            if yes_pressed:
                item.version = version_publicada
                item.url = url_repo
                item.server = server
                updater.actualiza(item)
        else:
            platformtools.dialog_ok("No hay ninguna actualización disponible", "Addon ya actualizado a su última versión")

    except:
        import traceback
        logger.info(traceback.format_exc())
        platformtools.dialog_ok("No hay ninguna actualización disponible", "Addon ya actualizado a su última versión")


def settings(item):
    config.open_settings()


def show_changes(item):
    import xbmcgui
    from core import filetools
    texto = filetools.read(filetools.join(config.get_runtime_path(), 'changelog.txt'))
    return xbmcgui.Dialog().textviewer("Changelog", texto)
