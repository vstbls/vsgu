import markdown
import os
import re
import json
from datetime import datetime
from hashlib import md5
from markdown.extensions.codehilite import CodeHiliteExtension

class PageConverter:
    def __init__(self) -> None:
        self.load_data()

        self.process_pages()
        
        self.generate_catalog()
        
        self.serialize_metadata()

    def load_data(self) -> None:
        self.load_metadata()
        self.load_posts()
        self.load_template()

    def load_metadata(self) -> None:
        with open("metadata.json", encoding="utf8") as m:
            self.metadata = json.load(m)
        for file in list(self.metadata["posts"].keys()): # Remove posts that've been deleted
            if not os.path.isfile(file):
                self.metadata["posts"].pop(file)

    def load_posts(self) -> None:
        print("Checking for posts...")
        self.post_files = os.listdir("./posts/")

    def load_template(self) -> None:
        print("Loading template...")
        with open("./html/template.html", encoding="utf8") as template_file:
            self.template = "".join(template_file.readlines())

    def process_pages(self) -> None:
        for p in self.post_files:
            print(f"Processing post {p}...")
            self.path = f"./posts/{p}"
            with open(self.path, encoding="utf8") as post_file:
                self.content = post_file.readlines()
            self.title = self.content[0][1:] if self.content[0][0] == "#" else self.content[0] # Ensuring the leading Markdown '#' doesn't end up in the title
            
            self.update_post_metadata()
            self.post_metadata = self.metadata["posts"][self.path] # Get current post's metadata for later on

            print("Converting to HTML...")
            self.content = markdown.markdown("".join(self.content), extensions=["codehilite"]) # TODO: Add CodeHilite
            
            self.check_latex()
            self.combine_template()

            self.write_post(p[:-2] + "html")

    def update_post_metadata(self) -> None:
        with open(self.path, "rb") as post_binary:
            post_hash = md5(post_binary.read()).hexdigest()
        if self.path not in self.metadata["posts"]:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.metadata["posts"][self.path] = {
                "title": self.title,
                "published": now,
                "modified": "",
                "hash": post_hash
            }
        elif self.metadata["posts"][self.path]["hash"] != post_hash:
            self.metadata["posts"][self.path]["hash"] = post_hash
            self.metadata["posts"][self.path]["modified"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    def check_latex(self) -> None:
        print("Checking for LaTeX...")
        if re.search(r"\\\[.*\\\]|\\\(.*\\\)", self.content): # Used to be r"\\{2}\[.*\\{2}\]|\\{2}\(.*\\{2}\)" when I checked before converting to HTML
            print("Found LaTeX pattern match, adding MathJax...")
            self.content += '''<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
            <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>'''

    def combine_template(self) -> None:
        print("Combining post with template...")
        self.post = self.template.replace(
            "[[content]]",
            self.content)
        self.post = self.post.replace(
            "[[title]]",
            self.title)
        self.post = self.post.replace(
            "[[date]]",
            self.post_metadata["published"])
        self.post = self.post.replace(
            "[[modified]]",
            self.post_metadata["modified"])
        # TODO: Add option for random text insertion
    
    def write_post(self, filename: str) -> None:
        print(f"Saving page to ./generated/{filename}...")
        with open(f"./generated/{filename}", "w", encoding="utf8") as generated:
            generated.write(self.post)

    def generate_catalog(self):
        return


    def serialize_metadata(self) -> None:
        print("Writing new metadata...")
        with open("metadata.json", "w", encoding="utf8") as m:
            json.dump(self.metadata, m)

if __name__ == "__main__":
    PageConverter()
    '''
    with open("metadata.json") as m:
        metadata: dict = json.load(m)
    for file in metadata["posts"].keys():
        if not os.path.isfile(file):
            metadata["posts"].pop(file)

    print("Checking for pages...")
    self.post_files = os.listdir("./pages/")
    
    print("Loading base...")
    with open("./html/main.html", encoding="utf8") as base_file:
        base = "\n".join(base_file.readlines())

    for p in self.post_files:
        print(f"Processing post {p}...")
        self.path = f"./pages/{p}"
        with open(self.path, encoding="utf8") as post_file:
            post = post_file.readlines()
            title = post[0][1:]
            if self.path not in metadata["posts"]:
                now = datetime.now()
                with open(self.path, "rb") as post_binary:
                    post_hash = md5(post_binary.read()).hexdigest()
                metadata["posts"][self.path] = {
                    "title": title,
                    "published": now,
                    "modified": now,
                    "hash": post_hash
                }
            if metadata["posts"][self.path]["hash"] != post_hash: # FIX THIS THIS IS A PLACEHOLDER
                metadata["posts"][self.path]["hash"] = post_hash # FIX THIS AS WELL
                metadata["posts"][self.path]["modified"] = datetime.now()
            post = "\n".join(post)
        
        print("Checking for LaTeX...")
        if re.search(r"\\{2}\[.*\\{2}\]|\\{2}\(.*\\{2}\)", post):
            print("Found LaTeX pattern match, adding MathJax...")
            post += '<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>\n<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>'
        
        print("Converting to HTML...")
        post = markdown.markdown(post)

        print("Combining with base...")
        post = base.replace("[[content]]", post)
        post = post.replace("[[title]]", title)

        filename = p[:-2] + "html"
        print(f"Saving page to ./generated/{filename}...")
        with open(f"./generated/{filename}", "w", encoding="utf8") as generated:
            generated.write(post)

    print("All done!")
    '''