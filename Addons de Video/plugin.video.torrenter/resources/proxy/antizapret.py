# -*- coding: utf-8 -*-

import os, re, fnmatch, threading, urllib2
from contextlib import contextmanager, closing
from functions import log, debug, tempdir

LOCKS = {}
PAC_URL = "http://antizapret.prostovpn.org/proxy.pac"
CACHE_DIR = tempdir()
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36"

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

CACHE = 24 * 3600 # 24 hour caching

#@contextmanager
def shelf(filename, ttl=0):
    import shelve
    filename = os.path.join(CACHE_DIR, filename)
    with LOCKS.get(filename, threading.RLock()):
#        with closing(shelve.open(filename, writeback=True)) as d:
        d = shelve.open(filename, writeback=True)
        #try:
        if True:
            import time
            if not dict(d):
                log('xxx')
                d.update({
                    "created_at": time.time(),
                    "data": {},
                })
            elif ttl > 0 and (time.time() - d["created_at"]) > ttl:
                log('xxx')
                d["created_at"] = time.time()
                d["data"] = {}
            return d
        #except:
        #    d.close()
        #    raise

_config = {}

def config():
    global _config
    if not _config:
#        with shelf("antizapret.pac_config", ttl=CACHE) as pac_config:
        d = shelf("antizapret.pac_config2", ttl=CACHE)
        pac_config = d['data']
        if not pac_config:
            log("[antizapret]: Fetching Antizapret PAC file on %s" %PAC_URL)
            try:
                pac_data = urllib2.urlopen(PAC_URL).read()
            except:
                pac_data = ""

            r = re.search(r"\"PROXY (.*); DIRECT", pac_data)
            if r:
                pac_config["server"] = r.group(1)
                pac_config["domains"] = map(lambda x: x.replace(r"\Z(?ms)", "").replace("\\", ""), map(fnmatch.translate, re.findall(r"\"(.*?)\",", pac_data)))
            else:
                pac_config["server"] = None
                pac_config["domains"] = []
        d.close()
        _config = pac_config
    return _config

class AntizapretProxyHandler(urllib2.ProxyHandler, object):
    def __init__(self):
        self.config = config()
        urllib2.ProxyHandler.__init__(self, {
            "http" : "<empty>", 
            "https": "<empty>", 
            "ftp"  : "<empty>", 
        })
    def proxy_open(self, req, proxy, type):
        import socket

        if socket.gethostbyname(req.get_host().split(":")[0]) in self.config["domains"]:
            debug("[antizapret]: Pass request through proxy " + self.config["server"])
            return urllib2.ProxyHandler.proxy_open(self, req, self.config["server"], type)

        return None

def url_get(url, params={}, headers={}, post = None):

    if params:
        import urllib
        url = "%s?%s" % (url, urllib.urlencode(params))

    if post:
        import urllib
        post = urllib.urlencode(post)

    req = urllib2.Request(url, post)
    req.add_header("User-Agent", USER_AGENT)

    for k, v in headers.items():
        req.add_header(k, v)

    try:
        with closing(urllib2.urlopen(req)) as response:
            data = response.read()
            if response.headers.get("Content-Encoding", "") == "gzip":
                import zlib
                return zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
            return data
    except urllib2.HTTPError as e:
        log("[antizapret]: HTTP Error(%s): %s" % (e.errno, e.strerror))
        return None

