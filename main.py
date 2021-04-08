import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "f77897f3dbed415b85e1884cf7fabd44"
CLIENT_SECRET = "c6ed803a923541ff89886a3ff6b4ddc6"
SPOTIPY_REDIRECT_URI = "http://example.com/callback/"
SCOPE = "playlist-modify-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=SCOPE,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

date = input("Which Year do you want to travel to ? Type the date in this format YYYY-MM-DD:\t")

URL = f"https://www.billboard.com/charts/hot-100/{date}"


response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html,"html.parser")

all_songs = soup.find_all(name="span",class_="chart-element__information__song text--truncate color--primary")

songs_title = [song.getText() for song in all_songs]


song_uris  = []

year = date.split("-")[0]

for song in songs_title:
    result = sp.search(q=f"track:{song} year:{year}",type="track")
    #print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")



playlist = sp.user_playlist_create(user=user_id,name=f"{date} Billboard 100",public=False)



sp.playlist_add_items(playlist_id=playlist["id"],items=song_uris)

