# Data

## Source
- Dataset: Spotify 1.2M Songs
- URL: https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs
- Format: CSV
- Size: 330MB, 1.2M tracks

## Schema
| Column | Type | Description |
|---|---|---|
| name | string | Track name |
| artists | string | Artist name |
| year | int | Release year |
| valence | float | Musical positiveness (0=sad, 1=happy) |
| tempo | float | Tempo in BPM |
| duration_ms | long | Duration in milliseconds |
| acousticness | float | Acoustic confidence (0~1) |
| energy | float | Energy level (0~1) |

## Note
Raw data is excluded via .gitignore.
Run src/ingest/download_data.py to download.
