import requests
from bs4 import BeautifulSoup


def get_drug_info(question):
    url = "https://www.drugs.com/search.php"
    params = {
        "searchterm": f"{question}",
        "a": "1"
    }

    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, "html.parser")

    first_result = soup.find("div", class_="ddc-media-list ddc-search-results").find("a")

    if first_result:
        href = first_result.get("href")

        if href:
            response = requests.get(href)
            soup = BeautifulSoup(response.content, "html.parser")
            result = soup.find("div", class_="contentBox")

            if result:
                return result.text
