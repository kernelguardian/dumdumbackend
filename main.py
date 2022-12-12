from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

from models.model import URL
from utils.util import is_youtube_url
from utils.youtubehelper import yt_subtitle_fetcher
from utils.transcriber import generate_transcript
from utils.summariser import generate_summary

app = FastAPI()


@app.post("/link")
def link(url: URL):
    if is_youtube_url(url.url):
        status, transcript = yt_subtitle_fetcher(url.url, lang="en")
    else:
        return JSONResponse(
            content={"message": "unprocessable url", "status_code": 422}
        )
    if status is False:
        transcript = generate_transcript()
    summary = generate_summary(transcript)
    return JSONResponse(content={"message": "OK", "status_code": 200, "data": summary})
