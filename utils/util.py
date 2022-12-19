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


def format_custom_response(summary: str):
    response_data = {}
    response_data["title"] = ""
    response_data["summary"] = summary.replace("\n", "")
    response_data["points"] = ""
    return response_data


summary = """\n\nTitle: Exploring Afghanistan: A Journey Through Taliban Country\n\nSummary: In this video, Benjamin takes a journey through Afghanistan to explore the country and gain a better understanding of its people and culture. He visits Kabul, the capital city, where he sees the Taliban flag flying in the breeze. He then travels to Bamyan Province, home to ancient Buddhist ruins that were destroyed by the Taliban. Along his journey he meets locals from different ethnic backgrounds and experiences their hospitality. He also visits an old American military base that was abandoned after US troops pulled out of Afghanistan in 2011. Finally, he stops at a Hazari community where he learns about their liberal views on women's rights despite living under constant threat from Isis and other extremist groups. \n\nImportant Points/Characters: \n- Benjamin - traveler exploring Afghanistan \n- Kabul - capital city with Taliban flags flying \n- Bamyan Province - home to ancient Buddhist ruins destroyed by Taliban \n- Local people from different ethnic backgrounds - friendly hospitality  \n- Old American military base - abandoned after US troops pulled out of Afghanistan in 2011  \n- Hazari community - liberal views on women's rights despite living under constant threat"""


def format_response(summary: str):
    response_data = {}
    summary = summary.replace("\n", "")
    first_split = summary.split("Summary:")
    response_data["title"] = first_split[0].replace("Title:", "").strip()
    response_data["summary"] = first_split[1].strip()
    response_data["points"] = first_split[1].split("Important Points")[1]
    response_data["og"] = summary
    return response_data


print(format_response(summary))
