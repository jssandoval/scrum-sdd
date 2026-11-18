# SSDD — Scrum Spec-Driven Development

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](#requirements)
[![Agents](https://img.shields.io/badge/agents-Claude%20Code%20%7C%20Codex%20%7C%20OpenCode%20%7C%20Antigravity%20%7C%20Pi-6e5494.svg)](#supported-agents)

**English** | [Español](README.es.md)

> AI coding agents invent requirements, lose traceability between specs and code, and drift past phases nobody approved. SSDD stops that: every phase ends at a gate only a human can open, and the chain **requirement → acceptance criterion → user story → test** is validated automatically, not by trusting the agent's word.

SSDD takes a project from idea to production by combining **Scrum**, **Spec-Driven Development**, and the **DERCAS** document (ISO/IEC/IEEE 29148). It works phase by phase, inside the agent you already use — no new IDE, no new chat window.

## Why SSDD

If you've tried a spec-driven workflow with an AI agent before, you've probably hit one of these:

- The agent "approves itself" and moves on to the next phase.
- Requirements, acceptance criteria, and tests drift apart silently — nobody notices until QA or production.
- Reverting a bad architectural decision means either living with it or nuking the whole history.

SSDD's answer to each:

| Problem | SSDD mechanism |
| --- | --- |
| Agent self-approves | `/ssdd-aprobar` and `/ssdd-aceptar` only run when a human types them, with `--por "Name"` attached |
| Spec/code drift | `/ssdd-trazabilidad` fails loudly if a requirement has no criterion, a story has no requirement, or a criterion has no test |
| Can't undo a phase safely | `/ssdd-revertir` archives the phase with a verifiable copy in `docs/historico-fases/` and revokes downstream approvals — without touching `src/`, `tests/`, or other phases' docs |
| Editing an approved doc goes unnoticed | Approval becomes invalid automatically the moment the approved document changes |

## How it works

```
idea ──▶ discovery ──▶ requirements ──▶ design ──▶ architecture ──▶ backlog ──▶ setup
                 (each phase ends at a human-only approval gate)
                                │
                                ▼
          per story:  implement ──▶ audit (fresh session) ──▶ accept ──▶ release ──▶ operate
```

No phase starts until the previous one is approved. No story is accepted until it's been audited in a clean session — the person who wrote the code doesn't audit it.

## Quick start

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/jssandoval/scrum-sdd/main/install-remote.sh | sh

# Windows / PowerShell
irm https://raw.githubusercontent.com/jssandoval/scrum-sdd/main/install-remote.ps1 | iex
```

Then, inside your project, in a new terminal:

```bash
ssdd init
ssdd doctor
```

Restart your agent so it picks up the new skills, then:

```
/ssdd-descubrir A workshop app for scheduling car repair appointments over WhatsApp
```

Review what landed in `docs/01-descubrimiento/` and approve it:

```
/ssdd-aprobar descubrimiento --por "Your Name"
```

That's the whole loop: run a skill, review what it generated, approve or send it back. Repeat through the remaining phases (full command reference below).

> Installers download a tagged release (`v0.4.7`), not the changing `main` branch. You can read the script before running it. No Node.js, npm, uv, pip, or Homebrew required.

## What's included

- **10 phase skills** — from discovery to operation.
- **5 control skills** — approve, accept, check status, validate traceability, revert.
- **Approval gates** — no phase starts if the previous one isn't approved; approval invalidates itself if the approved document is edited afterward.
- **Traceability validation** — fails if a requirement has no criterion, a story has no requirement, or a criterion has no test.
- **Three lanes** sized to the change: `complete` (new product), `feature` (addition to an existing project), `hotfix` (urgent fix).
- **Source-document ingestion** — start from manuals, forms, or spreadsheets (PDF/Word/Excel/Markdown/images) instead of a blank idea; SSDD builds a documentary traceability matrix with source IDs and SHA-256-verified locations.

## Requirements

- Python **3.9+** (used by the framework's own validators).
- A supported agent: Claude Code, Codex, OpenCode, Antigravity, or Pi.
- **No Node.js, npm, uv, pip, or Homebrew needed.**
- Git is recommended for working on the project, not required to install SSDD.

Detailed guide: [Installation and usage, step by step](docs/GUIA-INSTALACION-Y-USO.md) *(Spanish)*.

## Installation

Official repo: **https://github.com/jssandoval/scrum-sdd**

### From GitHub (recommended)

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/jssandoval/scrum-sdd/main/install-remote.sh | sh

# Windows / PowerShell
irm https://raw.githubusercontent.com/jssandoval/scrum-sdd/main/install-remote.ps1 | iex
```

```bash
ssdd init
ssdd doctor
```

### From a downloaded ZIP

1. Unzip and open a terminal **inside the `scrum-sdd` folder**.
2. Run the installer for your OS:

   ```bash
   sh install-cli.sh            # macOS / Linux
   ```
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\install-cli.ps1   # Windows
   ```
3. Open a **new terminal** and, in any project:

   ```bash
   cd path/to/my-project
   ssdd init
   ssdd doctor
   ```

`ssdd init` sets up every compatible agent by default. For one specific agent: `ssdd init --agent claude` (also `codex`, `opencode`, `antigravity`, `pi`). On an existing project it never overwrites `docs/estado.json`, `CLAUDE.md`, your source documents, specs, or code.

### CLI commands

| Command | Does |
| --- | --- |
| `ssdd init [path]` | Set up a new or existing project |
| `ssdd doctor` | Check environment and detect agents |
| `ssdd version` | Show installed version |
| `ssdd update [path]` | Sync managed resources into a project |

To update the global CLI itself, re-run `install-cli.sh` / `install-cli.ps1` from a newer downloaded version — `ssdd update` does not do this.

### What gets created in your project

```
my-project/
├── CLAUDE.md             # points to AGENTS.md
├── .claude/skills/       # the 15 skills (Claude Code)
├── .agents/skills/       # the same skills (Codex, OpenCode, Antigravity, Pi)
├── .opencode/commands/   # slash-command wrappers for OpenCode
├── .pi/prompts/          # slash-command wrappers for Pi
├── .framework/           # templates, scripts, version
├── docs/
│   ├── 00-fuentes/       # source documents you provide (manuals, forms...)
│   ├── estado.json       # gate and story status
│   ├── 01-descubrimiento/ … 07-operacion/
├── specs/                # one spec per story
├── src/
└── tests/
```

## Commands reference

### Phase skills

| Skill | Phase | Produces | Approved with |
| --- | --- | --- | --- |
| `/ssdd-descubrir <idea>` | 0. Discovery | Vision, Lean Canvas, hypotheses | `/ssdd-aprobar descubrimiento` |
| `/ssdd-dercas` | 1. Requirements | `DERCAS.md` with functional/non-functional requirements, business rules, Gherkin acceptance criteria | `/ssdd-aprobar requisitos` |
| `/ssdd-diseno` | 2. Design | BPMN, navigation, design system, screens | `/ssdd-aprobar diseno` |
| `/ssdd-arquitectura` | 3. Architecture | C4 diagrams, data model, OpenAPI, ADRs | `/ssdd-aprobar arquitectura` |
| `/ssdd-backlog` | 4. Planning | Backlog, Definition of Ready/Done, Sprint 1 | `/ssdd-aprobar backlog` |
| `/ssdd-setup` | 5. Environment | `AGENTS.md`, linters, Docker, CI | `/ssdd-aprobar setup` |
| `/ssdd-implementar HU-XXX` | 6. Execution | Story spec, tests, code | Pull Request review |
| `/ssdd-auditar HU-XXX` | 7. QA & security | Audit report, E2E tests | `/ssdd-aceptar HU-XXX` |
| `/ssdd-release` | 8. Deployment | Dockerfile, pipeline, runbook | CI/CD approval |
| `/ssdd-operar` | 9. Operation | SLOs, telemetry, alerts | Review & retrospective |

### Control skills

| Skill | For |
| --- | --- |
| `/ssdd-estado` | See which phases are approved, each story's status, and the next step |
| `/ssdd-aprobar <phase> --por "<name>"` | Record human approval of a phase |
| `/ssdd-aceptar HU-XXX --por "<name>"` | Record story acceptance after UAT |
| `/ssdd-trazabilidad [HU-XXX]` | Validate the requirement → criterion → story → test chain |
| `/ssdd-revertir <phase> --por "Name" --motivo "Reason"` | Archive an approved phase and revoke its approval and downstream ones |

`/ssdd-aprobar` and `/ssdd-aceptar` only run when a human types them in chat. In Claude Code and Pi the agent cannot invoke them on its own; in the others it depends on `AGENTS.md` instructions. **This is not an identity guarantee** — anyone with terminal or repo access can alter the state file directly.

### `$` vs `/`

Examples above use `/`; in Codex, type `$` instead (`$ssdd-descubrir`, `$ssdd-aprobar`).

## Lanes

Not every change needs all ten phases.

| Lane | When | Flow |
| --- | --- | --- |
| `complete` | New product | All ten phases, in order |
| `feature` | New capability on an installed project | `/ssdd-dercas` → `/ssdd-backlog` → `/ssdd-implementar` → `/ssdd-auditar` |
| `hotfix` | Urgent fix | `/ssdd-implementar` (with a regression test) → `/ssdd-auditar` |

```
/ssdd-implementar HU-042 --carril hotfix
```

### Adopting SSDD in an existing project

1. Run `install.sh` against the project.
2. Run `/ssdd-dercas` to document what's already built.
3. Approve under the feature lane:
   ```
   /ssdd-aprobar requisitos --por "Your Name" --carril feature
   /ssdd-setup
   /ssdd-aprobar setup --por "Your Name" --carril feature
   ```
4. Work every new change under `feature` or `hotfix`.

## Conventions

Scripts validate anything with a predictable shape — keep these identifiers exact:

| Element | Format | Where |
| --- | --- | --- |
| Functional requirement | `### RF-001 Title` + `**Prioridad:** Must` | DERCAS |
| Non-functional requirement | `### RNF-001 Title` | DERCAS |
| Business rule | `### RN-001 Title` | DERCAS |
| Acceptance criterion | `### CA-001 (RF-001) Title` | DERCAS |
| User story | `### HU-001 Title` + `**Requisitos:** RF-001` | Product backlog |
| Test | Test name/comment containing `CA-001`, with real assertions, and the suite actually runs | `tests/` or `src/` |

- Three-digit IDs, never reused. A dropped requirement is marked `Won't`, never deleted.
- MoSCoW priority: `Must`, `Should`, `Could`, `Won't`.
- No sub-headings inside an ID's section.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| A skill replies BLOCKED | A prior phase isn't approved | `/ssdd-estado` to see which, then `/ssdd-aprobar` |
| An approved phase shows as modified | The document was edited after approval | Review the change, then `/ssdd-aprobar` again |
| `/ssdd-trazabilidad` fails | A requirement with no criterion, a story with no requirement, or a criterion with no test | Fix per the report's pointer |
| `/ssdd-aceptar` rejects the story | It never went through `/ssdd-auditar` | Audit first, in a fresh session |
| Skills don't show up after `/` | Agent was opened before installing | Restart the agent |
| `/ssdd-release` replies BLOCKED | There are unaccepted stories | `/ssdd-estado`, then accept what's pending |

## Continuous integration

`/ssdd-setup` copies a GitHub Actions workflow to `.github/workflows/ci-cd.yml`. Every Pull Request validates traceability, lint, tests, and dependencies. Deploying to production requires accepted stories plus a manual approval on the `production` environment. You still need to wire in real deploy scripts and smoke tests — if they're missing, CI fails rather than faking a deployment.

## Updating

```bash
cd scrum-sdd && git pull
./install.sh /path/to/my-project
```

Reinstalling updates skills, templates, and scripts. It never touches `docs/`, `specs/`, `AGENTS.md`, or your code.

From older installs (v0.4.7 and earlier), re-run the remote installer above, then inside the project:

```bash
ssdd update --agent all
ssdd version
ssdd doctor
```

`ssdd update` preserves `docs/estado.json`, DERCAS, source documentation, and code.

## Supported agents

The installer prepares the project for all five. The skills themselves are identical — only where each agent looks for them and how it invokes them differs.

| Agent | Reads skills from | Project rules | Invocation |
| --- | --- | --- | --- |
| Claude Code | `.claude/skills/` | `CLAUDE.md` → `AGENTS.md` | `/ssdd-aprobar ...` |
| Codex | `.agents/skills/` | `AGENTS.md` | `$ssdd-aprobar ...` |
| OpenCode | `.agents/skills/` | `AGENTS.md` | `/ssdd-aprobar ...` |
| Antigravity / `agy` | `.agents/skills/` | `AGENTS.md` | `/ssdd-aprobar ...` |
| Pi | `.agents/skills/` | `AGENTS.md` | `/ssdd-aprobar ...` or `/skill:aprobar ...` |

- You can switch agents mid-project — state lives in `docs/estado.json`, not in the agent.
- For audits, always use a fresh session if your agent doesn't support clean-context subagents.
- In Pi, project skills/templates only load after marking the project as trusted.

## Source documents: manuals, forms, and matrices

You can start from existing documents instead of a blank idea. Drop PDFs, Word, Excel, Markdown, or images into `docs/00-fuentes/` (`manuales/`, `lineamientos/`, `formularios/`, `matrices/`, `requerimientos/`, `otros/`), run `/ssdd-descubrir`, review the inventory and contradiction analysis, resolve conflicts, and approve. `/ssdd-dercas` builds the documentary traceability matrix with source IDs and verifiable locations (path, size, SHA-256).

The inventory step is automatic; **interpreting content is the agent's job**. An unreadable file is marked pending — nothing gets invented. Changing sources after approval invalidates the corresponding discovery/requirements approvals.

Guide: [How to use source documents](docs/USAR-DOCUMENTOS-FUENTE.md) *(Spanish)*. Full example: [Customer registration with contradictory manual and form](examples/registro-clientes/README.md).

## Stack choice stays with the developer

During `/ssdd-arquitectura`, the agent recommends options and asks the developer to choose **frontend, backend, interoperability, persistence, and infrastructure** before producing the final ADR. The decision is recorded in `ADR-001-stack-tecnologico.md` and approved along with the phase.

## Reverting an approved phase

```text
/ssdd-revertir arquitectura --por "Name" --motivo "Change the chosen technology"
```

This saves a copy of the phase's state and documents under `docs/historico-fases/` and revokes approval for that phase and everything after it. Original documents, code, and stories are never deleted — it's a workflow revert, not a `git reset`.

## Repo structure

```
scrum-sdd/
├── LICENSE
├── VERSION
├── install.sh
├── constitution/     # AGENTS.md template
├── skills/           # 10 phase skills + 4 control skills
├── templates/        # DERCAS, backlog, story spec, ADR, audit
├── scripts/          # gate.py (gates), trace.py (traceability)
├── ci/               # GitHub Actions workflow template
└── examples/         # end-to-end sample project
```

## Project status

Version 0.4.7. Includes evidence validation and the framework's own automated tests. All five agents are still pending full integration testing on real-world projects — issues and PRs welcome.

## Verifying the framework itself

```bash
python3 -m unittest discover -s tests_framework -v
```

The traceability validator does a basic structural check — **it does not by itself prove** a test verifies a requirement. Always run the real test suite, review its meaning during `/ssdd-auditar`, and block the PR if it fails.

## A note on the approval gate

`/ssdd-aprobar` and `/ssdd-aceptar` require an explicit human invocation in chat, with `--por`. There's no additional authentication layer — this is a control on the agent's workflow, not a barrier against someone with direct file or terminal access.

## License

[MIT](LICENSE). Use, modify, and distribute freely, commercial use included, as long as the copyright notice stays. The installer copies the license into `.framework/LICENSE` in every project to satisfy that.
