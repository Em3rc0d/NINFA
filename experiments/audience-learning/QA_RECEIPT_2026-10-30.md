# Audience Learning v1 — local Node QA receipt (2026-10-30)

**Scope:** PR #17, branch `feat/mk1-audience-learning-2026-10-30`.

## Verified exact Git blob contents

The four reconstructed working files have the same Git blob IDs as the files fetched from the PR branch:

| File | Git blob SHA |
|---|---|
| `tools/audience-learning/learning.mjs` | `58d3367f8138f20c5d5d8d03230759d81901407c` |
| `tools/audience-learning/learning.test.mjs` | `deefde069e729688044c2d94dca8e1811212966b` |
| `experiments/audience-learning/studio-2026-10-30.json` | `75e08f659b7f0eee0289f66afc7aa98f5fbe1a7c` |
| `content/shorts/2026-10-30-learning-batch.json` | `27a472a7071fed75a82abfce3d047d8aaf189666` |

## Commands executed

```bash
node --version  # v22.16.0
git --version   # 2.47.3
node --test tools/audience-learning/learning.test.mjs
node tools/audience-learning/learning.mjs
```

### Results
- **11 tests passed, 0 failed.**
- CLI completed and returned **4 analytics observations** and **6 editorial candidates**.
- **All six candidates remained BLOCKED_PENDING_EVIDENCE_AND_HUMAN_QA.**
- Explicit missing-field flags preserved. No YouTube API access, provider upload, publication, media build, paid API or GitHub Actions invocation.
- Original repository could not be cloned over network in the local runtime, so four exact files were reconstructed and verified by Git blob hashes before testing. This validates the module and its fixtures; it is **not** a full NINFA repository-wide regression.
- Existing `.github/workflows/kokoro-short-narration.yml` triggers only when **that workflow file changes on main**. This PR leaves it unchanged; no media CI is requested.

## Still outside this gate
- Full motion-v1.x rendering/FFmpeg regression.
- Real experiment execution for NINFA-S01–S06.
- Human brand and mobile visual QA, source/claim review and YouTube publication approval.

**Decision:** code-only learning slice passes its local Node gate; no content release implied.
