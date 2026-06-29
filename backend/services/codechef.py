"""
CodeChef integration.

CodeChef has NO API of any kind -- official or unofficial. Every
CodeChef tracker either:
  (a) depends on a third-party community wrapper that itself scrapes
      CodeChef, or
  (b) scrapes the public profile page directly.

This is the most fragile integration in this app. Both layers can break
without warning if CodeChef changes their page markup.

Strategy:
  1. Try a community-run JSON wrapper first (less code on our side).
  2. If that fails, fall back to scraping codechef.com/users/{handle}
     directly with BeautifulSoup.
  3. If both fail, raise a clear error -- never return fake/zero data
     silently.
"""
from typing import Any, Dict, Optional
import httpx
from bs4 import BeautifulSoup

COMMUNITY_API = "https://codechef-api.vercel.app/handle/{handle}"
PROFILE_URL = "https://www.codechef.com/users/{handle}"


class CodeChefError(Exception):
    pass


async def _try_community_api(handle: str) -> Optional[Dict[str, Any]]:
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            resp = await client.get(COMMUNITY_API.format(handle=handle))
            if resp.status_code != 200:
                return None
            data = resp.json()
            if not data or data.get("success") is False:
                return None
            return {
                "platform": "codechef",
                "handle": handle,
                "rating": data.get("currentRating"),
                "max_rating": data.get("highestRating"),
                "stars": data.get("stars"),
                "global_rank": data.get("globalRank"),
                "country_rank": data.get("countryRank"),
                "source": "community-api",
            }
    except Exception:
        return None


async def _try_scrape(handle: str) -> Optional[Dict[str, Any]]:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; CodeTracker/1.0)"}
        async with httpx.AsyncClient(timeout=10, headers=headers) as client:
            resp = await client.get(PROFILE_URL.format(handle=handle))
            if resp.status_code != 200:
                return None
            soup = BeautifulSoup(resp.text, "html.parser")

            rating_el = soup.select_one(".rating-number")
            stars_el = soup.select_one(".rating-star")
            ranks = soup.select(".rating-ranks li a, .rating-ranks li")

            global_rank = None
            country_rank = None
            for r in ranks:
                text = r.get_text(strip=True)
                if "Global Rank" in text:
                    global_rank = "".join(c for c in text if c.isdigit())
                elif "Country Rank" in text:
                    country_rank = "".join(c for c in text if c.isdigit())

            if not rating_el:
                return None

            return {
                "platform": "codechef",
                "handle": handle,
                "rating": int(rating_el.get_text(strip=True)) if rating_el.get_text(strip=True).isdigit() else None,
                "max_rating": None,  # not reliably present in markup; left for future improvement
                "stars": stars_el.get_text(strip=True) if stars_el else None,
                "global_rank": int(global_rank) if global_rank else None,
                "country_rank": int(country_rank) if country_rank else None,
                "source": "scrape",
            }
    except Exception:
        return None


async def get_profile(handle: str) -> Dict[str, Any]:
    result = await _try_community_api(handle)
    if result:
        return result

    result = await _try_scrape(handle)
    if result:
        return result

    raise CodeChefError(
        f"Could not fetch CodeChef data for '{handle}'. "
        "Both the community API and direct scraping failed -- "
        "the user may not exist, or CodeChef/the wrapper may have changed."
    )
