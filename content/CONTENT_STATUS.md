# Content Status

Status date: 2026-10-02

## Voice engine — VALIDATED / PRODUCTION-CANDIDATE

Local Chatterbox voice cloning has been validated for Does It Automate.

Validated:
- Spanish reference → English narration,
- local Docker workflow,
- CPU fallback,
- NVIDIA CUDA path,
- GTX 1650 4 GB successful inference,
- zero paid TTS API requirement.

Measured baseline:
- CPU: ~83 s audio in 837 s, RTF ~10.08.
- GTX 1650: 79.9 s audio in 279.9 s, RTF ~3.50.
- observed GPU speedup vs CPU baseline: ~2.99x.

Canonical maintenance doc:
`docs/VOICE_CLONE_CHATTERBOX.md`.

## Video 001 — COMPLETE / PUBLISHED
**I Built an AI YouTube Video Factory for $0 — Here’s What Actually Worked**

Runtime: ~5:29.
YouTube: https://youtu.be/kWGgE9pFD_w

## Video 002 — COMPLETE / UPLOADED
**I Replaced a Paid AI Video Editor With Free Tools — Here’s What Happened**

Runtime: ~5:01.
Observed upload URL: https://youtu.be/aujH-Lla_Kc

Verify visibility in YouTube Studio when needed.

## Video 003 — READY FOR VOICEOVER PRODUCTION
**600 Real Business Tasks Exposed AI Agents — Here’s Where They Break**

The original plan to spend API credits running a fresh 100-task benchmark remains retired as unnecessary duplication.

Production approach:
- use public benchmark evidence,
- attribute every result to the organization/researchers who ran it,
- analyze real task structures and failure data,
- reconstruct visuals only when clearly labeled,
- spend $0 on benchmark API replication,
- generate narration in local Chatterbox using section-level WAV files.

Production package:
`content/video-003/PRODUCTION_PACKAGE_V1.md`.

Primary evidence:
**Zapier AutomationBench**
- 600 public scored tasks,
- six business domains,
- 47 simulated SaaS tools,
- deterministic final-state scoring.

The concrete failure replays currently used in Video 003 come from a published Qwen3.6-27B base AutomationBench run and must not be attributed to other models.

Separate public vs held-out/private benchmark splits must never be presented as the same run.

## Video 003 integrity rule

Do not say:
“I gave an AI agent 100 tasks”

unless we actually run such an experiment ourselves.

Allowed truthful formulations:
- “I analyzed public benchmark evidence”
- “Zapier tested agents across realistic business workflows”
- “The published trace/result shows…”
- “I reconstructed this example from published benchmark data”

## Priority queue after Video 003

1. **n8n vs AI Agents: What Should You Learn Now?**
2. **I Built an AI Employee for Less Than $20**
3. **5 AI Automations Businesses Will Actually Pay For**
4. **I Built a 24/7 AI Research Agent — Here’s What It Actually Gets Right**
5. **I Replaced 3 SaaS Tools With One AI Agent**
