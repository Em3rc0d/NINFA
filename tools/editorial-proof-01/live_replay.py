#!/usr/bin/env python3
"""Record a NEW live sequential synthetic SQLite experiment (not an archived run).

Shows real INSERT OR IGNORE results at the moment they execute.
No network provider, real payment, concurrency or production safety claim.
"""
from __future__ import annotations
import argparse
from contextlib import closing
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import time

EVENT = "evt_local_001"
NOTE = "synthetic fulfillment"
CANONICAL_SHA = "8dc48cde916fc45617a8d0022dccddca98c2886ef38e5e48971edf22c3e516b7"

def run_live(out: Path, pause: float = 0) -> dict:
    if not 0 <= pause <= 5:
        raise ValueError("POLICY_BLOCKED: pause outside 0..5 seconds")
    out = out.expanduser().resolve()
    here = Path(__file__).resolve()
    source_root = here.parents[2] if here.parent.name == "editorial-proof-01" else here.parent
    if out == source_root or source_root in out.parents:
        raise ValueError("POLICY_BLOCKED: evidence output must be outside Git/source folder")
    if out.exists():
        raise ValueError("POLICY_BLOCKED: cannot overwrite existing capture directory")
    out.mkdir(parents=True, exist_ok=False)
    print("NEW LOCAL TEST · sequential synthetic SQLite only", flush=True)
    print("This is a fresh run, NOT archival footage or a provider webhook.", flush=True)

    def case(guarded: bool) -> dict:
        name = "guarded" if guarded else "naive"
        path = out / (name + ".sqlite")
        with closing(sqlite3.connect(path)) as con, con:
            con.execute("CREATE TABLE actions (id INTEGER PRIMARY KEY, event_key TEXT NOT NULL, note TEXT NOT NULL)")
            if guarded:
                con.execute("CREATE UNIQUE INDEX idx_actions_event_key ON actions(event_key)")
        print("\n" + ("WITH UNIQUE(event_key)" if guarded else "WITHOUT UNIQUE INDEX"), flush=True)
        inserted: list[bool] = []
        for attempt in (1, 2):
            print(f"Attempt {attempt}/2: INSERT OR IGNORE event_key={EVENT}", flush=True)
            with closing(sqlite3.connect(path)) as con, con:
                cursor = con.execute("INSERT OR IGNORE INTO actions(event_key, note) VALUES(?, ?)", (EVENT, NOTE))
                accepted = cursor.rowcount == 1
            inserted.append(accepted)
            with closing(sqlite3.connect(path)) as con:
                rows = con.execute("SELECT event_key, note FROM actions ORDER BY id").fetchall()
            print(f"  affected_rows={1 if accepted else 0}; stored_actions={len(rows)}; "
                  f"{'INSERTED' if accepted else 'DUPLICATE SKIPPED'}", flush=True)
            if pause:
                time.sleep(pause)
        with closing(sqlite3.connect(path)) as con:
            rows = con.execute("SELECT event_key, note FROM actions ORDER BY id").fetchall()
        return {"mode": name, "attempts": 2, "new_actions": len(rows),
                "inserted": inserted, "stored_event_keys": [r[0] for r in rows]}

    naive = case(False)
    guarded = case(True)
    expected_naive = {"mode": "naive", "attempts": 2, "new_actions": 2,
                      "inserted": [True, True], "stored_event_keys": [EVENT, EVENT]}
    expected_guarded = {"mode": "guarded", "attempts": 2, "new_actions": 1,
                        "inserted": [True, False], "stored_event_keys": [EVENT]}
    if naive != expected_naive or guarded != expected_guarded:
        raise ValueError("POLICY_BLOCKED: unexpected SQLite experimental results")

    receipt = {
        "schema": "local-replay-v1", "experimental_mode": "LOCAL_SYNTHETIC_SEQUENTIAL",
        "description": "Two deliveries of the same synthetic event in separate SQLite connections",
        "inputs": {"event_key": EVENT, "sequence": [EVENT, EVENT]},
        "naive": naive, "guarded": guarded,
        "limitations": ["no external webhook provider", "no real money or business action",
                        "no concurrent delivery", "no network / API use", "no production reliability claim"],
        "api_spend_usd": 0, "github_actions_media": False, "published": False
    }
    digest = hashlib.sha256(json.dumps(receipt, ensure_ascii=False, sort_keys=True,
                                       separators=(",", ":")).encode("utf8")).hexdigest()
    if digest != CANONICAL_SHA:
        raise ValueError("POLICY_BLOCKED: differs from canonical content-hashed NINFA source")
    receipt["sha256_content"] = digest
    (out / "replay_evidence.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print("\nVERIFIED RESULT · WITHOUT UNIQUE: 2 · WITH UNIQUE: 1", flush=True)
    print("Sequential test only. Concurrency NOT tested. No real provider.", flush=True)
    print("Source receipt SHA-256: " + digest, flush=True)
    print("REVIEW ONLY · NO PUBLISH AUTHORITY", flush=True)
    return receipt

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--pause-seconds", type=float, default=0)
    args = p.parse_args()
    run_live(args.out, args.pause_seconds)

if __name__ == "__main__":
    main()
