import sys
import spotipy
import spotipy.util as util

scoping = 'user-library-read'
reading = 'user-top-read'
recent = 'user-read-recently-played'

scope = recent

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

def print_info(track):
    print(track['name'] + ' - ' + track['artists'][0]['name'] + ' - ' + str(track['popularity']))
    print(track['external_urls']['spotify'])


def history():
    results = sp.current_user_recently_played(limit=50)
    for track in results['items']:
        print_info(track['track'])

def playlists():
    results = sp.current_user_playlists()
    for i in results['items']:
        print(i['tracks'])

if token:
    sp = spotipy.Spotify(auth=token)
    #results = sp.current_user_saved_tracks()
    results = sp.recommendation_genre_seeds()
    #results = sp.current_user_top_tracks(limit=100)
    
    history()
    #playlists()
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



