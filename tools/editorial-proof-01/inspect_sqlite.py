#!/usr/bin/env python3
"""Read-only, evidence-grounded SQLite inspection for NINFA editorial capture.

Shows a fresh inspection of persisted rows, NOT footage of original inserts.
Requires the Motion v1.5 content-hashed local synthetic replay receipt.
No external API, no image/voice/media generation, no edits to evidence.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
from contextlib import closing
import sys
import time

EXPECTED_HASH = "8dc48cde916fc45617a8d0022dccddca98c2886ef38e5e48971edf22c3e516b7"
EVENT = "evt_local_001"
NOTE = "synthetic fulfillment"


def verify_receipt(folder: Path) -> dict:
    receipt = json.loads((folder / "replay_evidence.json").read_text(encoding="utf-8"))
    digest = receipt.pop("sha256_content", None)
    actual = hashlib.sha256(json.dumps(receipt, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()
    if digest != EXPECTED_HASH or actual != EXPECTED_HASH:
        raise ValueError("POLICY_BLOCKED: receipt hash does not match NINFA local source")
    if receipt.get("schema") != "local-replay-v1" or receipt.get("experimental_mode") != "LOCAL_SYNTHETIC_SEQUENTIAL":
        raise ValueError("POLICY_BLOCKED: source is not a sequential synthetic replay")
    if receipt.get("inputs") != {"event_key": EVENT, "sequence": [EVENT, EVENT]}:
        raise ValueError("POLICY_BLOCKED: synthetic event key mismatch")
    if receipt.get("api_spend_usd") != 0 or receipt.get("published") is not False:
        raise ValueError("POLICY_BLOCKED: unexpected source authority")
    if not any("no concurrent" in str(x) for x in receipt.get("limitations", [])):
        raise ValueError("POLICY_BLOCKED: missing concurrency limitation")
    return receipt


def inspect_db(path: Path, guarded: bool) -> tuple[list[tuple[int, str, str]], list[tuple]]:
    # file URI with mode=ro prevents writes. closing() releases Windows file handles.
    # sqlite3.Connection's own context manager only commits/rolls back; it does not close.
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as con:
        rows = con.execute("SELECT id, event_key, note FROM actions ORDER BY id").fetchall()
        indexes = con.execute("PRAGMA index_list('actions')").fetchall()
        index_defs = con.execute("SELECT name, sql FROM sqlite_master WHERE type='index'").fetchall()
    expected = [(i, EVENT, NOTE) for i in range(1, 2 if guarded else 3)]
    if rows != expected:
        raise ValueError("POLICY_BLOCKED: persisted database rows differ from the receipt")
    approved_idx = ("idx_actions_event_key", "CREATE UNIQUE INDEX idx_actions_event_key ON actions(event_key)")
    if guarded:
        if approved_idx not in index_defs or not any(index[1] == approved_idx[0] and index[2] == 1 for index in indexes):
            raise ValueError("POLICY_BLOCKED: unique key missing or misconfigured")
    elif indexes or index_defs:
        raise ValueError("POLICY_BLOCKED: naive database unexpectedly contains indexes")
    return rows, index_defs


def capture(folder: Path, pause: float) -> None:
    receipt = verify_receipt(folder)
    naive, ni = inspect_db(folder / "naive.sqlite", False)
    guarded, gi = inspect_db(folder / "guarded.sqlite", True)
    if receipt["naive"].get("new_actions") != len(naive) or receipt["guarded"].get("new_actions") != len(guarded):
        raise ValueError("POLICY_BLOCKED: recorded action counts differ from SQLite rows")
    if receipt["naive"].get("inserted") != [True, True] or receipt["guarded"].get("inserted") != [True, False]:
        raise ValueError("POLICY_BLOCKED: attempted writes do not match source receipt")
    if receipt["naive"].get("attempts") != 2 or receipt["guarded"].get("attempts") != 2:
        raise ValueError("POLICY_BLOCKED: incorrect number of attempts")

    def shot(heading: str, *lines: str) -> None:
        print("\n" + "=" * 64)
        print(heading)
        print("=" * 64)
        for line in lines:
            print(line)
        sys.stdout.flush()
        if pause:
            time.sleep(pause)

    shot("01 / SOURCE PROVENANCE · LOCAL SYNTHETIC SEQUENTIAL REPLAY",
         "A new read-only inspection of existing local SQLite databases.",
         "This is NOT recording of the original INSERT operations.",
         f"Verified source SHA256: {EXPECTED_HASH[:16]}…",
         "No provider webhook, API, concurrent traffic or production data.")
    shot("02 / CASE A · WITHOUT UNIQUE KEY",
         "SELECT id, event_key FROM actions ORDER BY id;",
         *(f"row {id}  |  {key}" for id, key, note in naive),
         f"Persisted rows: {len(naive)}",
         "Unique event-key index: ABSENT")
    shot("03 / CASE B · WITH UNIQUE(event_key)",
         gi[0][1],
         "SELECT id, event_key FROM actions ORDER BY id;",
         *(f"row {id}  |  {key}" for id, key, note in guarded),
         f"Persisted rows: {len(guarded)}",
         "Source receipt confirms second sequential INSERT was ignored.")
    shot("04 / RESULT · EVIDENCE-BOUND CLAIMS",
         "WITHOUT UNIQUE KEY  →  2 stored actions",
         "WITH UNIQUE KEY     →  1 stored action",
         "Sequential synthetic SQLite only · concurrency NOT tested.",
         "Do not portray as provider webhook or production safety proof.",
         "CAPTURE END · REVIEW ONLY · PUBLISH AUTHORITY NONE")
    print(json.dumps({"status": "CAPTURE_SOURCE_VERIFIED", "naive_rows": 2, "guarded_rows": 1,
                      "source_sha256": EXPECTED_HASH, "publish_authority": "NONE"}))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--evidence", type=Path, required=True, help="Directory containing naive.sqlite, guarded.sqlite and replay_evidence.json")
    p.add_argument("--pause-seconds", type=float, default=0, help="Per-section hold for an actual terminal screen recorder; 0..10")
    opts = p.parse_args()
    if not 0 <= opts.pause_seconds <= 10:
        p.error("--pause-seconds must be between 0 and 10")
    capture(opts.evidence, opts.pause_seconds)


if __name__ == "__main__":
    main()
