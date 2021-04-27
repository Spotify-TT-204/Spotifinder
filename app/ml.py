"""Machine learning functions"""
import logging
import random
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator
import pickle
import joblib
from .tfidf import dtm
from .tfidf import df1
from .tfidf import spotify_songs
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm.notebook import tqdm
from pandas import Series
from .data_model.find_songs import FindSongs
from os.path import dirname

DIR = dirname(__file__)

log = logging.getLogger(__name__)
router = APIRouter()


@router.get('/random')
def random_artist():
    return random.choice(['Tones and I', 'Arizona Zervas', 'Post Malone'])


@router.post('/song')

# def select_nearest_songs(artist, song):
#
#     # loaded_model = pickle.load(open('nlp_model.sav', 'rb'))
#     loaded_model = joblib.load('app/loaded_model.joblib')
#
#     # translate artist, song into doc dtm.iloc[x].values
#     artist_songs = df1.loc[df1['track_artist'] == artist]
#     selected_song = artist_songs.loc[artist_songs['track_name'] == song]
#     x = selected_song.index
#     x = x.item()
#     #x = x.tolist()
#     x = 0
#     doc = dtm.loc[x].values
#     result = loaded_model.kneighbors([doc])
#
#     song1 = result[1][0][1]  # gives the loc
#     #x = x.item().remove()
#
#     # translate the loc into an artist and song title
#     artist1 = spotify_songs.loc[song1]['track_artist']
#     song1 = spotify_songs.loc[song1]['track_name']
#
#     # translate result into song names
#     return artist1, song1

class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

    x1: float = Field(..., example=3.14)
    x2: int = Field(..., example=-42)
    x3: str = Field(..., example='banjo')

    def to_df(self):
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])

    @validator('x1')
    def x1_must_be_positive(cls, value):
        """Validate that x1 is a positive number."""
        assert value > 0, f'x1 == {value}, must be > 0'
        return value


@router.post('/predict')
async def predict(artist, song):


    # loaded_model = pickle.load(open('nlp_model.sav', 'rb'))
    loaded_model = joblib.load(DIR+'/loaded_model.joblib')

    # translate artist, song into doc dtm.iloc[x].values
    artist_songs = df1[df1['track_artist'] == artist.lower()]
    selected_song = artist_songs.loc[artist_songs['track_name'] == song.lower()]
    print(f'selected_song = {selected_song}')
    x = selected_song.index
    print(f'x = {x}')
    #x = x.item()
    x = x.tolist()
    print(f'x = {x}')
    artist1 = 'Unknown'
    song1 = 'Unknown'
    
    if len(x):
        doc = dtm.loc[x[0]].values
        result = loaded_model.kneighbors([doc])

        print(f'result = {result}')
        song1 = result[1][0][1]  # gives the loc
        
        # translate the loc into an artist and song title
        artist1 = spotify_songs.loc[song1]['track_artist']
        song1 = spotify_songs.loc[song1]['track_name']
        
        # translate result into song names
    return artist1, song1
    #}
