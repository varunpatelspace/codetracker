"""
Codeforces integration.

Codeforces has a real, official, documented public API:
https://codeforces.com/apiHelp

No API key needed for the read-only endpoints used here.
"""
from typing import Any, Dict, List
import httpx

BASE = "https://codeforces.com/api"


class CodeforcesError(Exception):
    pass


async def get_profile(handle: str) -> Dict[str, Any]:
    """
    Fetch core profile + rating history for a Codeforces handle.
    Raises CodeforcesError on failure (bad handle, API down, etc).
    """
    async with httpx.AsyncClient(timeout=10) as client:
        info_resp = await client.get(f"{BASE}/user.info", params={"handles": handle})
        info_data = info_resp.json()

        if info_data.get("status") != "OK":
            raise CodeforcesError(info_data.get("comment", "Unknown error fetching user.info"))

        user = info_data["result"][0]

        # Rating history (used to draw the rating graph). A brand-new user
        # with no rated contests gets a valid empty list here, not an error.
        rating_resp = await client.get(f"{BASE}/user.rating", params={"handle": handle})
        rating_data = rating_resp.json()
        rating_history: List[Dict[str, Any]] = (
            rating_data["result"] if rating_data.get("status") == "OK" else []
        )

        return {
            "platform": "codeforces",
            "handle": user.get("handle"),
            "rating": user.get("rating"),
            "max_rating": user.get("maxRating"),
            "rank": user.get("rank"),
            "max_rank": user.get("maxRank"),
            "avatar": user.get("titlePhoto"),
            "contribution": user.get("contribution"),
            "rating_history": [
                {
                    "contest_name": r.get("contestName"),
                    "rank": r.get("rank"),
                    "old_rating": r.get("oldRating"),
                    "new_rating": r.get("newRating"),
                    "date": r.get("ratingUpdateTimeSeconds"),
                }
                for r in rating_history
            ],
        }
