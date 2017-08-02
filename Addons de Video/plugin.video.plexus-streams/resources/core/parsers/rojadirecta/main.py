# -*- coding: utf-8 -*-

"""
Rojadirecta
"""

import sys,os
current_dir = os.path.dirname(os.path.realpath(__file__))
basename = os.path.basename(current_dir)
core_dir =  current_dir.replace(basename,'').replace('parsers','')
sys.path.append(core_dir)
from utils.webutils import *
from utils.pluginxbmc import *
from utils.directoryhandle import *
from utils.parsers import parser_resolver

base_url = "http://www.rinconrojadirecta.com/rd/rd.php"

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: rojadirecta_events()
	elif parserfunction == 'resolve_and_play': parser_resolver(name,url,os.path.join(current_dir,'icon.png'))

def rojadirecta_events():
	try:
		source = get_page_source(base_url)
	except Exception as e: source = "";xbmcgui.Dialog().ok(translate(40000),str(e))
	if source:
		#print source
		match = re.findall('<span class="(\d+)".*?<div class="menutitle".*?<span class="t">([^<]+)</span>(.*?)</div>',source,re.DOTALL)
		#print match
		for id,time,eventtmp in match:
			try:
				import datetime
				from utils import pytzimp
				d = pytzimp.timezone(str(pytzimp.timezone('Europe/Madrid'))).localize(datetime.datetime(2014, 6, 7, hour=int(time.split(':')[0]), minute=int(time.split(':')[-1])))
				timezona= settings.getSetting('timezone_new')
				my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
				convertido=d.astimezone(my_location)
				fmt = "%H:%M"
				time=convertido.strftime(fmt)
			except:pass
			eventnospanish = re.findall('<span class="es">(.+?)</span>', eventtmp)
			if eventnospanish:
				for spanishtitle in eventnospanish:
						eventtmp = eventtmp.replace('<span class="es">' + spanishtitle + '</span>','')
			eventclean=eventtmp.replace('<span class="en">','').replace('</span>','').replace(' ()','').replace('</time>','').replace('<span itemprop="name">','')
			matchdois = re.findall('(.*)<b>\s*(.*?)\s*</b>', eventclean)
			for sport,event in matchdois:
				express = '<span class="submenu" id="sub' + id+ '">.*?</span>\s*</span>'
				streams = re.findall(express,source,re.DOTALL)
				for streamdata in streams:
					p2pstream = re.findall('<td>P2P</td>[^<]+<td>([^<]*)</td>[^<]+<td>([^<]*)</td>[^<]+<td>([^<]*)</td>[^<]+<td>([^<]*)</td>[^<]+<td><b><a.+?href="(.+?)"', streamdata, re.DOTALL)
					already = False
					for canal,language,tipo,qualidade,urltmp in p2pstream:
						if "Sopcast" in tipo or "Acestream" in tipo:
							if not already:
								addLink("[B][COLOR orange]"+time+ " - " + sport + " - " + event + "[/B][/COLOR]",'',os.path.join(current_dir,'icon.png'))
								already = True
							if "ArenaVision" in canal: thumbnail = os.path.join(current_dir,'media','arenavisionlogo.png')
							elif "Vertigo" in canal: thumbnail = os.path.join(current_dir,'media','vertigologo.png')
							elif "Vikingo" in canal: thumbnail = os.path.join(current_dir,'media','vikingologo.png')
							elif "futbolsinlimites" in canal: thumbnail = os.path.join(current_dir,'media','futbolsinlimiteslogo.png')
							elif "La Catedral" in canal: thumbnail = os.path.join(current_dir,'media','lacatedrallogo.png')
							else: thumbnail = os.path.join(current_dir,'icon.png')
							addDir("[B]["+tipo.replace("<","").replace(">","")+"][/B]-"+canal.replace("<","").replace(">","")+" - ("+language.replace("<","").replace(">","")+") - ("+qualidade.replace("<","").replace(">","")+" Kbs)",urltmp[urltmp.rfind("http://"):],401,thumbnail,43,False,parser='rojadirecta',parserfunction='resolve_and_play')
					p2pdirect = re.findall('<td>P2P</td><td></td><td></td><td>(.+?)</td><td></td><td>.+?href="(.+?)"', streamdata)
					for tipo,link in p2pdirect:
						if tipo == "SopCast" and "sop://" in link:
							addDir("[B][SopCast][/B]- (no info)",link,401,os.path.join(current_dir,'icon.png'),43,False,parser='rojadirecta',parserfunction='resolve_and_play')
        #xbmc.executebuiltin("Container.SetViewMode(51)")

