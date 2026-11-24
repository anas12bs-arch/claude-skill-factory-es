# Contributing

Thanks for considering a contribution. This project exists to give Spanish-speaking builders native Claude Code skills that produce real deliverables, and the fastest way to extend it is for someone who knows a workflow to encode it once.

This guide covers what a contribution must contain, how it is reviewed, and the conventions that keep ten independent kits coherent.

---

## Before you start

- Read [`README.md`](./README.md) for the architecture and the ten existing kits.
- Check open issues and pull requests so you do not duplicate work. If your idea is not covered, open an issue first — a short proposal saves a long review.
- You need [Claude Code](https://docs.claude.com/en/docs/claude-code) to build and test a skill. Nothing else is required.

---

## What counts as a contribution

| Contribution | Accepted | Notes |
|---|---|---|
| A new kit (skill + `CLAUDE.md` + `INSTRUCCIONES.md`) | Yes | The main path. Build it with `kit-skill-creator` |
| A fix to an existing skill's workflow | Yes | Include the failing case that motivated it |
| A new example deliverable | Yes | Fictional data only, no client material |
| Documentation improvements | Yes | English for repository docs, Spanish for kit docs |
| A translation of a kit to another language | Discuss first | This repository is Spanish-first by design |
| A paid course, lead magnet or "make money" funnel | No | Out of scope |

---

## Build a kit with `kit-skill-creator`

The intended workflow is the one the project documents:

1. Open `kits/kit-skill-creator` in Claude Code.
2. Describe the manual process you want to encode, including the input you start from and the file you expect at the end.
3. Let the skill generate the first draft.
4. Run it on a real case. Fix the steps that break. Repeat until the output is something you would hand to a client.
5. Copy the result into a new folder following the contract below.

Generated drafts are a starting point, not a submission. Reviewers look for evidence that the skill survived contact with a real case.

---

## Kit folder contract

```
kits/kit-<slug>/
├── CLAUDE.md                              # onboarding contract, in Spanish
├── INSTRUCCIONES.md                       # human setup guide, in Spanish
├── .claude/
│   └── skills/
│       └── <NN>-<skill-name>.md           # the skill, in Spanish
└── assets/                                # optional: inputs, placeholders
```

### Naming

- Folder: `kit-<slug>` in kebab-case, Spanish where the domain term is Spanish (`kit-auditoria-seo`, not `kit-seo-audit`).
- Skill file: two-digit order prefix plus the skill name (`07-auditoria-negocio-digital.md`). Pick the next free number; do not renumber existing kits.
- The `name` in frontmatter matches the skill name without the numeric prefix.

### `CLAUDE.md`

Must contain, in this order:

1. One-paragraph description of what the kit produces.
2. A **"Comportamiento al iniciar"** section with the exact greeting Claude should give when the folder is opened.
3. A short explanation of what the skill analyses or builds.
4. Constraints, stated as rules. At minimum: never invent business data, prices or testimonials.

Keep it under roughly 60 lines. It is an onboarding contract, not documentation.

### The skill file

Frontmatter is mandatory and is the retrieval surface:

```yaml
---
name: auditoria-seo
description: "Analiza el SEO completo de una web y genera un informe visual… Triggers: 'audita el SEO de', 'por qué no posiciono', 'revisa mi web'."
---
```

Rules for the `description`:

- Write it in Spanish, the way a user speaks, not the way a specification is written.
- Include at least five trigger phrases, including the imperfect ones people actually type.
- State the deliverable, not the topic: "genera un informe HTML con puntuación" beats "experto en SEO".
- Do not keyword-stuff. If a phrase would not be said out loud, remove it.

Rules for the body:

- Procedural, numbered steps: collect inputs → research → analyse → generate → save → present.
- One explicit output contract: file name, format, required sections.
- Hard constraints repeated where they matter: no invented data, no fabricated reviews, no real personal data in examples.
- No secrets, no API keys, no tokens. Credentials belong in a local, git-ignored config, documented in `INSTRUCCIONES.md`.
- Self-contained output wherever possible: a single HTML file with inline CSS and JS beats a folder of dependencies.

### `INSTRUCCIONES.md`

Written for a non-technical Spanish speaker:

1. Requirements (usually just VS Code + the Claude Code extension).
2. How to open the folder.
3. Two or three example prompts.
4. Where the deliverable is saved and how to open it.

---

## Test before you submit

A submission is reviewed on behaviour, so include evidence:

- Run the skill on at least one realistic case. Keep the input and the produced file.
- Put the output in `examples/` only if it is fictional and adds something the existing examples do not. Otherwise describe the result in the pull request.
- Confirm the skill does not invent data when the input is incomplete — it should ask or use visible placeholders.
- Open the generated HTML in a browser and print it to PDF. Layout bugs that only appear in print are the most common defect.
- Check that it works when the user answers in one line and when they answer in five paragraphs.

### Review checklist

Reviewers will check:

- [ ] Folder and file names follow the contract.
- [ ] Frontmatter is valid YAML with a usable `description` and five or more trigger phrases.
- [ ] The workflow is procedural and has an explicit output contract.
- [ ] `CLAUDE.md` includes the onboarding greeting and the no-invented-data rule.
- [ ] `INSTRUCCIONES.md` is in Spanish and usable by a non-technical reader.
- [ ] No secrets, tokens, personal data or real client material anywhere in the diff.
- [ ] The generated deliverable was tested and is attached or described.
- [ ] Repository documentation (if touched) is in English; kit content stays in Spanish.

---

## Language policy

- **Kit content: Spanish.** `CLAUDE.md`, `INSTRUCCIONES.md`, skill files, example prompts and generated deliverables.
- **Repository documentation: English.** `README.md`, `ROADMAP.md`, `CONTRIBUTING.md`, issue titles and pull request descriptions.
- **Code identifiers: English.** CSS classes, JSON keys, function names.
- **Comments in code: either, but consistent within a file.**

This split is intentional. The skills are the product for a Spanish-speaking audience; the repository is the interface for an international open-source review process.

---

## Commits and pull requests

Commits follow a light Conventional Commits style, scoped to the kit:

```
feat(kit-auditoria-seo): add schema.org checks to the audit
fix(kit-web-scrolling): keep hero height on iOS Safari
docs(readme): document the installer proposal
```

Pull requests should contain:

1. **What** changed, in one or two sentences.
2. **Why** — the case that failed or the gap that existed.
3. **How it was tested** — input used, output inspected, browser checked.
4. Screenshots or the generated file when the change affects output.

Keep a pull request to one concern. A new kit plus a refactor of an existing one is two pull requests.

---

## Security and privacy

- Never commit API keys, tokens, `.env` files, `.mcp.json` with real credentials, or local editor settings. The repository `.gitignore` covers the common cases; do not weaken it.
- Example data must be synthetic. If you model a business, invent it and say so in the file's footer.
- If you find a secret in the repository, do not open a public issue with the value. Report it privately to the maintainer and rotate the credential.

---

## License of contributions

By submitting a pull request you agree that your contribution is licensed under the MIT License, the same terms as the rest of the repository. See [`LICENSE`](./LICENSE).

---

## Questions

Open an issue with the `question` label. If you are unsure whether an idea fits, ask before building — the answer is usually yes, with a narrower scope.
