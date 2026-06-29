# CodeTrack

A small tool that looks up your Codeforces, LeetCode, and CodeChef stats
and shows them on one page. No login, no database, no scheduler -- you
type in usernames and it fetches live.

This is deliberately small. See "Why so minimal" below before asking
for auth/DB/notifications -- that's a second phase, not phase one.

## Run it

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Check it's alive: open `http://localhost:8000/api/health` -> `{"status":"ok"}`
Interactive API docs: `http://localhost:8000/docs`

### 2. Frontend

No build step. Just open `frontend/index.html` in a browser.
(If your browser blocks local fetch() calls, run a tiny local server instead:
`cd frontend && python3 -m http.server 5500`, then open `localhost:5500`.)

If your backend isn't on `localhost:8000`, change the `API_BASE` constant
near the top of the `<script>` tag in `index.html`.

## What actually works vs. what's fragile

| Platform   | Data source                          | Reliability |
|------------|---------------------------------------|-------------|
| Codeforces | Official public API                   | High -- documented, stable, free |
| LeetCode   | Unofficial GraphQL endpoint           | Medium -- works today, no contract, can change/rate-limit without notice |
| CodeChef   | Community API wrapper, then HTML scrape fallback | Low -- no official data source exists at all |

**I have not been able to test live network calls to leetcode.com,
codeforces.com, or codechef.com from the environment that built this** --
that sandbox can only reach package registries (pypi, npm, github), not
arbitrary websites. The Codeforces logic is verified against the official
documented response schema. The LeetCode and CodeChef logic follows known
community patterns but you need to run it yourself against real usernames
to confirm it still works today.

If LeetCode or CodeChef break:
- LeetCode: check if the GraphQL query in `backend/services/leetcode.py`
  still matches what leetcode.com/graphql expects (open devtools on
  leetcode.com, look at the network tab on your own profile page).
- CodeChef: the community wrapper (`codechef-api.vercel.app`) may be down;
  the scrape fallback in `backend/services/codechef.py` depends on
  CSS classes (`.rating-number`, `.rating-ranks`) that CodeChef can rename
  any time they redesign their site.

## API

- `GET /api/codeforces/{handle}`
- `GET /api/leetcode/{handle}`
- `GET /api/codechef/{handle}`
- `GET /api/profile?cf=...&lc=...&cc=...` -- fetch any subset in parallel;
  a failure on one platform doesn't block the others.

Each platform endpoint caches successful responses in memory for 5 minutes,
so repeated lookups don't hammer the upstream services.

## Why so minimal

The original brief for this asked for auth, Postgres, a 15-minute background
sync job, achievements, leaderboards, an "AI coach," and 10 frontend pages
in one pass. That's not a sane build order -- you'd end up debugging
broken data-fetching logic *underneath* a pile of features that depend on it
working. This version proves the three integrations actually return real
data first. Once you've confirmed all three work with your own usernames,
the natural next pieces, in order, are:

1. A database (so you're not refetching from scratch every visit)
2. A background scheduler that runs the fetch on an interval
3. Accounts/auth (only needed once there's something per-user to protect)
4. Everything else (achievements, leaderboard, AI coach) sits on top of (1)-(3)

Say which of those you want next and I'll build it against this working base.
