# 데이터 정리

## 출처
- 데이터셋: Spotify 1.2M Songs
- URL: https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs
- 형식: CSV
- 크기: 330MB, 약 120만 곡

## 샘플 데이터

원본 데이터는 용량이 커서 저장소에 포함하지 않고, `data/sample/` 에 100줄 샘플만 포함했습니다.
원본 데이터 재수집 시 `src/ingest/download_data.py` 를 실행하세요.

## 주요 스키마

원본 csv 컬럼 중 분석에 실제로 사용한 주요 컬럼은 다음과 같습니다.

### 음악 데이터

- name : 곡 제목
- artists : 아티스트명
- year : 발매 연도
- release_date : 발매 날짜

### 음악 특성 데이터

- valence : 음악 감정 긍정도 (0=우울, 1=행복)
- tempo : 템포 (BPM)
- duration_ms : 곡 길이 (밀리초)
- acousticness : 어쿠스틱 정도 (0~1)
- energy : 에너지 수준 (0~1)
- danceability : 댄서빌리티 (0~1)
- loudness : 음량 (dB)
- speechiness : 음성 비율 (0~1)
- instrumentalness : 악기 비율 (0~1)
- liveness : 라이브 느낌 (0~1)


