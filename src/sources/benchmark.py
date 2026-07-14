import re
from html import unescape
from urllib.parse import urljoin

import requests


OPENINGS_PATTERN = re.compile(
    r"Open Positions \(Click the link to apply\):(.*?)</h4>", re.DOTALL
)
LINK_PATTERN = re.compile(
    r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', re.DOTALL
)
TAG_PATTERN = re.compile(r"<[^>]+>")


def parse_jobs(html, company):
    section = OPENINGS_PATTERN.search(html)
    if not section:
        raise RuntimeError(f"Open positions section was not found for {company['name']}")

    jobs = []
    for url, title_html in LINK_PATTERN.findall(section.group(1)):
        title = unescape(TAG_PATTERN.sub("", title_html)).strip()
        if not title:
            continue
        jobs.append(
            {
                "title": title,
                "org": company["name"],
                "location": company["default_location"],
                "url": urljoin(company["board_url"], unescape(url)),
                "description": "Location is not specified on Benchmark's jobs page.",
                "source": "benchmark",
            }
        )
    return jobs


def get_jobs(company):
    response = requests.get(
        company["board_url"],
        headers={"User-Agent": "Opportunity Radar/1.0"},
        timeout=30,
    )
    response.raise_for_status()
    return parse_jobs(response.text, company)
