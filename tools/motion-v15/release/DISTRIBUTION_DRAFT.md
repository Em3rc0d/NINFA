# The Duplicate Webhook — Distribution draft

**Status: DRAFT FOR HUMAN APPROVAL. DO NOT UPLOAD OR SCHEDULE.**
**Channel:** Does It Automate? — English only.
**Provenance:** [synthetic, sequential SQLite case](../replay_lab.py).
**Package:** the voiced private review master was delivered directly to the owner, **not committed** to GitHub.

## Suggested YouTube Shorts title

I Simulated a Webhook Twice — SQLite Stored 2 Actions

Alternative: One Event, Two Actions. Here's the SQLite Fix.

## Suggested description

I simulated the same webhook event arriving twice and replayed it through a local SQLite test. Without a UNIQUE event-key constraint, two actions were stored. With the constraint, one was stored and the duplicate was ignored.

This is a **synthetic, sequential local experiment** — not a live webhook provider test or a concurrent-request test.

Reproduce the experiment: https://github.com/Em3rc0d/NINFA/tree/main/tools/motion-v15

#DoesItAutomate #SoftwareEngineering #SQLite #Idempotency #Shorts

## Optional pinned comment

Idempotency stopped a duplicate sequential write in this test. Concurrent delivery needs a different test. Where would you enforce the guard — at the database, service, or both?

## Publishing blockers

- [ ] Owner checks actual YouTube editor visual guides on mobile; possible footer obstruction
- [ ] Owner compares all phrase-based captions against spoken recording
- [ ] Owner approves exact title, description, source disclosure and video
- [ ] An **independent explicit instruction** authorizes uploading/scheduling
- [ ] Separate platform/provider receipt confirms any publishing action

Until every gate is closed, **PUBLISH AUTHORITY = NONE**.
