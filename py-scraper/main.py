import requests
from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel, AnyHttpUrl
from datetime import date


class Episode(BaseModel):
    show_number: int
    date: date
    title: str
    url: AnyHttpUrl
    guest: str


base_url = "https://talkpython.fm"
url = "https://talkpython.fm/episodes/all"


def extract_episode_data(row: Tag) -> dict:
    model_data = {}
    row_data = row.select("td")

    for i, td in enumerate(row_data):
        if i == 0:
            model_data["show_number"] = td.text.replace("#", "")
        elif i == 1:
            model_data["date"] = td.text
        elif i == 2:
            # get the anchor tag and extract the href (add the base url) and text (title)
            link = td.find("a")
            if link and isinstance(link, Tag):
                model_data["url"] = base_url + link.attrs["href"]
                model_data["title"] = link.text
        elif i == 3:
            model_data["guest"] = td.text

    return model_data


if __name__ == "__main__":
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    rows = soup.select("tbody > tr")

    episodes = [Episode(**extract_episode_data(row)) for row in rows]

    search_term = input('Enter a search term: ')
    results = [e for e in episodes if search_term.lower() in e.title.lower()]

    print(f"\nEpisodes with the term {search_term}: ")
    print(results)

