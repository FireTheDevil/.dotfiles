# Snapshot inventory and sanitization

Only the individual sources listed below were copied or reconstructed. Source
locations are home-relative; there are no whole-root copies. Public Pi examples,
`questionnaire`, and `pi-skill-toggle` are referenced externally rather than
copied into this snapshot.

| Snapshot candidate | Source relative to home |
| --- | --- |
| `.wezterm.lua` | WezTerm configuration for Windows; deploy to `%USERPROFILE%\.wezterm.lua` |
| `config/shell/bashrc` | `.bashrc` |
| `config/shell/profile` | `.profile` |
| `config/npm/npmrc` | `.npmrc` |
| `config/bun/bunfig.toml` | `.bunfig.toml` |
| `config/herdr/config.toml` | `.config/herdr/config.toml` |
| `config/hunk/config.toml` | `.config/hunk/config.toml` |
| `config/uv/uv.toml` | `.config/uv/uv.toml` |
| `config/shell/zshrc` | `.zshrc` |
| `config/git/gitconfig` | `.gitconfig` |
| `config/pi/AGENTS.md` | `.pi/agent/AGENTS.md` |
| `config/pi/REALTIME-SYSTEM-PROMPT.md` | `.pi/agent/REALTIME-SYSTEM-PROMPT.md` |
| `config/pi/pi-codex-conversion.json` | `.pi/agent/pi-codex-conversion.json` |
| `config/pi/pi-codex-guardian.json` | `.pi/agent/pi-codex-guardian.json` |
| `config/pi/pi-pretty.json` | `.pi/agent/pi-pretty.json` |
| `config/pi/web-search.json` | `.pi/agent/web-search.json` |
| `config/pi/pi-herdsman/config.json` | `.pi/agent/pi-herdsman/config.json` |
| `config/pi/prompts/restate.md` | `.pi/agent/prompts/restate.md` |
| `config/pi/prompts/package-updates-info.md` | `.pi/agent/prompts/package-updates-info.md` |
| `config/pi/bin/pi` | `.pi/agent/bin/pi` |
| `config/pi/settings.json` | `.pi/agent/settings.json` |
| `config/pi/models.json` | `.pi/agent/models.json` |
| `config/pi/mcp.json` | `.pi/agent/mcp.json` |
| `config/pi/pi-fff.json` | `.pi/agent/pi-fff.json` |
| `config/pi/git-hooks/commit-msg` | `.pi/agent/git-hooks/commit-msg` |
| `pi-npm/package.json` | `.pi/agent/npm/package.json` |
| `pi-npm/package-lock.json` | `.pi/agent/npm/package-lock.json` |

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
  dependencies. Four Pi examples load from the installed 1.4.0 package, and
  `questionnaire` points to a separately cloned public repository.
- FFF database path overrides were removed in favor of package defaults, avoiding
  unsupported literal environment substitutions. No databases are included.
- Commit attribution remains functional, with an intentionally generic invalid-domain
  default and optional runtime identity overrides. No credential or personal identity
  is embedded in executable paths.
- npm manifests retain existing constraints, registry resolutions, integrity hashes
  and lifecycle allowlist. Packages were not installed or updated.

## Excluded classes

No authentication, runtime, history, cache, backups, machine trust, host OS terminal
configuration other than the explicitly included `.wezterm.lua`, obsolete integration packages or integration config/dependency
references are included. External agent definitions belong to their own source
repository and are not duplicated. Configuration roots, install releases and
`node_modules` are not vendored. The ignore file adds defensive exclusions; it is
not itself an export allowlist.

## Maintenance allowlist

The table above plus the explicit custom-source list below is the snapshot allowlist.
For an update, read each corresponding source without printing private values,
apply the transformations above in a separate destination, review all candidates,
then run syntax/privacy/whitespace checks. Existing sanitized files must never be
blindly overwritten from live sources. There is deliberately no automatic exporter.

## Outstanding compatibility gaps

The snapshot is not activated. Models and package releases are only observed source
configuration, not proof of future availability. The source model schema typo
`reaasoning` is retained and requires checking against the intended Pi version.
Global hook forwarding and terminal integration are preserved but not runtime-tested.
Nix scaffolding is deferred; no `flake.lock` was fabricated.

## Additional explicit source allowlist

External code is not part of the snapshot allowlist. Its public repository,
revision, source path, and integration limit are recorded in `pi-packages.json`.

| Snapshot candidate | Source relative to home |
| --- | --- |
| `config/pi/extensions/git-commit-attribution.ts` | `.pi/agent/extensions/git-commit-attribution.ts` |
| `config/pi/extensions/herdr-agent-state.ts` | `.pi/agent/extensions/herdr-agent-state.ts` |
| `config/pi/skills/asd-ste-100-with-adhd/LICENSE` | `.pi/agent/skills/asd-ste-100-with-adhd/LICENSE` |
| `config/pi/skills/asd-ste-100-with-adhd/SKILL.md` | `.pi/agent/skills/asd-ste-100-with-adhd/SKILL.md` |
| `config/pi/skills/asd-ste-100-with-adhd/examples/before-after.md` | `.pi/agent/skills/asd-ste-100-with-adhd/examples/before-after.md` |
| `config/pi/skills/asd-ste-100-with-adhd/references/writing-rules.md` | `.pi/agent/skills/asd-ste-100-with-adhd/references/writing-rules.md` |
| `config/pi/skills/install-anti-slop/SKILL.md` | `.pi/agent/skills/install-anti-slop/SKILL.md` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/effect/index.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/index.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/effect/rules/no-manual-effect-error-tag.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/rules/no-manual-effect-error-tag.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/effect/rules/no-manual-tag-comparison.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/rules/no-manual-tag-comparison.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/effect/rules/no-manual-tagged-construction.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/rules/no-manual-tagged-construction.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/effect/rules/no-service-constructor-imports.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/rules/no-service-constructor-imports.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/effect/rules/prefer-effect-match.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/rules/prefer-effect-match.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/effect/shared/tagged-values.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/effect/shared/tagged-values.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/index.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/index.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/no-array-filter-map.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-array-filter-map.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/no-chained-type-assertions.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-chained-type-assertions.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/no-conditional-empty-object-spread.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-conditional-empty-object-spread.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/no-known-value-widening.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-known-value-widening.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/no-module-mocking.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-module-mocking.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/no-object-parameters.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-object-parameters.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/no-reduce-accumulator-copy.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-reduce-accumulator-copy.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/no-reflect-apply.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-reflect-apply.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/no-reflect-get.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-reflect-get.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/no-runtime-typeof.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-runtime-typeof.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/no-shape-in-symbol-names.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-shape-in-symbol-names.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/no-unknown-parameters.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-unknown-parameters.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/no-unknown-returns.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-unknown-returns.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/no-unknown-type-aliases.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-unknown-type-aliases.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/no-unsafe-dictionary-type.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-unsafe-dictionary-type.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/no-widen-then-assert.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/no-widen-then-assert.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/require-readable-spacing.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/require-readable-spacing.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/rules/require-safety-comment-for-type-assertion.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/rules/require-safety-comment-for-type-assertion.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/shared/array-method.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/array-method.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/shared/dictionary-types.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/dictionary-types.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/shared/function-parameters.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/function-parameters.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/shared/lexical-type-parameters.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/lexical-type-parameters.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/shared/reflect-method.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/reflect-method.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/shared/scope.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/scope.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/shared/type-alias-resolution.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/shared/type-alias-resolution.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/LICENSE` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/LICENSE` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/UPSTREAM.md` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/UPSTREAM.md` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/padding-line-ast.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/padding-line-ast.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/padding-line-between-statements.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/padding-line-between-statements.ts` |
| `config/pi/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/padding-line-options.d.ts` | `.pi/agent/skills/install-anti-slop/assets/anti-slop/vendor/eslint-stylistic/padding-line-options.d.ts` |
| `config/pi/skills/install-anti-slop/references/update.md` | `.pi/agent/skills/install-anti-slop/references/update.md` |
| `config/pi/skills/install-anti-slop/scripts/install.mjs` | `.pi/agent/skills/install-anti-slop/scripts/install.mjs` |
| `config/pi/skills/qa/SKILL.md` | `.pi/agent/skills/qa/SKILL.md` |
| `config/pi/skills/strict-tdd/SKILL.md` | `.pi/agent/skills/strict-tdd/SKILL.md` |
| `config/pi/skills/strict-tdd/mocking.md` | `.pi/agent/skills/strict-tdd/mocking.md` |
| `config/pi/skills/strict-tdd/tests.md` | `.pi/agent/skills/strict-tdd/tests.md` |
| `config/pi/skills/thermo-nuclear-code-quality-review/SKILL.md` | `.pi/agent/skills/thermo-nuclear-code-quality-review/SKILL.md` |
| `config/pi/skills/typesafe-ai/LICENSE` | `.pi/agent/skills/typesafe-ai/LICENSE` |
| `config/pi/skills/typesafe-ai/SKILL.md` | `.pi/agent/skills/typesafe-ai/SKILL.md` |
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
  `protected-paths` load from Pi's installed 1.4.0 examples. The removed 1.3.0
  copies are byte-identical to the referenced 1.4.0 files.
- `questionnaire` points to the clean public checkout at
  `~/projects/pi-questionnaire`, pinned in `pi-packages.json`. Its repository
  has no Pi package manifest, so settings use a local file path.
- `pi-skill-toggle` points to current `dmmulroy/.dotfiles` revision
  `29ebc43b8b4afe7a6d667d4c36ad81f775d2c616`. This accepts the upstream
  canonical-realpath deduplication fix. The removed copy matched 20 of 22 files;
  the production fix and its expanded test are the two differences.
- Snapshot settings load `pi-pstack-herdsman` from the clean pinned GitHub
  package. Live Pi continues to use its local development checkout, whose 37
  uncommitted paths are not included. Public HEAD declares a Pi peer range below
  1.4.0, so a fresh deployment must verify compatibility.

These examples are not a general security boundary: `permission-gate` matches
only `bash`, and `protected-paths` matches only `write` and `edit`.

## Verification performed after externalization

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

## Verification performed (original snapshot, before externalization)

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
