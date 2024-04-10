import os

ACRCLOUD_HOST = os.environ.get("ACRCLOUD_HOST",
                               "identify-cn-north-1.acrcloud.cn")
ACRCLOUD_KEY = os.environ.get("ACRCLOUD_KEY")
ACRCLOUD_SECRET = os.environ.get("ACRCLOUD_SECRET")
if ACRCLOUD_KEY is None or ACRCLOUD_SECRET is None:
    raise ValueError("ACRCLOUD_KEY and ACRCLOUD_SECRET must be set")
ACRCLOUD_TIMEOUT = int(os.environ.get("ACRCLOUD_TIMEOUT", 10))

HTTP_USER_AGENT = os.environ.get(
    "HTTP_USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44"
)  # you may modify it using .env file
