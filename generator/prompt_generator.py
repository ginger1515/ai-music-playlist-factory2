import json
import random
from datetime import datetime
import os

with open("generator/config.json", "r") as f:
    data = json.load(f)

playlist_key = random.choice(list(data["playlists"].keys()))
playlist = data["playlists"][playlist_key]

title = f"{playlist['title']} - {datetime.now().strftime('%Y-%m-%d')}"

prompt = f"""
Create a {playlist['genre']} track.

Mood:
{playlist['mood']}

BPM Range:
{playlist['bpm']}

Sound Design:
{", ".join(playlist['sound_profile'])}

Context:
Designed for Spotify playlist: {playlist['title']}
Keywords: {playlist['keywords']}

Rules:
{", ".join(data['rules'])}

Structure:
- seamless loop
- no vocals
- no prominent melody
- long listening friendly
"""

# output Suno-ready file
os.makedirs("output/suno", exist_ok=True)

filename = datetime.now().strftime("%Y-%m-%d_%H-%M") + ".txt"
path = f"output/suno/{filename}"

with open(path, "w") as f:
    f.write(title + "\n\n" + prompt)

print("Generated:", title)
