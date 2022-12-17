from os import getenv
import openai
from utils.util import split_every

openai.api_key = getenv("openai")

pretext = "The below text is a youtube video transcript, Generate a title and a summary.Explain what it is about? if there are characters in this conversation mention about them. Also make a list of important points and references for later use"

pretext_notitle = "The below text is a youtube video transcript, Generate a summary.Explain what it is about? if there are characters in this conversation mention about them. make a list of important points and references for later use"

n = 100


def generate_summary(transcript):
    splitted_transcript = list(split_every(transcript, n))
    print(len(splitted_transcript))
    response = []
    for transcript_part in splitted_transcript:
        if len(response) == 0:
            prompt = pretext
        else:
            prompt = pretext_notitle
        for t in transcript_part:
            prompt += " " + t
            prompt += "\n"

        response.append(
            openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0,
                max_tokens=581,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
        )

    final_response = ""
    for r in response:
        final_response += r["choices"][0]["text"]
    return final_response
