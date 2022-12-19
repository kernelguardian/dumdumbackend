from urllib.parse import urlparse
from itertools import islice
from typing import List

from fastapi.responses import JSONResponse
import spacy

nlp = spacy.load("en_core_web_sm")
stop_words = spacy.lang.en.stop_words.STOP_WORDS


def is_youtube_url(url: str) -> bool:
    parsed_url = urlparse(url)
    if parsed_url.hostname == "www.youtube.com":
        return True
    return False


def split_every(iterable, n):
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))


def minimizer(transcript: List):
    LIMIT = 3000
    text_transcript = " ".join(transcript)
    doc = nlp(text_transcript)
    filtered_tokens = [token.text for token in doc if not token.is_stop]
    filtered_tokens_text = " ".join(filtered_tokens)
    filtered_tokens_text = filtered_tokens_text.replace("  ", " ")
    filtered_tokens_text = filtered_tokens_text.replace("  ", " ")

    spliced_transcript = filtered_tokens_text.split(" ")

    spliced_transcript = spliced_transcript[:LIMIT]
    spliced_transcript = " ".join(spliced_transcript)
    return spliced_transcript


def response_handler(data=None, message=None, status_code=200):
    if data is None:
        content = message
    else:
        content = data
    return JSONResponse(status_code=status_code, content=content)


def format_response(summary: str):
    response_data = {}
    summary = summary.replace("\n", "")
    first_split = summary.split("Summary:")
    response_data["title"] = first_split[0].replace("Title:", "").strip()
    response_data["summary"] = first_split[1].strip()
    response_data["points"] = first_split[1].split("Important Points:")[1]
    response_data["og"] = summary
    return response_data


def format_custom_response(summary: str):
    response_data = {}
    response_data["title"] = ""
    response_data["summary"] = summary.replace("\n", "")
    response_data["points"] = ""
    return response_data
