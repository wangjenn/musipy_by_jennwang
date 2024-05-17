import pandas as pd

big5music = pd.read_csv('/Users/jenniferwang/musipy_by_jennwang/data/big5_music_fixed.csv')
song_names = pd.read_csv('/Users/jenniferwang/musipy_by_jennwang/data/songs_names.csv')

merged = song_names.merge(big5music, how='left', on='Variable')