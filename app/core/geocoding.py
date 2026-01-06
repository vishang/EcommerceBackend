from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Optional, Tuple


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
    query = ", ".join(
        part
        for part in [line1, line2, suburb, city, state, country, pincode]
        if part
    )
    params = urllib.parse.urlencode({"format": "json", "q": query})
    url = f"https://nominatim.openstreetmap.org/search?{params}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "fastapi-course/1.0 (geocoding)"},
    )

    with urllib.request.urlopen(req, timeout=10) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    if not payload:
        return None

    first = payload[0]
    return float(first["lat"]), float(first["lon"])
