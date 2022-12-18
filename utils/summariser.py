from os import getenv
import openai
from utils.util import split_every


openai.api_key = getenv("openai")

pretext = "The below text is a youtube video transcript. generate a title and detailed summary. make a list of important points and characters if any"


def generate_summary(prompt, user_query=None):

    if user_query is not None:
        prompt = user_query + '\n"""' + prompt + '"""'
    else:
        prompt = pretext + '\n"""' + prompt + '"""'

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=650,
        top_p=0,
        frequency_penalty=1,
        presence_penalty=0,
    )
    summary = response["choices"][0]["text"]
    return summary, response
