# Snapshot inventory and sanitization

Only the individual sources listed below were copied or reconstructed. The `home/`
tree now mirrors their deployment paths; there are no whole-root copies. Public Pi
examples, `questionnaire`, and `pi-skill-toggle` remain external and are declared in
`sources.json` rather than copied into this snapshot.

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

The installer creates only individual WSL home-file links. It records only links it
creates, refuses existing nonmatching targets, and retains checkouts during unlink.
The Windows WezTerm copy remains a manual step.

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
- Settings omit device/changelog state and private local project references;
  telemetry is disabled. Missing enabled skills are not silently turned into working
  dependencies. The installer links four Pi 1.4.0 examples and `questionnaire` into
  Pi's extension directory, where normal extension discovery can load them.
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
runtime-tested. Nix scaffolding is deferred; no `flake.lock` was fabricated.

## Additional explicit source allowlist

External code is not part of the snapshot allowlist. Its public repository,
revision, source path, and integration limit are recorded in `sources.json` and
`pi-packages.json`.

| Snapshot candidate | Source relative to home |
| --- | --- |
| `home/.pi/agent/extensions/git-commit-attribution.ts` | `.pi/agent/extensions/git-commit-attribution.ts` |
| `home/.pi/agent/extensions/herdr-agent-state.ts` | `.pi/agent/extensions/herdr-agent-state.ts` |
| `home/.pi/agent/skills/asd-ste-100-with-adhd/LICENSE` | `.pi/agent/skills/asd-ste-100-with-adhd/LICENSE` |
| `home/.pi/agent/skills/asd-ste-100-with-adhd/SKILL.md` | `.pi/agent/skills/asd-ste-100-with-adhd/SKILL.md` |
| `home/.pi/agent/skills/asd-ste-100-with-adhd/examples/before-after.md` | `.pi/agent/skills/asd-ste-100-with-adhd/examples/before-after.md` |
| `home/.pi/agent/skills/asd-ste-100-with-adhd/references/writing-rules.md` | `.pi/agent/skills/asd-ste-100-with-adhd/references/writing-rules.md` |
| `home/.pi/agent/skills/install-anti-slop/SKILL.md` | `.pi/agent/skills/install-anti-slop/SKILL.md` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/index.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/index.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/rules/no-manual-effect-error-tag.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/rules/no-manual-effect-error-tag.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/rules/no-manual-tag-comparison.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/rules/no-manual-tag-comparison.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/rules/no-manual-tagged-construction.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/rules/no-manual-tagged-construction.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/rules/no-service-constructor-imports.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/rules/no-service-constructor-imports.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/rules/prefer-effect-match.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/rules/prefer-effect-match.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/shared/tagged-values.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/shared/tagged-values.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/index.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/index.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-array-filter-map.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-array-filter-map.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-chained-type-assertions.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-chained-type-assertions.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-conditional-empty-object-spread.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-conditional-empty-object-spread.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-known-value-widening.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-known-value-widening.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-module-mocking.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-module-mocking.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-object-parameters.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-object-parameters.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-reduce-accumulator-copy.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-reduce-accumulator-copy.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-reflect-apply.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-reflect-apply.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-reflect-get.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-reflect-get.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-runtime-typeof.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-runtime-typeof.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-shape-in-symbol-names.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-shape-in-symbol-names.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-unknown-parameters.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-unknown-parameters.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-unknown-returns.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-unknown-returns.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-unknown-type-aliases.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-unknown-type-aliases.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-unsafe-dictionary-type.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-unsafe-dictionary-type.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-widen-then-assert.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-widen-then-assert.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/require-readable-spacing.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/require-readable-spacing.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/require-safety-comment-for-type-assertion.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/require-safety-comment-for-type-assertion.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/array-method.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/array-method.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/dictionary-types.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/dictionary-types.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/function-parameters.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/function-parameters.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/lexical-type-parameters.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/lexical-type-parameters.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/reflect-method.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/reflect-method.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/scope.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/scope.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/type-alias-resolution.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/type-alias-resolution.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/LICENSE` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/LICENSE` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/UPSTREAM.md` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/UPSTREAM.md` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/padding-line-ast.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/padding-line-ast.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/padding-line-between-statements.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/padding-line-between-statements.ts` |
| `home/.pi/agent/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/padding-line-options.d.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/padding-line-options.d.ts` |
| `home/.pi/agent/skills/install-anti-slop/references/update.md` | `.pi/agent/skills/install-anti-slop/references/update.md` |
| `home/.pi/agent/skills/install-anti-slop/scripts/install.mjs` | `.pi/agent/skills/install-anti-slop/scripts/install.mjs` |
| `home/.pi/agent/skills/qa/SKILL.md` | `.pi/agent/skills/qa/SKILL.md` |
| `home/.pi/agent/skills/strict-tdd/SKILL.md` | `.pi/agent/skills/strict-tdd/SKILL.md` |
| `home/.pi/agent/skills/strict-tdd/mocking.md` | `.pi/agent/skills/strict-tdd/mocking.md` |
| `home/.pi/agent/skills/strict-tdd/tests.md` | `.pi/agent/skills/strict-tdd/tests.md` |
| `home/.pi/agent/skills/thermo-nuclear-code-quality-review/SKILL.md` | `.pi/agent/skills/thermo-nuclear-code-quality-review/SKILL.md` |
| `home/.pi/agent/skills/typesafe-ai/LICENSE` | `.pi/agent/skills/typesafe-ai/LICENSE` |
| `home/.pi/agent/skills/typesafe-ai/SKILL.md` | `.pi/agent/skills/typesafe-ai/SKILL.md` |
| `preserved/disabled-subagent/index.ts` | `.pi/agent/extensions/subagent/index.ts` |
| `preserved/disabled-subagent/agents.ts` | `.pi/agent/extensions/subagent/agents.ts` |
| `preserved/disabled-subagent/config.json` | `.pi/agent/extensions/subagent/config.json` |
| `preserved/disabled-subagent/README.md` | `.pi/agent/extensions/subagent/README.md` |

The modified disabled subagent implementation is preserved outside discovery; no
agent Markdown definitions or workflow presets were copied. It is not safe to
reactivate without compatibility and headless approval review. Its README preserves
historical instructions, not a deployment recommendation.

Local skill availability does not demonstrate recent use. Preserve these local
sources with their support files and licenses rather than guessing that they are
obsolete. The explicitly excluded strict-tdd skill stays excluded. Shared-tree
skills remain external with honest missing-revision/activity gaps in `skills.json`.
Herdr's extension is managed output and may be regenerated by its own tooling; its
portable runtime code is preserved, not host OS terminal configuration.

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
- Repository settings load `pi-pstack-herdsman` from the clean pinned GitHub
  package. Live Pi continues to use its local development checkout, whose 37
  uncommitted paths are not included. Public HEAD declares a Pi peer range below
  1.4.0, so a fresh deployment must verify compatibility.

These examples are not a general security boundary: `permission-gate` matches
only `bash`, and `protected-paths` matches only `write` and `edit`.

## Current verification status

No `dot` command, installer test, syntax check, privacy check, or deployment was run
after layout normalization and installer implementation. The executable was not
applied to this machine. The sections below are historical evidence for the earlier
manual snapshot only.

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
