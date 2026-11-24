# Roadmap

This document covers Phase 2: the work that turns ten working kits into a self-improving, composable system. Phase 1 — the ten native Spanish kits, the documentation and the reference deliverables — is complete.

Scope is intentionally narrow. Each initiative below has a concrete output, an acceptance criterion and an open issue. Anything that does not serve those three is out of scope for Phase 2.

---

## 1. Recursive self-improvement loop for `kit-skill-creator`

**Status:** proposed · **Issue:** `[Architecture] Build automated self-improvement loop for kit-skill-creator (evals + auto-refinement)`

Today `kit-skill-creator` generates a skill from a described process. It cannot tell whether the skill it produced actually works. The goal is a closed loop:

```
  ┌──────────────────────────────────────────────────────────────┐
  │                                                              │
  ▼                                                              │
generate ──► execute on synthetic cases ──► evaluate ──► refactor
  │              (fixtures)                 (rubric)      (patch)
  │                                                              │
  └──────────────────── version + regression suite ◄────────────┘
```

### 1.1 Execution harness

A skill must be runnable without a human in the loop.

- **Fixture format.** Each skill declares synthetic inputs in `evals/fixtures/<case>.json`: a business profile, a URL, a CSV, an invoice set. Fixtures are small, versioned and contain no real personal data.
- **Runner.** A Code Mode / shell runner that copies the fixture into a temporary project, invokes the skill headlessly, and captures: files produced, tool calls, wall-clock time, token cost and errors.
- **Determinism budget.** Skills that call the network are allowed to vary; the harness records inputs and diffs outputs rather than asserting byte equality. Deterministic skills (HTML generation from fixed input) assert on structure, not pixels.

**Acceptance:** a single command runs all fixtures for one skill and emits a machine-readable `report.json` with pass/fail per case.

### 1.2 Evaluation

Pass/fail alone is not enough; the output has to be judged.

- **Output contract.** Every skill declares what it must produce: required sections, minimum content, forbidden content. For example, an audit report must contain a global score, at least three findings with fixes, and a prioritised plan; it must not invent prices or client names.
- **Rubric scoring.** A second model pass scores each deliverable 1–5 on contract compliance, specificity (no generic filler), factual grounding (nothing invented beyond the fixture) and formatting integrity.
- **Regression gate.** A skill version cannot ship if its mean rubric score drops below the previous version, or if any contract check fails.

**Acceptance:** a skill is rejected automatically when it violates its own output contract, with a human-readable diff of what failed.

### 1.3 Automatic refactoring

The refactor step proposes a patch to the skill file, not a rewrite.

- **Diagnosis.** Map each failure to a section of the skill: missing trigger phrase, ambiguous step, absent output requirement, over-broad instruction.
- **Patch generation.** Produce a minimal diff to the Markdown skill, preserving frontmatter and structure.
- **Validation.** Re-run the harness on the patched skill. Keep the patch only if the score improves and no previously passing case regresses.
- **Human gate.** Patches are proposed as pull requests, never auto-merged. The loop is autonomous in evaluation, conservative in mutation.

**Acceptance:** for a deliberately broken skill (one missing step), the loop identifies the failing case, patches the file and restores a passing score in a single run.

### 1.4 Non-goals

- Fine-tuning models.
- Scraping real client data for evaluation.
- Optimising for token cost before output quality is stable.

---

## 2. Multi-skill orchestration pipelines

**Status:** proposed · **Issue:** `[Feature] Multi-skill orchestration pipeline (Prospecting -> SEO Audit -> Business Audit PDF)`

The kits currently run in isolation. Real agency work is a chain: find prospects, qualify them, audit them, package the audit as a client-facing PDF.

### Reference pipeline

```
kit-prospeccion            kit-auditoria-seo          kit-auditoria-negocio
      │                          │                            │
 find N businesses  ──►   score each site   ──►   full audit + PDF export
 with weak presence        (0–100)                per qualified prospect
      │                          │                            │
      └────────── shared run state / artifact contracts ──────┘
```

### 2.1 Artifact contracts

Each skill already produces a file; orchestration requires a stable machine-readable summary alongside it.

- Every kit emits a `<deliverable>.meta.json` next to its output: `{ skill, version, inputs_hash, score, findings_count, artifacts[], duration_ms }`.
- The orchestrator reads only `meta.json` to decide the next step. It never parses HTML.
- Contracts are versioned; a breaking change bumps the kit's minor version.

### 2.2 Orchestrator

A thin skill (`orquestador`) that:

1. Takes a pipeline definition — a short YAML list of steps with conditions.
2. Resolves which kits are installed.
3. Runs steps sequentially, passing the previous step's artifacts forward.
4. Stops on a failed contract and reports which step broke, with the artifact that caused it.
5. Writes one run log: inputs, per-step status, scores, total cost.

**Acceptance:** the reference pipeline runs end to end on ten fictional businesses and produces ten business-audit PDFs, with a run log that shows which prospects were filtered out and why.

### 2.3 Constraints

- No hidden state: every hand-off is a file on disk.
- Resumable: a failed run restarts from the last successful step.
- Cost ceiling per pipeline run, enforced by the orchestrator.

---

## 3. Unified CLI installer

**Status:** proposed · **Issue:** `[DX] Unified CLI installer to deploy individual skills directly into ~/.claude/skills/`

Today, using a kit means cloning the whole repository and opening a kit folder. That is fine for exploration and wrong for daily use: a user who wants only the SEO audit should not carry nine other kits.

### Target interface

```bash
# list what is available
npx claude-skill-factory list

# install one skill into ~/.claude/skills/
npx claude-skill-factory add auditoria-seo

# install several, pinned
npx claude-skill-factory add web-scrolling auditoria-negocio --version 1.2.0

# inspect before writing anything
npx claude-skill-factory add auditoria-seo --dry-run

# remove
npx claude-skill-factory remove auditoria-seo
```

### Requirements

- **No global install required.** Run through `npx`; no daemon, no background process.
- **Idempotent.** Re-running `add` on an installed skill reports "already installed" and exits 0, unless `--force`.
- **Non-destructive.** Never overwrite a user-modified skill without `--force`; print a diff first.
- **Transparent.** Show the exact destination path before writing. Support `--dest` for non-default locations.
- **Verifiable.** Verify a checksum against the published manifest; refuse to install on mismatch.
- **Offline-friendly.** Cache the manifest; fail with a clear message rather than a stack trace.

**Acceptance:** a clean machine can install `auditoria-seo` with one command, use it in Claude Code immediately, and uninstall it without leaving files behind.

---

## Milestones

| Milestone | Contents | Exit criterion |
|---|---|---|
| **M1 — Contracts** | `meta.json` in every kit, output-contract spec, fixture format | All ten kits emit valid metadata on a reference run |
| **M2 — Evals** | Harness, runner, rubric scoring, `report.json` | `kit-web-scrolling` and `kit-auditoria-negocio` fully covered |
| **M3 — Refactor loop** | Diagnosis, patch generation, regression gate, PR automation | Broken-skill fixture repaired automatically |
| **M4 — Orchestration** | Orchestrator skill, pipeline YAML, run log, cost ceiling | Reference pipeline produces ten PDFs end to end |
| **M5 — Installer** | `npx` CLI, manifest, checksums, dry-run, uninstall | One-command install verified on macOS, Linux and Windows |

Sequencing is deliberate: contracts before evaluation, evaluation before mutation, mutation before orchestration. An orchestrator built on unstable output contracts would multiply the instability by the number of steps.

---

## How to follow along

- Each initiative has a tracking issue labelled `enhancement`.
- Design notes live in the issue thread; accepted decisions are folded back into this document.
- Contributions are welcome at any milestone — read [`CONTRIBUTING.md`](./CONTRIBUTING.md) first.
