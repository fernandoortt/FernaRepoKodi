# -*- coding: utf-8 -*-
#------------------------------------------------------------
# deportesalacarta - XBMC Plugin
#------------------------------------------------------------

import re
import datetime
import urllib
from core import httptools
from core.scrapertools import *

from core import filetools
from core import config

host = "http://www.resultados-futbol.com/"

def get_matches(url):
    data = httptools.downloadpage(url, cookies=False).data
    data = re.sub(r"\n|\r|\t", '', data)
    
    now = datetime.datetime.today()
    prio = ["Primera Divisi\xc3\xb3n", "Segunda Divisi\xc3\xb3n", "Copa del Rey", "Premier League", "Serie A", "Bundesliga", "Champions League",
            "Mundial", "Eurocopa", "Supercopa Europa", "Mundial de Clubes", "Supercopa"]
    prio2 = ["Ligue 1", "Liga Portuguesa", "Liga Holandesa", "Europa League", "Clasificación Mundial Europa",
             "Clasificación Mundial Sudamérica", "EFL Cup", "FA Cup"]
    partidos = []
    bloques = find_multiple_matches(data, '<div class="title">.*?<a.*?>(.*?) »</a>(.*?)</table>')
    for liga, bloque in bloques:
        priority = 3
        if liga in prio:
            priority = 1
        elif "Clasificación Mundial Sudamérica" in liga or "Clasificación Mundial Europa" in liga or "Mundial Grupo" in liga \
            or "Eurocopa Grupo" in liga or "Clasificación Eurocopa" in liga or liga in prio2:
            priority = 2

        patron = '<div class="chk_hour"[^>]+>([^<]+)<.*?<td class="timer">.*?>(.*?)</span>.*?' \
                 'src="([^"]+)".*?<a[^>]+>([^<]+)<.*?<a href="([^"]+)".*?<div class="clase" data-mid="([^"]+)"[^>]*>' \
                 '(.*?)</div>.*?src="([^"]+)".*?<a[^>]+>([^<]+)<'
        matches = find_multiple_matches(bloque, patron)
        for hora, estado, t1thumb, team1, url, matchid, score, t2thumb, team2 in matches:
            h, m = hora.split(":")
            time_match = datetime.datetime(now.year, now.month, now.day, int(h), int(m))
            estado = htmlclean(estado).replace("\xc2\xa0", "")
            t1thumb = t1thumb.rsplit("?", 1)[0].replace("/small/", "/original/")
            t2thumb = t2thumb.rsplit("?", 1)[0].replace("/small/", "/original/")
            if "chk_hour" in score or "Aplazado" in estado:
                score = "-- : --"
            score = htmlclean(score)
            canal = find_single_match(bloque, '<td class="icons"><img src="([^"]+)"')
            if canal:
                canal = canal.replace(".gif", ".png")
                if not canal.startswith(host):
                    canal = host + canal
            partidos.append({"url": url, "hora": hora, "team1": team1, "team2": team2, "score": score,
                             "thumb1": t1thumb, "thumb2": t2thumb, "estado": estado, "liga": liga,
                             "priority": priority, "time_match": time_match, "matchid": matchid,
                             "canal": canal})

    partidos.sort(key=lambda p:(p['priority'], p["time_match"]))
    next = find_single_match(data, '<li class="nav2 navsig">\s*<a href="([^"]+)"')
    prev = find_single_match(data, '<li class="nav2 navant">\s*<a href="([^"]+)"')
    today = find_single_match(data, '<span class="titlebox date">([^<]+)</span>').replace("Partidos ", "")
    partidos.append({"next": next, "prev": prev, "today": today})

    return partidos

def get_minutos(url):
    data = httptools.downloadpage(url, cookies=False).data
    data = re.sub(r"\n|\r|\t", '', data)
    minuto = find_single_match(data, '<span class="jor-status.*?>([^<]+)<').replace("DIRECTO (", "").replace(")", "")

    return minuto

def refresh_score():
    from core import jsontools
    try:
        data = httptools.downloadpage("http://www.resultados-futbol.com/ajax/refresh_live.php").data
        data = jsontools.load_json(data)
        if not data:
            data = {}
        return data
    except:
        return {}

def get_info(url, reload=False):
    data = httptools.downloadpage(url, cookies=False).data
    data = re.sub(r"\n|\r|\t", '', data)
    
    jornada = find_single_match(data, '<div class="jornada".*?>([^<]+)</a>')
    fecha = find_single_match(data, '<span itemprop="startDate"[^>]+>([^<]+)<')
    minuto = find_single_match(data, '<span class="jor-status.*?>([^<]+)<').replace("DIRECTO (", "").replace(")", "")

    try:
        score1, score2 = find_multiple_matches(data, '<span class="claseR"[^>]+>(\d+)')
        hora = ""
    except:
        score1 = score2 = ""
        hora = find_single_match(data, '<span class="chk_hour".*?>([^<]+)<')

    try:
        t1am, t1roj = find_single_match(data, '<div class="te1"><span class="am">(\d+)</span><span class="ro">(\d+)')
        t2am, t2roj = find_single_match(data, '<div class="te2"><span class="am">(\d+)</span><span class="ro">(\d+)')
    except:
        t1am = t1roj = t2am = t2roj = "0"

    ref = find_single_match(data, 'Arbitro:\s*([^<]+)</span>').replace("\xc2\xa0", "")
    stadium = find_single_match(data, 'Estadio:\s*([^<]+)</span>').replace("\xc2\xa0", "")

    team1 = find_single_match(data, '<div class="team equipo1".*?<b itemprop="name" title="([^"]+)"')
    team2 = find_single_match(data, '<div class="team equipo2".*?<b itemprop="name" title="([^"]+)"')
    thumb1 = find_single_match(data, '<div class="team equipo1".*?src="([^"]+)"').replace("/medium/", "/original/").rsplit("?", 1)[0]
    thumb2 = find_single_match(data, '<div class="team equipo2".*?src="([^"]+)"').replace("/medium/", "/original/").rsplit("?", 1)[0]
    url1 = find_single_match(data, '<div class="team equipo1".*?href="([^"]+)"')
    if url1 and not url1.startswith(host):
        url1 = host[:-1] + url1
    url2 = find_single_match(data, '<div class="team equipo2".*?href="([^"]+)"')
    if url2 and not url2.startswith(host):
        url2 = host[:-1] + url2
    info = {"jornada": jornada, "fecha": fecha, "minuto": minuto, "ref": ref, "url1": url1, "url2": url2,
            "score1": score1, "score2": score2, "hora": hora, "estadio": stadium,
            "t1am": t1am, "t1roj": t1roj, "t2am": t2am, "t2roj": t2roj, "name1": team1, "name2": team2,
            "thumb1": thumb1, "thumb2": thumb2}

    img_stadium = find_single_match(data, '<div id="tab_match_stadium" class="dm_estadio dm_box hidden">\s*<img src="([^"]+)"').replace("?size=x85", "")
    asistencia = find_single_match(data, '<span itemprop="attendees">([^<]+)</span>')
    capacidad = find_single_match(data, '<li><strong>Capacidad:</strong>([^<]+)</li>')
    if capacidad:
        capacidad = "Capacidad: " + capacidad
    dimen = find_single_match(data, '<li><strong>Dimensiones:</strong>([^<]+)</li>')
    if dimen:
        dimen = "Dimensiones: " + dimen
    inagura = find_single_match(data, '<li><strong>Inaguraci.*?>([^<]+)</li>')
    if inagura:
        inagura = "Inauguración: " + inagura
    info["stadium"] = {"stadium": stadium, "img_stadium": img_stadium, "asistencia": asistencia, "capacidad": capacidad, "dimen": dimen, "inagura": inagura}
    
    info["cronica"] = []
    matches = find_multiple_matches(data, '<tr class="post post_cronica(.*?)</tr>')
    for content in matches:
        bold = False
        if "cronica_bold" in content:
            bold = True
        destaca = False
        if "cronica_important" in content:
            destaca = True
        time = find_single_match(content, 'class="cronica_time_value">([^<]+)<')
        text = find_single_match(content, '<div class="cronica_content">(.*?)</div>').replace("\xc2\xa0", "")
        ico = find_single_match(content, 'src="([^"]+)"')
        info["cronica"].append({"text": text, "time": time, "ico": ico, "bold": bold, "destaca": destaca})

    info["team1"] = {}
    info["team1"]["formation"] = find_single_match(data, '<div class="team team1">.*?<small class="align-code">([^<]+)<')
    info["team1"]["once"] = []
    once = find_multiple_matches(data, 'id="dreamteam1"(.*?)</li>')
    if not once:
        bloque = find_single_match(data, '<div class="team team1">(.*?)</ul>')
        once = find_multiple_matches(bloque, '<li>\s*<small class="align-dorsal(.*?)</li>')
    for jug in once:
        name = find_single_match(jug, 'title="([^"]+)"')
        if not name:
            name = find_single_match(jug, 'href=.*?>(.*?)<')
        img = find_single_match(jug, 'src="([^"]+)"').replace("?size=38x&5", "")
        num = find_single_match(jug, '<span class="num".*?>(\d+)')
        if not num:
            num = find_single_match(jug, '<span class="align-dorsal.*?>(\d+)<')
        url = find_single_match(jug, 'href="([^"]+)"')
        #url = re.sub(r'/\d{4}/', '/', url)
        if url and not url.startswith(host):
            url = host[:-1] + url
        info["team1"]["once"].append({"name": name, "img": img, "num": num, "url": url})
    supl = find_multiple_matches(data, '<div class="team team1">.*?Suplentes(.*?)</ul>')
    info["team1"]["supl"] = []
    for bloque in supl:
        matches = find_multiple_matches(bloque, '<small class="align-dorsal ">(.*?)<.*?<a href="([^"]+)".*?>([^<]+)<')
        for num, url, name in matches:
            #url = re.sub(r'/\d{4}/', '/', url)
            if url and not url.startswith(host):
                url = host[:-1] + url
            info["team1"]["supl"].append({"num": num, "name": name, "url": url})

    info["team2"] = {}
    info["team2"]["formation"] = find_single_match(data, '<div class="team team2">.*?<small class="align-code">([^<]+)<')
    info["team2"]["once"] = []
    once = find_multiple_matches(data, 'id="dreamteam2"(.*?)</li>')
    if not once:
        bloque = find_single_match(data, '<div class="team team2">(.*?)</ul>')
        once = find_multiple_matches(bloque, '<li>\s*<small class="align-dorsal(.*?)</li>')
    for jug in once:
        name = find_single_match(jug, 'title="([^"]+)"')
        if not name:
            name = find_single_match(jug, 'href=.*?>(.*?)<')
        img = find_single_match(jug, 'src="([^"]+)"').replace("?size=38x&5", "")
        num = find_single_match(jug, '<span class="num".*?>(\d+)')
        if not num:
            num = find_single_match(jug, '<span class="align-dorsal.*?>(\d+)<')
        url = find_single_match(jug, 'href="([^"]+)"')
        #url = re.sub(r'/\d{4}/', '/', url)
        if url and not url.startswith(host):
            url = host[:-1] + url
        info["team2"]["once"].append({"name": name, "img": img, "num": num, "url": url})

    supl = find_multiple_matches(data, '<div class="team team2">.*?Suplentes(.*?)</ul>')
    info["team2"]["supl"] = []
    for bloque in supl:
        matches = find_multiple_matches(bloque, '<small class="align-dorsal ">(.*?)<.*?<a href="([^"]+)".*?>([^<]+)<')
        for num, url, name in matches:
            #url = re.sub(r'/\d{4}/', '/', url)
            if url and not url.startswith(host):
                url = host[:-1] + url
            info["team2"]["supl"].append({"num": num, "name": name, "url": url})

    sprites = {'1': 'gol', '2': 'anulado', '3': 'penalty_fallado', '4': 'lesion', '5': 'asistencia',
               '6': 'sale', '7': 'entra', '8': 'amarilla', '9': 'roja', '10': 'doble', '11': 'penalty',
               '12': 'propia', '13': 'poste'}
    info["eventos"] = []
    matches = find_multiple_matches(data, '<div class="evento"(.*?)</span></div></div>')
    for bloque in matches:
        minuto = find_single_match(bloque, '<b>minuto</b>\s*(\d+)\'')
        img = find_single_match(bloque, '<img src="([^"]+)"').replace("?size=38x&5", "")
        desc = find_single_match(bloque, '<small>(.*?)</a>')
        desc = htmlclean(desc)
        desc = re.compile("<h5[^>]*>",re.DOTALL).sub("", desc)
        equipo, evento = find_single_match(bloque, '<span class="(right|left) event_(\d+)">')
        equipo = equipo.replace("left", "l").replace("right", "v")
        url = find_single_match(bloque, '<a href="([^"]+)"')
        #url = re.sub(r'/\d{4}/', '/', url)
        if url and not url.startswith(host):
            url = host[:-1] + url
        try:
            evento = sprites[evento]
            evento = filetools.join(config.get_runtime_path(), 'resources', 'images', 'matchcenter', '%s.png' % evento)
        except:
            evento = ""

        info["eventos"].append({"minuto": minuto, "equipo": equipo, "evento": evento, "desc": desc, "img": img, "url": url})
    if info["eventos"]:
        info["eventos"].sort(key=lambda i:int(i["minuto"].zfill(2)))

    info["stats"] = []
    matches = find_multiple_matches(data, '<tr class="barstyle bar4">.*?>(\d+[%]*)<.*?<h6>([^<]+)<.*?>(\d+[%]*)<')
    for local, tipo, visit in matches:
        info["stats"].append({"l": local, "v": visit, "tipo": tipo})

    info["videos"] = []
    matches = find_multiple_matches(data, '<a target="[^"]*" href="([^"]+)" title="([^"]+)" class="list-title match-video-link">')
    for url, title in matches:
        url = url.replace("cc.sporttube.com/embed/", "www.sporttube.com/play/")
        info["videos"].append({"url": url, "title": title})

    info["news"] = []
    matches = find_multiple_matches(data, '<h2 class="ni-title"><a href="([^"]+)">([^<]+)<.*?<span class="ni-date">([^<]+)<')
    for url, title, date in matches:
        info["news"].append({"url": url, "title": title, "date": date})

    info["tv"] = []
    matches = find_multiple_matches(data, '<td class="dptvt_name">.*?src="([^"]+)" alt="([^"]+)".*?<td>([^<]+)<.*?<td>([^<]+)<')
    for logo, nombre, tipo, idioma in matches:
        if tipo == "WEB":
            continue
        logo = host + logo.replace(".gif", ".png")
        nombre = nombre + " / " + idioma
        info["tv"].append({'logo': logo, 'nombre': nombre})

    if url1 and not reload:
        info["coach1"], info["twitter1"], info["nombre_corto1"] = get_data_team(url1)
    if url2 and not reload:
        info["coach2"], info["twitter2"], info["nombre_corto2"] = get_data_team(url2)

    return info


def get_table(league):
    if not league.startswith("http"):
        league = "%s%s" % (host, league)
    data = httptools.downloadpage(league, cookies=False).data
    data = re.sub(r"\n|\r|\t", '', data)
    
    equipos = []
    liga2, liga = find_single_match(data, '<small class="temp".*?(?:>([^<]+)</h3>|<div class="botonlivs">).*?<h1 >([^<]+)</h1>')
    if liga2:
        liga += " - %s" % liga2

    temporadas = []
    bloque = find_single_match(data, '<div id="desplega_temporadas"(.*?)</ul>')
    matches = find_multiple_matches(bloque, '<li(.*?)><a href="([^"]+)">Temp. (\d+)')
    for estado, url, temp in matches:
        select = False
        if "act" in estado:
            select = True
        temp = "%s/%s" % (int(temp)-1, temp)
        temporadas.append({"url": url, "temp": temp, "select": select})

    patron = '<tr class="(?:impar|cmp)"><th class="([^"]+)">(\d+)</th>.*?src="([^"]+)".*?href=\'([^\']+)\'>([^<]+)<' \
             '.*?>(\d+)</td>.*?>(\d+)</td>.*?>(\d+)</td>.*?>(\d+)</td>.*?>(\d+)</td>.*?>(\d+)</td>' \
             '.*?>(\d+)</td>'
    matches = find_multiple_matches(data, patron)
    for color, pos, img, url, team, pts, pj, win, draw, lose, gf, gc in matches:
        img = img.replace("?size=37x&5", "").replace("small", "original")
        url = "%spartidos%s" % (host, url)
        if "-cha" in color:
            color = "green"
        elif "-prev" in color:
            color = "blue"
        elif "-uefa" in color:
            color = "red"
        elif "-desc" in color:
            color = "red_strong"
        else:
            color = "fo"
        equipos.append({"url": url, "team": team, "img": img, "pos": pos, "pts": pts, "pj": pj, "win": win,
                        "draw": draw, "lose": lose, "gf": gf, "gc": gc, "color": color, "liga": liga})

    return equipos, temporadas


def get_team_matches(team):
    data = httptools.downloadpage(team, cookies=False).data
    data = re.sub(r"\n|\r|\t", '', data)

    year1, year2 = find_single_match(data, '<span>Temporada (\d+)/(\d+)')
    meses = {'Ene': 1, 'Feb': 2, 'Mar': 3, 'Abr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Ago': 8,
           'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dic': 12}
    final = []
    next = []
    bloques = find_multiple_matches(data, '<div class="title"><img alt="(.*?)"(.*?)</table>')
    for torneo, bloque in bloques:
        patron = '<td class="time".*?>([^<]+)<.*?<td class="timer">.*?>([^<]+)</span.*?<td class="team-home">.*?<a.*?>([^<]+)<' \
             '.*?src="([^"]+)".*?href="([^"]+)".*?<div class="clase".*?>([^<]+)<.*?src="([^"]+)".*?<a.*?>([^<]+)<'
        matches = find_multiple_matches(bloque, patron)
        for fecha, status, team1, img1, url, score, img2, team2 in matches:
            img1 = img1.replace("?size=37x&5", "").replace("small", "original")
            img2 = img2.replace("?size=37x&5", "").replace("small", "original")
            status = status.replace("\xc2\xa0", "")
            dia, mes, year = fecha.split(" ")
            mes = meses[mes]
            if year == year1[2:]:
                year = year1
            else:
                year = year2
            fecha_ord = datetime.date(int(year), mes, int(dia))
            if "Finalizado" in status or "'" in status:
                if "'" in status:
                    score = "[COLOR red]%s[/COLOR]" % score
                final.append({"fecha": fecha, "team1": team1, "team2": team2, "img1": img1, "img2": img2,
                              "score": score, "url": url, "torneo": torneo, "fecha_ord": fecha_ord})
            else:
                next.append({"fecha": fecha, "team1": team1, "team2": team2, "img1": img1, "img2": img2,
                             "score": score, "url": url, "status": status, "torneo": torneo, "fecha_ord": fecha_ord})

    final.sort(key=lambda x:x["fecha_ord"])
    next.sort(key=lambda x:x["fecha_ord"])
    return final, next


def get_data_team(url):
    data = httptools.downloadpage(url, cookies=False).data
    data = re.sub(r"\n|\r|\t", '', data)
    coach = ""
    if not re.search(r'/(\d){4}', url):
        coach = find_single_match(data, 'name="managerNow" size="60" value="(.*?)"')
    nombre_corto = find_single_match(data, 'name="short_name" size="60" value="(.*?)"')
    twitter = find_single_match(data, 'name="twitter" size="60" value="(.*?)"')
    twitter = htmlclean(twitter)
    if twitter.startswith("@"):
        twitter = twitter[1:]

    return coach, twitter, nombre_corto


def get_player_info(player_url):
    data = httptools.downloadpage(player_url, cookies=False).data
    data = re.sub(r"\n|\r|\t", '', data)

    info = {}
    info["escudo"] = find_single_match(data, '<div class="img-shield">\s*<img src="([^"]+)"').replace("?size=120x&3", "")
    info["position"] = htmlclean(find_single_match(data, '<div class="info position">(.*?)</a>'))
    info["temp"] = find_single_match(data, '<div class="player-season">.*?<span>([^<]+)<')
    try:
        info["equipo"], info["liga"] = find_single_match(data, '<div class="inner_txt">.*?>([^<]+)</a>.*?>([^<]+)</a>')
    except:
        info["equipo"], info["liga"] = find_single_match(data, '<div class="inner temp-from">.*?>([^<]+)</a>.*?>([^<]+)</a>')
    info["nombre"] = find_single_match(data, '<dt>Completo</dt>\s*<dd>([^<]+)<')
    
    info["seasons"] = []
    bloque = find_single_match(data, '<ul id="selector_temporadas".*?</ul>')
    matches = find_multiple_matches(bloque, '<li><a href="([^"]+)" class="(.*?)">([^<]+)<')
    for url, select, season in matches:
        select = (select)
        info["seasons"].append({"url": url, "season": season, "select": select})

    info["ficha"] = []
    edad = find_single_match(data, '<dt>Edad</dt>\s*<dd>([^<]+)<').strip()
    if edad:
        info["ficha"].append("[B]Edad: [/B]" + edad)
    fecha_nac = find_single_match(data, '<dt>Fecha de nacimiento</dt>\s*<dd>([^<]+)<').strip()
    if fecha_nac:
        info["ficha"].append("[B]Fecha de Nacimiento: [/B]" + fecha_nac)

    lugar = find_single_match(data, '<dt>Lugar de.*?>([^<]+)</dd>').strip()
    if lugar:
        info["ficha"].append("[B]Nacido en: [/B]" + lugar)
    pais = find_single_match(data, '<dt>País.*?>([^<]+)</dd>').strip()
    if pais:
        info["ficha"].append("[B]País: [/B]" + pais)
    
    puesto = find_single_match(data, '<dt>Demarcación</dt>\s*<dd>([^<]+)<').strip()
    if puesto:
        info["ficha"].append("[B]Posición: [/B]" + puesto)

    nacion = find_single_match(data, '<dt>Nacionalidad</dt>\s*<dd>([^<]+)<').strip()
    if nacion:
        info["ficha"].append("[B]Nacionalidad: [/B]" + nacion)

    altura = find_single_match(data, '<dt>Altura</dt>\s*<dd>([^<]+)<').strip()
    if altura:
        info["ficha"].append("[B]Altura: [/B]" + altura)
    peso = find_single_match(data, '<dt>Peso</dt>\s*<dd>([^<]+)<').strip()
    if peso:
        info["ficha"].append("[B]Peso: [/B]" + peso)
    
    twitter = find_single_match(data, '<dt>Twitter</dt>.*?>([^<]+)</a>')
    if twitter.startswith("@"):
        twitter = twitter[1:]
    info["twitter"] = twitter

    info["stats"] = []
    tipo = ['pj', 'titu', 'compl', 'supl', 'minutos', 'tam', 'troj', 'asist', 'goles']
    bloque = find_single_match(data, 'class="u-lined">Estadísticas(.*?)</table>')
    bloques = find_multiple_matches(bloque, '<th class="name">(.*?)</tr>')
    for b in bloques:
        img = find_single_match(b, 'src="([^"]+)"')
        liga = find_single_match(b, '<span class="team-name">([^<]+)<')
        match = find_multiple_matches(b, '<td>([^<]+)</td>')
        info["stats"].append({'img': img, 'liga': liga})
        for i, m in enumerate(match):
            info["stats"][-1][tipo[i]] = m

    info["news"] = []
    matches = find_multiple_matches(data, '<h2 class="ni-title"><a href="([^"]+)">([^<]+)<.*?<span class="ni-date">([^<]+)<')
    for url, title, date in matches:
        info["news"].append({"url": url, "title": title, "date": date})

    info["trayectoria"] = []
    tipo = ['temp', 'div', 'edad', 'pj', 'titu', 'compl', 'entra', 'sale', 'tam', 'troj', 'goles', 'minutos']
    bloque = find_single_match(data, 'Trayectoria<(.*?)</table>')
    bloques = find_multiple_matches(bloque, '<th class="name">(.*?)</tr>')
    for b in bloques:
        equipo = find_single_match(b, '<span class="team-name">([^<]+)<')
        match = find_multiple_matches(b, '<td[^>]*>(.*?)</td>')
        info["trayectoria"].append({'equipo': equipo})
        for i, m in enumerate(match):
            info["trayectoria"][-1][tipo[i]] = m
    info["trayectoria"].reverse()

    info["historico"] = []
    if not info["trayectoria"]:
        bloque = find_single_match(data, '<div id="historico_box"(.*?)</script>')
        matches = find_multiple_matches(bloque, '<h6 class="title-name">.*?src="([^"]+)".*?<span>([^<]+)</span>(.*?)</ul>')
        for img, equipo, temps in matches:
            seasons = find_multiple_matches(temps, '<li><a.*?>([^<]+)<')
            info["historico"].append({'img': img, 'equipo': equipo, 'seasons': ", ".join(seasons)})

    info["titulos"] = []
    matches = find_multiple_matches(data, '<div class="player-title">\s*<h6 class="title-name">(.*?)</h6>(.*?)</ul>')
    for titulo, temps in matches:
        copa, veces = find_single_match(titulo, '(.*?)\s*<small class="bullet">(\d+)</small>')
        copa = copa.replace("Liga Inglesa", 'Premier League').replace("Liga Italiana", "Serie A") \
                   .replace("Liga Holandesa", "Eredivisie").replace("Liga Alemana", "Bundesliga")
        titulo = "%s (%s)" % (copa, veces)
        seasons = find_multiple_matches(temps, '<li>([^<]+)</li>')
        info["titulos"].append({'titulo': titulo, "seasons": ", ".join(seasons), 'copa': copa})

    info["efeme"] = []
    bloque = find_single_match(data, '<h6 class="title-name">(.*?)</dl>')
    matches = find_multiple_matches(bloque, '<dt>([^<]+)</dt>\s*<dd>(.*?)</dd>')
    for desc, value in matches:
        if "<" in value:
            value = htmlclean(value)
            part, percent = value.split(" ", 1)
            value = "%s (%s)" % (percent, part)
        info["efeme"].append({'desc': desc, 'value': value})

    info["fotos"] = []
    if '/fotos">Fotos</a' in data:
        data_foto = httptools.downloadpage(player_url+"/fotos", cookies=False).data
        data_foto = re.sub(r"\n|\r|\t", '', data_foto)
        matches = find_multiple_matches(data_foto, '<div class="itemimg first">.*?src="([^"]+)"')
        for img in matches:
            img = img.rsplit("?", 1)[0]
            info["fotos"].append(img)
    else:
        info["fotos"].append(find_single_match(data, '<div id="previewArea">\s*<img src="([^"]+)"').replace("?size=120x&3", ""))
    
    return info


def get_news(url=""):
    idiomas = [["es", "noticias"], ["www", "news"], ["fr", "infos"], ["pt", "noticias"]]
    idioma = idiomas[int(config.get_setting("matchcenter_news"))]
    if not url:
        url = "http://%s.besoccer.com/%s" % (idioma[0], idioma[1])
    data = httptools.downloadpage(url, cookies=False).data
    data = re.sub(r"\n|\r|\t", '', data)

    news = {}
    patron = '<div class="new-item ni-half">.*?href="([^"]+)".*?src="([^"]+)".*?>([^<]+)</a></h2>.*?' \
             '<span class="ni-date">(.*?)<.*?<p class="ni-subtitle">(.*?)</p>'
    matches = find_multiple_matches(data, patron)
    i = 0
    for url, thumb, title, date, subtitle in matches:
        url = "http://%s.besoccer.com%s" % (idioma[0], url)
        news[i] = {"url": url, "thumb": thumb, "title": title, "date": date, "subtitle": subtitle}
        i += 1

    next_page = find_single_match(data, '<a href="([^"]+)" aria-label="Next">\s*<i class="md md-chevron-right">')
    if next_page:
        next_page = "http://%s.besoccer.com%s" % (idioma[0], next_page)
        news["next_page"] = next_page

    return news


def get_portadas():
    data = httptools.downloadpage("http://www.diariosdefutbol.com/portadas-deportivos/", cookies=False).data
    data = re.sub(r"\n|\r|\t", '', data)

    portadas = []
    first = True
    patron = "<a class='group1' href='([^']+)'"
    matches = find_multiple_matches(data, patron)
    if not matches:
        data = httptools.downloadpage("http://movil.resultados-futbol.com/portadas", cookies=False).data
        data = re.sub(r"\n|\r|\t", '', data)
        bloque = find_single_match(data, '<div id="ct-widget-gallery"(.*?)</ul>')
        matches = find_multiple_matches(bloque, 'src="([^"]+)"')
        first = False
        
    for thumb in matches:
        if first:
            thumb = "http://www.diariosdefutbol.com" + thumb
        else:
            thumb = thumb.rsplit("?", 1)[0]
        portadas.append(thumb)

    return portadas


def get_agenda(url="deporte"):
    data = httptools.downloadpage("http://www.futbolenlatv.com/%s" % url, cookies=False).data
    data = re.sub(r"\n|\r|\t", '', data)

    data_canales = httptools.downloadpage("http://www.futbolenlatv.com/canal", cookies=False).data
    data_canales = re.sub(r"\n|\r|\t", '', data_canales)

    eventos = []
    bloques = find_multiple_matches(data, 'class="(?:hidden-md hidden-lg|) dia-partido">([^<]+)<(.*?)(?:<tr class="">|</table>)')
    for dia, bloque in bloques:
        patron = '<tr class="event-row hidden-xs">.*?<td class="hora">([^<]+)<.*?url\(\'([^\']+)\'' \
                 '.*?<span title="([^"]+)"(.*?)</ul>(.*?)<td class="canales">(.*?)</ul>'
        matches = find_multiple_matches(bloque, patron)
        dia = decodeHtmlentities(dia)
        if matches:
            eventos.append({dia: []})
        for hora, icono, titulo, subtitle, info, canales in matches:
            subtitle1 = find_single_match(subtitle, '<li class="detalles-jornada">([^<]+)<')
            subtitle2 = find_single_match(subtitle, '<li class="detalles-detalles" title="([^"]+)"')
            if subtitle2:
                subtitle1 += " - " + subtitle2

            subtitle = decodeHtmlentities(subtitle1)
            titulo = decodeHtmlentities(titulo)

            info_evento = []
            patron = '<td class="local">.*?<span title="([^"]+)".*?<img src="([^"]+)".*?<img src="([^"]+)".*?<span title="([^"]+)"'
            match = find_single_match(info, patron)
            if not match:
                patron = '<td colspan="2" class="evento">(.*?)</td>'
                match = [find_single_match(info, patron)]
            for elem in match:
                elem = elem.replace("<br />", "\n")
                if "/img/32/" in elem:
                    elem = elem.replace("/img/32/", "/img/")
                elem = decodeHtmlentities(elem)
                info_evento.append(elem)

            canales_l = []
            patron = '<li class.*?title="([^"]+)"'
            match = find_multiple_matches(canales, patron)
            for canal in match:
                canal_search = canal.replace("(", "\(").replace(")", "\)")
                src = find_single_match(data_canales, 'src="([^"]+)" alt="%s"' % canal_search).replace("/img/32/", "/img/")
                src = urllib.quote(decodeHtmlentities(src), safe=":/")
                canal = decodeHtmlentities(canal)
                canales_l.append([canal, src])
            icono = icono.replace("/img/32/", "/img/")
            icono = urllib.quote(decodeHtmlentities(icono), safe=":/")
            eventos[-1][dia].append({'hora': hora, 'icono': icono, 'titulo': titulo, 'subtitle': subtitle,
                                     'info_evento': info_evento, 'canales': canales_l})

    return eventos