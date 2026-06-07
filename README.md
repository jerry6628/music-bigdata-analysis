# music-bigdata-analysis

시대별 음악 메타데이터 변화를 분석하기 위한 빅데이터 처리 및 분석 프로젝트

# 분석 개요

이번 프로젝트는 다양한 시대의 노래를 듣다보니 느껴지는 차이점으로부터 발발된 질의로 시대가 지나면서 음악의 특징이 어떻게 달라졌는지 알아보고자 시작하였다. 음악은 단순히 듣기만 하는 콘텐츠가 아니라, 그 시대의 분위기나 동시대 사람들의 취향을 어느 정도 반영한다고 생각한다. 그래서 여러 시대의 음악 데이터를 모아 분석하면 특정 시기에 어떤 장르가 많이 등장했는지, 곡의 길이나 템포 같은 특징이 어떻게 변했는지 확인할 수 있을 것이라고 생각했다.

이를 위해 kaggle에서 제공하는 spotify 음악 메타데이터를 수집하고, hadoop 기반 환경을 활용하여 시대별 음악 특징의 변화를 분석하고자 하였다. 즉, 이번 프로젝트의 중추는 단순한 데이터 조회가 아닌 1950년대부터 2020년대까지의 음악이 감정적으로, 또는 형식적으로, 그리고 소리가 담아낸 음악의 성질이 어떻게 바뀌었는지를 데이터로 확인하는 것이다.

# 1. 분석 문제 정의
분석하기 전 효율적인 분석을 위하여 주요 분석 질문들을 만들어 보자면 하기 사항과 같다.
1. 시대별 음악의 감정은 당시 시대상·대중 분위기와 어떤 관계가 있는가?
2. 시대별 평균 곡 길이와 템포는 어떻게 변했는가?
3. 시대별로 어쿠스틱 음악은 줄고 전자음악은 늘었는가?

# 2. 사용 데이터

본 프로젝트에서는 Kaggle에서 제공하는 공개 음악 메타데이터를 사용하였다.

- 데이터셋: Spotify 1.2M Songs
- 출처: [Kaggle](https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs)
- 형식: CSV
- 규모: 330MB, 약 120만 곡
- 수집 방법: Python 스크립트(download_data.py)를 통해 Kaggle API로 자동 수집

수집한 데이터는 HDFS에 업로드하여 분석에 사용하였다. 데이터의 크기가 크기 때문에 로컬 환경에서만 처리하지 않고, Hadoop 기반 환경에서 저장하고 처리하는 방식으로 진행하였다.

# 3. 기술 스택

| 단계 | 기술 | 역할 |
|---|---|---|
| 데이터 수집 | Python (Kaggle API) | 데이터 자동 다운로드 |
| 저장 | HDFS | 원본·처리·결과 데이터 저장 |
| 정제 | Apache Pig | 결측치 제거, 컬럼 선택, decade 컬럼 추가 |
| 분석 | Apache Spark / Spark SQL | 시대별 집계 및 통계 분석 |
| 시각화 | Matplotlib | 분석 결과 그래프 생성 |

# 4. 시스템 아키텍처
```
Kaggle 데이터 다운로드 (download_data.py)
        ↓
HDFS 적재 (/user/maria_dev/music/raw/)
        ↓  Pig: clean_music.pig
HDFS 정제 (/user/maria_dev/music/processed/)
        ↓  Spark: analyze_music.py
HDFS 결과 (/user/maria_dev/music/result/)
        ↓  Matplotlib: visualize.py
분석 결과 그래프 (music_analysis.png)
```

# 5. 데이터 처리 방법

## 1단계: 데이터 수집

Kaggle에서 제공하는 Spotify 1.2M Songs 데이터셋을 Python 스크립트(download_data.py)를 통해 자동 수집하였다. 수집된 데이터는 CSV 형식으로 약 120만 곡의 음악 메타데이터를 포함하며, 총 330MB 규모이다. 주요 컬럼은 다음과 같다.

- `name` : 곡 제목
- `artists` : 아티스트명
- `year` : 발매 연도
- `valence` : 음악 감정 긍정도 (0=우울, 1=행복)
- `tempo` : 템포 (BPM)
- `duration_ms` : 곡 길이 (밀리초)
- `acousticness` : 어쿠스틱 정도 (0~1)
- `energy` : 에너지 수준 (0~1)
- `loudness` : 음량 (dB)
- `danceability` : 댄서빌리티 (0~1)

## 2단계: HDFS 적재

수집한 CSV 파일을 HDFS의 `/user/maria_dev/music/raw/` 경로에 업로드하였다. 원본 데이터, 정제 데이터, 분석 결과를 각각 `raw/`, `processed/`, `result/` 디렉터리로 분리하여 관리하였다.

## 3단계: Pig 기반 데이터 정제

HDFS에 저장된 원본 CSV를 Pig로 불러와 다음과 같은 정제 작업을 수행하였다.

- **결측치 제거**: name, artists, year, tempo, duration_ms, acousticness, energy 컬럼에 null 값이 있는 레코드 제거
- **이상치 필터링**: year가 1900 이하이거나 2024 초과인 레코드, tempo가 0 이하인 레코드 제거
- **컬럼 선택**: 분석에 필요한 11개 컬럼만 추출
- **decade 컬럼 추가**: year를 10으로 나누어 시대 구간 컬럼 생성 (예: 1995 → 1990)
- **단위 변환**: duration_ms를 1000으로 나누어 초(sec) 단위로 변환

정제된 데이터는 HDFS의 `/user/maria_dev/music/processed/cleaned/` 경로에 저장하였다.

## 4단계: Spark 기반 분석

Pig로 정제된 데이터를 PySpark로 불러와 Spark SQL을 활용하여 3가지 분석 질문에 답하였다.

- **Q1 분석**: decade 기준으로 GROUP BY 후 valence, energy의 평균값 집계
- **Q2 분석**: decade 기준으로 GROUP BY 후 tempo, duration_sec의 평균값 및 표준편차 집계
- **Q3 분석**: decade 기준으로 GROUP BY 후 acousticness, energy의 평균값 집계 및 두 지표 간 변화 추이 비교

분석 결과는 HDFS의 `/user/maria_dev/music/result/` 경로에 CSV 형식으로 저장하였다.

## 5단계: 시각화

분석 결과 CSV를 로컬 환경으로 가져와 Matplotlib을 활용하여 시각화하였다.

- **Q1**: 시대별 valence 평균값 꺾은선 그래프
- **Q2**: 시대별 곡 길이(막대 그래프)와 템포(꺾은선 그래프)를 이중 축으로 표현
- **Q3**: 시대별 acousticness와 energy를 하나의 그래프에 겹쳐 두 지표의 교차 시점을 시각적으로 표현

# 6. 실행 방법

### 사전 준비
```bash
# Kaggle API 키 설정
mkdir -p ~/.kaggle
echo '{"username":"kaggle아이디","key":"kaggle키"}' > ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json

pip3 install kaggle --user
export PATH=$PATH:~/.local/bin
```

### 단계별 실행
```bash
# 1. 데이터 수집
python src/ingest/download_data.py

# 2. HDFS 업로드
hdfs dfs -mkdir -p /user/maria_dev/music/raw
hdfs dfs -put data/raw/tracks_features.csv /user/maria_dev/music/raw/

# 3. Pig 정제
pig -x mapreduce src/pipeline/clean_music.pig

# 4. Spark 분석
spark-submit src/pipeline/analyze_music.py

# 5. 결과 내보내기
hdfs dfs -getmerge /user/maria_dev/music/result/q1_valence result/q1_valence.csv
hdfs dfs -getmerge /user/maria_dev/music/result/q2_tempo_duration result/q2_tempo_duration.csv
hdfs dfs -getmerge /user/maria_dev/music/result/q3_acousticness result/q3_acousticness.csv

# 6. 시각화
python src/analyze/visualize.py
```

# 7. 분석 결과

![분석 결과 그래프](music_analysis.png)

### Q1. 시대별 음악 감정(valence) 변화
1950년대부터 1970년대까지는 valence가 0.55~0.56으로 비교적 높게 유지되었으나, 이후 지속적으로 하락하여 2020년대에는 0.406까지 떨어졌다. 1980년대에는 펑크·헤비메탈 등 사회적 저항 음악이 등장하며 감소세가 시작되었고, 1990년대에는 그런지·얼터너티브 록의 전성기를 맞아 우울하고 어두운 감성의 음악이 주류를 이루었다. 2010년대 이후에는 SNS의 확산과 함께 감성적이고 내면적인 음악 트렌드가 반영된 것으로 보인다.

### Q2. 시대별 곡 길이·템포 변화
곡 길이는 1960년대 199초로 가장 짧았다가 1970년대에 248초로 늘어난 뒤, 2020년대에는 다시 219초로 감소하는 추세를 보였다. 스트리밍 서비스가 보편화된 2010년대 이후 짧은 곡에 대한 선호가 반영된 것으로 해석된다. 템포는 114~121 BPM 범위에서 시대 전반에 걸쳐 큰 변화 없이 안정적으로 유지되었다.

### Q3. acousticness와 energy의 상관관계
acousticness는 1950년대 0.762에서 2020년대 0.282로 급감한 반면, energy는 같은 기간 0.372에서 0.609로 꾸준히 상승하였다. 두 지표는 1970년대에 교차점을 형성하며 이 시기를 기점으로 전자음악이 주류로 전환되었음을 보여준다. 즉 acousticness와 energy는 시대에 따라 뚜렷한 음의 상관관계를 나타낸다.

# 8. 참고 자료
- 데이터: [Spotify 1.2M Songs](https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs)
- Apache Pig: https://pig.apache.org/
- Apache Spark: https://spark.apache.org/

## AI Tool Usage
- Claude: 파이프라인 코드 구조 설계 보조, Pig/Spark 스크립트 디버깅, README 작성 보조

