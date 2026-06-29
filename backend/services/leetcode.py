"""
LeetCode integration.

LeetCode has NO official public API. This uses the same unofficial
GraphQL endpoint LeetCode's own website calls (leetcode.com/graphql).
It is widely relied on by community tools, but it is undocumented and
unsupported -- LeetCode can change or rate-limit it without notice.
If this stops working, that is why.
"""
from typing import Any, Dict
import httpx

GRAPHQL_URL = "https://leetcode.com/graphql"

PROFILE_QUERY = """
query userProfile($username: String!) {
  matchedUser(username: $username) {
    username
    profile {
      ranking
      reputation
      starRating
    }
    submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
      }
    }
  }
  userContestRanking(username: $username) {
    rating
    globalRanking
    attendedContestsCount
  }
}
"""


class LeetCodeError(Exception):
    pass


async def get_profile(username: str) -> Dict[str, Any]:
    headers = {
        "Content-Type": "application/json",
        # LeetCode's GraphQL endpoint rejects requests with no Referer/UA
        "Referer": f"https://leetcode.com/{username}/",
        "User-Agent": "Mozilla/5.0 (compatible; CodeTracker/1.0)",
    }
    payload = {"query": PROFILE_QUERY, "variables": {"username": username}}

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(GRAPHQL_URL, json=payload, headers=headers)
        data = resp.json()

        if "errors" in data:
            raise LeetCodeError(str(data["errors"]))

        matched = data.get("data", {}).get("matchedUser")
        if not matched:
            raise LeetCodeError(f"No LeetCode user found for '{username}'")

        ac_counts = {
            row["difficulty"]: row["count"]
            for row in matched["submitStatsGlobal"]["acSubmissionNum"]
        }
        contest = data.get("data", {}).get("userContestRanking")

        return {
            "platform": "leetcode",
            "handle": matched.get("username"),
            "total_solved": ac_counts.get("All", 0),
            "easy": ac_counts.get("Easy", 0),
            "medium": ac_counts.get("Medium", 0),
            "hard": ac_counts.get("Hard", 0),
            "ranking": matched.get("profile", {}).get("ranking"),
            "contest_rating": round(contest["rating"]) if contest and contest.get("rating") else None,
            "contest_global_rank": contest.get("globalRanking") if contest else None,
            "contests_attended": contest.get("attendedContestsCount") if contest else None,
        }
