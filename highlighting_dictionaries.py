import trope_constants

def create_highlight_dict():
    highlight_dict={

    "Mercha k'fulah":{'num': "11",'family' : trope_constants.DOUBLE_MERCHA_TROPE, 'tunes': trope_constants.DOUBLE_MERCHA_TROPE_TUNE, 'loop' : 0, 'anchor' : u'\u05A6'}
    	,
    "Yare-ach ben Yomo and Karnei Parah":{'num': "13",'family' : trope_constants.K_PARA_BYOMO_TROPE, 'tunes': trope_constants.K_PARA_BYOMO_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u059F'}
        ,
    "Etnachta":{'num': "1", 'family' : trope_constants.ETNACHTA_TROPE_LIST,'tunes': trope_constants.ETNACHTA_TROPE_TUNES, 'loop' : 0, 'anchor' : u'\u0591'}
    	,
    "Siluk (Sof-pasuk)":{'num': "2",'family' : trope_constants.SILUK_TROPE_LIST, 'tunes': trope_constants.SILUK_TROPE_TUNES,'loop' : 0,'anchor' : u'\u05BD'}
    	,
    #"Katon with Y'tiv": {'num': "3",'family' : trope_constants.YTIV_TROPE_LIST, 'tunes': trope_constants.YTIV_TROPE_TUNES,'loop' : 0, 'anchor' : u'\u059A'}
    #	,
    "Katon":{'num': "3",'family' : trope_constants.KATON_TROPE_LIST, 'tunes': trope_constants.KATON_TROPE_TUNES,'loop' : 0, 'anchor' : u'\u0594'}
    	,
    "Kadma v'azla":{'num': "7",'family' : trope_constants.KVAZLA_TROPE, 'tunes': trope_constants.KVAZLA_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u059C'}
        ,
    "Geresh":{'num': "7a",'family' : trope_constants.GERESH_TROPE, 'tunes': trope_constants.GERESH_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u059C'}
        ,
    "Kadma":{'num': "7",'family' : trope_constants.KADMA_TROPE, 'tunes': trope_constants.KADMA_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u05A8'}
        ,
    "R'vi-i":{'num': "4",'family' : trope_constants.RVII_TROPE_LIST, 'tunes': trope_constants.RVII_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u0597'}
    	,
    "Gershayim":{'num': "9",'family' : trope_constants.GERSHAYIM_TROPE, 'tunes': trope_constants.GERSHAYIM_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u059E'}
    	,
    "Darga":{'num': "6a",'family' : trope_constants.DARGA_TROPE, 'tunes': trope_constants.DARGA_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u05A7'}
    	,
    "T'vir":{'num': "6",'family' : trope_constants.TVIR_DARGA_TROPE_LIST, 'tunes': trope_constants.TVIR_DARGA_TROPE_TUNES,'loop' : 0, 'anchor' : u'\u059B'}
    	,
    "Pazer":{'num': "1a",'family' : trope_constants.PAZER_TROPE, 'tunes': trope_constants.PAZER_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u05A1'}
    	,
    "Zakef gadol" :{'num': "5",'family' : trope_constants.ZAKEF_GADOL_TROPE, 'tunes': trope_constants.ZAKEF_GADOL_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u0595'}
    	,
    "Segol" :{'num': "8",'family' : trope_constants.SEGOL_TROPE_LIST, 'tunes': trope_constants.SEGOL_TROPE_TUNES,'loop' : 0, 'anchor' : u'\u0592'}
    	,
    "Segol (postpositive double)" :{'num': "8",'family' : trope_constants.SEGOL_PP_TROPE_LIST, 'tunes': trope_constants.SEGOL_PP_TROPE_TUNES,'loop' : 0, 'anchor' : u'\u0073' }
     ,
    "T'lisha g'dolah (postpositive double)" : {'num': "10",'family' : trope_constants.TLISHA_GDOLA_PP_TROPE_LIST, 'tunes': trope_constants.TLISHA_GDOLA_PP_TROPE_TUNES,'loop' : 0, 'anchor' : u'\u0067'}
        ,
    "T'lisha g'dolah" : {'num': "10",'family' : trope_constants.TLISHA_GDOLA_TROPE_LIST, 'tunes': trope_constants.TLISHA_GDOLA_TROPE_TUNES,'loop' : 0, 'anchor' : u'\u05A0'}
    	,
    "T'lisha k'tanah" : {'num': "10",'family' : trope_constants.TLISHA_KTANA_TROPE_LIST, 'tunes': trope_constants.TLISHA_KTANA_TROPE_TUNES,'loop' : 0, 'anchor' : u'\u05A9'}
    	,
    "T'lisha k'tanah (postpositive double)" : {'num': "10",'family' : trope_constants.TLISHA_KTANA_PP_TROPE_LIST, 'tunes': trope_constants.TLISHA_KTANA_PP_TROPE_TUNES,'loop' : 0, 'anchor' : u'\u0074'}
    	,
    "Shalshelet":{'num': "12",'family' : trope_constants.SHALSHELET_TROPE, 'tunes': trope_constants.SHALSHELET_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u0593'}
    }
    return highlight_dict

def define_colors():
    #https://waterdata.usgs.gov/blog/tolcolors/
    colors = {
		"1": {"hex_color":"#549eb3" ,"font_color": "black"}, #mid blue, etnachta, #15 in in smooth rainbow scheme
		"1a":{"hex_color":"#549eb3" ,"font_color": "#FFFFFF"}, #mid blue, pazer, #15 in in smooth rainbow scheme
		"2": {"hex_color":"#e49c39", "font_color": "black"}, #orange, siluk, #25 in smooth rainbow scheme
		"3": {"hex_color":"#ddd8ef", "font_color": "black"}, #pale blue, katon and ytiv, #2 in smooth rainbow scheme
		"4": {"hex_color":"#a6be54", "font_color": "black"}, #pea green, rvii, #21 in in smooth rainbow scheme
		"5": {"hex_color":"#9b62a7", "font_color": "black"}, #deep purple, Zakef_Gadol, #7 in smooth rainbow scheme
		"6": {"hex_color":"#d1b541", "font_color": "black"}, #mustard, darga and tvir, #21 in smooth rainbow scheme
		"6a": {"hex_color":"#d1b541", "font_color": "#3d6e9e"}, #mustard, darga and tvir, #21 in smooth rainbow scheme
		"7": {"hex_color":"#b58fc2", "font_color": "black"}, #deeper purple, K-Vazla, #5 in smooth rainbow scheme
		"7a": {"hex_color":"#b58fc2", "font_color": "#FFFFFF"}, #deeper purple, Geresh, #5 in smooth rainbow scheme	"8": {"hex_color":"#69b190", "font_color": "black"}, #teal, segol, #18 in the smooth rainbow scheme
		"9": {"hex_color":"#e4632d", "font_color": "black"}, #coral, gershayim, #28 in smooth rainbow scheme
		"10":{"hex_color":"#6059a9", "font_color": "#f9ff33"}, #deepest purple, tlisha, #10 in smooth rainbow scheme
		"11":{"hex_color":"#b8221e", "font_color": "#FFFFFF"}, #RARE deep red, double mercha, #31 in smooth rainbow scheme
		"12":{"hex_color":"#4e79c5", "font_color": "#FFFFFF"}, #RARE royal blue, Shalshelet, #12 in smooth rainbow scheme
		"13":{"hex_color":"#8c6eb0", "font_color": "#FFFFFF"}  #RARE deep purple, Karnei_Para, #9 in smooth rainbow scheme}
		  }
    return colors