import requests
from bs4 import BeautifulSoup as soup
from private_audio import id_audio_verse_url
# all audio files are used with the permission of Cantor Wendy Shermet

def retrieve_audio(book, chapter,start_verse,end_verse):

    url = id_audio_verse_url(book, chapter,start_verse,end_verse)

    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage=page.text

    page_soup = soup(webpage, "html.parser")

    audio_files=[]
    requested_audio_files = []

    rows = page_soup.find_all('td')
    current_verse=start_verse
    for row in rows:
        if current_verse <= end_verse:

            verse_tag = row.find_all('p')[-1]
            span_tag = verse_tag.find('span')
            if(span_tag):
                verse=span_tag.get_text()
            else:
                verse=verse_tag.get_text()


            if(len(verse)>1):
                audio_file = row.find('audio')
                audio_files.append(audio_file['src'])

            specified_verse=str(chapter) + ":" + str(current_verse)


            abridged_verse_number=verse.split(' ')[-1]
            if abridged_verse_number==specified_verse:
                requested_audio_files.append(audio_files.pop())
                current_verse = current_verse + 1

    return requested_audio_files