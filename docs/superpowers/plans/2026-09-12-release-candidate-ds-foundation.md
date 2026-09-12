# Release Candidate DS Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish a reproducible Pokémon Platinum Rev 1 development baseline with CI that proves modified source builds while preventing full Nintendo DS ROM files from being committed or uploaded.

**Architecture:** Keep `main` as the untouched upstream baseline and execute all work on `feature/cagliari-vertical-slice`. Add a small Python policy test suite as the permanent copyright/distribution guardrail, then replace the upstream fork CI with a Release Candidate-specific workflow that creates `build/pokeplatinum.us.nds` only ephemerally and never uploads it.

**Tech Stack:** GitHub Actions, Python 3 `unittest`, pokeplatinum Make/Meson/Ninja toolchain, `gcc-arm-none-eabi`, Metroskrew.

**Spec:** `docs/superpowers/specs/2026-09-12-release-candidate-ds-cagliari-design.md`

## Global Constraints

- Platform is Nintendo DS (`.nds`).
- Base project is `pret/pokeplatinum` EN-US Rev 1.
- Baseline upstream commit is `3a85029d78d42a809125076e1cf2752f15739adb`.
- Stock Rev 1 SHA-1 is `0862ec35b24de5c7e2dcb88c9eea0873110d755c`.
- Work only on `feature/cagliari-vertical-slice`; do not merge to `main` without explicit user approval.
- Never commit or upload a complete `.nds` ROM.
- CI may create the ROM ephemerally to verify the build and must delete it before job completion.
- No GitHub Actions artifact upload is allowed in this foundation plan.

---

### Task 1: Add repository safety policy with a deliberately failing first run

**Files:**
- Create: `tests/release_candidate/test_repository_policy.py`
- Create: `.github/workflows/release-candidate-policy.yml`

**Interfaces:**
- Consumes: repository checkout and Git metadata.
- Produces: a Python `unittest` suite that fails if a tracked `.nds` exists or any workflow contains `actions/upload-artifact`.

- [ ] **Step 1: Add the failing policy tests**

Create `tests/release_candidate/test_repository_policy.py`:

```python
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"


class RepositoryPolicyTests(unittest.TestCase):
    def test_no_nds_rom_is_tracked(self):
        result = subprocess.run(
            ["git", "ls-files", "*.nds"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        tracked = [line for line in result.stdout.splitlines() if line.strip()]
        self.assertEqual([], tracked, f"Tracked .nds ROM(s): {tracked}")

    def test_workflows_do_not_upload_artifacts(self):
        offenders = []
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            if "actions/upload-artifact" in path.read_text(encoding="utf-8"):
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual([], offenders, f"Artifact-upload workflow(s): {offenders}")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Add a branch policy workflow**

Create `.github/workflows/release-candidate-policy.yml`:

```yaml
name: release-candidate-policy

on:
  push:
    branches:
      - feature/cagliari-vertical-slice
  pull_request:
    branches:
      - main

jobs:
  repository-policy:
    runs-on: ubuntu-24.04
    steps:
      - name: Checkout repository
        uses: actions/checkout@v6
        with:
          fetch-depth: 1

      - name: Run repository policy tests
        run: python3 -m unittest discover -s tests/release_candidate -p 'test_*.py' -v
```

- [ ] **Step 3: Observe RED in GitHub Actions**

Expected result: `test_no_nds_rom_is_tracked` passes, while `test_workflows_do_not_upload_artifacts` fails because the inherited `.github/workflows/build.yml` contains `actions/upload-artifact` for its failure archive.

- [ ] **Step 4: Commit checkpoint**

The remote file writes create commits on `feature/cagliari-vertical-slice`. Do not alter `main`.

---

### Task 2: Replace inherited CI with a Release Candidate-safe ephemeral ROM build

**Files:**
- Modify: `.github/workflows/build.yml`
- Test: `tests/release_candidate/test_repository_policy.py`

**Interfaces:**
- Consumes: pokeplatinum build system and Rev 1 source tree.
- Produces: `build/pokeplatinum.us.nds` temporarily during CI, verifies it exists, verifies the canonical SHA-1 only on stock `main`, and deletes the file before job completion.

- [ ] **Step 1: Replace the inherited workflow**

Set `.github/workflows/build.yml` to:

```yaml
name: release-candidate-build

on:
  push:
    branches:
      - main
      - 'feature/**'
    paths-ignore:
      - '**.md'
  pull_request:
    branches:
      - main
    paths-ignore:
      - '**.md'

env:
  BUILD: /var/tmp/pokeplatinum

jobs:
  build:
    runs-on: ubuntu-24.04
    steps:
      - name: Install software
        run: |
          sudo apt-get update -y
          sudo apt-get install -y --no-install-recommends \
            bison flex g++ gcc-arm-none-eabi git make ninja-build \
            pkg-config python3 wget xz-utils libpng-dev

      - name: Checkout repository
        uses: actions/checkout@v6

      - name: Run repository policy tests
        run: python3 -m unittest discover -s tests/release_candidate -p 'test_*.py' -v

      - name: Install Metroskrew
        run: sudo make skrew

      - name: Configure repository
        run: make configure

      - name: Build ROM ephemerally
        run: make rom

      - name: Verify ROM exists
        run: test -f build/pokeplatinum.us.nds

      - name: Verify stock Rev 1 hash on main
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        run: echo '0862ec35b24de5c7e2dcb88c9eea0873110d755c  build/pokeplatinum.us.nds' | sha1sum -c -

      - name: Remove ROM before job completion
        if: always()
        run: rm -f build/pokeplatinum.us.nds
```

This intentionally removes the inherited xMAP update and failure-archive upload. Neither is required for Release Candidate and the latter conflicts with the no-ROM-artifact policy.

- [ ] **Step 2: Observe GREEN policy**

Run/observe:

```bash
python3 -m unittest discover -s tests/release_candidate -p 'test_*.py' -v
```

Expected: 2 tests pass.

- [ ] **Step 3: Observe GREEN build workflow**

Expected GitHub Actions steps on `feature/cagliari-vertical-slice`:

- repository policy tests pass;
- Metroskrew installs;
- repository configures;
- `make rom` succeeds;
- `build/pokeplatinum.us.nds` exists;
- stock-hash step is skipped on the feature branch;
- ROM deletion step succeeds;
- no artifacts are created.

- [ ] **Step 4: Re-run policy after the build workflow commit**

Expected: `release-candidate-policy` remains green, proving no artifact-upload action was reintroduced.

---

### Task 3: Review foundation branch and open a non-merged PR

**Files:**
- No new source files.
- Review the branch diff against `main`.

**Interfaces:**
- Consumes: Tasks 1–2 and their successful checks.
- Produces: a reviewable PR for the DS foundation. It must stay unmerged until explicit user approval.

- [ ] **Step 1: Verify branch diff scope**

Expected changed paths at this foundation checkpoint:

```text
.github/workflows/build.yml
.github/workflows/release-candidate-policy.yml
docs/superpowers/specs/2026-09-12-release-candidate-ds-cagliari-design.md
docs/superpowers/plans/2026-09-12-release-candidate-ds-foundation.md
tests/release_candidate/test_repository_policy.py
```

No `.nds` file may appear.

- [ ] **Step 2: Verify latest CI status**

Both `release-candidate-policy` and `release-candidate-build` must be successful on the latest branch commit before claiming the foundation is complete.

- [ ] **Step 3: Open PR**

Title:

```text
DS foundation: safe Platinum build pipeline
```

Body must state:

- baseline: pokeplatinum EN-US Rev 1;
- no `.nds` is committed or uploaded;
- CI builds the ROM ephemerally and removes it;
- future distribution will use a patch;
- this PR contains infrastructure/design only, not Cagliari gameplay yet.

- [ ] **Step 4: Do not merge**

Leave the PR open for user review/approval. The next implementation plan begins the player-facing title/opening work on top of this verified foundation.
