#!/usr/bin/env python 3
from __future__ import with_statement                                                           

import contextlib
import requests

try:
    from urllib.parse import urlencode          

except ImportError:
    from urllib import urlencode
try:
    from urllib.request import urlopen

except ImportError:
    from urllib2 import urlopen

import sys
from flask import Flask, render_template_string, request


def make_tiny(url):
    request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url':url}))    
    with contextlib.closing(urlopen(request_url)) as response:                      
        return response.read().decode('utf-8')  # fixed typo in decode argument

app = Flask(__name__)

HTML_FORM = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>URL Shortener</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      background: linear-gradient(135deg, #f5f6fa 0%, #e5e9f2 100%);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      color: #222;
      margin: 0;
      padding: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .container {
      background: #fff;
      border-radius: 24px;
      box-shadow: 0 8px 32px 0 rgba(60,60,60,0.08);
      padding: 40px 32px 32px 32px;
      max-width: 420px;
      width: 100%;
      text-align: center;
    }
    h2 {
      font-weight: 600;
      margin-bottom: 24px;
      color: #222;
      letter-spacing: -1px;
    }
    form {
      margin-bottom: 18px;
    }
    input[type="text"] {
      width: 80%;
      padding: 12px 14px;
      border: 1px solid #d1d5db;
      border-radius: 12px;
      font-size: 1rem;
      outline: none;
      transition: border 0.2s;
      margin-bottom: 12px;
      background: #f8fafc;
    }
    input[type="text"]:focus {
      border: 1.5px solid #007aff;
      background: #fff;
    }
    input[type="submit"] {
      background: linear-gradient(90deg, #007aff 0%, #34c759 100%);
      color: #fff;
      border: none;
      border-radius: 12px;
      padding: 12px 32px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 2px 8px 0 rgba(0,122,255,0.08);
      transition: background 0.2s;
    }
    input[type="submit"]:hover {
      background: linear-gradient(90deg, #0051a8 0%, #28a745 100%);
    }
    .short-url {
      margin-top: 18px;
      padding: 16px;
      background: #f1f8ff;
      border-radius: 12px;
      box-shadow: 0 1px 4px 0 rgba(0,122,255,0.06);
      font-size: 1.1rem;
      word-break: break-all;
      display: inline-block;
    }
    a {
      color: #007aff;
      text-decoration: none;
      font-weight: 500;
    }
    a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>URL Shortener</h2>
    <form method="post">
      <input type="text" name="long_url" placeholder="Enter long URL" required>
      <br>
      <input type="submit" value="Shorten">
    </form>
    {% if short_url %}
      <div class="short-url">
        <strong>Shortened URL:</strong><br>
        <a href="{{ short_url }}" target="_blank">{{ short_url }}</a>
      </div>
    {% endif %}
  </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    if request.method == 'POST':
        long_url = request.form.get('long_url')
        if long_url:
            short_url = make_tiny(long_url)
            # Send webhook after getting the short URL
            if short_url:
                try:
                    requests.post(
                        "https://hooks.slack.com/triggers/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",
                        json={"tiny-url-code": short_url}
                    )
                except Exception as e:
                    pass  # Optionally log or handle webhook errors
    return render_template_string(HTML_FORM, short_url=short_url)

if __name__ == '__main__':
    app.run(debug=True)