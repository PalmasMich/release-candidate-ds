# Release Candidate DS — Cagliari Vertical Slice Design

## Goal

Build **Release Candidate** as a Nintendo DS ROM hack/decomp project on top of `pret/pokeplatinum`, developing the game in player-facing order and completing Cagliari before expanding to later cities.

The first meaningful milestone is a vertical slice that feels like Release Candidate from boot: custom title/branding, customized intro/protagonist, Cagliari as the opening location, original dialogue/events, and the choice among three Release Candidate starters. The first Cagliari gym/deploy follows as the completion of the Cagliari chapter.

## Technical baseline

- Platform: Nintendo DS (`.nds`).
- Base project: `pret/pokeplatinum`.
- Baseline upstream commit: `3a85029d78d42a809125076e1cf2752f15739adb` (2026-09-09).
- Base ROM target: Pokémon Platinum EN-US Rev 1.
- Stock Rev 1 SHA-1: `0862ec35b24de5c7e2dcb88c9eea0873110d755c`.
- Fork: `PalmasMich/release-candidate-ds`.
- Development branch: `feature/cagliari-vertical-slice`.
- `main` remains untouched until a reviewed, verified PR is explicitly approved for merge.

## Distribution and repository policy

The public repository must never publish or commit a complete `.nds` ROM. CI may create a ROM ephemerally in the runner only to prove that the source builds; the ROM must not be uploaded as an artifact.

Public distribution will use a patch derived from a known clean Rev 1 base. For Nintendo DS size constraints, the preferred patch format is `xdelta3` (`.xdelta`), not IPS. Any future CI artifact upload must be restricted to patch/documentation outputs and must never contain the full ROM or archives that may contain it.

Original Release Candidate graphics, text, scripts, maps, and other project-owned assets can live in the repository. Existing Pokémon assets are treated as inherited base-project material and should be progressively replaced where they are prominent to give Release Candidate its own identity.

## Development order

Work proceeds in the order the player experiences it:

1. **Foundation** — reproducible Platinum build, copyright-safe CI, project policy tests.
2. **Title and opening identity** — `RELEASE CANDIDATE` title screen and opening branding.
3. **Protagonist** — male protagonist visual based on the approved Release Candidate character direction, including the field sprite variants needed by the opening slice.
4. **Cagliari shell** — repurpose the Twinleaf opening flow into Cagliari, replacing place-facing copy/events first and then the map visuals/geometry needed for the intended environment.
5. **Cagliari narrative** — original NPCs, dialogue and opening events built around the software-development/consulting parody.
6. **Starter selection** — replace Turtwig/Chimchar/Piplup in the starter-selection flow with the three Release Candidate starter species and their original art/data.
7. **Cagliari chapter completion** — first challenge/gym and first deploy.

Later cities (Milano, India, Japan, Cupertino, etc.) are out of scope until Cagliari is coherent and playable end-to-end.

## Known integration points in pokeplatinum

### Title screen

- `src/applications/title_screen.c`
- `res/graphics/title_screen/logo.png`
- `res/graphics/title_screen/logo.NSCR`
- `res/graphics/title_screen/meson.build`

The title application already separates 2D logo/background layers from the 3D Giratina presentation, so the first identity pass can replace the prominent logo before deciding how much of the stock 3D sequence to retain.

### Opening

- `src/game_opening/ov77_021D25B0.c`
- other files under `src/game_opening/`
- `src/main.c` enqueues `gOpeningCutsceneAppTemplate`.

### Protagonist

Primary male overworld sprite source:

- `res/graphics/field_sprites/player/player_m.png`

Additional male variants in the same directory (bike, fishing, holding Poké Ball, Pokétch, save, surf, etc.) are updated only when they become reachable in our playable slice. YAGNI: do not redraw late-game-only variants during the Cagliari milestone.

### Opening city / Cagliari

The existing opening location provides a stable event/script scaffold:

- `res/field/scripts/scripts_twinleaf_town.s`
- `res/field/events/events_twinleaf_town.json`
- Twinleaf player-house scripts/events as needed by the opening flow.

We keep internal upstream identifiers such as `TWINLEAF_TOWN` initially when renaming them would create broad churn with no player-visible benefit. Player-facing place names, text, events and eventually map assets become Cagliari.

### Starter selection

- `src/choose_starter/choose_starter_app.c`

The app currently defines exactly three options via `SPECIES_TURTWIG`, `SPECIES_CHIMCHAR`, and `SPECIES_PIPLUP`. The Release Candidate starter task replaces both the species data/assets and these option bindings; changing only the constants is not considered complete.

## Cagliari creative direction

Cagliari is the true beginning of Release Candidate, not a renamed Twinleaf. It should feel Mediterranean and recognizable without requiring a photorealistic replica. The visual language can borrow recognizable cues—warm stone, sea/coast references, compact streets, local vegetation—while keeping the readability and scale of a DS-era Pokémon map.

The opening humor establishes the game's recurring metaphor: product/software work is the adventure. Requirements, deploys, UAT, incidents, stakeholders and change requests become the equivalent of quests, badges and league progression.

## First vertical-slice success criteria

A player on an Android DS emulator can:

- boot a Release Candidate-branded `.nds` built from the project;
- start a new game without relying on a pre-existing Platinum save;
- see the customized protagonist in the opening flow;
- enter an opening location presented as Cagliari with Release Candidate dialogue/events;
- reach the three-starter selection and see/select the three project starters;
- save and reload the game normally.

The repository/CI simultaneously proves:

- source build succeeds;
- no `.nds` is tracked;
- CI does not upload a full ROM;
- `main` is not modified until explicit merge approval.

## Testing strategy

Use three levels of verification:

1. **Static policy tests** for repository/CI safety and known integration bindings.
2. **Build verification** with `make rom` for modified branches; stock `main` may additionally verify the canonical Rev 1 SHA-1.
3. **Emulator UAT** on Android for boot, new game, movement, events, starter selection, saving and loading. A successful build alone is not reported as successful gameplay.

Graphics changes require visual UAT; code tests cannot establish that a title/logo, protagonist sprite or map composition looks correct.
