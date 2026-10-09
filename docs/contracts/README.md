# NINFA media contracts

This directory holds **versioned, reviewable channel-specific policies**, not runtime rendering binaries.

## Does It Automate? Shorts v1.0.0

- [Creative/editorial and release contract](DOES_IT_AUTOMATE_SHORTS_MOTION_V1.md)
- [JSON Schema — input structure](shorts-motion-v1.schema.json)
- [PV-POC-006 non-sensitive example](fixtures/pv-poc-006.reference.json)
- [Local validator](../../tools/contracts/validate_short_contract.mjs) and [19 offline unit scenarios](../../tools/contracts/test_short_contract.mjs)
- [2026-10-08 Motion v1.2 voiced batch acceptance receipt](decisions/MOTION_V1_2_OWNER_UAT_2026-10-08.md) — owner accepted three reviewed shorts as audiovisual baseline; publication and general template certification remain separately gated.
- [2026-10-08 Motion v1.3 local finishing proof](decisions/MOTION_V1_3_LOCAL_FINISHING_2026-10-08.md) — preflight, offline FFmpeg finishing, SHA-keyed cache and review-only QA; no full visual engine or release authority.
- [Motion v1.4 Scene Engine ADR](decisions/MOTION_V1_4_SCENE_ENGINE_ADR.md) and [local proof receipt](decisions/MOTION_V1_4_LOCAL_PROOF_2026-10-08.md) — three separate visual families, 20 local unit tests, silent review-only outputs, no automated publishing.
- [Motion v1.4 → v1.3 narrated integration proof](decisions/MOTION_V14_V13_NARRATION_INTEGRATION_2026-10-08.md) — fourth narrowly scoped demo composition, one-command local pipeline using privately held English voice, 26 local tests; publication still blocked.

Run locally from the NINFA repository root (no CI, paid APIs, social app or personal voice required):

\`\`\`bash
node tools/contracts/validate_short_contract.mjs docs/contracts/fixtures/pv-poc-006.reference.json
node tools/contracts/test_short_contract.mjs
\`\`\`

The expected valid fixture output says **\`CONTRACT_VALID\` with \`release: BLOCKED\`**. Passing contract consistency means its declarations follow policy; it does **not** prove that captions visually fit, the voice sounds good, the brand logo is authentic, real metrics exist, or a provider has actually published anything.

For a production candidate, use a new fixture tied to a verified source and human editorial approval; never edit the POC fixture to spoof a ready state.

**Authority hierarchy:** frozen [Does It Automate? Brand v1](../BRAND_IDENTITY.md) > [Channel Thesis](../CHANNEL_THESIS.md) > this motion style contract > individual scene templates. A prodAgentic/global policy is not authorized by this directory.

**Current status:** motion v1.0.0 creative policy is on `main`; the owner also accepted the voiced Motion v1.2 review batch as an audiovisual reference. Neither the original concept POC nor this batch constitutes publication authority, platform-safe-zone certification, or a generalized renderer/template certificate.
