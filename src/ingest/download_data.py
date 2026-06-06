import os
import subprocess

DATASET = "rodolfofigueroa/spotify-12m-songs"
RAW_DIR = "data/raw"

if not os.path.exists(RAW_DIR):
    os.makedirs(RAW_DIR)

print("[+] Downloading: " + DATASET)
ret = os.system("kaggle datasets download -d " + DATASET + " -p " + RAW_DIR + " --unzip")

if ret == 0:
    print("[Done] Download complete!")
else:
    print("[Failed] Error occurred")
