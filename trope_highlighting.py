import highlighting_dictionaries
import re


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

    highlight_dict = highlighting_dictionaries.create_highlight_dict()

    for trope_name in highlight_dict.keys():
        from_unicode_taamei = highlight_dict[trope_name]['anchor']
        number = just_trope_str.count(from_unicode_taamei)
        highlight_dict[trope_name]['loop'] = number
    return highlight_dict


def loop_through_trope_patterns(all_tropes_str, highlight_dict, trope_word_placement, verse):
    #print(verse)
    start_span={}
    end_span=[]

    adjusted_start=0
    adjusted_end=0

    res_span_mask=[0]*2


    tune_list={}
    ordered_tune_list=[]

    for trope_name in highlight_dict.keys():
        #print(trope_name)
        for j in range(0,highlight_dict[trope_name]['loop']):
            temp_tune_index=0

            for trope in highlight_dict[trope_name]['family']:

                #print(trope)
                pattern = re.compile(trope)
                res = pattern.search(all_tropes_str)

                if (res):

                    adjusted_start = trope_word_placement[res.start()]
                    adjusted_end = trope_word_placement[res.end()]
                    if adjusted_start == adjusted_end:
                        adjusted_end=adjusted_end+1
                    res_span_mask[0]=res.start()
                    res_span_mask[1]=res.end()
                    temp_tune_index= highlight_dict[trope_name]['family'].index(trope)
                    print("trope: " + trope +  "  temp_tune_index: "  + str(temp_tune_index))

            #start_span[adjusted_start]=highlight_dict[trope_name]['color']
            #start_span[adjusted_start]=colors[highlight_dict[trope_name]['num']]['hex_color']
            start_span[adjusted_start]=highlight_dict[trope_name]['num']
            tune_list[adjusted_start] = highlight_dict[trope_name]['tunes'][temp_tune_index]
            end_span.append(adjusted_end)
            #tune_list.append(highlight_dict[trope_name]['tunes'][temp_tune_index])
            print(tune_list)

            for r in range(res_span_mask[0], res_span_mask[1]):
                all_tropes_str = all_tropes_str[0:r] + "*" + all_tropes_str[r+1: ]
            #print(all_tropes_str)


            #print("start_span: "  + str(start_span))
            #print("end_span: "  + str(end_span))


    formatted_verse = "<br/>"
    #formatted_verse = "וַ"
    i = 0

    colors = highlighting_dictionaries.define_colors()

    verse_array= verse.split()

    for i in range (0, len(verse_array)):

        if (i in end_span) and (not(i in start_span)):
            formatted_verse = formatted_verse + "</span>" + verse_array[i] +  " "

        elif ((i in start_span) and not(i in end_span)):
            formatted_verse = (formatted_verse + "<span style=\"background-color:" + colors[start_span[i]]['hex_color'] + "; color:"+ colors[start_span[i]]['font_color'] + ";\">" + verse_array[i] + " ")
            #print(tune_list[i])
            ordered_tune_list.append(tune_list[i])

        elif ((i in start_span) and (i in end_span)):
            formatted_verse = formatted_verse + "</span><span style=\"background-color:" + colors[start_span[i]]['hex_color'] + "; color:"+ colors[start_span[i]]['font_color'] + ";\">" + verse_array[i] + " "
            #print(tune_list[i])
            ordered_tune_list.append(tune_list[i])

        else:
            formatted_verse = formatted_verse + verse_array[i] + " "



    formatted_verse =  formatted_verse + "</span>"

    return formatted_verse, ordered_tune_list
