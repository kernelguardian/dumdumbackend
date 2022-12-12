from urllib.parse import urlparse
from itertools import islice


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
