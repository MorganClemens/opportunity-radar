# Opportunity Radar

Opportunity Radar watches the official career pages of companies you would love
to work for and emails you when a new opening appears in one of your chosen
locations.

This project is also my experiment in agentic coding: I work with coding agents
to shape the product, research integrations, implement and test features, and
maintain the automation. It is a practical exploration of how people and agents
can build useful, evolving software together.

The configured watches cover San Francisco's commercial climbing gyms:

- Movement San Francisco in the Presidio
- Benchmark Climbing on Van Ness
- Touchstone Climbing's Mission Cliffs and Dogpatch Boulders
- Touchstone's forthcoming Aisle 19, once its jobs appear in the same feed

Only San Francisco postings are selected from company-wide job boards. Benchmark
does not label every role by gym, so Benchmark alerts explicitly ask you to
verify whether the opening is for San Francisco or Berkeley.
Touchstone roles labeled "Regional" are excluded because they can require travel
throughout Northern California.

## How it works

1. A daily GitHub Actions run opens each company's official job board.
2. Jobs are filtered by the locations configured for that company.
3. Previously reported job links are removed.
4. New openings are emailed immediately and recorded so they are not sent again.

No role keywords are required. If a watched company posts any position in a
chosen location, you hear about it.

## Add another company

Add an entry to `config/search_profile.yaml`:

```yaml
companies:
  - name: Movement
    source: dayforce
    board_url: https://jobs.dayforcehcm.com/movementgyms/CANDIDATEPORTAL
    locations:
      - San Francisco
    exclude_titles: []
```

The app supports the public Dayforce and Rippling job boards used by Movement
and Touchstone, plus Benchmark's company jobs page. Additional career systems
can be added as small source adapters under `src/sources/`.

## Run it locally

```bash
pip install -r requirements.txt
playwright install chromium
python src/main.py --no-email
```

The preview does not record jobs as seen. Remove `--no-email` to send an alert
and record the openings using `EMAIL_ADDRESS`, `EMAIL_APP_PASSWORD`, and
`EMAIL_TO` from your environment or `.env` file.
