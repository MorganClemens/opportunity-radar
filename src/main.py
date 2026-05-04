from sources.example_source import get_jobs

def main():
    jobs = get_jobs()

    print("\n🌊 Opportunity Radar Results:\n")

    for job in jobs:
        print(f"{job['title']} — {job['org']}")
        print(f"Location: {job['location']}")
        print(f"Link: {job['url']}")
        print("-" * 40)

if __name__ == "__main__":
    main()