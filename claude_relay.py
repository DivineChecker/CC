import os
import httpx
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse

RELAY_SECRET = os.environ.get("RELAY_SECRET", "")
UPSTREAM = "https://claude.ai/api/organizations"

app = FastAPI()

@app.get("/")
def health():
    return {"ok": True, "service": "claude-relay"}

@app.get("/organizations")
async def organizations(request: Request, x_relay_secret: str | None = Header(default=None)):
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
            "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        ),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://claude.ai/",
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.get(UPSTREAM, headers=headers)

    ct = r.headers.get("content-type", "")
    if "application/json" in ct:
        return JSONResponse(status_code=r.status_code, content=r.json())
    return PlainTextResponse(status_code=r.status_code, content=r.text)
