import asyncio, json
from urllib.parse import urlparse, urljoin
from playwright.async_api import async_playwright

START_URL = "https://teamupventures.com/"
MAX_PAGES = 50  # adjust as needed


async def crawl():
    site_map, visited, to_visit = {}, set(), [(None, START_URL)]  # (parent, url)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        while to_visit and len(visited) < MAX_PAGES:
            parent, url = to_visit.pop()
            if url in visited:
                continue
            visited.add(url)

            try:
                await page.goto(url, timeout=30000)
                title = await page.title()

                # collect links (same domain only)
                anchors = await page.eval_on_selector_all(
                    "a[href]", "els => els.map(e => e.href)"
                )
                parsed_start = urlparse(START_URL).netloc
                links = sorted(
                    set(
                        l.split("#")[0].rstrip("/")
                        for l in anchors
                        if urlparse(l).netloc.endswith(parsed_start)
                    )
                )

                # collect forms
                forms = []
                form_elements = await page.query_selector_all("form")
                for f in form_elements:
                    form_info = {
                        "action": await f.get_attribute("action"),
                        "method": (await f.get_attribute("method")) or "GET",
                        "inputs": [],
                        "buttons": [],
                    }
                    inputs = await f.query_selector_all("input, textarea, select")
                    for inp in inputs:
                        name = await inp.get_attribute("name")
                        itype = (await inp.get_attribute("type")) or "text"
                        placeholder = await inp.get_attribute("placeholder")
                        form_info["inputs"].append(
                            {"name": name, "type": itype, "placeholder": placeholder}
                        )
                    btns = await f.query_selector_all("button, input[type=submit]")
                    for b in btns:
                        text = (await b.inner_text()).strip()
                        value = await b.get_attribute("value")
                        if text or value:
                            form_info["buttons"].append(text or value)
                    forms.append(form_info)

                # store page info
                site_map[url] = {
                    "title": title,
                    "url": url,
                    "parent": parent,
                    "links": links,
                    "forms": forms,
                }

                # queue children
                for l in links:
                    if l not in visited and l not in [x[1] for x in to_visit]:
                        to_visit.append((url, l))

            except Exception as e:
                print(f"[error] {url}: {e}")

        await browser.close()

    with open("site_structure.json", "w", encoding="utf-8") as f:
        json.dump(site_map, f, indent=2)

    print(f"[ok] Crawled {len(site_map)} pages → site_structure.json")


# --- Convert JSON to PlantUML mind map ---
def site_map_to_plantuml(site_map, root_name="Website"):
    lines = ["@startmindmap", f"* {root_name}"]

    def add_nodes(url, depth=2):
        node = site_map[url]
        prefix = "*" * depth
        title = node.get("title") or url
        lines.append(f"{prefix} {title} ({urlparse(url).path or '/'})")

        # forms
        for form in node.get("forms", []):
            lines.append(f"{prefix}* Form: {form['method']} {form['action'] or ''}")
            for inp in form["inputs"]:
                inp_name = inp["name"] or inp.get("placeholder") or "unnamed"
                lines.append(f"{prefix}** Field: {inp_name} ({inp['type']})")
            for btn in form["buttons"]:
                lines.append(f"{prefix}** Button: {btn}")

        # children
        for child_url in node["links"]:
            if child_url in site_map and site_map[child_url]["parent"] == url:
                add_nodes(child_url, depth + 1)

    # find root nodes (no parent)
    for url, node in site_map.items():
        if node["parent"] is None:
            add_nodes(url, depth=2)

    lines.append("@endmindmap")
    return "\n".join(lines)


def json_to_plantuml(json_file, puml_file="mindmap.puml"):
    with open(json_file, "r", encoding="utf-8") as f:
        site_map = json.load(f)

    plantuml_code = site_map_to_plantuml(site_map, root_name="Teamup Ventures")

    with open(puml_file, "w", encoding="utf-8") as f:
        f.write(plantuml_code)

    print(f"[ok] PlantUML mind map saved to {puml_file}")


if __name__ == "__main__":
    asyncio.run(crawl())
    json_to_plantuml("site_structure.json")
