from config import load_config
from sources.manual import get_jobs
from filters import filter_jobs


def main():
    config = load_config()
    jobs = get_jobs()

    print(f"\nOpportunity Radar — {config['profile_name']}")
    print(f"Total jobs loaded: {len(jobs)}\n")

    jobs = filter_jobs(jobs, config)
    max_jobs = config["weekly_digest"]["max_jobs"]
    jobs = jobs[:max_jobs]

    for job in jobs:
        print(f"{job['title']} — {job['org']}")
        print(f"Location: {job['location']}")
        print(f"Link: {job['url']}")
        print(f"Matches: {', '.join(job['matches'])}")
        print("-" * 40)


if __name__ == "__main__":
    main()