import sys
import spotipy
import spotipy.util as util
import secret
import re

def print_info(track):
    print(track['name'] + ' - ' + track['artists'][0]['name'] + ' - ' + str(track['popularity']))
    print(track['external_urls']['spotify'])


def history():
    results = sp.current_user_recently_played(limit=50)
    for track in results['items']:
        print_info(track['track'])

song_freq = dict()

class Track:
    def __init__(self, name, artist):
        self.name = name
        self.artist = artist
    def __repr__(self):
        return self.name + ' - ' + self.artist + '\n'
    def __eq__(self, right):
        return self.name == right.name and self.artist == right.artist
    def __hash__(self):
        return hash(self.name + self.artist)

class Playlist:
    def __init__(self, name, p_id):
        self.name = name
        self.id = p_id
        tracks = sp.playlist_tracks(p_id)
        self.tracks = set()
        try:
            for t in tracks['items']:
                print(t['track']['id'])
                track_object = t['track']['name'], t['track']['artists'][0]['name']
                if track_object in song_freq:
                    song_freq[track_object] += 1
                else:
                    song_freq[track_object] = 1
                self.tracks.add(Track(name=track_object[0], artist=track_object[1]))
        except TypeError:
            pass
    def intersection(self, right):
        return self.tracks.intersection(right)


def playlist_info():
    results = sp.current_user_playlists(50)
    playlist_list = []
  
    for p in results['items']:
        new_playlist = Playlist(name=p['name'], p_id=p['id'])
        playlist_list.append(new_playlist)
        print(new_playlist.name)
        print(new_playlist.tracks) 
        print()
    
    for track in sorted(song_freq.items(), key= lambda t:t[1], reverse=True):
        print(track)
    
def follow_info():
    users = sp.user_follow_users()
    print(users)

def user_info():
    user_info = sp.current_user()
    print(user_info)

def playlist_intersect():
    taking_input = True
    playlists = list()
    pattern = '([\w:/.]+/playlist/)(?P<id>[\w]+)(\?[\w=]+)*'
    prog = re.compile(pattern)
    
    while taking_input:
        pl = input("Link to playlist, 'done' otherwise: ")
        if pl == 'done':
            if playlists:
                taking_input = False
            else:
                print('Playlist list cannot be empty')
        else:
            if prog.match(pl):
                playlists.append(pl)
            else:
                print('Invalid URL - Could not find playlist ID')
    
    # .group('id')
    common = set()
    for link in playlists:
        print(prog.match(link).group('id'))
        p = sp.playlist(prog.match(link).group('id'))
        one = Playlist(name=p['name'], p_id=p['id'])
        if not common:
            common = one.tracks
        else:
            common = one.intersection(common)

def playlist_destruct(p):
     s_id = ['2bJvI42r8EF3wxjOuDav4r']
     sp.user_playlist_replace_tracks(sp.me()['id'], p.id, s_id)

     #image_path = 'swag.png'
     #sp.playlist_upload_cover_image(p.id, image_path)

token = secret.token

if token:
    sp = spotipy.Spotify(auth=token)
    #results = sp.current_user_saved_tracks()
    #results = sp.recommendation_genre_seeds()
    #results = sp.current_user_top_tracks(limit=100)
    
    #history()
    #playlist_info()
    #follow_info()
    #user_info()
    
    taking_input = True
    playlists = list()
    pattern = '([\w:/.]+/playlist/)(?P<id>[\w]+)(\?[\w=]+)*'
    prog = re.compile(pattern)
    
    while taking_input:
        pl = input("Link to playlist, 'done' otherwise: ")
        if pl == 'done':
            if playlists:
                taking_input = False
            else:
                print('Playlist list cannot be empty')
        else:
            if prog.match(pl):
                playlists.append(pl)
            else:
                print('Invalid URL - Could not find playlist ID')
            
    for link in playlists:
        #print(prog.match(link).group('id'))
        p = sp.playlist(prog.match(link).group('id'))
        plist = Playlist(name=p['name'], p_id=p['id'])
        playlist_destruct(plist)
   
     
 
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

