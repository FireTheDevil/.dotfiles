# Windows + WSL2 development setup

This repository documents my Windows host and Ubuntu-on-WSL2 development setup.
My macOS configuration is not yet documented. Unless explicitly marked Windows-host,
configuration targets WSL Ubuntu. WezTerm runs on Windows; Pi and Herdr run in WSL.

Sanitized, manually reviewed configuration snapshot, **not an installer or a
complete machine backup**. Nothing here has been activated. No secrets, personal
identity, private server addresses or private repository URLs are required here.

## Manual use

`.wezterm.lua` configures WezTerm on Windows.
Copy it manually to `%USERPROFILE%\.wezterm.lua` on Windows, not the WSL home.
It targets the `Ubuntu` WSL distro and uses PowerShell (`pwsh.exe`), with
Monaspace Xenon and JetBrains Mono font preferences. Windows runtime behavior
has not been verified here.

Review each file before copying it. `config/shell/{zshrc,bashrc,profile}` correspond
to the home-directory dotfiles. `config/git/gitconfig` corresponds to `~/.gitconfig`;
`config/npm/npmrc` and `config/bun/bunfig.toml` to `~/.npmrc` and `~/.bunfig.toml`.
`config/{herdr,hunk,uv}/` go beneath `~/.config/`; the uv filename is `uv.toml`.
`config/pi/` corresponds to `~/.pi/agent/`. There is no automatic symlink/deploy step.
Shared skills and the agent-definition package must be restored privately as documented.
The Pi launcher and commit hook need executable permissions when manually deployed.

The four unmodified Pi examples are not copied into this repository. Settings load
them directly from the installed `@earendil-works/pi-coding-agent` 1.4.0 release.
Update those versioned paths when Pi changes. The questionnaire is also external:
clone [FireTheDevil/pi-questionnaire](https://github.com/FireTheDevil/pi-questionnaire)
at the revision in `pi-packages.json` to `~/projects/pi-questionnaire`.

`pi-skill-toggle` is referenced from
[dmmulroy/.dotfiles](https://github.com/dmmulroy/.dotfiles/tree/main/home/.pi/agent/extensions/pi-skill-toggle)
instead of being copied. Pi cannot install that nested package from the repository
URL directly. Clone the pinned repository, then add its nested directory as a local
Pi package. Snapshot settings load `pi-pstack-herdsman` from its pinned public
GitHub source. The live configuration can continue to use its local development
checkout. Its declared Pi peer range excludes Pi 1.4.0, so verify compatibility
before a fresh installation. See the inventory for exact revisions and limits.

Copy the examples in `templates/` outside the repository and fill in identity and
private settings there. The localhost model endpoint is an intentional substitute;
configure your actual endpoint and `LMSTUDIO_API_KEY` privately. MCP is disabled and
has no authorization header. Telemetry is disabled; configure it privately if wanted.
Git attribution uses a generic invalid-domain address unless local environment
variables override it. The local Git include deliberately supplies no user identity.

See [inventory](inventory.md), [tool dependencies](dependencies/tools.md),
[Pi package provenance](pi-packages.json), and [skills](skills.json).
`pi-npm/` preserves the existing npm manifests, not installed dependencies. No
package install or lifecycle script has been run. Review `allowScripts` before use.

## Safe maintenance

Run `python3 scripts/check-private-data` before sharing; it inspects Git candidates
(including untracked, nonignored files), prints only rule names and relative file
paths, and never uploads content. It is a heuristic, not a privacy guarantee.
Manual review remains required, particularly prose and metadata. You may pass
`--deny-file /path/outside/repo` containing one private literal per line for a local
literal scan; matching literals are never printed. Do not put that file in Git.

There is intentionally no raw `export-config` command. Updating this snapshot means
selecting individual allowlisted files, inspecting them read-only, manually applying
sanitization, and validating candidates before sharing. Never copy whole config roots,
symlink targets, authentication stores or environment files. Never substitute a
placeholder into an executable path and then enable it.

Nix scaffolding and `flake.lock` are omitted: this is a coherent manual snapshot,
not an unverified package/deployment design. No Nix installation, evaluation or
activation was attempted. Fresh-machine startup, package resolution, local services,
model availability and cross-version extension compatibility remain unverified.
