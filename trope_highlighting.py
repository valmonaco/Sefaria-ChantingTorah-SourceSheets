import "..static/trope_constants.py"
import re

def create_highlight_dict():
    highlight_dict={

    #'DoubleMercha':{'num': "11",'family' : double_mercha_trope, 'loop' : 0, 'anchor' : u'\u05A6'}
    #	,
    'Etnachta':{'num': "1", 'family' : trope_constants.ETNACHTA_TROPE_LIST, 'loop' : 0, 'anchor' : u'\u0591'}
    #	,
    #'Siluk':{'num': "2",'family' : siluk_trope_list, 'loop' : 0,'anchor' : u'\u05BD'}
    #	,
    #'Ytiv' : {'num': "3",'family' : ytiv_trope_list, 'loop' : 0, 'anchor' : u'\u059A'}
    #	,
    #'Katon':{'num': "3",'family' : katon_trope_list, 'loop' : 0, 'anchor' : u'\u0594'}
    #	,
    #'K-Vazla':{'num': "7",'family' : kvazla_trope, 'loop' : 0, 'anchor' : u'\u059C'}
    #	,
    #'Geresh':{'num': "7",'family' : geresh_trope, 'loop' : 0, 'anchor' : u'\u059C'}
    #	,
    #'Rvii':{'num': "4",'family' : rvii_trope_list, 'loop' : 0, 'anchor' : u'\u0597'}
    #	,
    #'Gershayim':{'num': "9",'family' : gershayim_trope, 'loop' : 0, 'anchor' : u'\u059E'}
    #	,
    #'Tvir':{'num': "6",'family' : tvir_trope_list, 'loop' : 0, 'anchor' : u'\u059B'}
    #	,
    #'Darga' :{'num': "6",'family' : darga_trope, 'loop' : 0, 'anchor' : u'\u05A7'}
    #	,
    #'Pazer':{'num': 1,'family' : pazer_trope, 'loop' : 0, 'anchor' : u'\u05A1'}
    #	,
    #'Zakef_Gadol' :{'num': "5",'family' : zakef_gadol_trope, 'loop' : 0, 'anchor' : u'\u0595'}
    #	,
    #'Segol' :{'num': "8",'family' : segol_trope_list, 'loop' : 0, 'anchor' : u'\u0592'}
    #	,
    #'Tlisha_G' : {'num': "10",'family' : tlisha_gdola_trope_list, 'loop' : 0, 'anchor' : u'\u05A0'}
    #	,
    #'Tlisha_K' : {'num': "10",'family' : tlisha_ktana_trope_list, 'loop' : 0, 'anchor' : u'\u05A9'}
    #	,
    #'Shalshelet':{'num': "12",'family' : shalshelet_trope, 'loop' : 0, 'anchor' : u'\u0593'}
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
		"11":{"hex_color":"#b8221e", "font_color": "white"}, # RARE deep red, double mercha, #31 in smooth rainbow scheme
		"12":{"hex_color":"#4e79c5", "font_color": "white"}, # RARE royal blue, Shalshelet, #12 in smooth rainbow scheme
		  }
    return colors


def extract_trope_characters(verse):
    trope_characters = ""
    cumulative_tropes=[]
    just_trope_str = ""

    w = 0

    verse_array = verse.split()

    for word in verse_array:
        #print(word)
        for character in word:
            if (u'\u0591' <= character <= u'\u05AF'):
                trope_characters = trope_characters + character
                #print(str(hex(ord(character))))
                cumulative_tropes.append(w)
        w=w+1


    trope_characters = trope_characters+ u'\u05BD'
    cumulative_tropes.append(w-1)
    cumulative_tropes.append(w)

    #print(cumulative_tropes)
    just_trope_str = trope_characters

    return just_trope_str

def map_trope_placement(verse):
    cumulative_tropes=[]

    w = 0

    verse_array = verse.split()

    for word in verse_array:
        for character in word:
            if (u'\u0591' <= character <= u'\u05AF'):
                cumulative_tropes.append(w)
        w=w+1

    cumulative_tropes.append(w-1)
    cumulative_tropes.append(w)

    return cumulative_tropes

def set_loop_counts(just_trope_str):

    highlight_dict = create_highlight_dict()

    for trope_name in highlight_dict.keys():

        from_unicode_taamei = highlight_dict[trope_name]['anchor']
        number = just_trope_str.count(from_unicode_taamei)
        highlight_dict[trope_name]['loop'] = number
        return highlight_dict




def loop_through_trope_patterns(all_tropes_str, highlight_dict, trope_word_placement, verse):

    start_span={}
    end_span=[]

    adjusted_start=0
    adjusted_end=0

    masked_trope_str = "*"*len(all_tropes_str)
    res_span_mask=[0]*2

    for trope_name in highlight_dict.keys():

        for j in range(0,highlight_dict[trope_name]['loop']):

            for trope in highlight_dict[trope_name]['family']:

                pattern = re.compile(trope)
                res = pattern.search(all_tropes_str)

                if (res):

                    adjusted_start = trope_word_placement[res.start()]
                    adjusted_end = trope_word_placement[res.end()]
                    if adjusted_start == adjusted_end:
                        adjusted_end=adjusted_end+1
                    res_span_mask[0]=res.start()
                    res_span_mask[1]=res.end()

            #start_span[adjusted_start]=highlight_dict[trope_name]['color']
            #start_span[adjusted_start]=colors[highlight_dict[trope_name]['num']]['hex_color']
            start_span[adjusted_start]=highlight_dict[trope_name]['num']
            end_span.append(adjusted_end)

            for r in range(res_span_mask[0], res_span_mask[1]):
                all_tropes_str = all_tropes_str[0:r] + "*" + all_tropes_str[r+1: ]

            j=j+1


            #print("start_span: "  + str(start_span))
            #print("end_span: "  + str(end_span))


    formatted_verse = "<br/>"
    #formatted_verse = "וַ"
    i = 0

    colors = define_colors()

    verse_array= verse.split()

    for i in range (0, len(verse_array)):

        if (i in end_span) and (not(i in start_span)):
            formatted_verse = formatted_verse + "</span>" + verse_array[i] +  " "

        elif ((i in start_span) and not(i in end_span)):
            formatted_verse = (formatted_verse + "<span style=\"background-color:" + colors[start_span[i]]['hex_color'] + "; color:"+ colors[start_span[i]]['font_color'] + ";\">" + verse_array[i] + " ")

        elif ((i in start_span) and (i in end_span)):
            formatted_verse = formatted_verse + "</span><span style=\"background-color:" + colors[start_span[i]]['hex_color'] + "; color:"+ colors[start_span[i]]['font_color'] + ";\">" + verse_array[i] + " "
        else:
            formatted_verse = formatted_verse + verse_array[i] + " "


    formatted_verse =  formatted_verse + "</span>"

    return formatted_verse



