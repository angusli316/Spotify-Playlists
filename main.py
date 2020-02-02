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
    def __init__(self, name, artist, tid):
        self.name = name
        self.artist = artist
        self.id = tid
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
                track_object = t['track']['name'], t['track']['artists'][0]['name'], t['track']['id']
                if track_object in song_freq:
                    song_freq[track_object] += 1
                else:
                    song_freq[track_object] = 1
                self.tracks.add(Track(name=track_object[0], artist=track_object[1], tid=track_object[2]))
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

def playlist_destruct(src, dest):
     #s_id = ['2bJvI42r8EF3wxjOuDav4r']
     id_list = []
     for t in src.tracks:
        if t.id is not None:
            id_list.append(t.id)
     sp.user_playlist_replace_tracks(sp.me()['id'], dest.id, id_list)

     #image_path = 'swag.jpeg'
     #csp.playlist_upload_cover_image(p.id, image_path)

token = secret.token

if token:
    sp = spotipy.Spotify(auth=token)
    csp = secret.csp
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
    src_found = False
    dest_found = False
    
    while taking_input:
        if not src_found:
            src = input("Playlist to copy: ")
        else:
            dest = input("Playlist to replace: ")
        if src_found and dest_found:
            if playlists:
                taking_input = False
            else:
                print('Playlist list cannot be empty')
        else:
            if not src_found and prog.match(src):
                src_found = True
            elif not dest_found and prog.match(dest):
                break
            else:
                print('Invalid URL - Could not find playlist ID')
     
    #folding laundry
    src_pl = sp.playlist(prog.match(src).group('id'))   
    spl = Playlist(name=src_pl['name'], p_id=src_pl['id'])
    
    dest_pl = sp.playlist(prog.match(dest).group('id'))
    dpl = Playlist(name=dest_pl['name'], p_id=dest_pl['id'])
 
    playlist_destruct(spl, dpl)
    #for link in playlists:
        #print(prog.match(link).group('id'))
    #    p = sp.playlist(prog.match(link).group('id'))
    #    plist = Playlist(name=p['name'], p_id=p['id'])
        #playlist_destruct(plist)
   
     
 
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

