import requests, json
from flask import current_app as app, flash, session, Markup
from trope_highlighting import extract_trope_characters, extract_trope_characters_nodups, map_trope_placement, set_loop_counts, loop_through_trope_patterns
from retrieve_verse_audio_file import retrieve_audio

def retrieve_Verse(verse) -> str:

    url = app.config['GET_URL'] + verse + '?context=0'
    Sefaria_Torah_verse = requests.get(url,verify="mysite/instance/cauldron-sefaria-org-chain-64.pem")

    Sefaria_Torah_verseJSON = Sefaria_Torah_verse.json()

    return Sefaria_Torah_verseJSON


def valid_ref(retrieved_JSON):
    if not("error") in retrieved_JSON:
        return True
    else:
        return False


def publish_sheet(values, capped_verses)->str:
    try:
        response = requests.post(app.config['POST_URL'], data=values,verify="mysite/instance/cauldron-sefaria-org-chain-64.pem")
        responseJSON = response.json()

        session.pop('_flashes', None)
        flash("Thanks for checking out the Torah Chanting Source Sheet Generator. Currently, the generator does not create source sheets on the main Sefaria site. The link provided below is for a temporary copy of the Sefaria site. The link will stop working at some point in the future and can't be searched for. Please bookmark it for the time being and check back later for updates.")

        new_sheet_url = "https://val.cauldron.sefaria.org/sheets/" + str(responseJSON["id"]) + "?lang=bi"
        response = requests.get(new_sheet_url, headers={'User-Agent': 'Mozilla/5.0'},verify="mysite/instance/cauldron-sefaria-org-chain-64.pem")
        while response.status_code != 200:
            response = requests.get(new_sheet_url, headers={'User-Agent': 'Mozilla/5.0'},verify="mysite/instance/cauldron-sefaria-org-chain-64.pem")

        link_text = "<a href=\"" + new_sheet_url + "\" target=\"_blank\">"+ new_sheet_url + "</a>"
        link = Markup(link_text)
        flash(link)

        flash(capped_verses)

    except urllib2.error.HTTPError as e:
        error_message = e.read()
        flash(error_message)


def generate_sheet(Book, Chapter, StartVerse, EndVerse, aliyah_ending):
    error_detected=False
    capped_verses=""

    if (StartVerse > EndVerse):
        link_text = "<a href=\"../home\">Try again.</a>"
        link = Markup(link_text)
        #flash(link)
        flash("Whoops! Starting verse must be before ending verse. " + link)

    elif (Book=="Exodus" and Chapter==20 and StartVerse >=2 and StartVerse <= 14):
        flash("Trope highlighting for the Ten Commandments in Exodus is not yet available. Please check back later.")

    elif (Book=="Deuteronomy" and Chapter==5 and StartVerse >=6 and StartVerse <= 18):
        flash("Trope highlighting for the Ten Commandments in Deuteronomy is not yet available. Please check back later.")

    elif (Book=="Exodus" and Chapter==15 and StartVerse >=1 and StartVerse <= 19):
        flash("Trope highlighting and tunes for the \"Song of the Sea\" in Exodus are not yet available. Please check back later.")

    else:

        if EndVerse - StartVerse >= 4:
            capped_verses = "ps. You requested " + str(EndVerse-StartVerse+1) + " verses, but we provided only the first 4 requested verses in this sheet."
            EndVerse = StartVerse + 3

        for i in range(0,(EndVerse-StartVerse)+1):
            if error_detected==False:

                Book_Chapter = str(Book) + " " + str(Chapter) + ":"
                verse_span = Book_Chapter + str(StartVerse+i) + "-" + str(StartVerse+i)
                Sefaria_Torah_verseJSON=retrieve_Verse(verse_span)


                if valid_ref(Sefaria_Torah_verseJSON) and (not(len(Sefaria_Torah_verseJSON['he'])==0)):
                    Torah_Audio_Files=retrieve_audio(Book, Chapter,StartVerse,EndVerse)
                    if i == 0:
                        sheet_json = {}
                        sheet_json["status"] = "public"
                        title="Torah Chanting: " + Book_Chapter + str(StartVerse)
                        sheet_json["sources"]=[]

                        comment_object={}
                        comment_object["comment"]= "<p><small>Please consult a rabbi, cantor, tutor, or <i>gabbai</i> when using this study sheet. The generator of the sheet (TorahChantingHelper.net) has sole responsibility for any errors. Please help make this program the best it can be by sending a detailed message describing any errors to: val@torahchantinghelper.net</small></p>"
                        sheet_json["sources"].append(comment_object)

                    ref_object={}
                    ref_object["ref"] = Sefaria_Torah_verseJSON['ref']
                    ref_object["heRef"]= ""
                    ref_object["text"] = {"en":Sefaria_Torah_verseJSON['text'], "he":Sefaria_Torah_verseJSON['he']}

                    sheet_json["sources"].append(ref_object)


                    highlighted_text_object={}
                    just_trope_str = extract_trope_characters(Sefaria_Torah_verseJSON['he'])
                    just_trope_str_no_dups = extract_trope_characters_nodups(Sefaria_Torah_verseJSON['he'])
                    cumulative_tropes = map_trope_placement(Sefaria_Torah_verseJSON['he'])
                    highlight_count_dict= set_loop_counts(just_trope_str_no_dups)


                    if len(just_trope_str) > 0:
                        highlighted_verse,tune_list,trope_tune_labels=loop_through_trope_patterns(just_trope_str,highlight_count_dict,cumulative_tropes,Sefaria_Torah_verseJSON['he'],aliyah_ending)

                    comment_object={}
                    comment_object["comment"]= "<p><small>If a trope pattern is not recognized, it will appear without highlighting and without a trope tune audio file. Refer to the full verse chanting audio file for guidance on how to chant unhighlighted text.<br/></small></p>"
                    sheet_json["sources"].append(comment_object)

                    highlighted_text_object["outsideText"]= highlighted_verse
                    sheet_json["sources"].append(highlighted_text_object)

                    comment_object={}
                    comment_object["comment"]= "<p><small>Trope Tunes (1st audio file corresponds to 1st highlighted trope).<br/></small></p>"
                    sheet_json["sources"].append(comment_object)


                    j = 1
                    for tune in tune_list:
                        #print(tune)
                        tune_label_html=""
                        media_object={}

                        if not tune.startswith('none'):
                            comment_object={}

                            if tune == "447591.mp3":
                                tune_label_html='<p><small> Trope '+ str(tune_list.index(tune)+1) +' <span style="background-color:' + trope_tune_labels[tune_list.index(tune)]['bgcolor'] + '; color:'+ trope_tune_labels[tune_list.index(tune)]['fgcolor']+ ';">&nbsp;' + 'Darga T\'vir' + '&nbsp;</small></span>'
                            elif tune == "447558.mp3":
                                tune_label_html='<p><small> Trope '+ str(tune_list.index(tune)+1) +' <span style="background-color:' + trope_tune_labels[tune_list.index(tune)]['bgcolor'] + '; color:'+ trope_tune_labels[tune_list.index(tune)]['fgcolor']+ ';">&nbsp;' + 'Katon with Y\'tiv' + '&nbsp;</small></span>'
                            elif tune == "447560.mp3":
                                tune_label_html='<p><small> Trope '+ str(tune_list.index(tune)+1) +' <span style="background-color:' + trope_tune_labels[tune_list.index(tune)]['bgcolor'] + '; color:'+ trope_tune_labels[tune_list.index(tune)]['fgcolor']+ ';">&nbsp;' + 'Katon with Y\'tiv' + '&nbsp;</small></span>'
                            else:
                                tune_label_html='<p><small> Trope '+ str(tune_list.index(tune)+1) +' <span style="background-color:' + trope_tune_labels[tune_list.index(tune)]['bgcolor'] + '; color:'+ trope_tune_labels[tune_list.index(tune)]['fgcolor']+ ';">&nbsp;' + trope_tune_labels[tune_list.index(tune)]['trope'] + '&nbsp;</small></span>'

                            comment_object["comment"]= tune_label_html
                            sheet_json["sources"].append(comment_object)

                            media_object["media"] = app.config['TROPE_TUNES_URL'] + tune
                            sheet_json["sources"].append(media_object)
                        else:

                            comment_object={}
                            tune_label_html='<p><small> Trope ' + str(j) +' <span style="background-color:'+ trope_tune_labels[j-1]['bgcolor']+ '; color:'+ trope_tune_labels[j-1]['fgcolor']+ ';">&nbsp;' + trope_tune_labels[j-1]['trope'] + '</span><br/><i>Trope tune currently unavailable (may be a shorten version of standard trope)</i>.</small></span>'
                            comment_object["comment"]= tune_label_html
                            sheet_json["sources"].append(comment_object)
                        j=j+1

                    comment_object={}
                    comment_object["comment"]= "<p><small>Full Verse Chanted</small></p>"
                    sheet_json["sources"].append(comment_object)

                    media_object={}
                    media_object["media"] = Torah_Audio_Files[i]
                    sheet_json["sources"].append(media_object)

                    sheet_json["options"] = {
                        "numbered": 0,
                        "assignable": 0,
                        "layout": "sideBySide",
                        "boxed": False,
                        "language": "hebrew",
                        "divineNames": "noSub",
                        "collaboration": "none",
                        "highlightMode": 0,
                        "bsd": 0,
                        "langLayout": "heRight"}

                else:  #verse found to be invalid

                    if i > 0:
                        #add comment to sheet about error
                        title = title + "-" + str((StartVerse+i)-1)
                        sheet_json["title"] = title

                        sheet_content = json.dumps(sheet_json)
                        values = {'json': sheet_content, 'apikey': app.config['API_KEY']}

                        publish_sheet(values,capped_verses)
                        error_detected=True


                    else:
                        print("first verse found to be invalid")

                        link_text = "<a href=\"../home\">Try again.</a>"
                        link = Markup(link_text)
                        flash(verse_span + " does not appear in the Torah. " + link)

                        error_detected=True

        if error_detected==False:

            if (aliyah_ending):
                comment_object={}
                comment_object["comment"]= "<p><small><b>Note:</b> Verse is at end of <i>aliyah</i>. Use alternative siluk/sof pasuk tune and modify tune to match trope.</small></p>"
                sheet_json["sources"].append(comment_object)

            comment_object={}
            comment_object["comment"]= "<p><small><i>All audio recordings by Cantor Wendy Shermet (Temple Israel, Omaha, NE). Please consider a <a href=\"https://www.templeisraelomaha.com/payment.php\">donation</a> to the Cantor Shermet Music Fund.</i></small></p>"
            sheet_json["sources"].append(comment_object)


            title = title + "-" + str((StartVerse+i))
            sheet_json["title"] = title
            sheet_content = json.dumps(sheet_json)
            values = {'json': sheet_content, 'apikey': app.config['API_KEY']}
            publish_sheet(values, capped_verses)

