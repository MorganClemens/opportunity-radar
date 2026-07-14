import json
import re

import requests


NEXT_DATA_PATTERN = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>'
)


def parse_jobs(html, company):
    match = NEXT_DATA_PATTERN.search(html)
    if not match:
        raise RuntimeError(f"Rippling job data was not found for {company['name']}")

    page_props = json.loads(match.group(1))["props"]["pageProps"]
    queries = page_props["dehydratedState"]["queries"]
    job_data = next(
        query["state"]["data"]
        for query in queries
        if "job-posts" in query.get("queryKey", [])
    )

    jobs = []
    for posting in job_data["items"]:
        location = ", ".join(
            item["name"] for item in posting.get("locations", [])
        ) or "Unknown"
        jobs.append(
            {
                "title": posting["name"],
                "org": company["name"],
                "location": location,
                "url": posting["url"],
                "description": "",
                "source": "rippling",
            }
        )

    return jobs, job_data["page"], job_data["totalPages"]


def get_jobs(company):
    board_url = company["board_url"]
    jobs = []
    page_number = 0

    while True:
        response = requests.get(
            board_url,
            params={"page": page_number} if page_number else None,
            headers={"User-Agent": "Opportunity Radar/1.0"},
            timeout=30,
        )
        response.raise_for_status()

        page_jobs, current_page, total_pages = parse_jobs(response.text, company)
        jobs.extend(page_jobs)
        if current_page + 1 >= total_pages:
            break
        page_number += 1

    return list({job["url"]: job for job in jobs}.values())
