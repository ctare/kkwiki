import requests
from bs4 import BeautifulSoup
import re


def authorize():
    with open("authorize") as f:
        return {"Authorization": f.read()[:-1]}


class Text:
    def __init__(self, text, start, end, digest, page, authorize):
        self.text = text
        self.start = start
        self.end = end
        self.digest = digest
        self.page = page
        self.authorize = authorize
        del self.text[start: end]
        self.end = start

    def write(self, text):
        self.text.insert(self.start, text + "\n")
        self.start += 1
        self.end += 1

    def __str__(self):
        return "\n".join(self.text)

    def set_text(self):
        url = "http://www2.teu.ac.jp/kiku/wiki/"
        headers = self.authorize.copy()

        return requests.post(url, headers=headers, data={
            "encode_hint": "ぷ",
            "cmd": "edit",
            "page": self.page,
            "digest": self.digest,
            "msg": str(self),
            "write": "ページの更新",
            "original": "#setlinebreak",
        })


def get_text():
    url = "http://www2.teu.ac.jp/kiku/wiki/?cmd=edit&page=%E8%8F%85%E9%87%8E%E8%B7%AF%E5%93%89"
    headers = authorize()

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.find("textarea").text

    text = text.split("\n")
    for i, t in enumerate(text):
        if re.match("// *kkwiki *begin", t):
            start = i + 1
        if re.match("// *kkwiki *end", t):
            end = i
    digest = soup.find("input", attrs={"name": "digest"})["value"]
    page = soup.find("input", attrs={"name": "page"})["value"]
    return Text(text, start, end, digest, page, headers)
