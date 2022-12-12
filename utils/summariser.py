from os import getenv
from math import floor
import openai

openai.api_key = getenv("openai")

pretext = "The below text is a conversation, can you explain what it is about? if there are characters in this conversation mention about them. Generate a title and a summary  also"


def generate_summary(transcript):
    transcript = transcript[:500]
    prompt = pretext
    for t in transcript:
        prompt += " " + t
    prompt += "\n"
    # print(prompt)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=581,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response["choices"][0]["text"]
