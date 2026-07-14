# Opportunity Radar

Opportunity Radar watches the official career pages of companies you would love
to work for and emails you when a new opening appears in one of your chosen
locations.

The first configured watch is **Movement in San Francisco**.

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

The initial version supports public Dayforce job boards. Additional career
systems can be added as small source adapters under `src/sources/`.

## Run it locally

```bash
pip install -r requirements.txt
playwright install chromium
python src/main.py --no-email
```

The preview does not record jobs as seen. Remove `--no-email` to send an alert
and record the openings using `EMAIL_ADDRESS`, `EMAIL_APP_PASSWORD`, and
`EMAIL_TO` from your environment or `.env` file.
