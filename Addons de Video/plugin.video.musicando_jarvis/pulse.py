# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Sourced From Online Templates And Guides
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Thanks To: Google Search For This Template
# Modified: Pulse
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.musicandojarvis'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

xbmc.executebuiltin('Container.SetViewMode(500)')

YOUTUBE_CHANNEL_ID_1 = "PL7sBCGkQNm0AOEGNydaPZydjDAysipw-R"
YOUTUBE_CHANNEL_ID_2 = "PLSKiP8AuSHih2m6mzB69N_tQXA6R1ExNC"
YOUTUBE_CHANNEL_ID_3 = "PL3YsvLz49R33YBAhMsrwnJ6YMQrilEw5y"
YOUTUBE_CHANNEL_ID_4 = "PLqRG33kmyQ-bQh1h_xu2A3iGlAIXtLBIC"
YOUTUBE_CHANNEL_ID_5 = "PL2A8718A6C9A98D14"
YOUTUBE_CHANNEL_ID_6 = "PL2D4A44B959D87893"
YOUTUBE_CHANNEL_ID_7 = "PLcfQmtiAG0X-fmM85dPlql5wfYbmFumzQ"
YOUTUBE_CHANNEL_ID_8 = "PLA_I2ay5YcUVJbVT8tb-cZQ6pGJHWlnHH"
YOUTUBE_CHANNEL_ID_9 = "PL539EAB0AAC7115D6"
YOUTUBE_CHANNEL_ID_10 = "PLhInz4M-OzRUsuBj8wF6383E7zm2dJfqZ"
YOUTUBE_CHANNEL_ID_11 = "PLFPg_IUxqnZNnACUGsfn50DySIOVSkiKI"
YOUTUBE_CHANNEL_ID_12 = "PL8F6B0753B2CCA128"
YOUTUBE_CHANNEL_ID_13 = "PLDcnymzs18LWrKzHmzrGH1JzLBqrHi3xQ" 
YOUTUBE_CHANNEL_ID_14 = "PLH6pfBXQXHEC2uDmDy5oi3tHW6X8kZ2Jo" 
YOUTUBE_CHANNEL_ID_15 = "PL47oRh0-pTouthHPv6AbALWPvPJHlKiF7"
YOUTUBE_CHANNEL_ID_16 = "PLYAYp5OI4lRLf_oZapf5T5RUZeUcF9eRO"
YOUTUBE_CHANNEL_ID_17 = "PLL4IwRtlZcbvbCM7OmXGtzNoSR0IyVT02" 
YOUTUBE_CHANNEL_ID_18 = "PL5AA7A6E1055205F2"
YOUTUBE_CHANNEL_ID_19 = "PLvLX2y1VZ-tFJCfRG7hi_OjIAyCriNUT2"
YOUTUBE_CHANNEL_ID_20 = "PLTN0khS5IJuj7PuKEzQgxXtIvwioWTHpg" 
YOUTUBE_CHANNEL_ID_21 = "PLr8RdoI29cXIlkmTAQDgOuwBhDh3yJDBQ"
YOUTUBE_CHANNEL_ID_22 = "PLFRSDckdQc1th9sUu8hpV1pIbjjBgRmDw"
YOUTUBE_CHANNEL_ID_23 = "PL64E6BD94546734D8" 
YOUTUBE_CHANNEL_ID_24 = "PL6o_1dl6P3DGZe0Ju52dcnHvNkM7Rj--W"
YOUTUBE_CHANNEL_ID_25 = "PL0zQrw6ZA60Z6JT4lFH-lAq5AfDnO2-aE"
YOUTUBE_CHANNEL_ID_26 = "PLXupg6NyTvTxw5-_rzIsBgqJ2tysQFYt5"
YOUTUBE_CHANNEL_ID_27 = "PLQog_FHUHAFUDDQPOTeAWSHwzFV1Zz5PZ" 
YOUTUBE_CHANNEL_ID_28 = "PL0qf-h7_tcFlVRoYS6f0tjvk0NWdR3aD_"
YOUTUBE_CHANNEL_ID_29 = "PLLQvN69uicxy8S5diyNJMKMzRIxzrLBYo"
YOUTUBE_CHANNEL_ID_30 = "PLWNXn_iQ2yrKzFcUarHPdC4c_LPm-kjQy"
YOUTUBE_CHANNEL_ID_31 = "PLLMA7Sh3JsOQQFAtj1no-_keicrqjEZDm"
YOUTUBE_CHANNEL_ID_32 = "PL9NMEBQcQqlzwlwLWRz5DMowimCk88FJk"
YOUTUBE_CHANNEL_ID_33 = "PLfY-m4YMsF-OM1zG80pMguej_Ufm8t0VC" 
YOUTUBE_CHANNEL_ID_34 = "PLVXq77mXV53-Np39jM456si2PeTrEm9Mj"
YOUTUBE_CHANNEL_ID_35 = "PLx0sYbCqOb8TBPRdmBHs5Iftvv9TPboYG"
YOUTUBE_CHANNEL_ID_36 = "PL55713C70BA91BD6E"
YOUTUBE_CHANNEL_ID_37 = "PLSFitF4B6yNS82pcRx5XvD1PB6m8lIs5J"
YOUTUBE_CHANNEL_ID_38 = "PLirAqAtl_h2pRAtj2DgTa3uWIZ3-0LKTA" 
YOUTUBE_CHANNEL_ID_39 = "PLtv6DWBXhImIiGKX13ZzZPkndP6W_nFBu"
YOUTUBE_CHANNEL_ID_40 = "PLDcnymzs18LWrKzHmzrGH1JzLBqrHi3xQ"
YOUTUBE_CHANNEL_ID_41 = "PLXogPMnvZ7sQqWN1pDfYVeGsrkWYRa6Ex"
YOUTUBE_CHANNEL_ID_42 = "PLkzjRJyqa7v1b7m_hZce-Tm9QjgYs-n_x"
YOUTUBE_CHANNEL_ID_43 = "PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj" 
YOUTUBE_CHANNEL_ID_44 = "PL-PXKb5jSjwZT2QzeJCIlYSqs0cZvy808"
YOUTUBE_CHANNEL_ID_45 = "PLDcnymzs18LWrKzHmzrGH1JzLBqrHi3xQ"
YOUTUBE_CHANNEL_ID_46 = "PLkop8kow5TsGKdGT_UGuQV8mfmzp5k0NJ"
YOUTUBE_CHANNEL_ID_47 = "PLCqukCFvcNBKN4okn9OFCQZvkFdbki2vH"
# Entry point
def run():
    plugintools.log("docu.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("docu.main_list "+repr(params))
	
    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- The Rolling Stones[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="",
        folder=True )
	
    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- AC/DC[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Iron Maiden[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="",
        folder=True )
		
	
    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Depeche Mode[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="",
        folder=True )
	

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Dire Straits[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="",
        folder=True )
	
    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Metallica[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Latino[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- RAP (ESP) 2017: lo mejor [/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- New Age [/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- House[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Electronica[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Jazz[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Pop [/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Hip Hop[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Rock Alternativo[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Reggae[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Trap[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Cafe Del Mar  [/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Country[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Zumba[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Pop Rock[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- R&B[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Dance[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Clasico (ESP)[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Asiatica[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Mejicana[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Soul[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Conciertos (ESP)[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Conciertos[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Rhythm & limes[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Cristiana[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail="",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Hard Rock[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Heavy Metal[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR lime]- Clasico[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail="",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR gold]RedMusic[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR gold]Billboard Top Songs 2017[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail="",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR gold]Los 40 Principales[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR gold]VEVO Videos de todos los tiempos[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_38+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR gold]Techno ( Videos Del Recuerdo )[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_39+"/",
        thumbnail="",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR gold]Las Mejores canciones pop [/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_40+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR gold]Los 70 mejores videos de la historia[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_41+"/",
        thumbnail="",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR gold]Los Mejores Videos del 2014,2015[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_42+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR gold]POP Music 2017[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_43+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR gold]POP (ESP) 2017[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_44+"/",
        thumbnail="",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR gold]Mejores canciones: Musica pop [/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_45+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR gold]Musica (ESP) 80/90/00 [/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_46+"/",
        thumbnail="",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR gold]Musica del Recuerdo 70, 80, 90[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_47+"/",
        thumbnail="",
        folder=True )


run()