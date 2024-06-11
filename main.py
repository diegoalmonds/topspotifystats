import json
from flask import Flask, render_template, url_for, session, redirect
import spotipy

from song import Song
from artist import Artist
from album import Album

user_top_tracks = []
user_top_artists = []

scopes = "user-top-read"
CLIENT_ID = "504a3dea7dcb44df9c225dd866fb9b4d"
CLIENT_SECRET = "" #hidden
REDIRECT_URI = "http://127.0.0.1:5000/redirect"

app = Flask(__name__)
app.secret_key = "temporary"

oauth_object = spotipy.oauth2.SpotifyOAuth(CLIENT_ID,CLIENT_SECRET,REDIRECT_URI,scope=scopes)
access_token = oauth_object.get_access_token(as_dict=False) #as_dict=True will return it as a dictionary, otherwise its only the token itself
spotify = spotipy.Spotify(auth=access_token)

def convert_milliseconds(ms):
    seconds = int(ms/1000)%60
    minutes = int(ms/60000)%60
    hours = int(ms/(1000*60*60))%24
    if (hours == 0):
        return f"{minutes:02d}:{seconds:02d}"
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def create_song_object(track):
    track_artists = []
    title = track['name']
    for idx, artist in enumerate(track['artists']):
        track_artists.append(create_artist_object(spotify.artist(artist['id'])))
    album = create_album_object(spotify.album(track['album']['id']))
    track_duration = convert_milliseconds(track['duration_ms'])
    return Song(title, track_artists, album, track_duration)

def create_album_object(album):
    name = album['name']
    songs = populate_album_tracks(spotify.album_tracks(album['id'])['items'])
    release_date = album['release_date']
    cover_art = album['images']
    return Album(name, songs, release_date, cover_art)
    
def create_artist_object(artist):
    artist_albums = []
    name = artist['name']
    albums = populate_artist_albums(spotify.artist_albums(artist['id'])['items'])
    genres = artist['genres']
    images = artist['images']
    top_tracks = populate_artist_top_tracks(spotify.artist_top_tracks(artist['id'])['tracks'])
    return Artist(name, albums, genres, images, top_tracks)

#this code should be fine
def populate_user_top_tracks(request_response):
    user_top_tracks.clear()
    for idx, track in enumerate(request_response):
        user_top_tracks.append(create_song_object(track))

def populate_user_top_artists(request_response):
    user_top_artists.clear()
    for idx, artist in enumerate(request_response):
        user_top_artists.append(create_artist_object(artist))
        
def populate_artist_albums(request_response):
    artist_albums = []
    for idx, album in enumerate(request_response):
        artist_albums.append(album['name'])
    return artist_albums

def populate_artist_top_tracks(request_response):
    artist_top_tracks = []
    for idx, track in enumerate(request_response):
        artist_top_tracks.append(track['name'])
    return artist_top_tracks

def populate_album_tracks(request_response):
    album_tracks = []
    for idx, track in enumerate(request_response):
        album_tracks.append(track['name'])
    return album_tracks

@app.route('/')
def home():
    return redirect(url_for("view_top_tracks", time_frame="short_term"))

@app.route('/tracks/<time_frame>')
def view_top_tracks(time_frame):
    populate_user_top_tracks(spotify.current_user_top_tracks(time_range=time_frame, limit=5)['items'])
    return render_template('tracks.html', user_top_tracks=user_top_tracks)

@app.route('/artists/<time_frame>')
def view_top_artists(time_frame):
    populate_user_top_artists(spotify.current_user_top_artists(time_range=time_frame, limit=5)['items'])
    return render_template('artists.html', user_top_artists=user_top_artists)

print(user_top_artists)
