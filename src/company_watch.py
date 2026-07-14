def find_company(job, companies):
    return next(
        (company for company in companies if company["name"] == job["org"]),
        None,
    )


def location_matches(location, wanted_locations):
    if not wanted_locations:
        return True

    location = location.lower()
    return any(wanted.lower() in location for wanted in wanted_locations)


def title_is_allowed(title, excluded_titles):
    title = title.lower()
    return not any(excluded.lower() in title for excluded in excluded_titles)


def filter_watched_jobs(jobs, companies):
    matched = []

    for job in jobs:
        company = find_company(job, companies)
        if not company:
            continue

        if not location_matches(job.get("location", ""), company.get("locations", [])):
            continue

        if not title_is_allowed(job.get("title", ""), company.get("exclude_titles", [])):
            continue

        matched.append(job)

    return matched
