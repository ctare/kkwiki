from glob import glob
import datetime
import os
import locale
import numpy as np

locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

if not os.path.exists("entries"):
    os.mkdir("entries")

today = datetime.date.today()
filename = f"{today:%F}-{today:%a}.md"
header = f"{today.month}月{today.day}日（{today:%a}）"

fullpath = f"entries/{filename}"

template = f"""## {header}

* 研究
// {'o' * int(np.abs(np.random.normal()) * 2 + 1)}
"""

if not os.path.exists(fullpath):
    with open(fullpath, "w") as f:
        f.write(template)
print(fullpath)
