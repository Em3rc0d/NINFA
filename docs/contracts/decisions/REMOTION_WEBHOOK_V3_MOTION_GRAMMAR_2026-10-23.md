# NINFA Motion grammar v1 — Webhook visual vertical slice

Date: 2026-10-23
**Status: DESIGN FROZEN FOR A SINGLE REVIEW-ONLY VERTICAL SLICE. Not a production design system.**
Parent evidence: Motion v1.5 `tools/motion-v15/story.json` and content-hashed local receipt. Owner rejected flat V1/V2 and V2 text collisions after inspecting six true MP4s.

## Creative direction (testable)
Create a **continuous animated mechanism**, not cards revealed as slides. Each 24-second shot has one question and one observable state transition. Camera composition is consistent, but visual action differs: two arrival tokens, persisted rows, unique-key gate, blocked second write, clear 2-versus-1 ledger. Cyan is information in transit; coral marks unprotected duplicate writes; mint marks guarded, recorded state. The background grid is supporting structure, not AI-themed decoration. Large English typography and purposeful whitespace; no synthesized brand mark.

## Motion invariants
1. **Exactly one active shot per rendered frame.** Use half-open `[start,end)` shot intervals, no overlapping shot DOM/opacity crossfade. A hard cut is preferable to double-visible titles.
2. **Every active interval has an explicit mechanism/action**, not an inert full-screen title. Event token positions depend on `useCurrentFrame()` and documented shot-local frames.
3. **Never infer physics/state from animation alone.** Illustrated pathways are a reconstructed explanatory model, not recorded SQLite GUI footage. Facts are limited to two synthetic sequential deliveries via separate connections: naive 2 new actions; `UNIQUE(event_key)` guarded 1.
4. **Never imply true webhook networking, concurrency or live money movement.** Final big disclosure: `CONCURRENCY NOT TESTED`; persistent small header `LOCAL SQLITE · SYNTHETIC REPLAY`.
5. Every number comes from adapter props or the canonical bounded contract. No silent substitution of real benchmark data with decorative counts.
6. Silent visual master only. No owner voice or arbitrary media. Narration/caption timings are a **draft script** until a recorded human voice or approved local voice is available; do not claim phrase alignment.
7. Keep reviewed palette consistent with frozen brand but omit real logo until actual canonical bytes are supplied. Device safe zones provisional: top 220 px / bottom 350 px / sides 85 px (1080×1920), separate clear caption reserve y1460..1570.
8. No publication authority, paid APIs, GitHub Actions encoding or automatic upload. FFmpeg Motion v1.3 finishing stays untouched.

## Timed shot contract

Frame ranges are start-inclusive, end-exclusive at 30fps. Source of truth: `tools/remotion-poc/storyboards/webhook-v3.json`.

| Frames | Seconds | Beat | Observable action |
|---|---|---|---|
| 0–77 | 0.00–2.60 | hook | Reveal two distinct sequential tokens with the same synthetic event key |
| 78–209 | 2.60–7.00 | naive | Animate two deliveries entering the naive SQLite write lane in sequence; append exactly two rows |
| 210–293 | 7.00–9.80 | naive-result | Hold the two persisted rows in the simulated ledger; highlight count 2 |
| 294–398 | 9.80–13.30 | constraint | Show the constraint inserted into an abstract pipeline; do not imply actual recorded GUI footage |
| 399–551 | 13.30–18.40 | guarded | First delivery reaches SQLite and inserts one row; second token stops at the guard; neither token implies concurrent execution |
| 552–635 | 18.40–21.20 | compare | Compare persisted naive count 2 against guarded count 1, without claiming global prevention |
| 636–719 | 21.20–24.00 | limitation | Show a final high-contrast scope disclaimer; no external provider or production reliability claim |

### Proposed English voice guide (NOT rendered/aligned)
- 0.00–2.60s: “One synthetic event. Delivered twice.”
- 2.60–7.00s: “Without a uniqueness rule, both attempts write a row.”
- 7.00–9.80s: “That leaves two actions from one event.”
- 9.80–13.30s: “Now add a unique key at the database.”
- 13.30–18.40s: “The first insert succeeds. The next duplicate is ignored.”
- 18.40–21.20s: “Same inputs: two writes before, one after.”
- 21.20–24.00s: “Sequential SQLite only. Concurrency not tested.”

## QA acceptance; known blockers
- Automated: schema, 720-frame contiguous nonoverlapping shot schedule; source/receipt verified; expected caveat; no authority escalation; renderer and CLI accept only known V3 entrypoint; 14 prior tests do not regress.
- Media: compile TypeScript and render V3 on Windows or other compatible local host; independently inspect ffprobe and source SHA; image captures of all 7 shots and **frames adjacent to every cut** (77/78, 209/210, 293/294, 398/399, 551/552, 635/636).
- Visual: no text ghosting, readable central elements at 270px/mobile preview, deliberate real-state changes through animation, consistent truth labeling and accessible color contrast.
- Editorial: assess one 24-second complete pilot, side-by-side with V1 and V2; avoid producing Cache V3 or Automation V3 until this single pilot passes.
- Finishing: narrator reads voice guide naturally; align captions using the actual recording, not manifest time guesses; validate Motion v1.3 on a private path.
- Source licensing, owner approval, phone QA and reach/retention metrics remain external gates.

**GO FOR NEXT ITERATION** if one Webhook pilot is readable, accurate, animated with real mechanism and mobile-accepted; **HOLD** if only code/tests pass; **REJECT** if a third revision still primarily produces cards/slides. In no case does this authorise YouTube publication or merging to main.
