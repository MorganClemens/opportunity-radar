import argparse

from company_watch import filter_watched_jobs
from config import load_config
from emailer import send_email
from seen_jobs import filter_seen_jobs, load_seen_jobs, mark_jobs_seen, save_seen_jobs


def collect_jobs(companies):
    jobs = []

    for company in companies:
        source = company.get("source")
        if source == "dayforce":
            from sources.dayforce import get_jobs as get_dayforce_jobs

            jobs.extend(get_dayforce_jobs(company))
        else:
            raise ValueError(
                f"Unsupported source '{source}' for company '{company['name']}'"
            )

    return jobs


def build_alert(jobs):
    count = len(jobs)
    lines = [
        "Opportunity Radar — New Company Openings",
        "",
        f"{count} new {'opening' if count == 1 else 'openings'} found.",
        "",
    ]

    for index, job in enumerate(jobs, start=1):
        lines.extend(
            [
                f"{index}. {job['title']} — {job['org']}",
                f"   Location: {job['location']}",
                f"   Link: {job['url']}",
                "",
            ]
        )

    return "\n".join(lines)


def run(send_notifications=True):
    config = load_config()
    companies = config.get("companies", [])
    if not companies:
        raise RuntimeError("Add at least one company to config/search_profile.yaml")

    all_jobs = collect_jobs(companies)
    watched_jobs = filter_watched_jobs(all_jobs, companies)
    seen_jobs = load_seen_jobs()
    new_jobs = filter_seen_jobs(watched_jobs, seen_jobs)

    if not new_jobs:
        print(
            f"Checked {len(companies)} watched companies; "
            "no new matching openings found."
        )
        return []

    alert = build_alert(new_jobs)
    print(alert)

    if send_notifications:
        send_email(
            subject=(
                "Opportunity Radar - "
                f"{len(new_jobs)} new {'opening' if len(new_jobs) == 1 else 'openings'}"
            ),
            body=alert,
        )

    if send_notifications:
        mark_jobs_seen(new_jobs, seen_jobs)
        save_seen_jobs(seen_jobs)
    return new_jobs


def main():
    parser = argparse.ArgumentParser(description="Monitor selected companies for jobs")
    parser.add_argument(
        "--no-email",
        action="store_true",
        help="print results without sending an email",
    )
    args = parser.parse_args()
    run(send_notifications=not args.no_email)


if __name__ == "__main__":
    main()
