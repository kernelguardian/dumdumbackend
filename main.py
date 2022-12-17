from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

load_dotenv()

from models.model import URL
from utils.util import is_youtube_url
from utils.youtubehelper import yt_subtitle_fetcher
from utils.transcriber import generate_transcript
from utils.summariser import generate_summary
from utils.loghelper import MyLogger

logger = MyLogger.__call__().get_logger()


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/link")
def link(url: URL):

    logger.info("API CALLED:/link: {}".format(url))
    print(url)
    if is_youtube_url(url.url):
        status, transcript = yt_subtitle_fetcher(url.url, lang="en")
    else:
        return JSONResponse(
            content={"message": "unprocessable url", "status_code": 422}
        )
    if status is False:
        transcript = generate_transcript()
    summary = generate_summary(transcript)
    
    response_data = {}
    response_data["title"] = "title"
    response_data["summary"] = summary
    response_data["notes"] = ["notes", "2"]
    return JSONResponse(
        content={"message": "OK", "status_code": 200, "data": response_data}
    )
