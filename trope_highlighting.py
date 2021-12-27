import highlighting_dictionaries
import re

def extract_trope_characters_nodups(verse):
    trope_characters_nodups = ""
    #cumulative_tropes=[]
    #just_trope_str = ""

    #w = 0

    verse_array = verse.split()

    for word in verse_array:
        previous_trope = ""
        for character in word:
            if (u'\u0591' <= character <= u'\u05AF'):
                if character != previous_trope:
                    trope_characters_nodups  = trope_characters_nodups  + character
                    previous_trope = character
                elif character == u'\u0592': #postpositive segol
                    trope_characters_nodups  = trope_characters_nodups  + 's'
                    print("found a postpositive segol")
                elif character == u'\u05A9':  #postpositive tvir
                    trope_characters_nodups  = trope_characters_nodups  + 't'
                elif character == u'\u05A0':  #postpositive T'lisha g'dolah
                    trope_characters_nodups  = trope_characters_nodups  + 'g'
                else:
                    trope_characters_nodups  = trope_characters_nodups  + character

        #w=w+1


    trope_characters_nodups  = trope_characters_nodups + u'\u05BD'
    #cumulative_tropes.append(w-1)
    #cumulative_tropes.append(w)
    #print("trope_characters_nodups: " + trope_characters_nodups)
    return trope_characters_nodups

def extract_trope_characters(verse):
    trope_characters = ""
    cumulative_tropes=[]
    just_trope_str = ""

    w = 0

    verse_array = verse.split()

    for word in verse_array:
        for character in word:
            if (u'\u0591' <= character <= u'\u05AF'):
                trope_characters = trope_characters + character
                cumulative_tropes.append(w)
        w=w+1


    trope_characters = trope_characters+ u'\u05BD'
    cumulative_tropes.append(w-1)
    cumulative_tropes.append(w)

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


def set_loop_counts(trope_characters_nodups):

    highlight_dict = highlighting_dictionaries.create_highlight_dict()

    for trope_name in highlight_dict.keys():
        #each trope has an anchor
        from_unicode_taamei = highlight_dict[trope_name]['anchor']
        #count how many anchors
        number = trope_characters_nodups.count(from_unicode_taamei)
        #loop through trope marks this many times
        highlight_dict[trope_name]['loop'] = number
    return highlight_dict


def loop_through_trope_patterns(all_tropes_str, highlight_dict, trope_word_placement, verse, aliyah):

    start_span={}
    end_span=[]

    adjusted_start=0
    adjusted_end=0

    res_span_mask=[0]*2


    tune_list={}
    ordered_tune_list=[]
    trope_tune_labels={}
    ordered_trope_tune_labels=[]

    colors = highlighting_dictionaries.define_colors()


    for trope_name in highlight_dict.keys():

        highlight_dict = set_loop_counts(all_tropes_str)

        for j in range(0,highlight_dict[trope_name]['loop']):
            temp_tune_index=0
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
                    temp_tune_index= highlight_dict[trope_name]['family'].index(trope)

            start_span[adjusted_start]=highlight_dict[trope_name]['num']
            tune_list[adjusted_start] = highlight_dict[trope_name]['tunes'][temp_tune_index]
            trope_tune_labels[adjusted_start] = {'bgcolor':colors[highlight_dict[trope_name]['num']]['hex_color'],'fgcolor':colors[highlight_dict[trope_name]['num']]['font_color'], 'trope':trope_name}


            end_span.append(adjusted_end)

            for r in range(res_span_mask[0], res_span_mask[1]):
                all_tropes_str = all_tropes_str[0:r] + "*" + all_tropes_str[r+1: ]

    formatted_verse = "<br/>"
    i = 0

    verse_array= verse.split()

    for i in range (0, len(verse_array)):

        if (i in end_span) and (not(i in start_span)):
            formatted_verse = formatted_verse.rstrip() + "</span>&nbsp;" + verse_array[i] +  " "

        elif ((i in start_span) and not(i in end_span)):
            formatted_verse = (formatted_verse + "<span style=\"background-color:" + colors[start_span[i]]['hex_color'] + "; color:"+ colors[start_span[i]]['font_color'] + ";\">" + verse_array[i] + " ")
            print("i in start_span:" + str(tune_list[i]))
            ordered_tune_list.append(tune_list[i])
            ordered_trope_tune_labels.append(trope_tune_labels[i])

        elif ((i in start_span) and (i in end_span)):
            formatted_verse = formatted_verse.rstrip() + "</span>&nbsp;<span style=\"background-color:" + colors[start_span[i]]['hex_color'] + "; color:"+ colors[start_span[i]]['font_color'] + ";\">" + verse_array[i] + " "
            print("i in both start_span and end span:" + str(tune_list[i]))
            ordered_tune_list.append(tune_list[i])
            ordered_trope_tune_labels.append(trope_tune_labels[i])

        else:
            formatted_verse = formatted_verse + verse_array[i] + " "



    formatted_verse =  formatted_verse + "</span>"
    if aliyah==True:
        ordered_tune_list.pop()
        ordered_tune_list.append("447567.mp3")

    return formatted_verse, ordered_tune_list, ordered_trope_tune_labels
