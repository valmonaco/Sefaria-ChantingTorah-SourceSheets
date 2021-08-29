from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from private_audio import id_audio_verse_url



def retrieve_audio(book, chapter,start_verse,end_verse):

    print(book, chapter,start_verse,end_verse)
    url = id_audio_verse_url(book, chapter,start_verse,end_verse)
    print(url)

    req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(req).read()
    page_soup = soup(webpage, "html.parser")

    audio_files=[]
    requested_audio_files = []

    rows = page_soup.find_all('td')
    current_verse=start_verse
    for row in rows:
        if current_verse <= end_verse:
            verse_tag = row.find('p')
            span_tag = verse_tag.find('span')
            if(span_tag):
                verse=span_tag.get_text()
            else:
                verse=verse_tag.get_text()

            #print("appending verse: " + verse)
            #verses.append(verse)

            if(len(verse)>1):
                audio_file = row.find('audio')
                audio_files.append(audio_file['src'])
                print("audio_files: " + str(audio_files))

            specified_verse=str(chapter) + ":" + str(current_verse)
            print("specified_verse:"  + specified_verse)

            #for verse in verses:
            abridged_verse_number=verse.split(' ')[-1]
            print("abridged_verse: " + abridged_verse_number)
            if abridged_verse_number==specified_verse:
                requested_audio_files.append(audio_files.pop())
                current_verse = current_verse + 1

    return requested_audio_files