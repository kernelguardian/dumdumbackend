from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from time import sleep

load_dotenv()

from models.model import URL
from utils.util import (
    is_youtube_url,
    minimizer,
    response_handler,
    format_response,
    format_custom_response,
    youtube_link_parser,
)
from utils.youtubehelper import yt_subtitle_fetcher
from utils.transcriber import generate_transcript
from utils.summariser import generate_summary
from utils.loghelper import MyLogger
from utils.parser import title_parser, summary_parser, keypoint_parser
from utils.supabase_handler import insert_data


logger = MyLogger.__call__().get_logger()


app = FastAPI(docs_url=None, redoc_url=None)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/summarizer")
async def summarizer(url: URL):

    logger.info("API CALLED:/summarizer: {}".format(url))
    is_youtube_link, video_id = youtube_link_parser(url.url)

    if is_youtube_link:
        custom_url = "https://www.youtube.com/watch?v=" + video_id
        status, transcript = yt_subtitle_fetcher(custom_url, lang="en")
    else:
        await insert_data(
            data={
                "link": url.url,
                "success": False,
                "error_type": "link_not_supported",
            }
        )
        return response_handler(
            message="I am sorry this link is not supported at this moment or there is something wrong with the link, please try again with another link, psst try this link  https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            status_code=422,
        )

    if status is False:
        await insert_data(
            data={
                "link": url.url,
                "success": False,
                "error_type": "no_transcript",
            }
        )
        return response_handler(
            message="Sorry, I am unable to process this video at this time, please check back soon, psst try this link  https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            status_code=422,
        )
        # Use this when transcriber is implemented
        transcript = generate_transcript()

    formatted_transcript = minimizer(transcript)
    summary, openai_response = generate_summary(formatted_transcript)

    await insert_data(
        data={"link": url.url, "transcript": transcript, "response": openai_response}
    )

    try:
        response_data = format_response(summary)
        return response_handler(data=response_data)
    except Exception as err:
        logger.warn("Formatting Error| URL:{} | error:{}".format(url, err))
        await insert_data(
            data={
                "link": url.url,
                "transcript": transcript,
                "response": openai_response,
                "success": False,
                "error_type": "formatting",
            }
        )
        return response_handler(
            message="Hmm, it looks like our bot messed something up, please try again",
            status_code=200,
        )


@app.post("/querysummarizer")
async def query_summarizer(request_body: URL):

    logger.info(
        "API CALLED:/querysummarizer: {} | {}".format(
            request_body, request_body.user_query
        )
    )
    is_youtube_link, video_id = youtube_link_parser(request_body.url)

    if is_youtube_link:
        custom_url = "https://www.youtube.com/watch?v=" + video_id

        status, transcript = yt_subtitle_fetcher(custom_url, lang="en")

    else:
        await insert_data(
            data={
                "link": request_body.url,
                "user_prompt": request_body.user_query,
                "success": False,
                "error_type": "link_not_supported",
            }
        )
        return response_handler(
            message="I am sorry this link is not supported at this moment or there is something wrong with the link, please try again with another link, psst try this link  https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            status_code=422,
        )

    if status is False:
        await insert_data(
            data={
                "link": request_body.url,
                "user_prompt": request_body.user_query,
                "success": False,
                "error_type": "no_transcript",
            }
        )
        return response_handler(
            message="Sorry, I am unable to process this video at this time, please check back soon, psst try this link  https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            status_code=422,
        )
        # Use this when transcriber is implemented
        transcript = generate_transcript()

    formatted_transcript = minimizer(transcript)
    summary, openai_response = generate_summary(
        formatted_transcript, request_body.user_query
    )
    formatted_response = format_custom_response(summary)

    await insert_data(
        data={
            "link": request_body.url,
            "user_prompt": request_body.user_query,
            "transcript": transcript,
            "response": openai_response,
        }
    )

    return response_handler(data=formatted_response)
