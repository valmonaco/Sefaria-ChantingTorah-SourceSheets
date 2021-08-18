# -*- coding: utf-8 -*
import sys, json, requests
import urllib.request as urllib2
from flask import current_app as app

# https://github.com/Sefaria/Sefaria-Project/wiki/Source-Sheets-Document-Format
def customize():

    sheet_json = {}
    sheet_json["status"] = "public"
    sheet_json["title"] = "test sheet"
    sheet_json["sources"] = []
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
         return("Sheet posted.")
         print(response.json())
    except urllib2.HTTPError as e:
         error_message = e.read()
         return(error_message)