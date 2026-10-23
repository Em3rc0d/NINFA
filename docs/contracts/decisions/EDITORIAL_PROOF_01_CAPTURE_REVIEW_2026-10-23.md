# NINFA Editorial Proof 01 — Owner screen-recording ingest QA

Date: **2026-10-23**, project: **Does It Automate?**
Status: **LIVE_SYNTHETIC_EVIDENCE_CAPTURE_ACCEPTED / EDITORIAL_MEDIA_QUALITY_HOLD / RELEASE_BLOCKED**

## Source file received and actually examined

Owner supplied a local OBS-style recording named `2026-10-23 15-39-14.mp4`. This is a **private user conversation attachment**; do not upload, copy or commit its bytes to public GitHub.

| Item | Observed on the uploaded file |
|---|---|
| Actual file SHA-256 | `f0b8a03ad336185c05254783222d79b0ba77f32a14536b41891aab45face2a8b` |
| Size | 13,450,205 bytes |
| Duration | 17.900 seconds |
| Video | H.264, 1280×720, 30fps, 537 video frames |
| Audio | AAC, 48 kHz, stereo, but near-silent (FFmpeg mean/max around -91 dB; silence detector from 0 through 17.856s) |
| Footage | Actual owner computer terminal as test is executed; Windows Terminal header and Windows taskbar visible |
| Visible content | Fresh `live_replay.py` execution; naive first and second INSERT accepted; guarded first accepted and second skipped; final counts 2 vs 1; explicit sequential-only/no provider/no concurrency statement; canonical receipt SHA printed |
| File identity caveat | Source video hash anchors this private attachment. A hash printed *inside the picture* is evidence of what the run displays, not an independent cryptographic binding between the video and the two SQLite database files. The previously owner-reported 5/5 test PASS is a separate fact. |
| Security caveat | Local Windows user/profile paths and terminal tabs are visible. No public release of this unredacted capture; redact/retake before any public use. |

The canonical SQLite synthetic source receipt displayed at the end is the known `8dc48cde916fc45617a8d0022dccddca98c2886ef38e5e48971edf22c3e516b7`. The inspected visual content is consistent with an authentic **new local sequential synthetic replay**. **It is not a real payment-provider webhook, live concurrent request test or historical capture of the earlier sqlite run.**

## Actual creative/footage review

**Evidence capture gate: PASS (scoped)**. A genuine computer-screen recording now shows the events executed, rather than merely reconstructed UI diagrams.

**Usable-for-editor-quality footage gate: HOLD**:
- Entire source is landscape 1280×720. The actual ~10–12px terminal text remains concentrated in the **upper-left**; the overwhelming majority is blank terminal. Enlarging in post would magnify tiny pixels and lack source detail, especially in 1080×1920 Shorts.
- Early part of the recording contains prior command history/setup, then the test. Source footage should start on the actual clean run; trim unneeded startup in an editor with source provenance intact.
- The unredacted Windows titlebar/tabs, user name path, taskbar and clock are not intended brand or editorial content. Any shot for release needs a clean window-focused crop/redaction that **does not falsify or remove evidence claims**.
- The audio stream is effectively silent. This is fine for raw technical B-roll; the final narrative requires **approved natural English audio**. The private previously owner-approved voice file from Motion v1.5 is not present in this attachment, and no assistant-made eSpeak replacement is acceptable.
- This is the **first real action shot**, not two visually independent camera sources or an automatically professional montage. A sustained terminal readout is insufficient to reverse the rejected PPT aesthetic.

## Production decision, next bounded step

1. **DO NOT** create another 24-second Remotion title-card video or an FFmpeg shake/zoom version of this tiny-text capture.
2. **Preserve** this MP4 unmodified as the private source evidence master. Source SHA above is for traceability; do not publish raw source identity data if it could reveal the owner’s local environment.
3. For clearer native shots, a **single retake** is helpful but not a source-truth requirement: use OBS Window Capture of the terminal (exclude taskbar and tabs where possible), Windows Terminal font enlarged to at least ~24px actual recording pixels, and keep content within a centered crop suitable for vertical editing. Use the same `live_replay.py` but generate a **new unique evidence directory**, clearly label it as another fresh sequential local run.
4. Locate and re-use the previously approved **private natural original English narration** if available and appropriate. Never commit raw voice, cloned reference audio, or private screen recordings to Git. Align edits to voice beats, not an arbitrary 24s scene grid.
5. Only after a sharp legible genuine evidence shot and natural narration are accessible, produce a **10–15s silent/voice-led hard-cut rough edit** incorporating the real operations and a separate authenticated result/constraint inspection. **No ambient bed, artificial shakes, decorative transitions, or invented 3D shot.**
6. The owner makes the aesthetic GO/HOLD/KILL decision by watching the rough cut at real-time speed, preferably on a real phone; tests and structural ffprobe cannot replace the editorial gate.

Owner's Windows inspector regression result: 5/5 PASS observed on console before this attachment. The newer live-replay tests have not been reported 9/9 on the owner's Windows host; do not claim they passed there.

**No code merge, production use, upload, publishing or release authority.**
