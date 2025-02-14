#!/usr/bin/env python3

from datetime import datetime
import json
import os
import time
import urllib.request

pageContent = "<h2>Server Status</h2><p>"

servers = [
    "anchor.hope.edu",
    "blogs.hope.edu",
    "hope.edu",
    "magazine.hope.edu",
    "opus.hope.edu",
    "wths.hope.edu",
]

for server in servers:
    try:
        with urllib.request.urlopen("https://"+server) as response:
            if response.status == 200:
                pageContent += "✅ <span style='color:#67c354;'>" + server + "</span> <span style='font-size:10px;'>(" + str(response.status) + ")</span>"
            else:
                pageContent += "🟨 <span style='color:#ed3f56;'>" + server + "</span> <span style='font-size:10px;'>(" + str(response.status) + ")</span>"
    except Exception as e:
        pageContent += "❌ <span style='color:#ed3f56;'>" + server + "</span> <span style='font-size:10px;'>(" + str(e) + ")</span>"
    pageContent += "<br>"
        
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
pageEnd = "<footer>Last updated: "+(datetime.now()).strftime('%l:%M%p %z on %b %d, %Y')+"</footer></body></html>"

# Build final page
newHtml = pageStart + pageContent + pageEnd

# Overwrite the current page contents
overwrite = open('index.html', 'w', encoding='utf-8')
overwrite.write(newHtml)
overwrite.close()
