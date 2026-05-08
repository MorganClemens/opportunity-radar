def job_text(job):
    return " ".join(
        [
            job.get("title", ""),
            job.get("org", ""),
            job.get("location", ""),
            job.get("description", ""),
        ]
    ).lower()

def find_matches(job, keywords):
    text = job_text(job)
    return [keyword for keyword in keywords if keyword.lower() in text]

def filter_jobs(jobs, config):
    include_keywords = config["keywords"]["include"]
    exclude_keywords = config["keywords"]["exclude"]

    filtered = []

    for job in jobs:
        include_matches = find_matches(job, include_keywords)
        exclude_matches = find_matches(job, exclude_keywords)

        if include_matches and not exclude_matches:
            job["matches"] = include_matches
            filtered.append(job)

    return filtered