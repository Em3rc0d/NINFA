# NINFA media contracts

This directory holds **versioned, reviewable channel-specific policies**, not runtime rendering binaries.

## Does It Automate? Shorts v1.0.0

- [Creative/editorial and release contract](DOES_IT_AUTOMATE_SHORTS_MOTION_V1.md)
- [JSON Schema — input structure](shorts-motion-v1.schema.json)
- [PV-POC-006 non-sensitive example](fixtures/pv-poc-006.reference.json)
- [Local validator](../../tools/contracts/validate_short_contract.mjs) and [17 offline unit scenarios](../../tools/contracts/test_short_contract.mjs)

Run locally from the NINFA repository root (no CI, paid APIs, social app or personal voice required):

\`\`\`bash
node tools/contracts/validate_short_contract.mjs docs/contracts/fixtures/pv-poc-006.reference.json
node tools/contracts/test_short_contract.mjs
\`\`\`

The expected valid fixture output says **\`CONTRACT_VALID\` with \`release: BLOCKED\`**. Passing contract consistency means its declarations follow policy; it does **not** prove that captions visually fit, the voice sounds good, the brand logo is authentic, real metrics exist, or a provider has actually published anything.

For a production candidate, use a new fixture tied to a verified source and human editorial approval; never edit the POC fixture to spoof a ready state.

**Authority hierarchy:** frozen [Does It Automate? Brand v1](../BRAND_IDENTITY.md) > [Channel Thesis](../CHANNEL_THESIS.md) > this motion style contract > individual scene templates. A prodAgentic/global policy is not authorized by this directory.

**Current status:** owner accepted PV-POC-006 **creative direction**. The prototype MP4, reused renderer, third-party platform-safe zones, and publication remain independently uncertified. Changes are kept on an isolated PR until merge authorization.
