data = LOAD '/user/maria_dev/music/raw/tracks_features.csv'
    USING PigStorage(',')
    AS (
        id:chararray, name:chararray, album:chararray,
        album_id:chararray, artists:chararray, artist_ids:chararray,
        track_number:chararray, disc_number:chararray, explicit:chararray,
        danceability:float, energy:float, key:int, loudness:float,
        mode:int, speechiness:float, acousticness:float,
        instrumentalness:float, liveness:float, valence:float,
        tempo:float, duration_ms:long, time_signature:chararray,
        year:int, release_date:chararray
    );

no_header = FILTER data BY year > 1900 AND year <= 2024;

cleaned = FILTER no_header BY
    name IS NOT NULL AND
    valence IS NOT NULL AND
    tempo IS NOT NULL AND tempo > 0.0 AND
    duration_ms IS NOT NULL AND duration_ms > 0 AND
    acousticness IS NOT NULL AND
    energy IS NOT NULL;

selected = FOREACH cleaned GENERATE
    name,
    artists,
    year,
    (int)((year / 10) * 10) AS decade,
    valence,
    tempo,
    (float)(duration_ms / 1000.0) AS duration_sec,
    acousticness,
    energy,
    loudness,
    danceability;

STORE selected INTO '/user/maria_dev/music/processed/cleaned'
    USING PigStorage(',');
