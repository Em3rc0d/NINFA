#!/usr/bin/env python3
"""Reproducible offline SQLite demo of duplicate delivery and idempotent handling.

DO NOT claim this simulates actual payment processors, networks, or concurrency.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
from contextlib import closing

SCHEMA = "local-replay-v1"
EVENT = "evt_local_001"  # synthetic, no personal/business data

def run_case(database: Path, guarded: bool) -> dict:
    if database.exists():
        raise ValueError("Refusing to overwrite an existing database")
    database.parent.mkdir(parents=True, exist_ok=True)
    inserted = []
    with closing(sqlite3.connect(database)) as con, con:
        con.execute("CREATE TABLE actions (id INTEGER PRIMARY KEY, event_key TEXT NOT NULL, note TEXT NOT NULL)")
        if guarded:
            con.execute("CREATE UNIQUE INDEX idx_actions_event_key ON actions(event_key)")
    for attempt in (1, 2):
        # Separate database connections to reflect distinct sequential deliveries.
        with closing(sqlite3.connect(database)) as con, con:
            cur = con.execute(
                "INSERT OR IGNORE INTO actions(event_key, note) VALUES(?, ?)",
                (EVENT, "synthetic fulfillment"),
            )
            inserted.append(cur.rowcount == 1)
    with closing(sqlite3.connect(database)) as con, con:
        rows = con.execute("SELECT event_key, note FROM actions ORDER BY id").fetchall()
    return {"mode": "guarded" if guarded else "naive", "attempts": 2,
            "new_actions": len(rows), "inserted": inserted,
            "stored_event_keys": [row[0] for row in rows]}

def generate(out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    a = run_case(out / "naive.sqlite", False)
    b = run_case(out / "guarded.sqlite", True)
    assert (a["attempts"], a["new_actions"], a["inserted"]) == (2, 2, [True, True])
    assert (b["attempts"], b["new_actions"], b["inserted"]) == (2, 1, [True, False])
    receipt = {
      "schema": SCHEMA, "experimental_mode": "LOCAL_SYNTHETIC_SEQUENTIAL",
      "description": "Two deliveries of the same synthetic event in separate SQLite connections",
      "inputs": {"event_key": EVENT, "sequence": [EVENT, EVENT]},
      "naive": a, "guarded": b,
      "limitations": ["no external webhook provider", "no real money or business action",
                      "no concurrent delivery", "no network / API use", "no production reliability claim"],
      "api_spend_usd": 0, "github_actions_media": False, "published": False}
    canonical = json.dumps(receipt, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    receipt["sha256_content"] = hashlib.sha256(canonical.encode()).hexdigest()
    (out / "replay_evidence.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return receipt

if __name__ == "__main__":
    p = argparse.ArgumentParser();p.add_argument("--out", required=True);args=p.parse_args()
    proof=generate(Path(args.out).resolve())
    print(json.dumps({"status":"PASS_LOCAL_SEQUENTIAL", "naive":proof["naive"]["new_actions"], "guarded":proof["guarded"]["new_actions"], "content_sha256":proof["sha256_content"]},indent=2))
