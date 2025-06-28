import requests
import logging
from typing import List, Dict


class LeetCodeClient:
    BASE_URL = "https://leetcode-stats-api.herokuapp.com"

    def __init__(self, timeout=5):
        self.timeout = timeout
        self.logger = logging.getLogger("LeetCodeClient")

    def _get_total_solved(self, username):
        url = f"{self.BASE_URL}/{username}"
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            if "totalSolved" not in data:
                self.logger.warning(f"Missing totalSolved in response for {username}")
                return None

            return data["totalSolved"]

        except requests.RequestException as e:
            self.logger.error(
                f"Network error while fetching LeetCode data for {username}: {e}"
            )
            return None

        except ValueError:
            self.logger.error(f"Invalid JSON response from LeetCode API for {username}")
            return None

        except Exception as e:
            self.logger.error(f"Unexpected error occured: {e}")
            return None

    def get_scores(self, users: List[str]) -> Dict[str, int]:
        scores = {}

        for username in users:
            score = self._get_total_solved(username)
            scores[username] = score

        return scores
