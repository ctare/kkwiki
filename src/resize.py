import util

resized = util.get_local_images(resized=True)
with open(util.resized_check_path, "a") as f:
    for filename in util.get_local_images(resized=False):
        if filename not in resized:
            print("resize!!!", filename)
            util.resize_image(filename)
            f.write(f"{filename}\n")
