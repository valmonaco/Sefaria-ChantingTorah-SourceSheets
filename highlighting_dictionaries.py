import trope_constants

def create_highlight_dict():
    highlight_dict={

    'DoubleMercha':{'num': "11",'family' : trope_constants.DOUBLE_MERCHA_TROPE, 'tunes': trope_constants.DOUBLE_MERCHA_TROPE_TUNE, 'loop' : 0, 'anchor' : u'\u05A6'}
    	,
    'Karnei_Para':{'num': "13",'family' : trope_constants.K_PARA_BYOMO_TROPE, 'tunes': trope_constants.K_PARA_BYOMO_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u059F'}
        ,
    'Etnachta':{'num': "1", 'family' : trope_constants.ETNACHTA_TROPE_LIST,'tunes': trope_constants.ETNACHTA_TROPE_TUNES, 'loop' : 0, 'anchor' : u'\u0591'}
    	,
    'Siluk':{'num': "2",'family' : trope_constants.SILUK_TROPE_LIST, 'tunes': trope_constants.SILUK_TROPE_TUNES,'loop' : 0,'anchor' : u'\u05BD'}
    	,
 #   'Ytiv' : {'num': "3",'family' : trope_constants.YTIV_TROPE_LIST, 'tunes': trope_constants.YTIV_TROPE_TUNES,'loop' : 0, 'anchor' : u'\u059A'}
 #   	,
    'Ytiv_Katon':{'num': "3",'family' : trope_constants.YTIV_KATON_TROPE_LIST, 'tunes': trope_constants.YTIV_KATON_TROPE_TUNES,'loop' : 0, 'anchor' : u'\u0594'}
    	,
 #  'K-Vazla':{'num': "7",'family' : trope_constants.KVAZLA_TROPE, 'tunes': trope_constants.KVAZLA_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u059C'}
 #   	,
    'Geresh_KVazla':{'num': "7",'family' : trope_constants.GERESH_KVAZLA_TROPE, 'tunes': trope_constants.GERESH_KVAZLA_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u059C'}
    	,
    'Rvii':{'num': "4",'family' : trope_constants.RVII_TROPE_LIST, 'tunes': trope_constants.RVII_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u0597'}
    	,
    'Gershayim':{'num': "9",'family' : trope_constants.GERSHAYIM_TROPE, 'tunes': trope_constants.GERSHAYIM_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u059E'}
    	,
    'Tvir_Darga':{'num': "6",'family' : trope_constants.TVIR_DARGA_TROPE_LIST, 'tunes': trope_constants.TVIR_DARGA_TROPE_TUNES,'loop' : 0, 'anchor' : u'\u059B'}
    	,
    #'Darga' :{'num': "6",'family' : trope_constants.DARGA_TROPE, 'tunes': trope_constants.DARGA_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u05A7'}
    #	,
    'Pazer':{'num': "1",'family' : trope_constants.PAZER_TROPE, 'tunes': trope_constants.PAZER_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u05A1'}
    	,
    'Zakef_Gadol' :{'num': "5",'family' : trope_constants.ZAKEF_GADOL_TROPE, 'tunes': trope_constants.ZAKEF_GADOL_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u0595'}
    	,
    'Segol' :{'num': "8",'family' : trope_constants.SEGOL_TROPE_LIST, 'tunes': trope_constants.SEGOL_TROPE_TUNES,'loop' : 0, 'anchor' : u'\u0592'}
    	,
    'Tlisha_G' : {'num': "10",'family' : trope_constants.TLISHA_GDOLA_TROPE_LIST, 'tunes': trope_constants.TLISHA_GDOLA_TROPE_TUNES,'loop' : 0, 'anchor' : u'\u05A0'}
    	,
    'Tlisha_K' : {'num': "10",'family' : trope_constants.TLISHA_KTANA_TROPE_LIST, 'tunes': trope_constants.TLISHA_KTANA_TROPE_TUNES,'loop' : 0, 'anchor' : u'\u05A9'}
    	,
    'Shalshelet':{'num': "12",'family' : trope_constants.SHALSHELET_TROPE, 'tunes': trope_constants.SHALSHELET_TROPE_TUNE,'loop' : 0, 'anchor' : u'\u0593'}
    }
    return highlight_dict

def define_colors():
    #https://waterdata.usgs.gov/blog/tolcolors/
    colors = {
		"1": {"hex_color":"#549eb3" ,"font_color": "black"}, #mid blue, etnachta, #15 in in smooth rainbow scheme
		"2": {"hex_color":"#e49c39", "font_color": "black"}, #orange, siluk, #25 in smooth rainbow scheme
		"3": {"hex_color":"#ddd8ef", "font_color": "black"}, #pale blue, katon and ytiv, #2 in smooth rainbow scheme
		"4": {"hex_color":"#a6be54", "font_color": "black"}, #pea green, rvii, #21 in in smooth rainbow scheme
		"5": {"hex_color":"#9b62a7", "font_color": "black"}, #deep purple, Zakef_Gadol, #7 in smooth rainbow scheme
		"6": {"hex_color":"#d1b541", "font_color": "black"}, #mustard, darga and tvir, #21 in smooth rainbow scheme
		"7": {"hex_color":"#b58fc2", "font_color": "black"}, #deeper purple, K-Vazla and geresh, #5 in smooth rainbow scheme
		"8": {"hex_color":"#69b190", "font_color": "black"}, #teal, segol, #18 in the smooth rainbow scheme
		"9": {"hex_color":"#e4632d", "font_color": "black"}, #coral, gershayim, #28 in smooth rainbow scheme
		"10":{"hex_color":"#6059a9", "font_color": "black"}, #deepest purple, tlisha, #10 in smooth rainbow scheme
		"11":{"hex_color":"#b8221e", "font_color": "#FFFFFF"}, #RARE deep red, double mercha, #31 in smooth rainbow scheme
		"12":{"hex_color":"#4e79c5", "font_color": "#FFFFFF"}, #RARE royal blue, Shalshelet, #12 in smooth rainbow scheme
		"13":{"hex_color":"#8c6eb0", "font_color": "#FFFFFF"}  #RARE deep purple, Karnei_Para, #9 in smooth rainbow scheme}
		  }
    return colors