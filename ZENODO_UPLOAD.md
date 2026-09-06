# Zenodo Release Notes

This repository is prepared for archiving through the GitHub-Zenodo integration.

## Before the GitHub Release

1. Confirm the repository is clean:
   ```bash
   git status
   ```
2. Confirm that no figure or large journal-export files are tracked:
   ```bash
   git ls-files | grep -E '(^figures/|\.(png|pdf|svg|tif|tiff|eps|zip)$)'
   ```
   This should print nothing.
3. Confirm the author metadata:
   ```bash
   git log --format='%an <%ae>' -5
   ```
   The commits should list Simon Salaj / simonator420 only.
4. Create and push a version tag:
   ```bash
   git tag -a v1.0.1 -m "Version 1.0.1"
   git push origin main --tags
   ```

## Zenodo GitHub Integration

1. Log in to Zenodo.
2. Connect the GitHub account if it is not already connected.
3. Open the Zenodo GitHub page, click **Sync now**, find
   `simonator420/shooting-profiles-nba-euroleague`, and enable the repository.
4. In GitHub, create a new release from tag `v1.0.1`.
5. Wait for Zenodo to ingest the release.
6. Open the new Zenodo record and check the metadata: title, creator, version,
   license, description, and repository link.
7. Copy the version DOI into the manuscript, README citation section, and any
   data availability statement.

## Manual Upload Alternative

If the GitHub integration is not enabled, upload a ZIP archive of the repository
manually as a Zenodo software record. Use:

- Title: `Do Shooting Profiles Travel? Shot Selection, Shot Quality, and Performance Adaptation Between the NBA and EuroLeague`
- Creator: `Simon Salaj`
- Resource type: `Software`
- Version: `v1.0.1`
- License: `MIT`
- Related identifier: `https://github.com/simonator420/shooting-profiles-nba-euroleague`

After publishing, Zenodo assigns a DOI. A published Zenodo record cannot have
its files changed, so check the draft before clicking publish.
