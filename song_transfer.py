import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = "9b34bf5e71624ab78162db17b227b554"
client_secret = "a6735effb9fb4b5c898fbd8023674064"
redirect_url = "http://localhost:8888/callback"

# spotify authorization setup

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
											   client_secret=client_secret,
											   redirect_uri=redirect_url,
											   scope="user-library-read playlist-modify-private"))

liked_tracks = []
results = sp.current_user_saved_tracks()
while results:
    for item in results['items']:
        track = item['track']
        liked_tracks.append(track['uri'])  # Collect track URIs
    # Check if there are more pages of results
    if results['next']:
        results = sp.next(results)
    else:
        break

user_id = sp.current_user()['id']
playlist_name = "New Playlist"
new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
playlist_id = new_playlist['id']

# Step 3: Add liked songs to the playlist
# Spotify limits batch additions to 100 songs, so we'll chunk if needed
for i in range(0, len(liked_tracks), 100):
    sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=liked_tracks[i:i+100])

print(f"All liked songs added to playlist '{playlist_name}'!")