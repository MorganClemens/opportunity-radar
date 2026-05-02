# Opportunity Radar

**Opportunity Radar** is a lightweight tool for discovering mission-aligned opportunities in outdoor education, conservation, climate, and tech.

The goal is to make meaningful opportunities easier to find, filter, and act on.

---

## 🌱 Status

🚧 Early build — core job aggregation and filtering in progress

---

## 🔍 Features (Planned)

- Aggregate job listings from curated sources
- Filter by keywords (e.g., conservation, education, Python)
- Daily or weekly job digest
- Simple tracking system for saved/applied roles

---

## 🧱 Project Structure

```
src/
  main.py          # Entry point
  filters.py       # Keyword + logic filtering
  models.py        # Job data structures
  notifier.py      # Email/alerts (future)

  sources/
    example_source.py   # Example job source

data/
  jobs.json        # Stored job listings

docs/
  roadmap.md       # Future ideas
```

---

## 🚀 Getting Started

```bash
git clone git@github.com:YOUR_USERNAME/opportunity-radar.git
cd opportunity-radar
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

---

## 🌊 Vision

Opportunity Radar is inspired by the idea that the best opportunities aren't always the most visible. Also, sifting through job boards kinda sucks...

This project aims to surface work at the intersection of:
- Environment
- Education
- Technology

...because that's what I'm interested in! Cheers. 