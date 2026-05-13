import requests

def get_jobs(board_token="watershed"):
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    jobs = []

    for job in data.get("jobs", []):
        jobs.append(
            {
                "title": job.get("title", "No title"),
                "org": board_token,
                "location": job.get("location", {}).get("name", "Unknown"),
                "url": job.get("absolute_url", ""),
                "description": "",
                "source": "greenhouse",
            }
        )

    return jobs

