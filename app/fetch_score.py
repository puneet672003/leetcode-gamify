import requests


class LeetCodeAPIError(Exception):
    """Custom exception for LeetCode API errors."""


class LeetCodeAPI:
    URL = "https://leetcode.com/graphql/"

    def __init__(self, username: str):
        self.username = username

    def _make_request(self, query: str, variables: dict, operation_name: str):
        payload = {
            "operationName": operation_name,
            "query": query,
            "variables": variables,
        }

        headers = {
            "Content-Type": "application/json",
            "Referer": f"https://leetcode.com/u/{self.username}/",
        }

        try:
            response = requests.post(
                self.URL, json=payload, headers=headers, timeout=10
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise LeetCodeAPIError(f"Request failed: {e}")

        try:
            data = response.json()
            data = data["data"]
        except ValueError:
            raise LeetCodeAPIError("Invalid JSON response")

        return data

    def get_question_progress(self):
        query = """
        query userProfileUserQuestionProgressV2($userSlug: String!) {
          userProfileUserQuestionProgressV2(userSlug: $userSlug) {
            numAcceptedQuestions {
              count
              difficulty
            }
          }
        }
        """

        data = self._make_request(
            query=query,
            variables={"userSlug": self.username},
            operation_name="userProfileUserQuestionProgressV2",
        )

        try:
            return data["userProfileUserQuestionProgressV2"]["numAcceptedQuestions"]
        except (KeyError, TypeError):
            raise LeetCodeAPIError(f"Unexpected response format: {data}")
