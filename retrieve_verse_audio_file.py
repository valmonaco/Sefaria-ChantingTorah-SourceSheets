from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup



def retrieve_audio(book_chapter,start_verse,end_verse):

    formatted_book_chapter= book_chapter.lower()
    formatted_book_chapter= formatted_book_chapter.replace(" ", "-ch-")
    formatted_book_chapter= formatted_book_chapter.replace(":", "")

    url = "https://www.templeisraelomaha.com/" + formatted_book_chapter + ".html"
    req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(req).read()
    page_soup = soup(webpage, "html.parser")

    audio_files=[]
    requested_audio_files =[]

    rows = page_soup.find_all('td')
    for row in rows:
        audio_file = row.find('audio')
        audio_files.append(audio_file['src'])

    for loc in range (start_verse, end_verse+1):
        requested_audio_files.append(audio_files[loc-1])

    print(formatted_book_chapter +"  "+ url +"  "+ str(requested_audio_files))
    return requested_audio_files