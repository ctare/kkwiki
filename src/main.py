import mistune
from glob import glob
import util

class PukiwikiRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return f"ok {code} ok"
        return f"ok {code}:{lang} ok"

    def header(self, text, level, raw=None):
        return f"{'*' * level} {text}\n"

    def list(self, body, ordered=True):
        return f"\n{body}"

    def list_item(self, text):
        return f"- {text}\n\n"

    def paragraph(self, text):
        return f"{text}\n\n"

    def image(self, link, title, alt):
        return f"#ref({link.split('/')[-1]},left)"

    def link(self, link, title, text):
        return f"[[{text}:{link}]]"

puki = PukiwikiRenderer()
md = mistune.Markdown(renderer=puki)

def puki(filename):
    with open(filename) as f:
        return md(f.read()) + "\n#comment\n"


print("merging")
merged = "\n".join([puki(filename) for filename in sorted(glob("./entries/*"), reverse=True)])

print("getting text")
text = util.get_text()

text.write(merged)
print("writing text")
response = text.set_text()
print(response)
