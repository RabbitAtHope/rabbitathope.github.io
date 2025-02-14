#!/usr/bin/env python3

import json
import os
import urllib.request

# html = open('index.html', 'r', encoding='utf-8').read()

# Build page content
pageStart = "<!DOCTYPE html><html><body>"
pageContent = "<h1>Testing</h1><p>Testing...</p>"
pageEnd = "</body></html>"

# Build final page
newHtml = pageStart + pageContent + pageEnd

# Overwrite the current page contents
overwrite = open('index.html', 'w', encoding='utf-8')
overwrite.write(newHtml)
overwrite.close()
