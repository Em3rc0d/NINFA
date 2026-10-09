# Motion v1.4 Scene Engine — local proof receipt

**Date:** 2026-10-08 (America/Lima). **Status:** `ENGINEERING_POC_PASS / OWNER_V1_4_UAT_PENDING / RELEASE_BLOCKED`.

The exact source, fixtures and tests were authored and executed in the assistant's isolated local Linux container, then independently fetched from the NINFA feature branch and checked by matching Git blob SHA-1. **No Actions, paid API, voice, posting, or publishing.**

## Executed evidence

| Fixture | Composition family | Content status | Frames / seconds | MP4 SHA-256 | Render elapsed |
|---|---|---|---|---|---|
| `cache-proof` | `cache_race` | bounded real local v1.3 cache measurement | 180 / 6.0 | `b392ac82db3aaf1d34e8b4098d361f0ce5966e88d61da6da098b26ad6556ddc1` | 4.79s final inspected render |
| `breaker-demo` | `circuit_breaker` | DEMO, no real HTTP calls | 180 / 6.0 | `8d77b9b2c289bd1bd822a87cd5aff76696b7326cd6e1a9d66780eeae8ff082b2` | 5.32s final render |
| `source-demo` | `source_lineage` | DEMO, no real verification event | 180 / 6.0 | `291dcdc2d7043e3843178dac4f2913eca99a587c2ae8bae1f495de8d5be28de5` | 5.41s final render |

All 3 FFprobe checks: `1080 × 1920`, `30/1 fps`, `H.264`, `180 decoded video frames`, video-only, duration `6.0 seconds`.

- **20/20 Python unit/negative tests PASS**, including source attribution, fake metrics, hidden/demo status, budgets, brand/English, unknown keys, unsafe markup and overflowing text.
- Exact committed blob SHA-1 for `tools/motion-v14/engine.py`: `c85c8c516ef6accce471bc0c2f096ae209e52815`.
- Exact committed blob SHA-1 for `tools/motion-v14/tests/test_engine.py`: `9ee133ef641efd32c7d02092884436d247bc730b`.
- Each of 3 JSON fixture blobs also matched the locally exercised sources.
- All three output videos are structurally compatible with v1.3's `assert_visual` validator (checked against real output files, 180 frames).
- Five pairs of 1-second-separated thumbnails per video had **nonzero** frame difference; this detects identical frozen frames but does not prove motion attractiveness.
- No personal voice, full MP4 or downloaded fonts are stored in GitHub.

## Boundaries

Not an independent owner visual acceptance, not certified TikTok or Shorts safe-zone compliance, not a cross-topic arbitrary animation spec, not an external benchmark rerun and not a production provider authorization.

The numeric `4.80s` vs `1.15s` reflects a **single already observed local caching test** and is **not** an external benchmark or a promised performance ratio.

**Contract result:** `ADOPT_EXPERIMENTAL_MODULE`, `HOLD_AUTOMATED_PRODUCTION`, `HOLD_HUMAN_UAT`, `HOLD_PUBLISH`.
