import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from sources.benchmark import parse_jobs as parse_benchmark_jobs
from sources.gravity_vault import parse_jobs as parse_gravity_vault_jobs
from sources.rippling import parse_jobs as parse_rippling_jobs


class SourceParserTests(unittest.TestCase):
    def test_rippling_structured_jobs(self):
        data = {
            "props": {
                "pageProps": {
                    "dehydratedState": {
                        "queries": [
                            {
                                "queryKey": ["board", "touchstone", "job-posts"],
                                "state": {
                                    "data": {
                                        "items": [
                                            {
                                                "name": "Front Desk - Mission Cliffs",
                                                "url": "https://example.com/job/1",
                                                "locations": [
                                                    {"name": "San Francisco, CA"}
                                                ],
                                            }
                                        ],
                                        "page": 0,
                                        "totalPages": 1,
                                    }
                                },
                            }
                        ]
                    }
                }
            }
        }
        html = (
            '<script id="__NEXT_DATA__" type="application/json">'
            + json.dumps(data)
            + "</script>"
        )

        jobs, page, total_pages = parse_rippling_jobs(
            html, {"name": "Touchstone Climbing"}
        )

        self.assertEqual(jobs[0]["location"], "San Francisco, CA")
        self.assertEqual(jobs[0]["source"], "rippling")
        self.assertEqual((page, total_pages), (0, 1))

    def test_benchmark_open_positions_section(self):
        html = """
        <h4><strong>Open Positions (Click the link to apply):</strong>
        <a href="https://example.com/coach">Freelance Coach</a>
        </h4>
        <a href="https://example.com/not-a-job">Apply Now</a>
        """
        company = {
            "name": "Benchmark Climbing",
            "board_url": "https://www.benchmarkclimbing.com/jobs",
            "default_location": "San Francisco / Berkeley (verify with Benchmark)",
        }

        jobs = parse_benchmark_jobs(html, company)

        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["title"], "Freelance Coach")
        self.assertIn("San Francisco", jobs[0]["location"])

    def test_gravity_vault_roles_have_unique_fragment_urls(self):
        html = """
        <article class="career">
          <a name="team-coach-5"></a>
          <h5 class="title"><a href="javascript:;">Team Coach</a></h5>
        </article>
        <article class="career">
          <a name="shift-supervisor-26"></a>
          <h5 class="title"><a href="javascript:;">Shift Supervisor</a></h5>
        </article>
        """
        company = {
            "name": "The Gravity Vault Marin",
            "board_url": "https://gravityvault.com/careers?zipcode=94903",
            "default_location": "San Rafael, Marin County",
        }

        jobs = parse_gravity_vault_jobs(html, company)

        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[0]["location"], "San Rafael, Marin County")
        self.assertTrue(jobs[0]["url"].endswith("#team-coach-5"))
        self.assertNotEqual(jobs[0]["url"], jobs[1]["url"])


if __name__ == "__main__":
    unittest.main()
