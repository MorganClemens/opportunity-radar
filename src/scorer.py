def score_job(job, config, seen_jobs):
    score = 0
    reasons = []

    matches = job.get("matches", [])
    score += len(matches) * 2

    if matches:
        reasons.append(f"{len(matches)} keyword match(es)")

    location = job.get("location", "").lower()
    preferred_locations = config["locations"]["include"]

    for preferred_location in preferred_locations:
        if preferred_location.lower() in location:
            score += 2
            reasons.append(f"preferred location: {preferred_location}")
            break
    
    if "remote" in location:
        score += 1
        reasons.append("remote")

    if job["url"] in seen_jobs:
        score -= 1
        job["is_new"] = False
        reasons.append("seen before")
    else:
        score += 1
        job["is_new"] = True
        reasons.append("new")

    job["score"] = score
    job["score_reasons"] = reasons

    return job


def rank_jobs(jobs, config, seen_jobs):
    scored_jobs = [score_job(job, config, seen_jobs) for job in jobs]
    return sorted(scored_jobs, key=lambda job: job["score"], reverse=True)

