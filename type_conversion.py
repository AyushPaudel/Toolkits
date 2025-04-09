# requires: Pydantic

from pydantic import BaseModel
from typing import List
import json


class Content(BaseModel):
    speaker: str
    context: str


class Episode(BaseModel):
    title: str
    speakers: List[str]
    content: List[Content]


class Podcast(BaseModel):
    body: List[Episode]


def parse_string_to_json(file_path: str) -> Podcast:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    episodes = []
    current_episode = None
    speakers_set = set()
    content_list = []

    for line in lines:
        line = line.strip()
        if line.startswith("Episode"):
            if current_episode:
                episodes.append(
                    Episode(
                        title=current_episode,
                        speakers=list(speakers_set),
                        content=content_list,
                    )
                )
                speakers_set = set()
                content_list = []

            current_episode = line
        elif ": " in line:
            speaker, context = line.split(": ", 1)
            speakers_set.add(speaker.strip())
            content_list.append(
                Content(speaker=speaker.strip(), context=context.strip())
            )

    if current_episode:
        episodes.append(
            Episode(
                title=current_episode,
                speakers=list(speakers_set),
                content=content_list,
            )
        )

    podcast = Podcast(body=episodes)
    return podcast


if __name__ == "__main__":
    input_file = "./string.txt"

    podcast = parse_string_to_json(input_file)

    output_file = "./stream.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(podcast.model_dump(), f, ensure_ascii=False, indent=4)

    print(f"Podcast JSON saved to {output_file}")
