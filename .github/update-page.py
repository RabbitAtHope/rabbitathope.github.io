#!/usr/bin/env python3

import json
import os
import requests
import urllib.request

pageContent = "<p>"

servers = [
    "anchor.hope.edu",
    "blogs.hope.edu",
    "hope.edu",
    "magazine.hope.edu",
    "opus.hope.edu",
    "wths.hope.edu",
]

for server in servers:
    r = requests.get(server, allow_redirects=True, verify=False, timeout=3.0)
    if r.status_code == 200:
        pageContent += "✅"
    else:
        pageContent += "❌"
    pageContent += " " + server
        
pageContent += "</p>"

# Build page content
pageStart = "<!DOCTYPE html><html><body><style>" + \
    "* {background-color:#1d1b30;color:white;font-family:monospace;}" + \
    "hr { margin-block-start:0px;margin-block-end:0px;border-color:#3a3257; }" + \
    "h1 { font-size:1.7em;margin-block-start:0.4em;margin-block-end:0.4em; }" + \
    "h2 { font-size:1.2em;margin-block-start:0px;margin-block-end:0px;background-image:linear-gradient(to right, #3a3257, #1d1b30);border:2px solid #3a3257; }" + \
    "h3 { font-size:12px;margin-block-start:0.4em;margin-block-end:0.4em; }" + \
    "h4 { font-size:0.8em;margin-block-start:0.4em;margin-block-end:0.4em; }" + \
    "</style>"
pageEnd = "</body></html>"

# Build final page
newHtml = pageStart + pageContent + pageEnd

# Overwrite the current page contents
overwrite = open('index.html', 'w', encoding='utf-8')
overwrite.write(newHtml)
overwrite.close()
