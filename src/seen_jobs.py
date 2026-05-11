import json

def load_seen_jobs(path="data/seen_jobs.json"):
    with open(path, "r") as file:
        return set(json.load(file))


def save_seen_jobs(seen_jobs, path="data/seen_jobs.json"):
    with open(path, "w") as file:
        json.dump(sorted(seen_jobs), file, indent=2)


def get_job_id(job):
    return job["url"]


def filter_seen_jobs(jobs, seen_jobs):
    return [job for job in jobs if get_job_id(job) not in seen_jobs]


def mark_jobs_seen(jobs, seen_jobs):
    for job in jobs:
        seen_jobs.add(get_job_id(job))

    return seen_jobs