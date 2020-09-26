# Define a function that when called will return lyrics for a given column of track names/ids
from bs4 import BeautifulSoup
import requests
import unidecode
import re
import pandas as pd
import numpy as np

df = pd.read_csv('SpotifyFeatures.csv')

ARTIST = "Bts"
SONG = "Dynamite"


def scrape_lyrics(artist, song):

    url = f"https://genius.com/{'-'.join(artist.capitalize().split() + song.lower().split())}-lyrics"
    response = requests.get(url)
    if response.status_code == 200:
        print(type(response.status_code))
        soup = BeautifulSoup(response.text, "html.parser")
        dirty = soup.find('p')
        # remove unicode characters
        non_unicode = unidecode.unidecode(dirty.text)
        # remove the bracket stuff []
        more_clean = re.sub("\[[^[\]]*\]", "", non_unicode)
        # remove (...)
        cleaner = re.sub("\([^()]*\)", "", more_clean)
        # Make all whitespace 1
        clean = re.sub("\s+", " ", cleaner)
        return clean
    else:
        return np.nan

lyrics = []
for i in df.shape[0]:
    artist = df.iloc[i]['artist_name'].replace("&", "and")
    song = df.iloc[i]['track_name'].replace("&", "and")
    lyrics.append(scrape_lyrics(artist, song))
df['lyrics'] = pd.Series(lyrics)

# print(scrape_lyrics('Whitney Houston', 'I Will Always Love You'))

