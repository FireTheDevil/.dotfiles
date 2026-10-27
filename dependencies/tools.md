# Dependencies and portability

This is an inventory, not an installation script or guarantee of version availability.

| Component | Requirement / observed source |
| --- | --- |
| Platform | Windows host with Ubuntu on WSL2; macOS setup is not documented |
| WezTerm (Windows) | Nightly build `20261010-083911-e2a98e1b`; installation method not recorded. Configuration: [`.wezterm.lua`](../.wezterm.lua) |
| Shell | Bash, Zsh; optional Oh My Zsh (`clean` theme, `git` plugin) |
| Shell additions | Optional Bun completion, NVM and browser-use environment; guarded if absent |
| Git | Linux Git; choose identity and credential helper privately |
| Runtime | Node.js/npm for Pi; Bun and uv configuration is retained independently |
| Pi (WSL) | Snapshot records managed coding-agent release `1.3.0`; launcher expects `install/current-version` and a release directory, not bundled here |
| Pi packages | Existing npm lock in `pi-npm/`; see `pi-packages.json` for independent sources |
| Terminal tools | Herdr runs in WSL; Hunk configuration is also preserved. Terminal image/hyperlink settings require compatible terminal support |
| Browser QA | `browser-use` skill/CLI is an independent dependency; see skills provenance |
| Optional services | LM Studio and Obsidian MCP: intentionally localhost examples, MCP disabled; private configuration required |
| Auth | Provider login, API credentials, environment and credential helpers are deliberately absent |

## Herdr plugin inventory (WSL)

| Plugin | Installation status | Version / source | Configuration |
| --- | --- | --- | --- |
| Plannotator | Installed in Herdr, confirmed by the user | Version, installation source and restore command not yet recorded | [Herdr config](../config/herdr/config.toml) includes `annotate.capture`, `annotate.copy-context`, `annotate.manage`, `annotate.open` and `annotate.last` bindings; document-review bindings are labeled `plannotator-tui` |

This Herdr plugin is separate from the `@plannotator/pi-extension` Pi package
recorded in `pi-packages.json`. The inventory records user-confirmed installation,
not a runtime verification or an exhaustive discovery of installed Herdr plugins.

Recorded Windows version output: `wezterm 20261010-083911-e2a98e1b`.
The nightly channel moves; this identifies the installed build, not a version pin.

The npm lock has registry-hosted tarball URLs and integrity hashes from the source;
it does not pin all of the runtime, tools, private repositories, skills or model APIs.
No package installation, dependency execution, TypeScript build, application startup,
or fresh-machine verification was performed. Package `allowScripts` is preserved,
not newly endorsed. Existing model IDs and the source model field `reaasoning` are
retained rather than silently migrating uncertain schema/behavior.

No Nix files or fabricated lockfile are supplied. A future Home Manager design
requires explicit tool ownership/version and deployment decisions and its own validation.
