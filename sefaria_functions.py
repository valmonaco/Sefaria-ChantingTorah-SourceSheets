import requests, json
from flask import current_app as app
import urllib as urllib2


def query_Sefaria_Reference(verses):
    url = app.config['GET_URL'] + verses + '?context=0'
    Sefaria_Torah_verse = requests.get(url)
    print(url)

    Sefaria_Torah_verseJSON = Sefaria_Torah_verse.json()
    if not(valid_ref(Sefaria_Torah_verseJSON)== "error"):
        print("attempting sheet generation")
        generate_sheet(Sefaria_Torah_verseJSON)
    else:
        print(Sefaria_Torah_verseJSON["error"])


def valid_ref(retrieved_JSON):
    if not("error") in retrieved_JSON:
        return("Valid Reference")
    else:
        return("error")


def generate_sheet(verse_JSON):

    print(verse_JSON)

    sheet_json = {}
    sheet_json["status"] = "public"
    sheet_json["title"] = "Torah Chanting: " + verse_JSON['ref']

    sheet_json["sources"]=[]

    ref_object={}
    ref_object["ref"] = verse_JSON['ref']
    ref_object["heRef"]=verse_JSON['heRef']
    ref_object["text"] = {"en":verse_JSON['text'][0], "he":verse_JSON['he'][0]}

    sheet_json["sources"].append(ref_object)


    #comment_object={}
    #comment_object["comment"]= "<p>This is a comment.</p>"

    #media_object={}
    #media_object["media"] = "https://tbeboca.org/wp-content/Audio/DEUTERONOMY/TORAH/Torah%20V-Zot%20HaBracha/TORAH_V'zot_HaBracha_V5.mp3"

    #highlighted_text_object={}
    #highlighted_text_object["outsideText"]= '<br/><span style="background-color:#a6be54; color:black;">וּמֹשֶׁ֗ה </span><span style="background-color:#d1b541; color:black;">בֶּן־מֵאָ֧ה וְעֶשְׂרִ֛ים </span><span style="background-color:#549eb3; color:black;">שָׁנָ֖ה בְּמֹת֑וֹ </span><span style="background-color:#e49c39; color:black;">לֹא־כָהֲתָ֥ה עֵינ֖וֹ וְלֹא־נָ֥ס לֵחֹֽה׃ </span>'


    #sheet_json["sources"].append(comment_object)
    #sheet_json["sources"].append(media_object)
    #sheet_json["sources"].append(highlighted_text_object)

    sheet_json["options"] = {
        "numbered": 0,
        "assignable": 0,
        "layout": "sideBySide",
        "boxed": 0,
        "language": "hebrew",
        "divineNames": "noSub",
        "collaboration": "none",
        "highlightMode": 0,
        "bsd": 0,
        "langLayout": "heRight"}

    sheet_content = json.dumps(sheet_json)
    values = {'json': sheet_content, 'apikey': app.config['API_KEY']}

    try:
         response = requests.post(app.config['POST_URL'], data=values)
         print(response.text)
         print ("Your sheet will be available in just a bit.")
    except urllib2.HTTPError as e:
         error_message = e.read()
         print(error_message)
         return(error_message)


