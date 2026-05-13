from config import load_config
from sources.manual import get_jobs as get_manual_jobs
from filters import filter_jobs
from emailer import send_email
from seen_jobs import (
    filter_seen_jobs,
    load_seen_jobs,
    mark_jobs_seen,
    save_seen_jobs,
)
from sources.greenhouse import get_jobs as get_greenhouse_jobs

def build_digest(jobs, config):
    profile_name = config["profile_name"]
    max_jobs = config["weekly_digest"]["max_jobs"]
    goal_applications = config["weekly_digest"]["goal_applications"]

    lines = [
        f"Opportunity Radar — {profile_name}",
        "",
        f"Goal: apply to {goal_applications} jobs this week.",
        f"Showing up to {max_jobs} matching opportunities.",
        "",
    ]

    if not jobs:
        lines.append("No matching jobs found this week.")
        return "\n".join(lines)
    
    for index, job in enumerate(jobs, start=1):
        matches = ", ".join(job.get("matches", []))

        lines.append(f"{index}. {job['title']} — {job['org']}")
        lines.append(f"   Location: {job['location']}")
        lines.append(f"   Matches: {matches}")
        lines.append(f"   Link: {job['url']}")
        lines.append("")

    return "\n".join(lines)


def main():
    config = load_config()
    manual_jobs = get_manual_jobs()
    greenhouse_jobs = get_greenhouse_jobs()

    jobs = manual_jobs + greenhouse_jobs

    jobs = filter_jobs(jobs, config)
    seen_jobs = load_seen_jobs()
    jobs = filter_seen_jobs(jobs, seen_jobs)
    max_jobs = config["weekly_digest"]["max_jobs"]
    jobs = jobs[:max_jobs]

    digest = build_digest(jobs, config)
    print(digest)

    send_email(
        subject="Opportunity Radar - Weekly Digest",
        body=digest
    )

    seen_jobs = mark_jobs_seen(jobs, seen_jobs)
    save_seen_jobs(seen_jobs)

if __name__ == "__main__":
    main()