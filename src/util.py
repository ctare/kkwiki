import requests
from bs4 import BeautifulSoup
import re
from glob import glob
import cv2
import os


def get_main_url():
    with open("url") as f:
        return f.read()[:-1]
main_url = get_main_url()

def authorize():
    with open("authorize") as f:
        return {"Authorization": f.read()[:-1]}

mime = "multipart/form-data"


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
        url = main_url
        return requests.post(url, headers=self.authorize, data={
            "encode_hint": "ぷ",
            "cmd": "edit",
            "page": self.page,
            "digest": self.digest,
            "msg": str(self),
            "write": "ページの更新",
            "original": "#setlinebreak",
        })

    def upload_image(self, filename):
        url = main_url
        with open(filename, 'rb') as binary:
            files = {"attach_file": (filename.split("/")[-1], binary, mime)}

            return requests.post(url, headers=self.authorize, data={
                "encode_hint": "ぷ",
                "pcmd": "post",
                "plugin": "attach",
                "refer": self.page,
                "max_file_size": "10485760",
            }, files=files)

    def get_home(self):
        url = f"{main_url}?{self.page}"
        response = requests.get(url, headers=self.authorize)
        return BeautifulSoup(response.text, "html.parser")

    def get_images(self):
        soup = self.get_home()
        return [a.text for a in soup.find(id="attach").find_all("a")[::2]]

def get_text():
    url = f"{main_url}?cmd=edit&page=%E8%8F%85%E9%87%8E%E8%B7%AF%E5%93%89"
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


def resize_image(filename, size=600):
    img = cv2.imread(filename)
    h, w = img.shape[:2]
    if h < w:
        nh = size
        nw = int((w * nh) / h)
    else:
        nw = size
        nh = int((h * nw) / w)
    img = cv2.resize(img, (nw, nh))
    cv2.imwrite(filename, img)


resized_check_path = "./images/resized.txt"
def get_local_images(resized=False):
    if resized:
        if not os.path.exists(resized_check_path):
            with open(resized_check_path, "w+"):
                pass

        with open(resized_check_path, "r") as f:
            return f.read().split("\n")[:-1]
    else:
        names = []
        for filename in glob("./images/*"):
            if filename.endswith(".txt"):
                continue
            names.append(filename)
        return names
