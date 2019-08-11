import mistune

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
        return f"{text}\n"

    def image(self, link, title, alt):
        return f"#ref({link},left)"

    def link(self, link, title, text):
        return f"[[{text}:{link}]]"

puki = PukiwikiRenderer()
md = mistune.Markdown(renderer=puki)

text = ""
try:
    while True:
        text += input() + "\n"
except: pass

print(md(text) + "\n#comment")
