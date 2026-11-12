#!/usr/bin/env python3
"""Add a version stamp to the site's CSS and JS links so browsers load the newest files.

Browsers keep old copies of .css and .js files. After changing styles or scripts,
run:  python bump_version.py
Every page then asks for the files with a new ?v= stamp, so visitors get the update right away.
"""
import os, re, glob
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
STAMP = datetime.now().strftime("%Y%m%d%H%M")
PAT = re.compile(r'((?:href|src)="[^"]*?(?:Styles|JS)/[^"?]+\.(?:css|js))(?:\?v=[0-9A-Za-z]+)?"')


def bump(path):
    with open(path, encoding="utf-8", newline="") as f:
        s = f.read()
    new = PAT.sub(lambda m: f'{m.group(1)}?v={STAMP}"', s)
    if new != s:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new)
        return True
    return False


def main():
    files = glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "Articles", "Article_HTMLs", "*.html"))
    n = sum(bump(p) for p in files)
    for extra in ("generate_article.py", "update_nav.py"):
        bump(os.path.join(ROOT, extra))
    print(f"Version stamp {STAMP} applied to {n} pages.")


if __name__ == "__main__":
    main()
