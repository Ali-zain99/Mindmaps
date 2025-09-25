import zlib
import requests

# ---------- PlantUML encoding ----------
def encode6bit(b: int) -> str:
    if b < 10:
        return chr(48 + b)
    b -= 10
    if b < 26:
        return chr(65 + b)
    b -= 26
    if b < 26:
        return chr(97 + b)
    b -= 26
    if b == 0:
        return "-"
    if b == 1:
        return "_"
    return "?"

def append3bytes(b1: int, b2: int, b3: int) -> str:
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return (
        encode6bit(c1 & 0x3F)
        + encode6bit(c2 & 0x3F)
        + encode6bit(c3 & 0x3F)
        + encode6bit(c4 & 0x3F)
    )

def encode64(data: bytes) -> str:
    res = ""
    i = 0
    length = len(data)
    while i < length:
        if i + 2 == length:
            res += append3bytes(data[i], data[i + 1], 0)
        elif i + 1 == length:
            res += append3bytes(data[i], 0, 0)
        else:
            res += append3bytes(data[i], data[i + 1], data[i + 2])
        i += 3
    return res

def plantuml_encode(text: str) -> str:
    compressed = zlib.compress(text.encode("utf-8"))[2:-4]  # strip zlib headers
    return encode64(compressed)

def generate_mindmap(uml_code: str, output_file: str = "mindmap.svg"):
    encoded = plantuml_encode(uml_code)
    url = f"http://www.plantuml.com/plantuml/svg/{encoded}"  # <-- SVG instead of PNG
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(resp.content)
        print(f"[ok] Mind map saved to {output_file}")
    else:
        print(f"[error] PlantUML server {resp.status_code}: {resp.text[:200]}")

# ---------- Example PlantUML with screenshot link ----------
uml_code = """@startmindmap

* Site Mind Map
** Home - 340B Price Guide
*** Links
**** https://www.340bpriceguide.net/
**** https://www.340bpriceguide.net/340b-search
**** https://www.340bpriceguide.net/about-us
**** https://www.340bpriceguide.net/articles-news
**** https://www.340bpriceguide.net/articles-news/126-weekly-product-shortages
**** https://www.340bpriceguide.net/articles-news/50-what-is-340b
**** https://www.340bpriceguide.net/client-login?view=registration
**** https://www.340bpriceguide.net/client-login?view=remind
**** https://www.340bpriceguide.net/client-login?view=reset
**** https://www.340bpriceguide.net/contact-us
**** https://www.340bpriceguide.net/index.php
**** https://www.340bpriceguide.net/index.php/about-us
**** https://www.340bpriceguide.net/index.php/articles-news
**** https://www.340bpriceguide.net/index.php/contact-us
*** Forms
**** Form 1: Action=/, Method=post
***** Input: name=searchword, type=text, placeholder=None
****** Buttons: Go
**** Form 2: Action=/, Method=post
***** Input: name=username, type=text, placeholder=None
***** Input: name=password, type=password, placeholder=None
***** Input: name=remember, type=checkbox, placeholder=None
***** Input: name=Submit, type=submit, placeholder=None
***** Input: name=Submit, type=submit, placeholder=None
****** Buttons: Log in, Sign up / i’m New
**** Form 3: Action=None, Method=GET
***** Input: name=searchword, type=text, placeholder=Enter a medication
****** Buttons: FIND 340B PRICES

** Contact Us - 340B Price Guide
*** Links
**** https://www.340bpriceguide.net/340b-search
**** https://www.340bpriceguide.net/about-us
**** https://www.340bpriceguide.net/articles-news
**** https://www.340bpriceguide.net/client-login?view=registration
**** https://www.340bpriceguide.net/client-login?view=remind
**** https://www.340bpriceguide.net/client-login?view=reset
**** https://www.340bpriceguide.net/component/mailto/?tmpl=component&template=rt_chapelco_child&link=20a9a98bd3685953cd19aae8554484753618b4d3
**** https://www.340bpriceguide.net/contact-us
**** https://www.340bpriceguide.net/contact-us?tmpl=component&print=1
**** https://www.340bpriceguide.net/index.php
**** https://www.340bpriceguide.net/index.php/about-us
**** https://www.340bpriceguide.net/index.php/articles-news
**** https://www.340bpriceguide.net/index.php/contact-us
*** Forms

@endmindmap

"""

# Generate mind map as SVG
generate_mindmap(uml_code, "teamup_mindmap.svg")
