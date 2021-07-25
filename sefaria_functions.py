import requests
from flask import current_app as app


def query_Sefaria_Reference(verses) -> str:
    url = app.config['URL']+'/api/texts/' + verses + '?context=0'
    Sefaria_Torah_verse = requests.get(url)
    print(url)

    Sefaria_Torah_verseJSON = Sefaria_Torah_verse.json()
    return valid_ref(Sefaria_Torah_verseJSON)


def valid_ref(retrieved_JSON):
    if "error" in retrieved_JSON:
        return(retrieved_JSON['error'])
    else:
        return("Valid Reference")
