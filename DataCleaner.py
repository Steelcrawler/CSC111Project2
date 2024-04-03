import pandas as pd
file_path = 'spotify_songs.csv'
df = pd.read_csv(file_path)
columns_to_keep = ['track_artist','track_name', 'track_id', 'valence', 'energy', 'danceability', 'instrumentalness', 'tempo', 'speechiness', 'loudness', 'track_popularity']
cleaned_df = df.dropna(subset=columns_to_keep)
cleaned_df = cleaned_df[columns_to_keep]
cleaned_df = cleaned_df.reset_index(drop=True)
output_file_path = 'cleaned_spotify_songs.csv'
cleaned_df.to_csv(output_file_path, index=False)
summary_statistics = cleaned_df.describe()
output_file_path2='summary_stats.csv'
summary_statistics.to_csv(output_file_path2, index=False)
