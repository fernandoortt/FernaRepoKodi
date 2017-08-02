# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Kodi Add-on for http://avezy.tk
# Version 1.2.1
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#------------------------------------------------------------
# Changelog:
# 1.2.1
# - Eliminar sopcast
# - Eliminar diferencia ace/sop
# 1.2.0
# - Nueva version plugintools 1.0.8
# - Muestra el idioma en el listado de canales
# 1.1.4
# - Gestion de errores en peticiones HTTP
# 1.1.3
# - Nueva URL para JSON
# 1.1.2
# - Colores distintos para ace/sop
# 1.1.1
# - Fix URL JSON
# 1.1.0
# - Soporte canales Sopcast
# 1.0.6
# - Cambio ubicacion repo
# 1.0.5
# - Auto actualizacion
# 1.0.4
# - Mostrar agenda completa
# - Pantalla de ajustes
# - Posibilidad elegir servidor (ToDo)
# - Iconos para categorias
# 1.0.3
# - First public release
# 1.0.2
# - Minor fixes
# 1.0.1
# - Use public URL
# 1.0.0
# - First release
#---------------------------------------------------------------------------

import os
import sys
import urllib
import urllib2
import json
from datetime import date
from datetime import time
from datetime import datetime
import plugintools
import tools
import xbmcgui
import xbmcaddon
import xbmcplugin

addon         = xbmcaddon.Addon('plugin.video.arenavisionezy')
addon_id      = addon.getAddonInfo('id')
addon_name    = addon.getAddonInfo('name')
addon_version = addon.getAddonInfo('version')

# Servidor origen
if addon.getSetting('av_source_server') == "0":
  parserJsonUrl = "https://avezy.tk/json.php"
elif addon.getSetting('av_source_server') == "1":
  parserJsonUrl = "http://arenavision.esy.es/json.php"
else:
  parserJsonUrl = "https://avezy.tk/json.php"

# Devel
#parserJsonUrl = "http://localhost/arena/json.php"

# Debug servidor seleccionado
tools.debug("arenavisionezy Servidor: " + addon.getSetting('av_source_server'))
tools.debug("arenavisionezy Json: " + parserJsonUrl)

# Entry point
def run():
    #plugintools.log("arenavisionezy.run")

    # Get params
    params = plugintools.get_params()
    plugintools.log("arenavisionezy.run " + repr(params))

    if params.get("action") is None:
        plugintools.log("arenavisionezy.run No hay accion")
        listado_categorias(params)
    else:
        action = params.get("action")
        plugintools.log("arenavisionezy.run Accion: " + action)
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def listado_categorias(params):
  plugintools.log("arenavisionezy.listado_categorias "+repr(params))

  # Definir URL del JSON
  jsonUrl = parserJsonUrl
  plugintools.log("arenavisionezy.listado_categorias Parsing: " + jsonUrl)
  
  # Peticion del JSON
  jsonSrc = makeRequest(jsonUrl)
  plugintools.log("arenavisionezy.listado_eventos Recibido jsonSrc: " + jsonSrc)

  # Comprobar formato respuesta
  if(is_json(jsonSrc) == False):
    errorTitle = 'Respuesta no JSON'
    errorMsg   = "La respuesta recibida no tiene formato JSON"
    mostrar_errores(errorTitle, errorMsg, jsonSrc)
    return

  # Cargar respuesta en json
  datos = json.loads(jsonSrc)

  # Comprobar error en la respuesta
  if('error' in datos):
    errorTitle = 'Error procesando categorias'
    errorMsg   = datos['msg']
    mostrar_errores(errorTitle, errorMsg)
    return
  
  categorias  = datos['categories']
  last_update = datos['last_update']
  
  # Informacion del evento
  titulo01 = "                    [COLOR skyblue]ArenaVision EZY[/COLOR] Version "+addon_version+" (Wazzu)"
  titulo02 = "                    [COLOR deepskyblue]Ultima actualizacion: "+last_update+"[/COLOR]"
  plugintools.add_item( title = titulo01 , thumbnail = generar_miniatura('default'), folder = False )
  plugintools.add_item( title = titulo02 , thumbnail = generar_miniatura('default'), folder = False )

  # Todos los eventos
  plugintools.add_item(
    action     = "mostrar_agenda" ,
    title      = "[COLOR deepskyblue][VER AGENDA COMPLETA][/COLOR]",
    plot       = '' ,
    url        = "plugin://plugin.video.arenavisionezy/?action=mostrar_agenda",
    thumbnail  = generar_miniatura('default'),
    isPlayable = True,
    folder     = True
  )

  # Listado de categorias
  for categoria in categorias:
      
      # Miniatura
      category_thumb = generar_miniatura(categoria['categoria'])
      plugintools.log("arenavisionezy.category_thumb "+category_thumb)
      
      # Items
      plugintools.add_item(
        action     = "listado_eventos" , 
        title      = "[UPPERCASE]" + categoria['categoria'] + "[/UPPERCASE]" + " (" +  categoria['items'] + " eventos)", 
        plot       = '' , 
        url        = "plugin://plugin.video.arenavisionezy/?action=listado_eventos&cat="+urllib.quote(categoria['categoria']),
        thumbnail  = category_thumb,
        isPlayable = True, 
        folder     = True
      )

# Listado de toda la agenda
def mostrar_agenda(params):
  plugintools.log("arenavisionezy.mostrar_agenda "+repr(params))

  # Parse json
  jsonUrl = parserJsonUrl + '?cat=all'
  plugintools.log("arenavisionezy.mostrar_agenda Parsing: " + jsonUrl)
  jsonSrc     = urllib2.urlopen(jsonUrl)
  datos       = json.load(jsonSrc)
  eventos     = datos['eventos']
  last_update = datos['last_update']

  # Titulo de la categoria
  titulo01 = "                [COLOR skyblue]Agenda completa[/COLOR] (actualizado: "+last_update+")"
  plugintools.add_item( title = titulo01 , thumbnail = generar_miniatura('default'), action='', url='', isPlayable = False, folder = False )

  # Para cada evento
  for evento in eventos:
    title     = "[COLOR skyblue]" + evento['fecha'] + " " + evento['hora'] + "[/COLOR] " + evento['titulo']
    plot      = ""
    thumbnail = generar_miniatura(evento['categoria'])
    url       = "plugin://plugin.video.arenavisionezy/?action=listado_canales&evento="+evento['id']
    plugintools.add_item(
      action="listado_canales" ,
      title=title ,
      plot=plot ,
      url=url ,
      thumbnail=thumbnail ,
      isPlayable=True,
      folder=True
    )

# Listado de eventos de una categoria
def listado_eventos(params):
  plugintools.log("Python Version: " + (sys.version))
  plugintools.log("arenavisionezy.listado_eventos "+repr(params))
  categoria = params['cat']
  
  # Parse json
  jsonUrl = parserJsonUrl + '?cat='+urllib.quote(categoria)
  plugintools.log("arenavisionezy.listado_eventos Parsing: " + jsonUrl)
  jsonSrc = makeRequest(jsonUrl)
  plugintools.log("arenavisionezy.listado_eventos Recibido jsonSrc: " + jsonSrc)

  # Cargar respuesta en json
  datos = json.loads(jsonSrc)

  # Comprobar error en la respuesta
  if('error' in datos):
    errorTitle = 'Error procesando eventos'
    errorMsg   = datos['msg']
    mostrar_errores(errorTitle, errorMsg)
    return

  eventos     = datos['eventos']
  last_update = datos['last_update']

  # Titulo de la categoria
  titulo01 = "                [COLOR skyblue][UPPERCASE]"+categoria+"[/UPPERCASE][/COLOR] (actualizado: "+last_update+")"
  plugintools.add_item( title = titulo01 , thumbnail = generar_miniatura('default'), action='', url='', isPlayable = False, folder = False )
  
  # Para cada evento
  for evento in eventos:
    # ToDo eventos del pasado
    #plugintools.log("Fecha: " + fecha_hora)
    #showDate = datetime.strptime(fecha_hora, "%d/%m/%y %H:%M:%S").date()
    #todayDate = datetime.today().date()
    #if(showDate < todayDate):
    #  color = 'grey'
    #else:
    #  color = 'skyblue'
    color = 'skyblue'
    title     = "[COLOR "+color+"]" + evento['fecha'] + " " + evento['hora'] + "[/COLOR] " + evento['titulo']
    plot      = ""
    thumbnail = generar_miniatura(categoria)
    url       = "plugin://plugin.video.arenavisionezy/?action=listado_canales&evento="+evento['id']
    plugintools.add_item(
      action="listado_canales" , 
      title=title , 
      plot=plot , 
      url=url ,
      thumbnail=thumbnail , 
      isPlayable=True, 
      folder=True
    )

# Listado de canales de un evento
def listado_canales(params):
  plugintools.log("arenavisionezy.listado_canales "+repr(params))
  evento = params['evento']
  
  # Parse json
  jsonUrl = parserJsonUrl + '?evento='+evento
  plugintools.log("arenavisionezy.listado_canales Parsing: " + jsonUrl)
  jsonSrc = makeRequest(jsonUrl)
  plugintools.log("arenavisionezy.listado_eventos Recibido jsonSrc: " + jsonSrc)

  # Cargar respuesta en json
  evento = json.loads(jsonSrc)

  # Comprobar error en la respuesta
  if('error' in evento):
    errorTitle = 'Error procesando canales'
    errorMsg   = evento['msg']
    mostrar_errores(errorTitle, errorMsg)
    return
    return
  
  # Datos del evento
  categoria = evento['categoria']
  titulo    = evento['titulo']
  fecha     = evento['fecha']
  canales   = evento['canales']

  # Informacion del evento
  titulo01 = "[COLOR skyblue] " + categoria + " - " + fecha + "[/COLOR]"
  plugintools.add_item( title = titulo01 , thumbnail = generar_miniatura('default'), isPlayable = True, folder = True )
  titulo01 = "[COLOR skyblue] " + titulo + "[/COLOR]"
  plugintools.add_item( title = titulo01 , thumbnail = generar_miniatura('default'), isPlayable = True, folder = True )

  # Canales del evento
  for canal in canales:
    canal_nombre = canal['canal']
    canal_enlace = canal['enlace']
    canal_idioma = canal['idioma']
    canal_mode   = canal['mode']
	
    etiqueta = "["+canal_idioma+"] [COLOR red]" + canal_nombre + "[/COLOR]" + " "

    etiqueta = etiqueta + "  " + titulo
    enlace   = "plugin://program.plexus/?url=" + canal_enlace + "&mode="+canal_mode+"&name=" + titulo
    plugintools.add_item( 
      title      = etiqueta , 
      url        = enlace , 
      thumbnail  = generar_miniatura(categoria) ,
      isPlayable = True, 
      folder     = False 
    )

# Ruta de la miniatura
def generar_miniatura(categoria):
  thumb = categoria.lower().replace(" ", "_")
  thumb_path = os.path.dirname(__file__) + "/resources/media/" + thumb + ".png"
  if(os.path.isfile(thumb_path)):
    # Miniatura especifica
    category_thumb = "special://home/addons/" + addon_id + "/resources/media/" + thumb + ".png"
  else:
    # Miniatura generica
    category_thumb = "special://home/addons/" + addon_id + "/resources/media/default.png"
  return category_thumb

# Mostrar errores
def mostrar_errores(titulo, mensaje, debug=""):
    plugintools.log("ERROR: " + titulo)

    errTitle = "[COLOR red][UPPERCASE]ERROR: " + titulo + "[/UPPERCASE][/COLOR]"
    errMsg   = mensaje + "[CR]Para mas informacion, por favor, consulta el registro."
    
    plugintools.add_item( title = errTitle, thumbnail = generar_miniatura('default'), action='', url='', isPlayable = False, folder = False )
    plugintools.add_item( title = errMsg, thumbnail = generar_miniatura('default'), action='', url='', isPlayable = False, folder = False )
    return

# Realizar peticion HTTP
def makeRequest(url):
  plugintools.log("makeRequest: " + url)

  try:
    req      = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data     = response.read()
    response.close()
    return data
  except urllib2.URLError, e:
    errorMsg = str(e)
    plugintools.log(errorMsg);
    xbmc.executebuiltin("Notification(ArenavisionEzy,"+errorMsg+")")
    data_err = []
    data_err.append(['error', True])
    data_err.append(['msg', errorMsg])
    data_err = json.dumps(data_err)
    data_err = "{\"error\":\"true\", \"msg\":\""+errorMsg+"\"}"
    return data_err

# Comprobar si la cadena es json
def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError, e:
        return False
    return True

# Main loop
run()