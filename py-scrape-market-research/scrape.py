import orjson
from curl_cffi import requests
from selectolax.parser import HTMLParser
from rich import print

url = "https://ravecoffee.co.uk/products/best-selling-coffee-bundle?variant=19949439418422"
resp = requests.get(url, impersonate="chrome120")
html = HTMLParser(resp.text)
scripts = html.css("script[type='application/ld+json']")

for script in scripts:
    if "offers" in script.text():
        data = orjson.loads(script.text())
        print(data)
