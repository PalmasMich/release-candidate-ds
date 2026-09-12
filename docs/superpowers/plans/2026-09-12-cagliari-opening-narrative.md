# Cagliari Opening Narrative Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the first minutes of a new game feel unmistakably like Release Candidate by rewriting the Platinum onboarding, the first home interactions, and the first Cagliari NPC copy in Italian while preserving the existing opening flow.

**Architecture:** Keep all Platinum scripts, IDs, warps and sequence logic intact; change only player-facing text banks and protect the new narrative with source-level JSON tests. Rowan remains a temporary visual placeholder but is reframed as the Delivery Manager / onboarding character until custom visual assets are integrated in a later plan.

**Tech Stack:** pokeplatinum text JSON resources, Python 3 `unittest`, GitHub Actions, `make rom` build verification.

**Spec:** `docs/superpowers/specs/2026-09-12-release-candidate-ds-cagliari-design.md`

## Global Constraints

- Work only on `feature/cagliari-vertical-slice`.
- New Release Candidate dialogue is written in Italian.
- Internal Platinum identifiers remain unchanged unless a player-facing requirement demands otherwise.
- Do not modify `main`.
- Never commit or upload a complete `.nds` ROM.
- Every behavior change follows RED → GREEN and the latest commit must pass policy tests plus the full modified-ROM build before this plan is considered complete.

---

### Task 1: Rewrite the new-game onboarding as Release Candidate project onboarding

**Files:**
- Create: `tests/release_candidate/test_cagliari_opening_text.py`
- Modify: `res/text/rowan_intro.json`

**Interfaces:**
- Consumes: existing Rowan intro message IDs and the unchanged new-game sequence.
- Produces: Italian Release Candidate onboarding copy without changing script flow.

- [ ] **Step 1: Write failing intro-copy tests**

Create `tests/release_candidate/test_cagliari_opening_text.py` with a JSON helper and assertions for these exact messages:

```python
import json
import unittest
from pathlib import Path


def load_messages(path):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return {message["id"]: message["en_US"] for message in payload["messages"]}


class CagliariOpeningTextTests(unittest.TestCase):
    def test_intro_establishes_release_candidate_onboarding(self):
        messages = load_messages("res/text/rowan_intro.json")
        self.assertEqual(
            messages["RowanIntro_Text_HelloThere"],
            [
                "Ciao!\n",
                "Benvenuto in Release Candidate.\r",
                "Sei stato assegnato a un progetto\n",
                "già avviato.\r",
            ],
        )
        self.assertEqual(
            messages["RowanIntro_Text_MyNameRowan"],
            [
                "Io coordino il delivery.\r",
                "Qui mi chiamano il Manager.\r",
                "I requisiti sono quasi definitivi.\n",
                "Quasi.\r",
                "Prima di partire, facciamo un breve\n",
                "allineamento.\r",
            ],
        )

    def test_intro_sends_player_to_cagliari_and_uat(self):
        messages = load_messages("res/text/rowan_intro.json")
        self.assertEqual(
            messages["RowanIntro_Text_EndDialogue"],
            [
                "Perfetto, {STRVAR_1 3, 0, 0}.\n",
                "Il progetto è ufficialmente partito.\r",
                "Prima tappa: Cagliari.\r",
                "Raccogli requisiti, gestisci le\n",
                "change request e prepara il deploy.\r",
                "Buon lavoro. Ci vediamo in UAT.\r",
            ],
        )


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the policy test workflow and verify RED**

Expected: `test_intro_establishes_release_candidate_onboarding` and `test_intro_sends_player_to_cagliari_and_uat` fail because `rowan_intro.json` still contains stock Platinum copy.

- [ ] **Step 3: Replace only the required Rowan messages**

Update `RowanIntro_Text_HelloThere`, `RowanIntro_Text_MyNameRowan`, `RowanIntro_Text_AdventureInfo0`, `RowanIntro_Text_AdventureInfo2`, `RowanIntro_Text_AboutYourself`, `RowanIntro_Text_GenderDialogue`, `RowanIntro_Text_NameDialogue`, and `RowanIntro_Text_EndDialogue`. Use:

```json
"RowanIntro_Text_AdventureInfo0": [
  "Il tuo obiettivo è semplice:\n",
  "portare il progetto in produzione."
]
```

```json
"RowanIntro_Text_AdventureInfo2": [
  "Ogni deploy apre nuove strade.\n",
  "Ogni change request ne chiude due."
]
```

```json
"RowanIntro_Text_AboutYourself": [
  "Prima dell’onboarding, dimmi qualcosa\n",
  "su di te.\r"
]
```

```json
"RowanIntro_Text_GenderDialogue": [
  "Sei un ragazzo?\n",
  "O una ragazza?\r"
]
```

```json
"RowanIntro_Text_NameDialogue": "Come ti chiami?\r"
```

Do not alter control-help messages or intro application code in this task.

- [ ] **Step 4: Verify GREEN**

Expected: all tests under `tests/release_candidate` pass.

- [ ] **Step 5: Commit**

Commit message: `feat: rewrite new-game intro as project onboarding`.

---

### Task 2: Reframe the first home interactions without changing story logic

**Files:**
- Modify: `tests/release_candidate/test_cagliari_opening_text.py`
- Modify: `res/text/twinleaf_town_player_house_1f.json`

**Interfaces:**
- Consumes: existing player-house message IDs and events.
- Produces: first-home dialogue that matches the Release Candidate tone while preserving all event triggers.

- [ ] **Step 1: Add failing assertions**

Assert:

```python
self.assertEqual(
    messages["TwinleafTownPlayerHouse1F_Text_RivalAlreadyLeft"],
    [
        "Mamma: {STRVAR_1 3, 0, 0}!\r",
        "{STRVAR_1 3, 1, 0} è già uscito.\r",
        "Ha detto che c’è un allineamento\n",
        "urgente. Come sempre.\r",
    ],
)
```

and:

```python
self.assertEqual(
    messages["TwinleafTownPlayerHouse1F_Text_DontGoIntoTallGrass"],
    [
        "Mamma: Ah, {STRVAR_1 3, 0, 0}!\r",
        "Non entrare nell’erba alta senza\n",
        "una creatura con te.\r",
        "E non fare deploy il venerdì.\n",
        "Per sicurezza.\r",
    ],
)
```

- [ ] **Step 2: Verify RED**

Expected: both assertions fail against stock English player-house text.

- [ ] **Step 3: Replace only those two message payloads**

Do not change their IDs, scripts, events, flags or warp logic.

- [ ] **Step 4: Verify GREEN**

Expected: all Release Candidate tests pass.

- [ ] **Step 5: Commit**

Commit message: `feat: add Release Candidate home dialogue`.

---

### Task 3: Give the first Cagliari NPCs the project-parody voice

**Files:**
- Modify: `tests/release_candidate/test_cagliari_opening_text.py`
- Modify: `res/text/twinleaf_town.json`

**Interfaces:**
- Consumes: existing non-critical Twinleaf NPC message IDs.
- Produces: three optional NPC interactions that establish the recurring requirements/deploy/change-request humor.

- [ ] **Step 1: Add failing assertions**

Assert these exact values:

```python
self.assertEqual(
    messages["TwinleafTown_Text_EveryoneGoesOnAdventures"],
    [
        "Qui tutti partono con un MVP...\n",
        "e tornano con quattordici change request."
    ],
)
self.assertEqual(
    messages["TwinleafTown_Text_TechnologyBlowsMeAway"],
    [
        "La tecnologia è incredibile!\r",
        "Ora puoi rompere produzione\n",
        "da qualunque parte del mondo."
    ],
)
self.assertEqual(
    messages["TwinleafTown_Text_HelpingPutTogetherPokedex"],
    [
        "Stai raccogliendo requisiti?\r",
        "Segnati tutto. Quello che oggi è\n",
        "implicito domani sarà bloccante."
    ],
)
```

- [ ] **Step 2: Verify RED**

Expected: all three assertions fail against the current messages.

- [ ] **Step 3: Replace only those three NPC messages**

Keep `TwinleafTown_Text_MapSign` and the global `LocationNames_Text_TwinleafTown` Cagliari changes already implemented.

- [ ] **Step 4: Verify GREEN**

Expected: every test under `tests/release_candidate` passes.

- [ ] **Step 5: Commit**

Commit message: `feat: add Cagliari project-parody NPC dialogue`.

---

### Task 4: Verify the opening narrative checkpoint

**Files:**
- No new source files.

**Interfaces:**
- Consumes: Tasks 1–3.
- Produces: a buildable text-complete opening narrative checkpoint for the later visual/starter plans.

- [ ] **Step 1: Run/observe the complete policy suite**

Expected: all Release Candidate tests pass; no `.nds` is tracked and no artifact-upload workflow is introduced.

- [ ] **Step 2: Run/observe the full modified-ROM build**

Expected: GitHub Actions `build` completes successfully using `make rom` on the latest commit.

- [ ] **Step 3: Confirm no ROM artifacts**

Expected: the workflow run exposes zero uploaded artifacts.

- [ ] **Step 4: Keep PR #1 draft and unmerged**

Do not merge to `main`; continue the Cagliari v0.1 work on `feature/cagliari-vertical-slice`.
