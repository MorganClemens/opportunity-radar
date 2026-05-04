def filter_jobs(jobs, keywords):
    filtered = []

    for job in jobs:
        text = (job["title"] + job["org"]).lower()

        if any(keyword.lower() in text for keyword in keywords):
            filtered.append(job)

    return filtered