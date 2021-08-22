import requests, json
from flask import current_app as app, flash, session, Markup
import urllib as urllib2
from trope_highlighting import extract_trope_characters, map_trope_placement, set_loop_counts, loop_through_trope_patterns


def retrieve_Verse(verse) -> str:
    #verse_span = Book_Chapter + str(StartVerse) + "-" + str(EndVerse)

    url = app.config['GET_URL'] + verse + '?context=0'
    Sefaria_Torah_verse = requests.get(url)

    Sefaria_Torah_verseJSON = Sefaria_Torah_verse.json()
    #print(Sefaria_Torah_verseJSON)
    #print("")

    return Sefaria_Torah_verseJSON


def valid_ref(retrieved_JSON):
    print(retrieved_JSON)
    if not("error") in retrieved_JSON:
        return True
    else:
        return False


def publish_sheet(values)->str:
    try:
        response = requests.post(app.config['POST_URL'], data=values)
        responseJSON = response.json()
        print(response.text)
        session.pop('_flashes', None)
        flash("A link to your Sefaria Torah Chanting sheet will appear soon.")

        new_sheet_url = "https://val.cauldron.sefaria.org/sheets/" + str(responseJSON["id"]) + "?lang=bi"
        response = requests.get(new_sheet_url)
        while response.status_code != 200:
            response = requests.get(new_sheet_url)

        link_text = "<a href=\"" + new_sheet_url + "\" target=\"_blank\">Link to Source Sheet</a>"
        link = Markup(link_text)
        flash(link)

    except urllib2.error.HTTPError as e:
        error_message = e.read()
        print(error_message)
        flash(error_message)


def generate_sheet(Book_Chapter, StartVerse, EndVerse):
    flash("here we go!")
    error_detected=False

    if (StartVerse > EndVerse):
        flash("Whoops! Starting verse must be before ending verse.")

    else:

        for i in range(0,(EndVerse-StartVerse)+1):
            if error_detected==False:

                verse_span = Book_Chapter + str(StartVerse+i) + "-" + str(StartVerse+i)
                Sefaria_Torah_verseJSON=retrieve_Verse(verse_span)

                if valid_ref(Sefaria_Torah_verseJSON) and (not(len(Sefaria_Torah_verseJSON['he'])==0)):
                    session.pop('_flashes', None)
                    flash("Pulling together your customized sheet.")
                    if i == 0:
                        sheet_json = {}
                        sheet_json["status"] = "public"
                        title="Torah Chanting: " + Book_Chapter + str(StartVerse)
                        sheet_json["sources"]=[]

                        comment_object={}
                        comment_object["comment"]= "<p><super>Please consult a rabbi, tutor, or a <i>gabbai</i> when using this study sheet. The creator of the sheet (not Sefaria) has sole responsibility for any errors. Please help make this program the best it can be by sending a detailed message describing any errors to: blahblah@gmail.com</super></p>"
                        sheet_json["sources"].append(comment_object)

                    ref_object={}
                    #ref_object["ref"] = verse_JSON['ref']
                    #ref_object["heRef"]= verse_JSON['heRef']
                    ref_object["ref"] = ""
                    ref_object["heRef"]= ""
                    ref_object["text"] = {"en":Sefaria_Torah_verseJSON['text'], "he":Sefaria_Torah_verseJSON['he']}
                    ref_object["options"]= {"PrependRefWithEn": Book_Chapter + str(StartVerse+i)}

                    sheet_json["sources"].append(ref_object)

                    #media_object={}
                    #media_object["media"] = "https://tbeboca.org/wp-content/Audio/DEUTERONOMY/TORAH/Torah%20V-Zot%20HaBracha/TORAH_V'zot_HaBracha_V5.mp3"

                    highlighted_text_object={}
                    just_trope_str = extract_trope_characters(Sefaria_Torah_verseJSON['he'])
                    cumulative_tropes = map_trope_placement(Sefaria_Torah_verseJSON['he'])
                    highlight_count_dict= set_loop_counts(just_trope_str)


                    if len(just_trope_str) > 0:
                        highlighted_verse=loop_through_trope_patterns(just_trope_str,highlight_count_dict,cumulative_tropes,Sefaria_Torah_verseJSON['he'])

                    highlighted_text_object["outsideText"]= highlighted_verse
                    sheet_json["sources"].append(highlighted_text_object)


                    #sheet_json["sources"].append(media_object)

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

                        publish_sheet(values)
                        error_detected=True


                    else:
                        print("first verse found to be invalid")
                        #flash("len(Sefaria_Torah_verseJSON['he'])" + str(len(Sefaria_Torah_verseJSON['he'])))
                        flash(verse_span + " does not appear in the Torah.")
                        error_detected=True

                        #flash(Sefaria_Torah_verseJSON["error"])

        if error_detected==False:
            title = title + "-" + str((StartVerse+i))
            sheet_json["title"] = title
            sheet_content = json.dumps(sheet_json)
            values = {'json': sheet_content, 'apikey': app.config['API_KEY']}
            flash("Getting ready to put everything into a source sheet. This can sometimes take awhile.")
            publish_sheet(values)

