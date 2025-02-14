#!/usr/bin/env python3

import os
import json
import urllib.request

html = open('index.html', 'r', encoding='utf-8').read()
start_pos = html.find('\u200B') + len('\u200B') # zero-width spaces
end_pos = html.find('\u200B', start_pos)

newHtml = html[:start_pos] + 'Testing...' + html[end_pos:]

overwrite = open('index.html', 'w', encoding='utf-8')
overwrite.write(newHtml)
overwrite.close()
