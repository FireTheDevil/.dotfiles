# Live Pi workflow — 2026-11-01

This is a sanitized record of the live setup, not a migration plan. No live
packages, skills, or instructions were changed for this snapshot.

## Runtime and extension ownership

Pi is 1.4.0 and Node is 24.22.1. The npm manifest and lock record the live
dependencies; [package provenance](../pi-packages.json) lists their versions.
Herdsman explicitly loads `dist/index.js`, its orchestration `SKILL.md`, and
`skills/agent-definitions/SKILL.md`. These skills belong to the npm package;
do not copy or independently pin them in the public skill lock.

Questionnaire and pi-skill-toggle still match their recorded source revisions.
Live Pi loads these from local checkouts; the installer uses normalized managed
checkouts. The four safety examples remain Pi 1.4.0 sources. Their legacy tool-name
matching is not a general security boundary for Code Mode or Codex tools.

Live pstack uses clean revision `efc173dac343cd1fd9bf11bcc01af6907ecd0c33`, also
present on the locally recorded `origin/update/pstack-upstream-0.15.34` branch.
The snapshot pins this same revision rather than the older master revision.
Remote availability was not revalidated. Its declared requirements are Node >=24,
Pi >=1.1.0 <1.4.0, and Herdsman >=0.25.1 <0.30.0. The observed Pi 1.4.0 and
Herdsman 0.36.3 combination is outside those peer ranges. The metadata is retained
honestly: this repository records the live combination, not a repaired upstream
manifest or a compatibility certification.

Private telemetry remains external. Its live source revision is recorded in
package provenance, but its package entry, endpoint, and content-capture settings
are not enabled in the snapshot. MCP, identity, model endpoints, credentials,
device IDs, and other intentional privacy transformations remain unchanged.

## Notes and context continuity

`@howaboua/pi-notes-compaction` 0.0.13 owns notes/history tools, checkpoint policy,
local storage, sharing, and context windows. PCC 4.0.7 supplies optional integration
and the selected provider compaction method; Pi owns session lifecycle.

The live preferences are captured in
`home/.pi/agent/notes-compaction/settings.json`:

- Active for all models; normal compaction and ranked history search enabled.
- Note-save markers and subagent context sharing enabled.
- Unrestricted new-window requests and idle rollover set to 715 minutes.
- Task-boundary reminder set to 0; the stored model whitelist is retained even
  though all-model activation makes it inactive.

The PCC snapshot also retains its live compaction fields, including the 715-minute
idle value, but these legacy fields are not the sole Notes configuration. Existing
Notes settings take precedence over first-use migration from PCC. Notebook journals
are on and checkpoint cleanup is `never`.

The live extension-provided policy requires a successful checkpoint before
`new_context`. Keep one concise task note, record decisions and next steps, and use
history for details rather than copying the conversation. Save notes at meaningful
milestones and before handoff or rollover. This policy belongs to the extension;
do not duplicate its changing implementation prompt in global AGENTS.md.

Only preferences are stored here. Notes databases, journals, checkpoints, session
transcripts, remote-delivery state, and caches remain excluded.

## Skill ownership

Installed does not mean enabled for every session. Skill-toggle and runtime
selection can limit discovery. The 32 public skills in `skills-lock.json` still
match their installed content hashes; no content update or source repinning was
needed for this refresh.

| Skill group | Live owner and snapshot treatment |
| --- | --- |
| 28 locked skills under `~/.agents/skills` | skills.sh/global directories; retain the existing lock. The Pi browser-use entry is a symlink into this tree. |
| `install-anti-slop`, `qa`, `thermo-nuclear-code-quality-review`, `typesafe-ai` | Separate directories under `~/.pi/agent/skills`; their content matches the lock. Keep this live ownership documented. The optional installer refuses these copies instead of relocating or replacing them. |
| `asd-ste100-with-adhd` | Local `myskills` repository, `skills/asd-ste100-with-adhd`, exposed through a Pi symlink. Snapshot only LICENSE, SKILL.md, examples/before-after.md, and references/writing-rules.md. The previous `asd-ste-100-with-adhd` snapshot name is retired. |
| `repo-setup` | Same local `myskills` repository, `skills/repo-setup`; explicitly selected through a local absolute path in live settings. Not vendored and not installed by dot. Restore from its owner and configure the local path privately. |
| `tufte-viz`, `wiki` | Local global skill directories; wiki also has a Pi symlink. No source entry exists in the local skills.sh lock. Record them as externally owned, not reproducibly pinned; do not invent a public source. |
| `strict-tdd` | Local Pi skill, explicitly disabled in live settings. Preserve the exclusion; do not add it to the restoration lock. |
| `agents`, `agent-definitions` | Herdsman npm package; selected by its package settings. |

The local `myskills` checkout was clean at
`8a56d85b11f8e752e15949ea695ccd9f522b7446`; no remote was configured. Its local
source and restoration responsibility are separate from this snapshot. Runtime
`.pi` data beneath that checkout is not skill source and is not copied.

The current communication skill includes Grice's Maxims and the live activation
and clarity instructions. Global AGENTS.md already matches live workflow policy
apart from deliberate identity/path sanitization, so it is unchanged.

`code-review` and `handoff` retain their actual upstream content. The audit's
possible adaptations were recommendations, not live changes: this documentation
refresh does not silently implement them. Pi's higher-priority asynchronous-agent
and Notes instructions continue to govern their use.

## Prompt and deployment boundaries

The live package-review prompt is `/pi-package-updates`, stored in
`home/.pi/agent/prompts/pi-package-updates.md`. It reviews Pi and installed
extensions using their own release notes, supports a component-name scope, and
does not install updates. It replaces the old `/package-updates-info` snapshot.

The optional installer layout is not the live ownership layout. Read-only
`dot check` can therefore fail on existing files without indicating a runtime
problem. Do not run apply merely to make the check green. This refresh does not
replace local sources, alter skill ownership, or certify a fresh-machine restore.
