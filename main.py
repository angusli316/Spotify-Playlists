import sys
import spotipy
import spotipy.util as util
import secret


def print_info(track):
    print(track['name'] + ' - ' + track['artists'][0]['name'] + ' - ' + str(track['popularity']))
    print(track['external_urls']['spotify'])


def history():
    results = sp.current_user_recently_played(limit=50)
    for track in results['items']:
        print_info(track['track'])

class Track:
    def __init__(self, name, artist):
        self.name = name
        self.artist = artist
    def __repr__(self):
        return self.name + ' - ' + self.artist + '\n'

class Playlist:
    def __init__(self, name, p_id):
        self.name = name
        tracks = sp.playlist_tracks(p_id)
        self.tracks = []
        for t in tracks['items']:
            #print(t['track']['artists'][0]['name'])
            self.tracks.append(Track(name=t['track']['name'], artist=t['track']['artists'][0]['name']))


def playlist_info():
    results = sp.current_user_playlists()
    playlist_list = []
    
    for p in results['items']:
        new_playlist = Playlist(name=p['name'], p_id=p['id'])
        playlist_list.append(new_playlist)
        print(new_playlist.name)
        print(new_playlist.tracks) 
        print()

token = secret.token

if token:
    sp = spotipy.Spotify(auth=token)
    #results = sp.current_user_saved_tracks()
    results = sp.recommendation_genre_seeds()
    #results = sp.current_user_top_tracks(limit=100)
    
    #history()
    playlist_info()
    '''
    tracks = results['items']
    for track in sorted(tracks, key= lambda t:t['popularity'], reverse=True):
        #print(item.keys())
        #track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'] + ' - ' + str(track['popularity']))
        print(track['external_urls']['spotify'])
        print()
    '''

else:
    print("Can't get token for", username)



