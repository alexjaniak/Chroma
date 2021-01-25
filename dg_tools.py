# tools for data gen/collection
# 1-24-21

# == todo == #
# add class desc
# make SpotifyTools class instance based
# -> playlist class??

# == imports == #
import spotipy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string

# == spotify tools == #
class SpotifyTools:

    # gets a feature/obj from a 2d list
    # lst: list, obj: str/int
    get_obj = lambda lst, obj : [lst[i][obj] for i in range(len(lst))] 

    # refines a list of playlist items
    # assumed Spotify obj is authenticated
    @classmethod
    def get_playlist(cls,_id:int, sp: spotipy.Spotify) -> pd.DataFrame:

        _playlist = sp.playlist_tracks(_id, market='US') # fetch playlist
        track_count = _playlist['total']
        
        # 100 item limit per request
        while track_count != len(_playlist['items']):
            batch = sp.playlist_tracks(_id, offset = len(_playlist['items']), market='US')
            _playlist['items'].extend(batch['items'])

        # removes tracks that are unplayable in the US market
        items = _playlist['items']
        items[:] = [item for item in items if item['track']['is_playable']]
        track_count -= track_count-len(items)

        # get specific features
        tracks = cls.get_obj(items,'track')
        artists = cls.get_obj(tracks,'artists')

        artist_names = [] #mutliple artists per track
        for ix in range(track_count):
            z = [] 
            for jx in range(len(artists[ix])):
                z.append(artists[ix][jx]['name'])
            artist_names.append(z)
        
        # return pandas DF with selected fatures
        return pd.DataFrame({
            'name': cls.get_obj(tracks,'name'),
            'artist_name': artist_names,
            'id': cls.get_obj(tracks,'id'),
        })

    # returns audio features given a list of track ids
    # assumed Spotify obj is authenticated
    @classmethod
    def get_track_audio_features(cls,_ids:list, sp:spotipy.Spotify) -> pd.DataFrame:
        audio_features = []
        total = len(_ids)
        
        # 100 item limit per request
        for i in range(total//100):
            audio_features.extend(sp.audio_features(_ids[i*100:i*100+100]))
        audio_features.extend(sp.audio_features(_ids[len(audio_features):total]))
        
        # convert to pandas dataframe
        return pd.DataFrame({
            'danceability': cls.get_obj(audio_features,'danceability'),
            'energy': cls.get_obj(audio_features,'energy'),
            'key': cls.get_obj(audio_features,'key'),
            'loudness': cls.get_obj(audio_features,'loudness'),
            'mode': cls.get_obj(audio_features,'mode'),
            'speechiness': cls.get_obj(audio_features,'speechiness'),
            'acousticness': cls.get_obj(audio_features,'acousticness'),
            'instrumentalness': cls.get_obj(audio_features,'instrumentalness'),
            'liveness': cls.get_obj(audio_features,'liveness'),
            'valence': cls.get_obj(audio_features,'valence'),
            'tempo': cls.get_obj(audio_features,'tempo')
        })

# == color tools == #
class ColorTools:

    # converts hsl to rgb
    @classmethod
    def hsl_to_rgb(cls, h:'hue', s:'saturation', l:'lightness') -> '[r,g,b]': 
        # h∈[0,365], s∈[0,1], l∈[0,1]
        # returns rgb conversion where r, g, b ∈ [0,255]
        r, g, b = 0, 0, 0
        
        c = (1-abs(2*l-1))*s #chroma
        hp = h/60
        x = c * (1-abs(hp%2-1))
        m = l - 0.5*c
        
        if 0 <= hp <= 1:
            r, g, b = c, x, 0
        elif 1 < hp <= 2:
            r, g, b = x, c, 0
        elif 2 < hp <= 3:
            r, g, b = 0, c, x
        elif 3 < hp <= 4:
            r, g, b = 0, x, c
        elif 4 < hp <= 5:
            r, g, b = x, 0, c
        elif 5 < hp < 6:
            r, g, b = c, 0, x
        
        rgb = (np.array([r,g,b])+m)*255
        return np.ceil(rgb).astype(int)

    # display a grid of colors using mpl subplots
    # originally designed for a jupyter notebook
    @classmethod
    def plot_colors(cls, colors:'[[r,g,b]]', grid:'(rows,cols)' = (1,1),
                    axis:bool = True, save_path:str = None):
        # assumed rows*cols == len(colors)
        if grid == (1,1): # if single cell 
            plt.imshow([[colors[0]]])
            plt.axis('off')
            
        else:
            i = 0
            nrows, ncols = grid
            fig, axs = plt.subplots(nrows, ncols)
            col_labels = list(string.ascii_lowercase)
            row_labels = list(range(1,nrows+1))
        
            if nrows == 1 or ncols == 1: # if single col or row
                nimgs = ncols if nrows == 1 else nrows
                for imgx in range(nimgs):
                    ax = axs[imgx]
                    ax.imshow([[colors[i]]])
                    if not axis: ax.axis('off') 
                    else: # include axis 
                        ax.tick_params(axis='both', which='both',length=0)
                        if nrows == 1:
                            ax.set_xticks([0])
                            ax.set_xticklabels([col_labels[imgx]])
                            ax.xaxis.tick_top()
                            ax.set_yticklabels([])
                        else:
                            ax.set_yticks([0])
                            ax.set_yticklabels([row_labels[imgx]])
                            ax.set_xticklabels([])
                    i += 1
            else:
                for rowx in range(nrows):
                    for colx in range(ncols):
                        ax = axs[rowx,colx]
                        ax.imshow([[colors[i]]])
                        
                        if not axis: ax.axis('off')
                        else: # include axis
                            ax.tick_params(axis='both', which='both',length=0)
                            ax.set_xticks([0])
                            ax.set_yticks([0])
                            
                            if rowx != 0:
                                ax.set_xticklabels([])
                            else:
                                ax.xaxis.tick_top()
                                ax.set_xticklabels([col_labels[colx]])
                                
                            if colx != 0:
                                ax.set_yticklabels([])
                            else:
                                ax.set_yticklabels([row_labels[rowx]])                
                        i += 1

        fig.patch.set_facecolor('white')           
        if save_path: plt.savefig(save_path, dpi=300)
        plt.show()
