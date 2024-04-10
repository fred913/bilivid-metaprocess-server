from fastapi import FastAPI

from metaproc.bili_acrcloud import acrcloud_recognition_to_human_readables

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/recog_music_in_bili_video")
def api_recog_music_in_bili_video(video_aid: int, pid: int, target_sec: int):
    target_area = (target_sec, target_sec + 5)
    return acrcloud_recognition_to_human_readables(video_aid, pid, target_area)
