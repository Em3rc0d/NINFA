# NINFA × Remotion — Windows render evidence (owner-reported)

**Observation date:** 2026-10-23 (America/Lima)
**Environment:** Windows PowerShell, Node.js v24.11.1, pinned Remotion 4.0.538
**Commit under test:** `03ea083be017ab2dbfa56b550a9920febb276e07` on `exp/remotion-local-poc-20261023`
**Status:** `WINDOWS_TECHNICAL_RENDER_PASS_REPORTED / DIRECT_MEDIA_REVIEW_PENDING / RELEASE_BLOCKED`

## Console evidence

- Fast-forward from `dbd9100` to `03ea083` applied.
- `npm test`: **10 PASS / 0 FAIL**, including free-port regression.
- `npm run typecheck`: **PASS** (no errors reported).
- All 3 Remotion CLI renders reached encoding/output completion after dynamically allocating ports other than 3000.
- Review receipts were produced by the existing wrapper **after** its FFprobe frame/stream checks.

| Case | Frames | FPS | Dimensions | Video length | Elapsed | Approx output | SHA-256 reported |
|---|---:|---:|---|---|---:|---:|---|
| CacheRace | 180 | 30 | 1080×1920 | 6s | 14,550 ms | 126.3 kB | `d7acce60a668accdd40e532a76e51fd233d7cf7bfc140df8fc82fd3144832f5e` |
| WebhookReplay | 720 | 30 | 1080×1920 | 24s | 48,476 ms | 529 kB | `e3ef3a5d9e936f4c11b2df8711b357a2083016264f78bf471df0f0de2128dda8` |
| AutomationFailure | 180 | 30 | 1080×1920 | 6s | 19,656 ms | 185.1 kB | `445a0eae53775a4d6eb55def0e7942985eb1d9192b8fe625e2351aec33d39b86` |

The script validates H.264, 1080×1920, 30 FPS, exact frame count and no unexpected audio before writing its receipt. The user-visible receipts preserve `release_state=BLOCKED` and `publish_authority=NONE`.

**Evidence limitation:** This record is based on the owner's console transcript. Final MP4 bytes and receipts were not uploaded for independent media inspection. It proves reported Windows technical execution, **not** visual quality, safe-area validity, factual claims, or audience results.

## Node 24 warning

All 3 runs emitted `[DEP0190]`: using `spawnSync` with the Windows `.cmd` shim and `shell:true` concatenates unescaped arguments. Subsequent hardening invokes the installed `@remotion/cli/remotion-cli.js` directly via `process.execPath`, with `shell:false`. The hardening's isolated helper tests passed locally in a Node 22 sandbox; the updated render itself must still be tested on the owner's Windows host.

## Open gates

1. View the real MP4s on desktop and physical phone: clarity, distinct purposeful motion, captions, overlays, factual disclaimers, canonical brand use.
2. Run same-host cold and warm baselines against Pillow Motion v1.4/v1.5; no renderer speed winner is established by three different compositions.
3. Validate v1.3 finishing with private voice/captions and human approval separately.
4. Audit and commit dependency lockfile, confirm rights/license, then decide whether the candidate meets the ADR promotion gates.
5. No autonomous publishing and no automatic merge.

Original media remains local in the sibling `NINFA-Review/renders` directory outside the checkout. No heavy MP4, human voice or sensitive hashes are included beyond the public render/output content fingerprints already in this receipt.
