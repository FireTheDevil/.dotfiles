# Windows + WSL2 development setup

This repository manages my Windows host and Ubuntu-on-WSL2 development setup.
The `home/` tree mirrors the WSL home directory. WezTerm runs on Windows, while
Pi and Herdr run in WSL. My macOS configuration is not yet documented.

The tracked configuration is sanitized. It excludes secrets, personal identity,
private server addresses, authentication stores, and private repository URLs.

## Install in WSL

Prerequisites:

- Git and Python 3
- Pi 1.4.0 installed, including the four example extension source files
- A Windows-side WezTerm installation for the separate manual step

Clone the repository to a permanent location, then inspect and apply the plan:

```sh
git clone <repository-url> ~/dotfiles
cd ~/dotfiles
./dot plan
./dot apply
./dot check
```

`dot apply` shows the plan and asks for confirmation. Use `./dot apply --yes` only
for an intentional noninteractive installation. It creates an individual symlink
for each file below `home/`; it does not replace whole directories.

Run `./dot unlink` to remove installer-owned links. The command removes a link only
when it is recorded in `~/.local/state/dotfiles/state.json` and still points to the
recorded source. It retains source checkouts and directories. Use `--yes` to skip
the unlink confirmation.

## Safety model

- `dot plan` and `dot check` are read-only.
- `dot apply` never overwrites an existing file or a different symlink.
- A pre-existing correct symlink is accepted but is not claimed as installer-owned.
- Existing Git checkouts must have the exact origin and a clean worktree. The
  installer can move a clean checkout to its pinned revision; a dirty or unexpected
  checkout blocks the operation.
- A failed new clone is removed. Managed checkouts live below
  `~/.local/share/dotfiles/sources/`.
- State writes are atomic. Each newly created link is recorded before the installer
  continues to the next link.

The source manifest is [`sources.json`](sources.json). It pins questionnaire,
`pi-skill-toggle`, the four Pi examples, and the configured `pi-pstack-herdsman`
package. [`pi-packages.json`](pi-packages.json) retains wider package provenance.
The installer does not start Pi or install npm packages.

The four Pi examples link to the installed
`@earendil-works/pi-coding-agent` 1.4.0 release. If those files are absent,
`dot plan` reports a blocked prerequisite instead of creating broken links.
Questionnaire and `pi-skill-toggle` use sparse, pinned public Git checkouts.
`pi-pstack-herdsman` remains a pinned Pi Git package in settings and is reconciled
by Pi itself.

## Windows step

The installer does not write across the WSL/Windows boundary. Copy
[`windows/.wezterm.lua`](windows/.wezterm.lua) to
`%USERPROFILE%\.wezterm.lua` on Windows. It targets the `Ubuntu` WSL distro and
uses `pwsh.exe`, with Monaspace Xenon and JetBrains Mono font preferences.

## Local and private configuration

Copy the examples in `templates/` outside the repository and add identity and
private settings there. The localhost model endpoint is an intentional substitute;
configure the real endpoint and `LMSTUDIO_API_KEY` privately. MCP and telemetry are
disabled. Git attribution uses a generic invalid-domain address unless local
environment variables override it.

The npm manifest and lock are stored in `home/.pi/agent/npm/`. No package install
or lifecycle script is run by `dot`; review `allowScripts` before separate use.

See the [inventory](inventory.md), [tool dependencies](dependencies/tools.md),
[Pi package provenance](pi-packages.json), and [skills](skills.json).

## Verification status

The normalized layout and `dot` installer were implemented without running any
installer command or test. Historical checks for the earlier manual snapshot are
recorded in the inventory and do not validate the new installer.

## Safe maintenance

Run `python3 scripts/check-private-data` before sharing. It inspects Git candidates,
prints only rule names and relative paths, and never uploads content. It is a
heuristic, not a privacy guarantee. For a local literal scan, pass
`--deny-file /path/outside/repo` with one private literal per line. Never add that
file to Git. Manual review remains required.

There is intentionally no raw export command. Update individual allowlisted files,
review the candidate content, then run the privacy check. Never copy whole config
roots, symlink targets, authentication stores, or environment files.

Nix scaffolding remains omitted. No Nix installation, evaluation, or activation was
attempted.
