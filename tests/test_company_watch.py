import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from company_watch import filter_watched_jobs, location_matches, title_is_allowed
from main import build_alert


class CompanyWatchTests(unittest.TestCase):
    def setUp(self):
        self.companies = [
            {
                "name": "Movement",
                "locations": ["San Francisco"],
                "exclude_titles": [],
            }
        ]

    def test_location_matching_is_case_insensitive(self):
        self.assertTrue(
            location_matches("San Francisco, California", ["san francisco"])
        )
        self.assertFalse(location_matches("Golden, Colorado", ["San Francisco"]))

    def test_empty_location_list_watches_every_location(self):
        self.assertTrue(location_matches("Anywhere", []))

    def test_excluded_titles_are_optional(self):
        self.assertTrue(title_is_allowed("Route Setter", []))
        self.assertFalse(title_is_allowed("Senior Director", ["director"]))

    def test_filter_keeps_only_company_location_matches(self):
        jobs = [
            {
                "title": "Route Setter",
                "org": "Movement",
                "location": "San Francisco, California",
                "url": "https://example.com/1",
            },
            {
                "title": "Route Setter",
                "org": "Movement",
                "location": "Golden, Colorado",
                "url": "https://example.com/2",
            },
        ]

        self.assertEqual(filter_watched_jobs(jobs, self.companies), [jobs[0]])

    def test_alert_contains_the_opening(self):
        alert = build_alert(
            [
                {
                    "title": "Route Setter",
                    "org": "Movement",
                    "location": "San Francisco",
                    "url": "https://example.com/job",
                }
            ]
        )

        self.assertIn("1 new opening found", alert)
        self.assertIn("Route Setter — Movement", alert)


if __name__ == "__main__":
    unittest.main()
