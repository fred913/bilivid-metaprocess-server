import tempfile
from functools import lru_cache

import requests

from metaproc.bilibili_api.downloader import Aria2
from metaproc.bilibili_api.models import UserNotFound
from metaproc.bilibili_api.netcore import WebConnectionPool
from metaproc.config import HTTP_USER_AGENT

aria2 = Aria2()


class BilibiliAPI:

    def __init__(self):
        self._connections_pool = WebConnectionPool()
        self.cookies = {}

    @property
    def sess(self) -> requests.Session:
        """
        A shortcut to the current Session in this thread
        """
        self._connections_pool.sess.headers.update(
            {"User-Agent": HTTP_USER_AGENT})
        return self._connections_pool.sess

    def get_normal_video_url(self,
                             aid=None,
                             cid=None,
                             qn=None,
                             platform="pc",
                             fnval=None) -> dict:
        """Get the video URL for the given parameters.

        Args:
            cid (int): The cid of the video
            qn (int): The video quality level
            platform (str): The platform (pc or html5)

        Returns:
            dict: The JSON response from the API

        Raises:
            requests.exceptions.RequestException: If the request fails for any reason, including network errors,
            authentication failures, or invalid parameters.
        """
        url = "https://api.bilibili.com/x/player/playurl"

        params = {
            "avid": aid,
            "cid": cid,
            "qn": qn,
            "platform": platform,
            "fnval": fnval or 1
        }
        response = self.sess.get(
            url,
            params=params,
            cookies=self.cookies,
            headers={"Referer": "https://www.bilibili.com"})
        response.raise_for_status()
        response.encoding = "utf-8"
        try:
            return response.json()['data']
        except KeyError as e:
            print(response.json())
            raise e

    def get_video_info(self, aid: int | str) -> dict:
        """
        Retrieves the detailed information for a Bilibili video with the given aid or bvid.

        Args:
            aid (int | str): The AVID of the video.

        Returns:
            dict: A dictionary containing the detailed information of the video, including title, description, author,
            upload time, duration, etc. The keys of the dictionary are described in the Bilibili API documentation.

        Raises:
            requests.exceptions.RequestException: If the request fails for any reason, including network errors,
            authentication failures, or invalid parameters.
        """
        url = 'https://api.bilibili.com/x/web-interface/wbi/view'
        params = {'aid': aid}
        response = self.sess.get(url, params=params, cookies=self.cookies)
        response.raise_for_status()
        response.encoding = "utf-8"
        try:
            return response.json()['data']
        except KeyError as e:
            print(response.json())
            raise e

    def get_user_info(self, uid: str | int) -> dict:

        url = 'https://api.bilibili.com/x/space/acc/info'
        params = {'mid': uid}
        response = self.sess.get(url, params=params, cookies=self.cookies)
        response.raise_for_status()
        response.encoding = "utf-8"
        if response.json()['code'] == -404:
            raise UserNotFound(uid)
        try:
            return response.json()['data']
        except KeyError as e:
            print(response.json())
            raise e

    def search_user(self, prompt: str) -> dict:
        url = "https://api.bilibili.com/x/web-interface/search/type"
        params = {"search_type": "bili_user", "keyword": prompt}
        response = self.sess.get(url, params=params, cookies=self.cookies)
        response.raise_for_status()
        response.encoding = "utf-8"
        try:
            return response.json()['data']
        except KeyError as e:
            print(response.json())
            raise e

    @lru_cache(1024, True)
    def download_video_by_cid(self, aid: int, cid: int, qn=16):
        video_url_resp = self.get_normal_video_url(cid=cid, aid=aid, qn=qn)
        # ext = os.path.splitext(video_url_resp['durl'][0]['url'])[1]
        with tempfile.NamedTemporaryFile("wb", suffix=".mp4",
                                         delete=True) as tempf:
            print("Downloading video")
            tempf.close()
            filename = aria2.download(
                video_url_resp['durl'][0]['url'], {},
                tempf.name,
                headers={"Referer": "https://www.bilibili.com/"})
            return filename

    @lru_cache(1024, True)
    def download_aonly_by_cid(self, aid: int, cid: int, qn=16):
        video_url_resp = self.get_normal_video_url(cid=cid,
                                                   aid=aid,
                                                   qn=qn,
                                                   fnval=16)
        print(video_url_resp)
        # ext = os.path.splitext(video_url_resp['durl'][0]['url'])[1]
        with tempfile.NamedTemporaryFile("wb", suffix=".m4s",
                                         delete=True) as tempf:
            print("Downloading video")
            tempf.close()
            filename = aria2.download(
                video_url_resp['dash']['audio'][0]['base_url'], {},
                tempf.name,
                headers={"Referer": "https://www.bilibili.com/"})
            return filename

    @lru_cache(1024, True)
    def url_shorten(self, link: str):
        url = 'https://api.bilibili.com/x/share/click'
        data = {
            'build': '9331',
            'buvid': 'qp92wvbiiwercf5au381g1bzajou85hg',
            'oid': link,
            'platform': 'ios',
            'share_channel': 'COPY',
            'share_id': 'public.webview.0.0.pv',
            'share_mode': '3'
        }
        response = self.sess.post(url, data)
        response.encoding = "utf-8"
        datalink = response.json().get('data')['content']
        return datalink
