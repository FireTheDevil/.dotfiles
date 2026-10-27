# User and scope

Defer to the user when a decision requires their preferences, priorities, or approval.  Otherwise, use sound judgment and proceed independently.

Some skills support clear communication and sustained attention; use them when applicable. Keep conversations focused, easy to scan, and clear about decisions and next actions. Preserve necessary detail without adding unnecessary cognitive load.

These instructions define the user's default workflow in Pi. Keep repository-specific build, test, and coding instructions in each repository.

# Questions for the user

When you need an answer from the user to proceed, use the questionnaire tool instead of asking in chat. If the tool is unavailable, ask in chat. Do not ask unnecessary questions.

# Permission to act

A request to audit, review, or suggest improvements does not authorize changes. For implementation requests, stay within scope and preserve unrelated work.

# Outcome-first execution

- Identify the observable result that satisfies the request before starting substantial work.
- Choose the smallest complete change that delivers that result. Small diffs alone are not the goal.
- Every investigation, delegation, and check must resolve a relevant uncertainty or verify an acceptance condition.
- Use focused verification that demonstrates the requested behavior and covers plausible regressions. Broaden checks only for a concrete risk or a required repository check. Reuse valid evidence; repeat checks only when relevant inputs change.
- If the work requires substantially broader changes, explain why before expanding scope and obtain approval when the expansion goes beyond the authorized request.
- Stop when the result is demonstrated and required checks pass. Do not add cleanup, abstractions, or polish without a concrete need within the authorized scope.
- If two attempts produce no useful new evidence, reassess the approach rather than repeat it.

# Completion reports

Report the achieved outcome first, then what changed, what verification ran, and any remaining limitations. Distinguish verified results from assumptions. Do not describe work as complete while required checks or delegated tasks remain unresolved.

# Local file links

When linking to local files in responses, use Markdown links with absolute `file://` URLs, such as `[index.html](file:///path/to/project/index.html)`. Do not use relative URLs, bare paths, or `~` as link targets. Percent-encode spaces and other URL-special characters in path components.

# Asynchronous agents in Pi

First handle any user request or required agent-control action. When further progress depends only on delegated work, end the turn without claiming completion; agent results will resume the conversation. Do not poll agents or make tool calls solely to wait. Never use placeholder, whitespace-only, or no-op tool calls to wait.

# Tool composition

Before using tools, identify the next bounded set of operations. Batch independent operations when useful, for example with Promise.all. Run dependent operations sequentially only when their inputs and next steps are already known. Do not run operations concurrently when they modify shared state or depend on each other's results.

Keep intermediate results inside the program and return compact findings. Pause for judgment when a result determines the next step. Do not split known work across calls merely to inspect intermediate output, or speculatively chain unplanned next steps. Simple operations do not require a larger batch.

Use the runtime's tool catalog to check callable names and contracts when needed. Composition must not bypass tool-specific safety or concurrency constraints, duplicate delegated work, or keep a turn alive while waiting for agents.

# Web-development browser verification

For web-development tasks requiring browser verification, use the `browser-use` skill and CLI instead of Playwright. Read `~/.pi/agent/skills/browser-use/SKILL.md` before use. When delegating verification, assign a shell-capable agent and explicitly pass it that skill file and this tool preference.

If browser-use is unavailable, report the blocker. Do not silently substitute Playwright or claim browser verification succeeded.

# Coding

Don't write unit tests.
