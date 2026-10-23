# NINFA × Remotion — Windows render evidence (owner-reported)

**Observation date:** 2026-10-23 (America/Lima)
**Environment:** Windows PowerShell, Node.js v24.11.1, pinned Remotion 4.0.538
**Commit under test:** `03ea083be017ab2dbfa56b550a9920febb276e07` on `exp/remotion-local-poc-20261023`
**Status:** `WINDOWS_TECHNICAL_RENDER_AND_NODE24_HARDENING_PASS_REPORTED / DIRECT_MEDIA_REVIEW_PENDING / RELEASE_BLOCKED`

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

All 3 runs emitted `[DEP0190]`: using `spawnSync` with the Windows `.cmd` shim and `shell:true` concatenates unescaped arguments. Subsequent hardening invokes the installed `@remotion/cli/remotion-cli.js` directly via `process.execPath`, with `shell:false`. The hardening passed its new regression checks and a real cache re-render on the owner's Windows Node.js 24.11.1 host, without a DEP0190 warning in the supplied transcript.

## Windows Node 24 hardening retest — 2026-10-23

**Commit actually tested:** `f5606c2ee304f89e98345bdf5be40eacc3108d94`. After `git pull --ff-only` from `03ea083` to `f5606c2`:

- `npm test`: **13 passed / 0 failed**, including direct Node launch, rejecting invalid composition/port, and isolated-port behavior.
- `npm run typecheck`: **PASS** (no output/errors).
- `node scripts/render.mjs cache ".../renders/cache-hardened.mp4"`: **PASS**, using an isolated dynamic port `65045`, H.264, 1080 × 1920, 30 fps, 180 frames, silently rendered.
- Total `elapsed_ms: 18632`; video approx. `126.3 kB`; props SHA matches the prior CacheRace run.
- Hardening run MP4 SHA: `d7acce60a668accdd40e532a76e51fd233d7cf7bfc140df8fc82fd3144832f5e`, **the same** as the pre-hardening run at `03ea083`. This is evidence of identical encoded output in the supplied receipts; the MP4 bytes themselves were not uploaded for independent hashing.
- The transcript shows **no `[DEP0190]` warning** on the hardened run. This validates the mitigation in this Windows test; it is not a general proof about all environments.
- Difference between original 14,550 ms and hardened 18,632 ms does **not** establish a performance regression: single runs, different state/load, no same-host matched repeated sample.

**Current technical gate:** `NODE24_HARDENING_PASS_REPORTED`. New media was still not directly uploaded for visual inspection. The prior webhook and automation media were generated using the original launcher; their rendering had already passed structural QA, but they were not rerun with the hardened script (unnecessary for this narrow launch-security check).

### Still required before production adapter adoption

1. Inspect real `cache.mp4`, `webhook.mp4` and `automation.mp4` visually (or contact sheets/video snippets), including first/last frames and transitions, accurate benchmark attribution, legible factual caveats, safe areas on a physical device, contrast and original composition.
2. Run representative Pillow/FFmpeg baselines with a fair repeated protocol on the same Windows host.
3. Test a human-approved private voice/caption finishing case with unchanged Motion v1.3.
4. Review pinned dependency lockfile and licensing, then obtain explicit owner decision. **NO MERGE / NO PUBLISH until gates are independently satisfied.**

## Open gates

1. View the real MP4s on desktop and physical phone: clarity, distinct purposeful motion, captions, overlays, factual disclaimers, canonical brand use.
2. Run same-host cold and warm baselines against Pillow Motion v1.4/v1.5; no renderer speed winner is established by three different compositions.
3. Validate v1.3 finishing with private voice/captions and human approval separately.
4. Audit and commit dependency lockfile, confirm rights/license, then decide whether the candidate meets the ADR promotion gates.
5. No autonomous publishing and no automatic merge.

Original media remains local in the sibling `NINFA-Review/renders` directory outside the checkout. No heavy MP4, human voice or sensitive hashes are included beyond the public render/output content fingerprints already in this receipt.
