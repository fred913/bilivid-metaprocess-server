import os
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote
import aria2p
import subprocess

from metaproc.config import HTTP_USER_AGENT


def encode_cookies(cookies: Dict[str, str] | List[Tuple[str, str]]) -> str:
    results = []
    for k, v in (cookies.items() if isinstance(cookies, dict) else cookies):
        results.append("%s=%s" % (k, quote(v)))
    return "; ".join(results)


class Aria2:

    def __init__(self) -> None:
        self._init_rpc()

    def _init_rpc(self):
        self.child = subprocess.Popen([
            "/usr/bin/aria2c", "--enable-rpc", "--enable-rpc",
            "--disable-ipv6", "-x", "16", "-j", "16", "-s", "16"
        ])
        self.rpc = aria2p.API(aria2p.Client())

    def _check_rpc(self):
        if self.child.pid is None:
            self._init_rpc()

    def download(self,
                 url: str,
                 cookies: Dict[str, str] | List[Tuple[str, str]],
                 output_path: str,
                 headers: Optional[Dict[str, str]] = None,
                 user_agent: Optional[str] = None):
        self._check_rpc()
        print("Downloading", url, "to", output_path)
        d, o = os.path.split(output_path)
        headers_ = ["Cookie: " + encode_cookies(cookies)]
        if len(cookies) == 0:
            headers_ = []
        for k, v in (headers or {}).items():
            headers_.append("%s: %s" % (k, v))
        print("Built headers:", headers_)
        opt = aria2p.Options(self.rpc, {
            "allow_overwrite": True,
            "header": headers_,
            "out": o,
            "dir": d
        })
        opt.user_agent = user_agent or HTTP_USER_AGENT
        result = self.rpc.add(url, options=opt)[0]
        while not (result.is_complete or not result.is_active):
            result.update()
        if not result.is_complete:
            print(result.options.header)
            raise RuntimeError("Invalid download status")
        print("Downloaded", result.files[0].path)
        return str(result.files[0].path)