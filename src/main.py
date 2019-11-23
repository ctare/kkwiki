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
        size = "50%"
        if ":" in alt:
            size = alt.split(":")[-1]
        return f"#ref({link.split('/')[-1]},left,{size})"

    def link(self, link, title, text):
        return f"[[{text}:{link}]]"

puki = PukiwikiRenderer()
md = mistune.Markdown(renderer=puki)

def puki(filename, comments):
    with open(filename) as f:
        name = filename.split("/")[-1]
        comment = "\n".join(comments.get(name, ""))
        return md(f.read()) + f"\n//{name} cmt_begin\n{comment}\n#comment\n//{name} cmt_end\n"


print("getting text")
text = util.get_text()

print("merging")
merged = "\n".join([puki(filename, text.comments) for filename in sorted(glob("./entries/*"), reverse=True)])

text.write(merged)
print("writing text")
response = text.set_text()
print(response)
