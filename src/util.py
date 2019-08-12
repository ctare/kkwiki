import requests
from bs4 import BeautifulSoup
import re
from glob import glob
import cv2
import os


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
        url = "http://www2.teu.ac.jp/kiku/wiki/"
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
        url = "http://www2.teu.ac.jp/kiku/wiki/"
        with open(filename, 'rb') as binary:
            files = {"attach_file": (filename.split("/")[-1], binary, mime)}

            return requests.post(url, headers=self.authorize, data={
                "encode_hint": "ぷ",
                "pcmd": "post",
                "plugin": "attach",
                "refer": self.page,
                "max_file_size": "10485760",
            }, files=files)

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


def resize_image(filename, size=300):
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


# resized_check_path = "./images/resized.txt"
# if not os.path.exists(resized_check_path):
#     with open(resized_check_path, "w+"):
#         pass
#
# with open(resized_check_path, "r") as f:
#     resized = f.read().split("\n")[:-1]
#
# with open(resized_check_path, "a") as f:
#     for filename in glob("./images/*"):
#         if filename.endswith(".txt"):
#             continue
#         if filename not in resized:
#             print("resize!!!", filename)
#             resize_image(filename)
#             f.write(f"{filename}\n")

text = get_text()
text.upload_image("./images/kkwiki_test.png")
