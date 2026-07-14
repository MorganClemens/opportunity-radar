from urllib.parse import urljoin

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


def _extract_jobs(page, company):
    postings = page.locator('[test-id="job-posting-card"]').evaluate_all(
        """
        cards => cards.map(card => ({
            title: card.querySelector('[test-id="job-title"]')?.textContent?.trim() || 'No title',
            location: card.querySelector('[test-id="job-location"]')?.textContent?.trim() || 'Unknown',
            description: card.querySelector('[test-id="job-description"]')?.textContent?.trim() || '',
            href: card.querySelector('a[href*="/jobs/"]')?.getAttribute('href') || ''
        }))
        """
    )

    board_url = company["board_url"].rstrip("/") + "/"
    return [
        {
            "title": posting["title"],
            "org": company["name"],
            "location": posting["location"],
            "url": urljoin(board_url, posting["href"]),
            "description": posting["description"],
            "source": "dayforce",
        }
        for posting in postings
        if posting["href"]
    ]


def get_jobs(company):
    """Return every currently open job on a company's public Dayforce board."""
    board_url = company["board_url"]
    jobs = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        page_number = 1
        while True:
            separator = "&" if "?" in board_url else "?"
            page_url = (
                board_url
                if page_number == 1
                else f"{board_url}{separator}page={page_number}"
            )
            page.goto(page_url, wait_until="domcontentloaded", timeout=60_000)

            try:
                page.locator('[test-id="job-posting-card"]').first.wait_for(
                    state="visible", timeout=30_000
                )
            except PlaywrightTimeoutError:
                if page_number == 1 and "could not find any jobs" not in page.content().lower():
                    raise RuntimeError(
                        f"Dayforce did not load job results for {company['name']}"
                    )
                break

            page_jobs = _extract_jobs(page, company)
            if not page_jobs:
                break

            jobs.extend(page_jobs)
            if len(page_jobs) < 25:
                break
            page_number += 1

        browser.close()

    # Dayforce can repeat a posting when pagination changes during a run.
    return list({job["url"]: job for job in jobs}.values())
