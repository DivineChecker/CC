import os
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from curl_cffi import requests as cffi_requests

RELAY_SECRET = os.environ.get("RELAY_SECRET", "")
UPSTREAM = "https://claude.ai/api/organizations"

# Browser to impersonate at the TLS/JA3 + HTTP/2 fingerprint level.
# This is what gets us past Cloudflare's "Just a moment..." challenge.
IMPERSONATE = os.environ.get("IMPERSONATE", "chrome124")

app = FastAPI()


@app.get("/")
def health():
    return {"ok": True, "service": "claude-relay", "impersonate": IMPERSONATE}


@app.get("/organizations")
def organizations(
    request: Request,
    x_relay_secret: str | None = Header(default=None),
):
    if RELAY_SECRET and x_relay_secret != RELAY_SECRET:
        raise HTTPException(status_code=401, detail="bad relay secret")

    cookie = request.headers.get("cookie", "")
    if not cookie:
        raise HTTPException(status_code=400, detail="missing Cookie header")

    headers = {
        "Cookie": cookie,
        "User-Agent": request.headers.get(
            "user-agent",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        ),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://claude.ai/",
        "Origin": "https://claude.ai",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    try:
        r = cffi_requests.get(
            UPSTREAM,
            headers=headers,
            impersonate=IMPERSONATE,
            timeout=25,
            allow_redirects=False,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"upstream error: {e}")

    ct = r.headers.get("content-type", "")
    if "application/json" in ct:
        try:
            return JSONResponse(status_code=r.status_code, content=r.json())
        except Exception:
            pass
    return PlainTextResponse(status_code=r.status_code, content=r.text)
