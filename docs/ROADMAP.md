# Roadmap

This file tracks remaining work only.

## Next Ticket

Ticket ID: Sprint 5 - Ticket 5.3

Objective:

- Formalize quality evaluation for restored images.

Expected outputs:

- Per-image quality classification.
- Failure case list.
- Artifact summary.
- Recommendation for whether to continue to broader batch validation.

Success criteria:

- Each restored image is marked acceptable, marginal, or failed.
- Known artifact patterns are documented.
- Required detector/mask/inpainting improvements are identified.

## Remaining Work

1. Quality evaluation for the first 10 restored images.
2. Improve batch runtime by keeping models loaded across images.
3. Expand validation beyond the first 10 images.
4. Decide whether LaMa quality is sufficient or whether MAT/SDXL should be benchmarked.
5. Add production `POST /restore`.
6. Move validated providers from playground into `app/`.
7. Add n8n integration.
8. Add deployment automation scripts:
   - `scripts/setup_windows.ps1`
   - `scripts/verify_install.py`
9. Add Docker deployment support.
10. Review validation image rights/privacy before public release.
11. Decide whether to purge old generated artifacts and large model blobs from history in a future maintenance task.
