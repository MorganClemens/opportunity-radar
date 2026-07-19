import re
from html import unescape
from urllib.parse import urlsplit, urlunsplit

import requests


CAREER_PATTERN = re.compile(
    r'<article class="career">(.*?)</article>', re.DOTALL
)
ANCHOR_PATTERN = re.compile(r'<a name="([^"]+)"')
TITLE_PATTERN = re.compile(
    r'<h5 class="title">\s*<a[^>]*>(.*?)</a>', re.DOTALL
)
TAG_PATTERN = re.compile(r"<[^>]+>")


def _clean_text(value):
    return " ".join(unescape(TAG_PATTERN.sub(" ", value)).split())


def _job_url(board_url, anchor):
    parts = urlsplit(board_url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, anchor))


def parse_jobs(html, company):
    jobs = []

    for career_html in CAREER_PATTERN.findall(html):
        anchor = ANCHOR_PATTERN.search(career_html)
        title = TITLE_PATTERN.search(career_html)
        if not anchor or not title:
            continue

        jobs.append(
            {
                "title": _clean_text(title.group(1)),
                "org": company["name"],
                "location": company["default_location"],
                "url": _job_url(company["board_url"], anchor.group(1)),
                "description": "",
                "source": "gravity_vault",
            }
        )

    if not jobs and "There were 0 result(s)" not in html:
        raise RuntimeError(
            f"Gravity Vault career listings were not found for {company['name']}"
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
