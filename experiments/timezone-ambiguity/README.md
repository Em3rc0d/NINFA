# S01 — Time-zone ambiguity experiment

Proof of one **local, deterministic scheduling-input edge case**, not a live calendar integration.

Run from repo root with Python 3.11+ and installed IANA timezone database:

```bash
python -m unittest discover -s experiments/timezone-ambiguity -v
python experiments/timezone-ambiguity/run.py --out experiments/timezone-ambiguity/evidence.json
```

Local observed environment: Python 3.13.5. **7 tests passed, 0 failed**.

Evidence file SHA-256 from that execution: `7bdc78a27ccf6c0423ed023f96697cf019ad05391dea2d356a43081b145d6089`.

Four cases: fall repeated hour (2 candidates), spring missing hour (0), two regular times (1 each). A permissive fold=0 conversion chooses a UTC time even when input is ambiguous or invalid; explicit validation blocks and asks the caller to clarify.

System tzdb version is not pinned; time-zone rules can change. No Google Calendar, Microsoft Outlook, user account, AI model, or real appointment tested. This evidence supports the narrow Python simulation only.

See `STORYBOARD_DRAFT.md` for a release-blocked short concept. No video was rendered, uploaded, or published.
