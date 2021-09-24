import shutil
import os
import requests
from TikTokAPI import TikTokAPI

def create_dirs(path) -> bool:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return True
    except:
        return False

async def download(api_with_cookies: TikTokAPI, video_id: int, filename: str, no_watermark = False):
    try:
        video_info = await api_with_cookies.getVideoById(video_id)
        if no_watermark:
            video_url = video_info["itemInfo"]["itemStruct"]["video"]["downloadAddr"]
        else:
            video_url = video_info["itemInfo"]["itemStruct"]["video"]["playAddr"]
        if create_dirs(filename):
            r = requests.get(video_url, stream=True)
            if r.status_code == 200:
                with open(filename, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
            return filename
        else:
            raise ValueError("Couldn't create dirs.")
    except:
        raise ValueError("An error occurred when downloading the video.")
