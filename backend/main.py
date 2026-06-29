"""
CodeTracker backend.

Run with:  uvicorn main:app --reload --port 8000

Endpoints:
  GET /api/codeforces/{handle}
  GET /api/leetcode/{handle}
  GET /api/codechef/{handle}
  GET /api/profile?cf=...&lc=...&cc=...   (fetch any subset, in parallel)
"""
import asyncio
import time
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from services import codeforces, leetcode, codechef

app = FastAPI(title="CodeTracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for local/dev use; lock this down before any real deploy
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- tiny in-memory cache --------------------------------------------------
# Codeforces/LeetCode/CodeChef all rate-limit or dislike being hit repeatedly.
# A simple TTL cache means refreshing a page in the browser doesn't refetch
# everything immediately. Good enough for single-instance/dev use; swap for
# Redis if this ever runs as more than one process.
_CACHE: Dict[str, Dict[str, Any]] = {}
TTL_SECONDS = 5 * 60


def _cache_get(key: str) -> Optional[Dict[str, Any]]:
    entry = _CACHE.get(key)
    if entry and (time.time() - entry["ts"]) < TTL_SECONDS:
        return entry["data"]
    return None


def _cache_set(key: str, data: Dict[str, Any]) -> None:
    _CACHE[key] = {"data": data, "ts": time.time()}


# --- individual platform endpoints -----------------------------------------

@app.get("/api/codeforces/{handle}")
async def get_codeforces(handle: str):
    cache_key = f"cf:{handle.lower()}"
    cached = _cache_get(cache_key)
    if cached:
        return cached
    try:
        data = await codeforces.get_profile(handle)
        _cache_set(cache_key, data)
        return data
    except codeforces.CodeforcesError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/leetcode/{handle}")
async def get_leetcode(handle: str):
    cache_key = f"lc:{handle.lower()}"
    cached = _cache_get(cache_key)
    if cached:
        return cached
    try:
        data = await leetcode.get_profile(handle)
        _cache_set(cache_key, data)
        return data
    except leetcode.LeetCodeError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/codechef/{handle}")
async def get_codechef(handle: str):
    cache_key = f"cc:{handle.lower()}"
    cached = _cache_get(cache_key)
    if cached:
        return cached
    try:
        data = await codechef.get_profile(handle)
        _cache_set(cache_key, data)
        return data
    except codechef.CodeChefError as e:
        raise HTTPException(status_code=404, detail=str(e))


# --- aggregate endpoint ------------------------------------------------

@app.get("/api/profile")
async def get_combined_profile(
    cf: Optional[str] = Query(None, description="Codeforces handle"),
    lc: Optional[str] = Query(None, description="LeetCode username"),
    cc: Optional[str] = Query(None, description="CodeChef username"),
):
    """
    Fetch whichever platforms were given, in parallel. A failure on one
    platform does not block the others -- each comes back with either
    its data or an 'error' field.
    """
    if not (cf or lc or cc):
        raise HTTPException(status_code=400, detail="Provide at least one of: cf, lc, cc")

    async def safe_fetch(coro, label: str):
        try:
            return await coro
        except Exception as e:
            return {"platform": label, "error": str(e)}

    tasks = []
    if cf:
        tasks.append(safe_fetch(get_codeforces(cf), "codeforces"))
    if lc:
        tasks.append(safe_fetch(get_leetcode(lc), "leetcode"))
    if cc:
        tasks.append(safe_fetch(get_codechef(cc), "codechef"))

    results = await asyncio.gather(*tasks)
    return {r["platform"]: r for r in results}


@app.get("/api/health")
async def health():
    return {"status": "ok"}
