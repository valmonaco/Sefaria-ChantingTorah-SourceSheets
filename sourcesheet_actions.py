# -*- coding: utf-8 -*
import sys, json, requests
import urllib.request as urllib2
from flask import current_app as app

# https://github.com/Sefaria/Sefaria-Project/wiki/Source-Sheets-Document-Format
def customize(ref):

    print("Ref is: " + ref)



    sheet_json = {}
    ref_object={}
    ref_object["ref"] = ref
    ref_object["heRef"]="וּמֹש"
    ref_object["text"] = {"en":"this is english text", "he":"וּמ"}

    comment_object={}
    comment_object["comment"]= "<p>This is a comment.</p>"

    media_object={}
    media_object["media"] = "https://tbeboca.org/wp-content/Audio/DEUTERONOMY/TORAH/Torah%20V-Zot%20HaBracha/TORAH_V'zot_HaBracha_V7.mp3"

    highlighted_text_object={}
    highlighted_text_object["outsideText"]= '<br/><span style="background-color:#a6be54; color:black;">וּמֹשֶׁ֗ה </span><span style="background-color:#d1b541; color:black;">בֶּן־מֵאָ֧ה וְעֶשְׂרִ֛ים </span><span style="background-color:#549eb3; color:black;">שָׁנָ֖ה בְּמֹת֑וֹ </span><span style="background-color:#e49c39; color:black;">לֹא־כָהֲתָ֥ה עֵינ֖וֹ וְלֹא־נָ֥ס לֵחֹֽה׃ </span>'

    sheet_json["status"] = "public"
    sheet_json["title"] = "Torah Chanting: " + ref
    sheet_json["sources"] = []

    sheet_json["sources"].append(ref_object)
    sheet_json["sources"].append(comment_object)
    sheet_json["sources"].append(media_object)
    sheet_json["sources"].append(highlighted_text_object)

    #print(sheet_json)

    sheet_json["options"] = {
        "numbered": 0,
        "assignable": 0,
        "layout": "sideBySide",
        "boxed": 0,
        "language": "bilingual",
        "divineNames": "noSub",
        "collaboration": "none",
        "highlightMode": 0,
        "bsd": 0,
        "langLayout": "heRight"}

    sheet_content = json.dumps(sheet_json)
    values = {'json': sheet_content, 'apikey': app.config['API_KEY']}

    try:
         response = requests.post(app.config['POST_URL'], data=values)
         return(response.text)
    except urllib2.HTTPError as e:
         error_message = e.read()
         print(error_message)
         return(error_message)