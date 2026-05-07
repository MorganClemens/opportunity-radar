import feedparser

FEED_URL = "https://www.higheredjobs.com/search/rss.cfm?JobCat=54"


def get_jobs():
    feed = feedparser.parse(
        FEED_URL,
        request_headers={
            "User-Agent": "OpportunityRadar/0.1 (+https://opensurf.org)"
        },
    )

    if feed.bozo:
        print(f"Feed parser warning: {feed.bozo_exception}")

    print(f"Feed status: {feed.get('status', 'unknown')}")
    print(f"Feed title: {feed.feed.get('title', 'No feed title found')}")

    jobs = []

    for entry in feed.entries:
        jobs.append(
            {
                "title": entry.get("title", "No title"),
                "org": entry.get("author", "HigherEdJobs"),
                "location": "Unknown",
                "url": entry.get("link", ""),
            }
        )

    return jobs