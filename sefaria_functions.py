import requests, json
from flask import current_app as app, flash, session, Markup
import urllib as urllib2
from trope_highlighting import extract_trope_characters, map_trope_placement, set_loop_counts, loop_through_trope_patterns
from retrieve_verse_audio_file import retrieve_audio

def retrieve_Verse(verse) -> str:
    #verse_span = Book_Chapter + str(StartVerse) + "-" + str(EndVerse)

    url = app.config['GET_URL'] + verse + '?context=0'
    Sefaria_Torah_verse = requests.get(url)

    Sefaria_Torah_verseJSON = Sefaria_Torah_verse.json()
    #print(Sefaria_Torah_verseJSON)
    #print("")

    return Sefaria_Torah_verseJSON


def valid_ref(retrieved_JSON):
    #print(retrieved_JSON)
    if not("error") in retrieved_JSON:
        return True
    else:
        return False


def publish_sheet(values, capped_verses)->str:
    try:
        response = requests.post(app.config['POST_URL'], data=values)
        responseJSON = response.json()
        #print(response.text)
        session.pop('_flashes', None)
        flash("Shhh!  We are in stealth mode pending Sefaria review and approval. This link won't be around forever and can't be searched for.")

        new_sheet_url = "https://val.cauldron.sefaria.org/sheets/" + str(responseJSON["id"]) + "?lang=bi"
        response = requests.get(new_sheet_url)
        while response.status_code != 200:
            response = requests.get(new_sheet_url)

        link_text = "<a href=\"" + new_sheet_url + "\" target=\"_blank\">"+ new_sheet_url + "</a>"
        link = Markup(link_text)
        flash(link)

        flash(capped_verses)

    except urllib2.error.HTTPError as e:
        error_message = e.read()
        #print(error_message)
        flash(error_message)


def generate_sheet(Book, Chapter, StartVerse, EndVerse, aliyah_ending):
    error_detected=False
    capped_verses=""

    if (StartVerse > EndVerse):
        link_text = "<a href=\"../home\">Try again.</a>"
        link = Markup(link_text)
        #flash(link)
        flash("Whoops! Starting verse must be before ending verse. " + link)

    else:

        if EndVerse - StartVerse >= 4:
            capped_verses = "ps. You requested " + str(EndVerse-StartVerse) + " verses, but we provided only the first 4 requested verses in this sheet."
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
                        comment_object["comment"]= "<p><small>Please consult a rabbi, tutor, or a <i>gabbai</i> when using this study sheet. The creator of the sheet (not Sefaria) has sole responsibility for any errors. Please help make this program the best it can be by sending a detailed message describing any errors to: blahblah@gmail.com</small></p>"
                        sheet_json["sources"].append(comment_object)

                    ref_object={}
                    #ref_object["ref"] = verse_JSON['ref']
                    #ref_object["heRef"]= verse_JSON['heRef']
                    ref_object["ref"] = ""
                    ref_object["heRef"]= ""
                    ref_object["text"] = {"en":Sefaria_Torah_verseJSON['text'], "he":Sefaria_Torah_verseJSON['he']}
                    ref_object["options"]= {"PrependRefWithEn": Book_Chapter + str(StartVerse+i)}

                    sheet_json["sources"].append(ref_object)


                    highlighted_text_object={}
                    just_trope_str = extract_trope_characters(Sefaria_Torah_verseJSON['he'])
                    cumulative_tropes = map_trope_placement(Sefaria_Torah_verseJSON['he'])
                    highlight_count_dict= set_loop_counts(just_trope_str)
                    #print(highlight_count_dict)


                    if len(just_trope_str) > 0:
                        highlighted_verse,tune_list=loop_through_trope_patterns(just_trope_str,highlight_count_dict,cumulative_tropes,Sefaria_Torah_verseJSON['he'],aliyah_ending)

                    print("inside generate_sheet, returned tune_list: " + str(tune_list))
                    highlighted_text_object["outsideText"]= highlighted_verse
                    sheet_json["sources"].append(highlighted_text_object)

                    comment_object={}
                    comment_object["comment"]= "<p><small>Trope Tunes (1st audio file corresponds to 1st highlighted trope).<br/> Trope Tunes awaiting permission of Northern Virginia Hebrew Congregation and Cantor Caro.</small></p>"
                    sheet_json["sources"].append(comment_object)


                    for tune in tune_list:
                        print(tune)
                        media_object={}
                        if tune != "none":
                            media_object["media"] = "http://www.nvhcreston.org/wp-content/uploads/" + tune
                            sheet_json["sources"].append(media_object)
                        else:
                            comment_object={}
                            comment_object["comment"]= "<p><small>Missing trope tune in verse.</small></p>"
                            sheet_json["sources"].append(comment_object)

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
                        print("later verse found to be invalid")
                        #add comment to sheet about error
                        title = title + "-" + str((StartVerse+i)-1)
                        sheet_json["title"] = title

                        sheet_content = json.dumps(sheet_json)
                        values = {'json': sheet_content, 'apikey': app.config['API_KEY']}

                        publish_sheet(values,capped_verses)
                        error_detected=True


                    else:
                        print("first verse found to be invalid")
                        #flash("len(Sefaria_Torah_verseJSON['he'])" + str(len(Sefaria_Torah_verseJSON['he'])))
                        #flash(verse_span + " does not appear in the Torah.")

                        link_text = "<a href=\"../home\">Try again.</a>"
                        link = Markup(link_text)
                        #flash(link)
                        flash(verse_span + " does not appear in the Torah. " + link)

                        error_detected=True

                        #flash(Sefaria_Torah_verseJSON["error"])

        if error_detected==False:

            if (aliyah_ending):
                comment_object={}
                comment_object["comment"]= "<p><small><b>Note:</b> Verse is at end of <i>aliyah</i>. Use alternative siluk/sof pasuk tune and modify tune to match trope.</small></p>"
                sheet_json["sources"].append(comment_object)

            title = title + "-" + str((StartVerse+i))
            sheet_json["title"] = title
            sheet_content = json.dumps(sheet_json)
            values = {'json': sheet_content, 'apikey': app.config['API_KEY']}
            publish_sheet(values, capped_verses)

