# Snapshot inventory and sanitization

Only the individual sources listed below were copied or reconstructed. The `home/`
tree now mirrors their deployment paths; there are no whole-root copies. Public Pi
examples, `questionnaire`, and `pi-skill-toggle` remain external and are declared in
`sources.json` rather than copied into this snapshot. Public skills are locked in
`skills-lock.json`; only the customized `asd-ste-100-with-adhd` skill is copied.

| Snapshot candidate | Source relative to home |
| --- | --- |
| `windows/.wezterm.lua` | WezTerm configuration for Windows; deploy to `%USERPROFILE%\.wezterm.lua` |
| `home/.bashrc` | `.bashrc` |
| `home/.profile` | `.profile` |
| `home/.npmrc` | `.npmrc` |
| `home/.bunfig.toml` | `.bunfig.toml` |
| `home/.config/herdr/config.toml` | `.config/herdr/config.toml` |
| `home/.config/hunk/config.toml` | `.config/hunk/config.toml` |
| `home/.config/uv/uv.toml` | `.config/uv/uv.toml` |
| `home/.zshrc` | `.zshrc` |
| `home/.gitconfig` | `.gitconfig` |
| `home/.pi/agent/AGENTS.md` | `.pi/agent/AGENTS.md` |
| `home/.pi/agent/REALTIME-SYSTEM-PROMPT.md` | `.pi/agent/REALTIME-SYSTEM-PROMPT.md` |
| `home/.pi/agent/pi-codex-conversion.json` | `.pi/agent/pi-codex-conversion.json` |
| `home/.pi/agent/pi-codex-guardian.json` | `.pi/agent/pi-codex-guardian.json` |
| `home/.pi/agent/pi-pretty.json` | `.pi/agent/pi-pretty.json` |
| `home/.pi/agent/web-search.json` | `.pi/agent/web-search.json` |
| `home/.pi/agent/pi-herdsman/config.json` | `.pi/agent/pi-herdsman/config.json` |
| `home/.pi/agent/prompts/restate.md` | `.pi/agent/prompts/restate.md` |
| `home/.pi/agent/prompts/package-updates-info.md` | `.pi/agent/prompts/package-updates-info.md` |
| `home/.pi/agent/bin/pi` | `.pi/agent/bin/pi` |
| `home/.pi/agent/settings.json` | `.pi/agent/settings.json` |
| `home/.pi/agent/models.json` | `.pi/agent/models.json` |
| `home/.pi/agent/mcp.json` | `.pi/agent/mcp.json` |
| `home/.pi/agent/pi-fff.json` | `.pi/agent/pi-fff.json` |
| `home/.pi/agent/git-hooks/commit-msg` | `.pi/agent/git-hooks/commit-msg` |
| `home/.pi/agent/npm/package.json` | `.pi/agent/npm/package.json` |
| `home/.pi/agent/npm/package-lock.json` | `.pi/agent/npm/package-lock.json` |

## Deployment artifacts

- `dot` is the executable command wrapper.
- `installer/dot.py` implements planning, application, checking, and unlinking with
  the Python standard library.
- `sources.json` pins managed public sources, Pi example paths, package declarations,
  the installer data root, and the ownership-state path.
- `skills-lock.json` pins the public skill repositories, revisions, source paths,
  and content hashes used by the skills.sh installation step.

The installer creates only individual WSL home-file links. It records only links it
creates, refuses existing nonmatching targets, installs missing locked skills globally
for Pi, and retains checkouts and skills during unlink. The Windows WezTerm copy
remains a manual step.

## Deliberate transformations

- Zsh was reconstructed from its useful PATH, Oh My Zsh, Bun, NVM, browser-use and
  Pi terminal settings. Credential retrieval, telemetry identity and private
  environment sourcing were removed. A guarded private local override replaces them.
- Bash keeps its standard behavior; the captured PATH containing 57 host OS
  entries was removed, leaving runtime PATH and portable Bun/local prefixes.
- Git keeps pager and Pi hook integration; personal identity and all credential
  helper sections are excluded. A private local include is supplied instead.
- AGENTS content retains behavioral instructions, with generic user references and
  a nonidentifying absolute file-URL example. It is snapshot content, not stripped.
- Model endpoint is localhost and API key is an environment-variable name. MCP is
  disabled, localhost-only and stripped of authorization headers.
- Settings omit device/changelog state, private local project references, and obsolete
  per-directory skill overrides; telemetry is disabled. The installer links four Pi
  1.4.0 examples and `questionnaire` into Pi's extension directory and installs the
  source-verified skills locked for global Pi discovery.
- FFF database path overrides were removed in favor of package defaults, avoiding
  unsupported literal environment substitutions. No databases are included.
- Commit attribution remains functional, with an intentionally generic invalid-domain
  default and optional runtime identity overrides. No credential or personal identity
  is embedded in executable paths.
- npm manifests retain existing constraints, registry resolutions, integrity hashes
  and lifecycle allowlist. Packages were not installed or updated.

## Excluded classes

No authentication, runtime, history, cache, backups, machine trust, host OS terminal
configuration other than the explicitly included `windows/.wezterm.lua`, obsolete
integration packages, or integration config/dependency references are included.
External agent definitions belong to their own source repository and are not
duplicated. Configuration roots, install releases and `node_modules` are not
vendored. The ignore file adds defensive exclusions; it is not itself an export
allowlist.

## Maintenance allowlist

The table above plus the explicit custom-source list below is the snapshot allowlist.
For an update, read each corresponding source without printing private values,
apply the transformations above in a separate destination, review all candidates,
then run syntax/privacy/whitespace checks. Existing sanitized files must never be
blindly overwritten from live sources. There is deliberately no automatic exporter.

## Outstanding compatibility gaps

The normalized snapshot and installer are not activated. Models and package releases
are only observed source configuration, not proof of future availability. The source
model schema typo `reaasoning` is retained and requires checking against the intended
Pi version. Global hook forwarding and terminal integration are preserved but not
runtime-tested. The skills.sh installation path is also untested. Nix scaffolding is
deferred; no `flake.lock` was fabricated.

## Additional explicit source allowlist

External code is not part of the snapshot allowlist. Its public repository,
revision, source path, and integration limit are recorded in `sources.json`,
`pi-packages.json`, and `skills-lock.json`.

| Snapshot candidate | Source relative to home |
| --- | --- |
| `home/.pi/agent/extensions/git-commit-attribution.ts` | `.pi/agent/extensions/git-commit-attribution.ts` |
| `home/.pi/agent/extensions/herdr-agent-state.ts` | `.pi/agent/extensions/herdr-agent-state.ts` |
| `home/.pi/agent/skills/asd-ste-100-with-adhd/LICENSE` | `.pi/agent/skills/asd-ste-100-with-adhd/LICENSE` |
| `home/.pi/agent/skills/asd-ste-100-with-adhd/SKILL.md` | `.pi/agent/skills/asd-ste-100-with-adhd/SKILL.md` |
| `home/.pi/agent/skills/asd-ste-100-with-adhd/examples/before-after.md` | `.pi/agent/skills/asd-ste-100-with-adhd/examples/before-after.md` |
| `home/.pi/agent/skills/asd-ste-100-with-adhd/references/writing-rules.md` | `.pi/agent/skills/asd-ste-100-with-adhd/references/writing-rules.md` |
| `preserved/disabled-subagent/index.ts` | `.pi/agent/extensions/subagent/index.ts` |
| `preserved/disabled-subagent/agents.ts` | `.pi/agent/extensions/subagent/agents.ts` |
| `preserved/disabled-subagent/config.json` | `.pi/agent/extensions/subagent/config.json` |
| `preserved/disabled-subagent/README.md` | `.pi/agent/extensions/subagent/README.md` |

The modified disabled subagent implementation is preserved outside discovery; no
agent Markdown definitions or workflow presets were copied. It is not safe to
reactivate without compatibility and headless approval review. Its README preserves
historical instructions, not a deployment recommendation.

The customized `asd-ste-100-with-adhd` directory is the only copied skill. Third-party
skills are restored from `skills-lock.json` instead of vendored snapshots. Skills
without verified public source metadata are not inferred or silently added. Herdr's
extension is managed output and may be regenerated by its own tooling; its portable
runtime code is preserved, not host OS terminal configuration.

## External Pi sources

- `confirm-destructive`, `dirty-repo-guard`, `permission-gate`, and
  `protected-paths` are installer-managed links to Pi's installed 1.4.0 examples.
  The removed 1.3.0 copies are byte-identical to the referenced 1.4.0 files.
- The installer sparse-clones `questionnaire` to
  `~/.local/share/dotfiles/sources/pi-questionnaire` and links its extension into
  `~/.pi/agent/extensions`. Its repository has no Pi package manifest.
- The installer sparse-clones `pi-skill-toggle` from `dmmulroy/.dotfiles` revision
  `29ebc43b8b4afe7a6d667d4c36ad81f775d2c616`. This accepts the upstream
  canonical-realpath deduplication fix. The removed copy matched 20 of 22 files;
  the production fix and its expanded test are the two differences.
- `skills-lock.json` records 32 source-verified public skills from 12 GitHub
  repositories. Each entry has a full commit and a skills@1.7.4 content hash. QA is
  pinned to its own historical Matt Pocock commit because the newer shared commit no
  longer contains that directory.
- `dot apply` installs missing locked skills with `skills@1.7.4`, global scope, and
  the Pi target. It refuses modified canonical directories and separate Pi-specific
  copies rather than replacing them. No skills.sh command was run for this change.
- Repository settings load `pi-pstack-herdsman` from the clean pinned GitHub
  package. Live Pi continues to use its local development checkout, whose 37
  uncommitted paths are not included. Public HEAD declares a Pi peer range below
  1.4.0, so a fresh deployment must verify compatibility.

These examples are not a general security boundary: `permission-gate` matches
only `bash`, and `protected-paths` matches only `write` and `edit`.

## Current verification status

No `dot` command, installer behavior test, skills.sh command, or deployment was run
after adding locked skill installation. Locally installed skills and skills.sh state
were not changed. Static checks parsed the installer source and all 15 JSON files,
validated the lock's counts and ordering, passed `git diff HEAD --check`, and found
no private-data matches in 49 candidate files. Read-only provenance work matched all
32 locked skills to the recorded upstream commits and content hashes. The sections
below are historical evidence for the earlier manual snapshot only.

## Historical verification after externalization, before normalization

- Parsed every JSON candidate.
- Loaded all five configured external extension paths with Pi 1.4.0's resource
  loader in an isolated agent directory; no path was missing and no load error occurred.
- Verified the pinned public revisions and all recorded source paths. The four
  installed Pi examples match the files in the Earendil `v1.4.0` Git tag.
- Confirmed that the removed source paths are absent and no stale snapshot path or
  private source placeholder remains for these packages.
- Advanced `pi-skill-toggle` to public revision `29ebc43...`, switched global
  Pi to a clean sparse checkout of that revision, and ran its eight existing tests.
- Confirmed snapshot settings use the pinned pstack GitHub package while global Pi
  still uses the unchanged local development checkout.
- The privacy checker passed 94 candidates with zero findings. All 94 candidates
  also passed trailing-whitespace and final-newline checks.
- No package install, staging, commit, or push was performed during externalization.

## Historical verification of the original snapshot

- Inspected all 116 exact nonignored Git candidates, including untracked files;
  no staged files, commits or remotes were created.
- Parsed all 17 JSON and four TOML candidates. npm root manifest/lock dependencies
  agree; every lockfile resolution uses the public npm registry.
- Bash, Zsh and POSIX shell syntax checks passed for six shell/template files.
- All 61 TypeScript/JavaScript candidates passed Node's TypeScript transform plus
  module syntax parsing without linking, executing extensions, or installing dependencies.
  This is not TypeScript typechecking. Direct `node --check` did not handle these
  typed module sources; the transform/parser check was used instead.
- Ran the four existing pi-skill-toggle test files with Node 24's experimental
  TypeScript transform: seven tests passed. No new unit tests were written.
- Candidate privacy checker and separate source-derived private identity, endpoint,
  device-ID and credential-literal comparisons passed without printing values.
  Public documentation/registry hosts and required third-party license attribution
  remain; they are not the user's identity. An initial substring-only name scan
  matched ordinary expression identifiers; boundary-aware identity checks cleared them.
- No symlinks, agent-definition directories, runtime state or prohibited integration
  configuration/dependency references were present. Ignore rules intentionally name
  excluded files defensively.
- `git diff --check` passed; because files are untracked, every candidate also passed
  an equivalent trailing-whitespace/final-newline check.
- Compared SHA-256 hashes of 107 inspected/copied live source files: unchanged.

Privacy checks are heuristic and source-content comparisons are not a complete
machine-state audit. The original snapshot made no live configuration edits. A
later live Pi example replacement was separate from this repository externalization.
The later upstream-pin update changed only global Pi's `pi-skill-toggle` source;
the live pstack entry remained unchanged. No packages were installed, Nix activated,
or configurations/applications launched. Fresh-machine operation, full TypeScript
typechecking and complete reproducibility remain unverified.
