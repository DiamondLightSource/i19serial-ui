from pathlib import Path
from typing import Any

import httpx

SERVER = "https://numtracker.diamond.ac.uk/graphql"


# YEP, except I still need to figure out how to get the token out of i19-2-blueapi!
def run_query(query: str, token: str | None = None) -> dict[str, Any]:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    res = httpx.post(SERVER, json={"query": query}, headers=headers)
    return res.json()["data"]


def query_numtracker_for_visit_directory(
    instrument_session: str, token: str | None = None
):
    query = f"""{{
        paths(instrument: 'i19', instrumentSession: {instrument_session}) {{
            path
        }}
    }}"""
    visit_directory = run_query(query, token)
    return Path(visit_directory["paths"]["path"])
