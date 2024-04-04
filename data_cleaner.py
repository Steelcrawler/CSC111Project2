"""CSC111 Project 2

File used to clean the spotify_songs.csv file. To run the cleaner, simply delete the else statement.
Note: Running the cleaning process will override files currently in the directory.
"""
import doctest
import pandas as pd
import python_ta

if __name__ == '__main__':
    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['pandas'],
        'max-line-length': 120
    })
else:
    file_path = 'spotify_songs.csv'
    df = pd.read_csv(file_path)
    columns_to_keep = ['track_artist', 'track_name', 'track_id', 'valence', 'energy',
                       'danceability', 'instrumentalness', 'tempo',
                       'speechiness', 'loudness', 'track_popularity']  # columns to keep from csv file
    cleaned_df = df.dropna(subset=columns_to_keep)  # drops rows with missing data
    cleaned_df = cleaned_df[columns_to_keep]
    cleaned_df = cleaned_df.reset_index(drop=True)
    output_file_path = 'cleaned_spotify_songs.csv'
    cleaned_df.to_csv(output_file_path, index=False)  # saves the cleaned data
    summary_statistics = cleaned_df.describe()
    output_file_path2 = 'summary_stats.csv'  #generates summary statistics for the data
    summary_statistics.to_csv(output_file_path2, index=False)
