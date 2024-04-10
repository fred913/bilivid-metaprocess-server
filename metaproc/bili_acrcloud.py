import json
import os

from acrcloud.recognizer import ACRCloudRecognizer

from metaproc.bilibili_api import biliapi
from metaproc.config import (ACRCLOUD_HOST, ACRCLOUD_KEY, ACRCLOUD_SECRET,
                             ACRCLOUD_TIMEOUT)
from metaproc.ffutils import convert_media_to_wav


def acrcloud_recognition_to_human_readables(
        video_aid: int, pid: int, target_area: tuple[int, int]) -> str:
    # First, get CID and get video basic information
    print("Video2Text - Running now")
    cid, duration = None, None
    all_pages = []
    video_info = biliapi.get_video_info(aid=video_aid)
    for page in video_info['pages']:
        all_pages.append(page['page'])
        if page['page'] == pid:
            cid = page['cid']
            duration = page['duration']
            break
    if cid is None:
        raise ValueError("无效分P。有效值：" + ("、".join([str(i) for i in all_pages])))
    assert cid is not None
    assert duration is not None
    audio_path = biliapi.download_aonly_by_cid(aid=video_aid, cid=cid)
    audio_path = convert_media_to_wav(audio_path)

    acrrec = ACRCloudRecognizer({
        'host': ACRCLOUD_HOST,
        'access_key': ACRCLOUD_KEY,
        'access_secret': ACRCLOUD_SECRET,
        'timeout': ACRCLOUD_TIMEOUT
    })

    result = json.loads(
        str(
            acrrec.recognize_by_file(audio_path,
                                     target_area[0],
                                     rec_length=(target_area[1] -
                                                 target_area[0]))))

    # def convert_music_metadata_to_human_readables(data: dict,
    #                                               show_first_n: int = 3):
    #     try:
    #         result = "识别到%d个结果，显示前%d个：\n" % (
    #             len(data['metadata']['music']),
    #             min(len(data["metadata"]['music']), show_first_n))
    #         for count, music in enumerate(
    #                 data['metadata']['music'][:show_first_n]):
    #             title = music['title']
    #             contributors = [i['name'] for i in music['artists']]
    #             album = music['album']['name']
    #             play_offset = music['play_offset_ms'] / 1000
    #             reliability = music['score']

    #             result += f"#{count+1} - ({reliability}%) {title}" + "\n"
    #             result += "艺术家：" + ', '.join(contributors) + "\n"
    #             result += "专辑：" + album + "\n"
    #             result += f"音乐播放到 {play_offset:.2f} 秒" + ("\n" * 2)
    #         return result.strip()
    #     except KeyError as e:
    #         if data['status']['code'] == 1001:
    #             return "很抱歉，听歌识曲没有识别到结果！"
    #         import traceback
    #         traceback.print_exc()
    #         print(json.dumps(data, ensure_ascii=False, indent=4))
    #         raise e from None

    # result = convert_music_metadata_to_human_readables(result)
    return result
