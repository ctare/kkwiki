import util
from glob import glob

text = util.get_text()
image_names = text.get_images()
for filename in util.get_local_images():
    if filename.split("/")[-1] not in image_names:
        text.upload_image(filename)
        print("upload!!!", filename)

