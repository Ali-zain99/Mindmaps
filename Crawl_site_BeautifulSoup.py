#!/usr/bin/env python3
"""
Scrape a website (respecting robots.txt), extract pages + headings, build a PlantUML mindmap,
and fetch an SVG from the public PlantUML server.

Usage:
    python crawl_to_mindmap.py https://teamupventures.com/ --max-pages 100 --output mindmap.svg

Notes:
- The script respects robots.txt for the user-agent " * ".
- Keep `max_pages` reasonable to avoid heavy crawling.
- The public PlantUML server is used for convenience; for heavy or repeated use, host your own PlantUML server.
"""

import sys
import time
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import urllib.robotparser
import zlib

# ---------- PlantUML encoding (from PlantUML docs) ----------
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
    r = ""
    r += encode6bit(c1 & 0x3F)
    r += encode6bit(c2 & 0x3F)
    r += encode6bit(c3 & 0x3F)
    r += encode6bit(c4 & 0x3F)
    return r

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
    compressed = zlib.compress(text.encode("utf-8"))[2:-4]
    return encode64(compressed)

# ---------- Crawler + parser ----------
HEADERS = {
    "User-Agent": "site-mindmap-bot/1.0 (+https://example.com/contact)"
}

def allowed_to_crawl(base_url: str, path: str) -> bool:
    rp = urllib.robotparser.RobotFileParser()
    robots_url = urljoin(base_url, "/robots.txt")
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch("*", path)
    except Exception:
        # If robots can't be fetched, be conservative: allow (or you can return False)
        return False

def extract_headings(html: str):
    soup = BeautifulSoup(html, "html.parser")
    headings = []
    for level in range(1, 7):
        for tag in soup.find_all(f"h{level}"):
            text = tag.get_text(separator=" ", strip=True)
            if text:
                headings.append((level, text))
    return headings

def canonicalize_link(link: str, base_domain: str):
    if not link:
        return None
    parsed = urlparse(link)
    if parsed.scheme and parsed.netloc:
        # full URL
        target_domain = parsed.netloc
        if target_domain.endswith(base_domain):
            # keep path + scheme
            return link.split('#')[0].rstrip('/')
        return None
    # relative
    return None

def crawl_site(start_url: str, max_pages: int = 200, delay: float = 0.5):
    parsed_start = urlparse(start_url)
    base_domain = parsed_start.netloc
    base_url_root = f"{parsed_start.scheme}://{base_domain}"

    to_visit = [start_url.rstrip('/')]
    visited = set()
    site_map = {}   # url -> {"title":..., "headings":[(level,text)], "links":[...]}
    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue

        path = urlparse(url).path or "/"
        if not allowed_to_crawl(base_url_root, path):
            print(f"[robots.txt] Skipping disallowed: {url}")
            visited.add(url)
            continue

        try:
            print(f"[crawl] GET {url}")
            resp = requests.get(url, headers=HEADERS, timeout=15)
        except Exception as e:
            print(f"[error] fetching {url} => {e}")
            visited.add(url)
            time.sleep(delay)
            continue

        if resp.status_code != 200:
            print(f"[status] {resp.status_code} for {url}")
            visited.add(url)
            time.sleep(delay)
            continue

        html = resp.text
        soup = BeautifulSoup(html, "html.parser")

        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else url

        headings = extract_headings(html)

        # collect internal links
        links = set()
        for a in soup.find_all("a", href=True):
            href = a.get("href").split('?')[0]
            # make absolute
            full = urljoin(url, href).split('#')[0].rstrip('/')
            parsed_full = urlparse(full)
            if parsed_full.netloc.endswith(base_domain):
                links.add(full)

        site_map[url] = {
            "title": title,
            "headings": headings,
            "links": sorted(list(links))
        }

        visited.add(url)
        # enqueue new links
        for l in sorted(links):
            if l not in visited and l not in to_visit and len(visited) + len(to_visit) < max_pages:
                to_visit.append(l)

        time.sleep(delay)

    return site_map

# ---------- Build PlantUML mindmap ----------
def build_mindmap_chunks(site_map: dict, root_name: str = "Site", chunk_size: int = 20):
    """
    Build multiple PlantUML mindmap chunks to avoid hitting PlantUML server URL size limits.
    Each chunk will contain up to `chunk_size` pages.
    Returns a list of (filename, plantuml_text).
    """
    pages = sorted(site_map.items(), key=lambda x: x[0])
    chunks = [pages[i:i + chunk_size] for i in range(0, len(pages), chunk_size)]
    
    outputs = []
    for idx, chunk in enumerate(chunks, 1):
        lines = ["@startmindmap", "* " + root_name]
        for url, meta in chunk:
            title = meta.get("title") or url
            safe_title = f"{title} — {url}"
            lines.append("** " + escape_plantuml(safe_title))
            # Add headings as children
            for level, text in meta.get("headings", []):
                indent = "*" * (3 + min(level - 1, 3))  # reasonable depth
                lines.append(f"{indent} {escape_plantuml(text)}")
        lines.append("@endmindmap")
        outputs.append((f"mindmap_{idx}.puml", "\n".join(lines)))
    return outputs

# ---------- Fetch PlantUML server with chunks ----------
def fetch_plantuml_chunks(chunks, output_prefix="mindmap"):
    for puml_file, plantuml_text in chunks:
        encoded = plantuml_encode(plantuml_text)
        url = f"http://www.plantuml.com/plantuml/svg/{encoded}"
        print(f"[plantuml] requesting {url[:120]}...")  # truncate log
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code == 200:
            svg_file = puml_file.replace(".puml", ".svg").replace("mindmap", output_prefix)
            with open(svg_file, "wb") as f:
                f.write(resp.content)
            print(f"[ok] saved SVG to {svg_file}")
        else:
            print(f"[error] PlantUML server returned {resp.status_code}: {resp.text[:200]}")

def escape_plantuml(s: str) -> str:
    # PlantUML mindmap nodes are plain text; replace newlines and some control chars
    return s.replace("\n", " ").replace("\r", " ").strip()

# ---------- Request PlantUML server ----------
def fetch_plantuml_svg(plantuml_text: str, out_file: str = "mindmap.svg"):
    encoded = plantuml_encode(plantuml_text)
    url = f"http://www.plantuml.com/plantuml/svg/{encoded}"
    print(f"[plantuml] requesting {url}")
    resp = requests.get(url, headers=HEADERS, timeout=30)
    if resp.status_code == 200:
        with open(out_file, "wb") as f:
            f.write(resp.content)
        print(f"[ok] saved SVG to {out_file}")
    else:
        print(f"[error] PlantUML server returned {resp.status_code}: {resp.text[:200]}")

# ---------- Optional: export markdown for Markmap ----------
def export_markmap_markdown(site_map: dict, out_file: str = "structure.md"):
    """
    Create a Markdown outline from the site map suitable for markmap.
    """
    lines = ["# Site Structure"]
    for url, meta in sorted(site_map.items(), key=lambda x: x[0]):
        title = meta.get("title") or url
        lines.append(f"## {title}")
        lines.append(f"- URL: {url}")
        for level, text in meta.get("headings", []):
            indent = "  " * (level - 1)
            lines.append(f"{indent}- {text}")
        lines.append("")  # blank line
    md = "\n".join(lines)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[ok] saved markdown to {out_file}")

# ---------- CLI ----------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("start_url", help="Start URL (e.g. https://teamupventures.com/)")
    parser.add_argument("--max-pages", type=int, default=100, help="Maximum pages to crawl")
    parser.add_argument("--delay", type=float, default=0.6, help="Delay (seconds) between requests")
    parser.add_argument("--output", default="mindmap.svg", help="Output SVG filename prefix")
    parser.add_argument("--export-md", action="store_true", help="Also export markdown suitable for Markmap")
    args = parser.parse_args()

    start_url = args.start_url.rstrip('/')
    print(f"[start] crawling {start_url} (max_pages={args.max_pages})")

    site_map = crawl_site(start_url, max_pages=args.max_pages, delay=args.delay)
    print(f"[done] crawled {len(site_map)} pages")

    # Build chunked PlantUMLs
    chunks = build_mindmap_chunks(site_map, root_name=start_url, chunk_size=20)

    # Save PUML sources + fetch SVGs
    for puml_file, plantuml_text in chunks:
        with open(puml_file, "w", encoding="utf-8") as f:
            f.write(plantuml_text)
        print(f"[ok] saved PlantUML source to {puml_file}")

    fetch_plantuml_chunks(chunks, output_prefix=args.output.replace(".svg", ""))

    if args.export_md:
        export_markmap_markdown(site_map, out_file="structure.md")
        
if __name__ == "__main__":
    main()
