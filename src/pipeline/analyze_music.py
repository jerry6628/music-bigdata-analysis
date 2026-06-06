from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("MusicAnalysis").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

df = spark.read.csv(
    "/user/maria_dev/music/processed/cleaned",
    header=False
).toDF("name","artists","year","decade","valence","tempo",
       "duration_sec","acousticness","energy","loudness","danceability")

df = df.withColumn("year", F.col("year").cast("int")) \
       .withColumn("decade", F.col("decade").cast("int")) \
       .withColumn("valence", F.col("valence").cast("float")) \
       .withColumn("tempo", F.col("tempo").cast("float")) \
       .withColumn("duration_sec", F.col("duration_sec").cast("float")) \
       .withColumn("acousticness", F.col("acousticness").cast("float")) \
       .withColumn("energy", F.col("energy").cast("float")) \
       .withColumn("loudness", F.col("loudness").cast("float")) \
       .withColumn("danceability", F.col("danceability").cast("float"))

df.createOrReplaceTempView("music")

print("=== Q1: Valence by Decade ===")
q1 = spark.sql("""
    SELECT decade,
           COUNT(*) AS track_count,
           ROUND(AVG(valence), 3) AS avg_valence,
           ROUND(AVG(energy), 3) AS avg_energy
    FROM music
    WHERE decade >= 1950
    GROUP BY decade
    ORDER BY decade
""")
q1.show()
q1.coalesce(1).write.mode("overwrite").option("header","true") \
  .csv("/user/maria_dev/music/result/q1_valence")

print("=== Q2: Tempo and Duration by Decade ===")
q2 = spark.sql("""
    SELECT decade,
           COUNT(*) AS track_count,
           ROUND(AVG(tempo), 2) AS avg_tempo,
           ROUND(AVG(duration_sec), 1) AS avg_duration_sec
    FROM music
    WHERE decade >= 1950
    GROUP BY decade
    ORDER BY decade
""")
q2.show()
q2.coalesce(1).write.mode("overwrite").option("header","true") \
  .csv("/user/maria_dev/music/result/q2_tempo_duration")

print("=== Q3: Acousticness by Decade ===")
q3 = spark.sql("""
    SELECT decade,
           COUNT(*) AS track_count,
           ROUND(AVG(acousticness), 3) AS avg_acousticness,
           ROUND(AVG(energy), 3) AS avg_energy
    FROM music
    WHERE decade >= 1950
    GROUP BY decade
    ORDER BY decade
""")
q3.show()
q3.coalesce(1).write.mode("overwrite").option("header","true") \
  .csv("/user/maria_dev/music/result/q3_acousticness")

print("Done!")
spark.stop()
