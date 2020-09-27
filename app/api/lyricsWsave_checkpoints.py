from beautifulsoup4 import BeautifulSoup
import requests
import unidecode
import re
import pandas as pd
import numpy as np
from time import sleep


df = pd.read_csv('dummy.csv')

#Original Code
# def scrape_lyrics(artist, song):
#     """
#     Pass it an artist and asong, will look for lyrics on genius
#     """
#     url = f"https://genius.com/{'-'.join(artist.capitalize().split() + song.lower().split())}-lyrics"
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, "html.parser")
#         dirty = soup.find('p')
#         # remove unicode characters
#         non_unicode = unidecode.unidecode(dirty.text)
#         # remove the bracket stuff []
#         more_clean = re.sub("\[[^[\]]*\]", "", non_unicode)
#         # remove (...)
#         cleaner = re.sub("\([^()]*\)", "", more_clean)
#         # Make all whitespace 1
#         clean = re.sub("\s+", " ", cleaner)
#         return clean
#     else:
#         return np.nan


# # lyrics = []
# # for i in range(100, df.shape[0] + 1, 100):
# BATCH_SIZE = 5
# # finds the last ending index, that is to say if we stopped at 5 next time we'll continue from 6
# # did this because 200k songs at 1 song a second + 1 sec sleep == 111 hours. This way we can stop it whenever we feel like it
# with open('lyrics.txt', "r") as file:
#     content = file.readlines()
#     start = int(content[-BATCH_SIZE - 1].strip("\n").split()[-1]) + 2
# # finds the next ending range for the nested for loop

# for i in range(BATCH_SIZE,df.shape[0] + BATCH_SIZE,BATCH_SIZE):

# # if the ending range is > the last ending index try to find lyrics for this batch
#     if i >= start:

#         # write the ending batch index
#         with open('lyrics.txt', "a") as file:
#             file.write(f"The ending index for this batch is: {i - 1}\n")

#         # if the data is not a multiple of your batch size it will miss anything in the 'final' batch so we're forcing it to go
#         # over in the above loop by adding batchsize to stop and that'll cause and idex error so try except
#         try:
#             for c in range(i-5, i):
#                 # for every index in the batch get a song
#                 artist = df.iloc[c]['artist_name'].replace("&", "and")
#                 song = df.iloc[c]['track_name'].replace("&", "and")
#                 lyrics = scrape_lyrics(artist, song)
#                 # write the lyrics or nan if no lyrics on genius
                
#                 with open('lyrics.txt', "a") as file:
#                     file.write(f"{lyrics}\n")
#                 sleep(1)
#         except IndexError:
#             break



# Practice Cell
#Trying to define a function that when called will return lyrics for a given column of track names/ids
from bs4 import BeautifulSoup
import requests
import unidecode
import re
# ARTIST = "Bts"
# SONG = "Dynamite"
def scrape_lyrics(artist, song):
    url = f"https://genius.com/{'-'.join(artist.capitalize().split() + song.lower().split())}-lyrics"
    response = requests.get(url)
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
lyrics = []
for i in range(len(df['track_name'])):
    artist = df.iloc[i]['artist_name']
    song = df.iloc[i]['track_name']
    lyrics.append(scrape_lyrics(artist, song))
    df['lyrics'] = pd.Series(lyrics)
    
print(df['lyrics'])