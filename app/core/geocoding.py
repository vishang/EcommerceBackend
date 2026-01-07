from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Optional, Tuple

from app.core.config import settings


def geocode_address(
    *,
    line1: str,
    line2: Optional[str],
    suburb: str,
    city: str,
    state: str,
    country: str,
    pincode: str,
) -> Optional[Tuple[float, float]]:
    if not settings.GOOGLE_GEOCODING_API_KEY:
        return None

    query = ", ".join(
        part
        for part in [line1, line2, suburb, city, state, country, pincode]
        if part
    )
    params = urllib.parse.urlencode(
        {
            "address": query,
            "key": settings.GOOGLE_GEOCODING_API_KEY,
        }
    )
    url = f"https://maps.googleapis.com/maps/api/geocode/json?{params}"
    req = urllib.request.Request(url)

    with urllib.request.urlopen(req, timeout=10) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    if not payload or payload.get("status") != "OK":
        return None

    results = payload.get("results", [])
    if not results:
        return None

    location = results[0].get("geometry", {}).get("location", {})
    if "lat" not in location or "lng" not in location:
        return None

    return float(location["lat"]), float(location["lng"])
