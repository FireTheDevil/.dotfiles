#!/usr/bin/env python3
"""Safe, manifest-driven deployment for this dotfiles repository."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "sources.json"
HOME_ROOT = Path(
    os.path.abspath(os.environ.get("HOME") or str(Path.home()))
)
FULL_REVISION = re.compile(r"^[0-9a-f]{40}$")
SAFE_VERSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class DotError(Exception):
    """An expected, user-facing installer error."""


class ConfigError(DotError):
    """An invalid repository manifest or state file."""


@dataclass(frozen=True)
class SourceLink:
    source: str
    target: Path


@dataclass(frozen=True)
class GitSource:
    source_id: str
    repository: str
    revision: str
    checkout: Path
    sparse_paths: Tuple[str, ...]
    required_paths: Tuple[str, ...]
    links: Tuple[SourceLink, ...]


@dataclass(frozen=True)
class PiExamples:
    version: str
    source_template: str
    target_directory: Path
    names: Tuple[str, ...]


@dataclass(frozen=True)
class Configuration:
    managed_root: Path
    state_file: Path
    git_sources: Tuple[GitSource, ...]
    pi_examples: PiExamples
    manual_steps: Tuple[str, ...]


@dataclass(frozen=True)
class LinkSpec:
    source: Path
    target: Path
    git_source_id: Optional[str] = None


@dataclass(frozen=True)
class Finding:
    group: str
    status: str
    name: str
    detail: str


def _lexical(path: Path) -> Path:
    return Path(os.path.abspath(str(path)))


def _is_within(path: Path, parent: Path) -> bool:
    try:
        _lexical(path).relative_to(_lexical(parent))
        return True
    except ValueError:
        return False


def _display(path: Path) -> str:
    path = _lexical(path)
    for base, label in ((REPO_ROOT, "."), (HOME_ROOT, "~")):
        try:
            relative = path.relative_to(_lexical(base))
        except ValueError:
            continue
        if str(relative) == ".":
            return label
        return f"{label}/{relative.as_posix()}"
    return str(path)


def _read_json(path: Path, label: str) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as error:
        raise ConfigError(f"Missing {label}: {path}") from error
    except json.JSONDecodeError as error:
        raise ConfigError(
            f"Invalid JSON in {label} at line {error.lineno}, column {error.colno}."
        ) from error
    except UnicodeError as error:
        raise ConfigError(f"{label} is not valid UTF-8: {path}") from error
    except OSError as error:
        raise ConfigError(f"Cannot read {label}: {path}: {error}") from error


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ConfigError(f"{label} must be a JSON object.")
    return value


def _array(value: Any, label: str) -> Sequence[Any]:
    if not isinstance(value, list):
        raise ConfigError(f"{label} must be a JSON array.")
    return value


def _string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ConfigError(f"{label} must be a nonempty string.")
    if "\x00" in value:
        raise ConfigError(f"{label} contains a null byte.")
    return value


def _home_path(value: Any, label: str) -> Path:
    raw = _string(value, label)
    if raw == "~":
        return HOME_ROOT
    if not raw.startswith("~/"):
        raise ConfigError(f"{label} must start with '~/'.")
    return _lexical(HOME_ROOT / raw[2:])


def _relative_path(value: Any, label: str) -> str:
    raw = _string(value, label)
    path = PurePosixPath(raw)
    if (
        path.is_absolute()
        or raw in (".", "..")
        or path.as_posix() != raw
        or any(part in ("", ".", "..") for part in path.parts)
    ):
        raise ConfigError(f"{label} must be a safe relative POSIX path.")
    if "\\" in raw:
        raise ConfigError(f"{label} must use '/' as its path separator.")
    return raw


def _full_revision(value: Any, label: str) -> str:
    revision = _string(value, label)
    if not FULL_REVISION.fullmatch(revision):
        raise ConfigError(f"{label} must be a full lowercase 40-character Git revision.")
    return revision


def _package_sources(settings: Mapping[str, Any]) -> Tuple[str, ...]:
    values = _array(settings.get("packages"), "home/.pi/agent/settings.json packages")
    sources: List[str] = []
    for index, value in enumerate(values):
        if isinstance(value, str):
            sources.append(value)
            continue
        entry = _mapping(value, f"settings packages[{index}]")
        sources.append(_string(entry.get("source"), f"settings packages[{index}].source"))
    return tuple(sources)


def load_configuration() -> Configuration:
    manifest = _mapping(_read_json(MANIFEST_PATH, "source manifest"), "sources.json")
    if manifest.get("formatVersion") != 1:
        raise ConfigError("sources.json formatVersion must be 1.")

    managed_root = _home_path(manifest.get("managedRoot"), "managedRoot")
    state_file = _home_path(manifest.get("stateFile"), "stateFile")
    if managed_root == HOME_ROOT or not _is_within(managed_root, HOME_ROOT):
        raise ConfigError("managedRoot must be below the home directory.")
    if not _is_within(state_file, HOME_ROOT):
        raise ConfigError("stateFile must be inside the home directory.")

    git_sources: List[GitSource] = []
    source_ids = set()
    source_checkouts = set()
    for index, raw_value in enumerate(_array(manifest.get("gitSources"), "gitSources")):
        label = f"gitSources[{index}]"
        raw = _mapping(raw_value, label)
        source_id = _string(raw.get("id"), f"{label}.id")
        if source_id in source_ids:
            raise ConfigError(f"Duplicate Git source id: {source_id}")
        source_ids.add(source_id)

        repository = _string(raw.get("repository"), f"{label}.repository")
        if not repository.startswith("https://") or not repository.endswith(".git"):
            raise ConfigError(f"{label}.repository must be an HTTPS .git URL.")
        revision = _full_revision(raw.get("revision"), f"{label}.revision")
        checkout = _home_path(raw.get("checkout"), f"{label}.checkout")
        sources_root = managed_root / "sources"
        if checkout == sources_root or not _is_within(checkout, sources_root):
            raise ConfigError(f"{label}.checkout must be below managedRoot/sources.")
        if checkout in source_checkouts:
            raise ConfigError(f"Duplicate Git checkout path: {_display(checkout)}")
        source_checkouts.add(checkout)

        sparse_paths = tuple(
            _relative_path(value, f"{label}.sparsePaths")
            for value in _array(raw.get("sparsePaths"), f"{label}.sparsePaths")
        )
        if not sparse_paths or len(set(sparse_paths)) != len(sparse_paths):
            raise ConfigError(f"{label}.sparsePaths must contain unique paths.")
        required_paths = tuple(
            _relative_path(value, f"{label}.requiredPaths")
            for value in _array(raw.get("requiredPaths"), f"{label}.requiredPaths")
        )
        if not required_paths:
            raise ConfigError(f"{label}.requiredPaths must not be empty.")

        links: List[SourceLink] = []
        for link_index, link_value in enumerate(_array(raw.get("links"), f"{label}.links")):
            link_label = f"{label}.links[{link_index}]"
            link = _mapping(link_value, link_label)
            source = _relative_path(link.get("source"), f"{link_label}.source")
            target = _home_path(link.get("target"), f"{link_label}.target")
            if not _is_within(target, HOME_ROOT) or target == HOME_ROOT:
                raise ConfigError(f"{link_label}.target must be below the home directory.")
            links.append(SourceLink(source=source, target=target))

        git_sources.append(
            GitSource(
                source_id=source_id,
                repository=repository,
                revision=revision,
                checkout=checkout,
                sparse_paths=sparse_paths,
                required_paths=required_paths,
                links=tuple(links),
            )
        )

    example_raw = _mapping(manifest.get("piExamples"), "piExamples")
    version = _string(example_raw.get("version"), "piExamples.version")
    if not SAFE_VERSION.fullmatch(version):
        raise ConfigError("piExamples.version contains unsupported characters.")
    source_template = _string(
        example_raw.get("sourceTemplate"), "piExamples.sourceTemplate"
    )
    if "{version}" not in source_template or "{name}" not in source_template:
        raise ConfigError(
            "piExamples.sourceTemplate must contain {version} and {name}."
        )
    target_directory = _home_path(
        example_raw.get("targetDirectory"), "piExamples.targetDirectory"
    )
    expected_target_directory = HOME_ROOT / ".pi" / "agent" / "extensions"
    if target_directory != expected_target_directory:
        raise ConfigError("piExamples.targetDirectory must be ~/.pi/agent/extensions.")
    names = tuple(
        _relative_path(value, "piExamples.names")
        for value in _array(example_raw.get("names"), "piExamples.names")
    )
    if not names or len(set(names)) != len(names):
        raise ConfigError("piExamples.names must contain unique names.")
    for name in names:
        if "/" in name or not SAFE_VERSION.fullmatch(name):
            raise ConfigError(f"Invalid Pi example name: {name}")
        try:
            rendered = source_template.format(version=version, name=name)
        except (IndexError, KeyError, ValueError) as error:
            raise ConfigError("piExamples.sourceTemplate has invalid placeholders.") from error
        rendered_path = _home_path(rendered, "rendered Pi example source")
        expected_release = (
            HOME_ROOT / ".pi" / "agent" / "install" / "releases" / version
        )
        if not _is_within(rendered_path, expected_release):
            raise ConfigError(
                "piExamples.sourceTemplate must stay inside its pinned Pi release."
            )

    settings_path = REPO_ROOT / "home" / ".pi" / "agent" / "settings.json"
    settings = _mapping(_read_json(settings_path, "Pi settings"), "Pi settings")
    configured_extensions = tuple(
        _string(value, "Pi settings extensions")
        for value in _array(settings.get("extensions"), "Pi settings extensions")
    )
    if configured_extensions != ("+builtin:codemode",):
        raise ConfigError(
            "home/.pi/agent/settings.json must leave installer-linked extensions "
            "to normal discovery."
        )
    configured_packages = set(_package_sources(settings))
    package_ids = set()
    for index, package_value in enumerate(
        _array(manifest.get("piPackages"), "piPackages")
    ):
        label = f"piPackages[{index}]"
        package = _mapping(package_value, label)
        package_id = _string(package.get("id"), f"{label}.id")
        if package_id in package_ids:
            raise ConfigError(f"Duplicate Pi package id: {package_id}")
        package_ids.add(package_id)
        _string(package.get("repository"), f"{label}.repository")
        revision = _full_revision(package.get("revision"), f"{label}.revision")
        configured = _string(package.get("configuredSource"), f"{label}.configuredSource")
        if configured not in configured_packages:
            raise ConfigError(
                f"{label}.configuredSource is absent from home/.pi/agent/settings.json."
            )
        if configured.startswith("git:") and not configured.endswith(f"@{revision}"):
            raise ConfigError(f"{label}.configuredSource does not pin its revision.")
        if "sourcePath" in package:
            source_path = _relative_path(package.get("sourcePath"), f"{label}.sourcePath")
            matching = [
                source
                for source in git_sources
                if source.repository == package.get("repository")
                and source.revision == revision
            ]
            if len(matching) != 1:
                raise ConfigError(f"{label} must match one managed Git source.")
            configured_path = _lexical(
                HOME_ROOT / ".pi" / "agent" / configured
            )
            expected_path = _lexical(matching[0].checkout / source_path)
            if configured_path != expected_path:
                raise ConfigError(
                    f"{label}.configuredSource does not resolve to its managed sourcePath."
                )

    manual_steps: List[str] = []
    for index, step_value in enumerate(
        _array(manifest.get("manualSteps"), "manualSteps")
    ):
        label = f"manualSteps[{index}]"
        step = _mapping(step_value, label)
        _string(step.get("id"), f"{label}.id")
        manual_steps.append(_string(step.get("instruction"), f"{label}.instruction"))
    windows_config = REPO_ROOT / "windows" / ".wezterm.lua"
    if not windows_config.is_file() or windows_config.is_symlink():
        raise ConfigError("Missing regular Windows configuration: windows/.wezterm.lua")

    return Configuration(
        managed_root=managed_root,
        state_file=state_file,
        git_sources=tuple(git_sources),
        pi_examples=PiExamples(
            version=version,
            source_template=source_template,
            target_directory=target_directory,
            names=names,
        ),
        manual_steps=tuple(manual_steps),
    )


def _home_links() -> List[LinkSpec]:
    home_tree = REPO_ROOT / "home"
    if not home_tree.is_dir():
        raise ConfigError(f"Missing normalized home tree: {home_tree}")

    links: List[LinkSpec] = []
    for root_value, directory_names, file_names in os.walk(home_tree, followlinks=False):
        root = Path(root_value)
        directory_names.sort()
        file_names.sort()
        for directory_name in directory_names:
            directory = root / directory_name
            if directory.is_symlink():
                raise ConfigError(
                    f"Repository home tree contains a directory symlink: {_display(directory)}"
                )
        for file_name in file_names:
            source = root / file_name
            if source.is_symlink() or not source.is_file():
                raise ConfigError(
                    f"Repository home tree contains a non-regular file: {_display(source)}"
                )
            relative = source.relative_to(home_tree)
            links.append(
                LinkSpec(
                    source=_lexical(source),
                    target=_lexical(HOME_ROOT / relative),
                )
            )
    return links


def desired_links(configuration: Configuration) -> Tuple[LinkSpec, ...]:
    links = _home_links()
    for source in configuration.git_sources:
        for link in source.links:
            links.append(
                LinkSpec(
                    source=_lexical(source.checkout / link.source),
                    target=link.target,
                    git_source_id=source.source_id,
                )
            )

    examples = configuration.pi_examples
    for name in examples.names:
        rendered = examples.source_template.format(
            version=examples.version,
            name=name,
        )
        links.append(
            LinkSpec(
                source=_home_path(rendered, f"Pi example {name}"),
                target=_lexical(examples.target_directory / f"{name}.ts"),
            )
        )

    targets: Dict[Path, LinkSpec] = {}
    for link in links:
        if not _is_within(link.target, HOME_ROOT) or link.target == HOME_ROOT:
            raise ConfigError(f"Link target is outside the home directory: {link.target}")
        if link.target in targets:
            raise ConfigError(
                f"Two sources declare the same link target: {_display(link.target)}"
            )
        targets[link.target] = link
    return tuple(sorted(links, key=lambda link: str(link.target)))


def _run_git(
    arguments: Sequence[str],
    *,
    input_text: Optional[str] = None,
    inspect_only: bool = False,
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["GIT_TERMINAL_PROMPT"] = "0"
    if inspect_only:
        environment["GIT_OPTIONAL_LOCKS"] = "0"
    try:
        return subprocess.run(
            ["git", *arguments],
            input=input_text,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            env=environment,
        )
    except FileNotFoundError as error:
        raise DotError("Git is required but was not found on PATH.") from error
    except OSError as error:
        raise DotError(f"Could not start Git: {error}") from error


def _git_read(source: GitSource, *arguments: str) -> Optional[str]:
    result = _run_git(
        ["-C", str(source.checkout), *arguments],
        inspect_only=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _git_write(
    source: GitSource,
    arguments: Sequence[str],
    *,
    input_text: Optional[str] = None,
) -> None:
    result = _run_git(
        ["-C", str(source.checkout), *arguments],
        input_text=input_text,
    )
    if result.returncode != 0:
        command = " ".join(arguments[:2])
        raise DotError(
            f"Git command failed for {source.source_id}: {command} "
            f"(exit {result.returncode})."
        )


def _path_exists(path: Path) -> bool:
    return os.path.lexists(path)


def _bad_parent(path: Path) -> Optional[Path]:
    parent = path.parent
    while not _path_exists(parent):
        if parent == parent.parent:
            return parent
        parent = parent.parent
    if not parent.is_dir():
        return parent
    return None


def inspect_git_source(source: GitSource) -> Finding:
    path = source.checkout
    if not _path_exists(path):
        bad_parent = _bad_parent(path)
        if bad_parent is not None:
            return Finding(
                "sources",
                "conflict",
                source.source_id,
                f"parent is not a directory: {_display(bad_parent)}",
            )
        return Finding(
            "sources",
            "change",
            source.source_id,
            f"clone {source.repository} at {source.revision[:12]} into {_display(path)}",
        )
    if path.is_symlink() or not path.is_dir():
        return Finding(
            "sources",
            "conflict",
            source.source_id,
            f"checkout path is not an ordinary directory: {_display(path)}",
        )

    top_level = _git_read(source, "rev-parse", "--show-toplevel")
    if top_level is None:
        return Finding(
            "sources",
            "conflict",
            source.source_id,
            f"existing directory is not a Git checkout: {_display(path)}",
        )
    if Path(top_level).resolve() != path.resolve():
        return Finding(
            "sources",
            "conflict",
            source.source_id,
            f"checkout belongs to a different Git work tree: {_display(path)}",
        )

    origin = _git_read(source, "remote", "get-url", "origin")
    if origin != source.repository:
        return Finding(
            "sources",
            "conflict",
            source.source_id,
            "origin URL does not exactly match the manifest",
        )

    dirty = _git_read(source, "status", "--porcelain=v1", "--untracked-files=all")
    if dirty is None:
        return Finding(
            "sources",
            "conflict",
            source.source_id,
            "Git could not inspect the working tree",
        )
    if dirty:
        return Finding(
            "sources",
            "conflict",
            source.source_id,
            "working tree is dirty; preserve or remove those changes first",
        )

    changes: List[str] = []
    head = _git_read(source, "rev-parse", "HEAD")
    if head != source.revision:
        changes.append(f"checkout {source.revision[:12]}")

    sparse_output = _git_read(source, "sparse-checkout", "list")
    sparse_paths = tuple(sorted(sparse_output.splitlines())) if sparse_output is not None else ()
    if sparse_paths != tuple(sorted(source.sparse_paths)):
        changes.append("set sparse paths")

    if not changes:
        missing = [
            path
            for path in source.required_paths
            if not (source.checkout / path).is_file()
        ]
        if missing:
            changes.append("restore required paths")

    if changes:
        return Finding(
            "sources",
            "change",
            source.source_id,
            f"{', '.join(changes)} in {_display(path)}",
        )
    return Finding(
        "sources",
        "ok",
        source.source_id,
        f"clean at {source.revision[:12]}",
    )


def _symlink_points_to(target: Path, source: Path) -> bool:
    if not target.is_symlink():
        return False
    try:
        value = Path(os.readlink(target))
    except OSError:
        return False
    if not value.is_absolute():
        value = target.parent / value
    return _lexical(value) == _lexical(source)


def inspect_link(link: LinkSpec) -> Finding:
    if _path_exists(link.target):
        if _symlink_points_to(link.target, link.source):
            if not link.source.is_file() and link.git_source_id is None:
                return Finding(
                    "links",
                    "blocked",
                    _display(link.target),
                    f"source is missing: {_display(link.source)}",
                )
            return Finding(
                "links",
                "ok",
                _display(link.target),
                f"points to {_display(link.source)}",
            )
        return Finding(
            "links",
            "conflict",
            _display(link.target),
            "target exists and is not the requested symlink",
        )

    bad_parent = _bad_parent(link.target)
    if bad_parent is not None:
        return Finding(
            "links",
            "conflict",
            _display(link.target),
            f"parent is not a directory: {_display(bad_parent)}",
        )
    if not link.source.is_file() and link.git_source_id is None:
        return Finding(
            "links",
            "blocked",
            _display(link.target),
            f"source is missing: {_display(link.source)}",
        )
    suffix = " after its Git source is ready" if not link.source.is_file() else ""
    return Finding(
        "links",
        "change",
        _display(link.target),
        f"link to {_display(link.source)}{suffix}",
    )


def collect_findings(
    configuration: Configuration,
    links: Sequence[LinkSpec],
) -> Tuple[Finding, ...]:
    findings: List[Finding] = [
        inspect_git_source(source) for source in configuration.git_sources
    ]
    findings.extend(inspect_link(link) for link in links)
    bad_state_parent = _bad_parent(configuration.state_file)
    if bad_state_parent is None:
        findings.append(
            Finding(
                "state",
                "ok",
                _display(configuration.state_file),
                "state path is usable",
            )
        )
    else:
        findings.append(
            Finding(
                "state",
                "conflict",
                _display(configuration.state_file),
                f"parent is not a directory: {_display(bad_state_parent)}",
            )
        )
    return tuple(findings)


def _render_findings(
    findings: Sequence[Finding],
    manual_steps: Sequence[str],
    *,
    heading: str,
) -> None:
    print(heading)
    for group, title in (
        ("sources", "Pinned sources"),
        ("links", "Managed links"),
        ("state", "Installer state"),
    ):
        group_findings = [finding for finding in findings if finding.group == group]
        if not group_findings:
            continue
        actionable = [finding for finding in group_findings if finding.status != "ok"]
        print(f"\n{title}:")
        if actionable:
            for finding in actionable:
                print(f"  [{finding.status}] {finding.name}: {finding.detail}")
        correct = len(group_findings) - len(actionable)
        if correct:
            print(f"  {correct} already correct")

    if manual_steps:
        print("\nManual Windows step:")
        for step in manual_steps:
            print(f"  - {step}")

    counts = {
        status: sum(finding.status == status for finding in findings)
        for status in ("change", "conflict", "blocked", "ok")
    }
    print(
        "\nSummary: "
        f"{counts['change']} change(s), "
        f"{counts['conflict']} conflict(s), "
        f"{counts['blocked']} blocked, "
        f"{counts['ok']} correct."
    )


def _has_blockers(findings: Sequence[Finding]) -> bool:
    return any(finding.status in ("conflict", "blocked") for finding in findings)


def _has_changes(findings: Sequence[Finding]) -> bool:
    return any(finding.status == "change" for finding in findings)


def _git_sparse_paths(source: GitSource) -> Tuple[str, ...]:
    output = _git_read(source, "sparse-checkout", "list")
    if output is None:
        return ()
    return tuple(sorted(output.splitlines()))


def _remove_partial_checkout(path: Path) -> None:
    if not _path_exists(path):
        return
    if path.is_symlink() or not path.is_dir():
        path.unlink()
        return
    shutil.rmtree(path)


def ensure_git_source(source: GitSource) -> None:
    initial = inspect_git_source(source)
    if initial.status == "ok":
        return
    if initial.status != "change":
        raise DotError(f"Cannot update {source.source_id}: {initial.detail}")

    if not _path_exists(source.checkout):
        source.checkout.parent.mkdir(parents=True, exist_ok=True)
        print(f"Cloning {source.source_id} into {_display(source.checkout)}")
        created_checkout = False
        try:
            source.checkout.mkdir(mode=0o700)
            created_checkout = True
            result = _run_git(
                [
                    "clone",
                    "--filter=blob:none",
                    "--no-checkout",
                    "--origin",
                    "origin",
                    source.repository,
                    str(source.checkout),
                ]
            )
            if result.returncode != 0:
                raise DotError(
                    f"Git clone failed for {source.source_id} "
                    f"(exit {result.returncode})."
                )
            _git_write(source, ["sparse-checkout", "init", "--no-cone"])
            _git_write(
                source,
                ["sparse-checkout", "set", "--no-cone", "--stdin"],
                input_text="".join(f"{path}\n" for path in source.sparse_paths),
            )
            _git_write(
                source,
                ["fetch", "--filter=blob:none", "origin", source.revision],
            )
            _git_write(source, ["checkout", "--detach", source.revision])
        except BaseException:
            if created_checkout:
                _remove_partial_checkout(source.checkout)
            raise
    else:
        print(f"Updating {source.source_id} in {_display(source.checkout)}")
        required_missing = any(
            not (source.checkout / path).is_file()
            for path in source.required_paths
        )
        if (
            _git_sparse_paths(source) != tuple(sorted(source.sparse_paths))
            or required_missing
        ):
            _git_write(source, ["sparse-checkout", "init", "--no-cone"])
            _git_write(
                source,
                ["sparse-checkout", "set", "--no-cone", "--stdin"],
                input_text="".join(f"{path}\n" for path in source.sparse_paths),
            )
        head = _git_read(source, "rev-parse", "HEAD")
        if head != source.revision:
            _git_write(
                source,
                ["fetch", "--filter=blob:none", "origin", source.revision],
            )
            _git_write(source, ["checkout", "--detach", source.revision])

    final = inspect_git_source(source)
    if final.status != "ok":
        raise DotError(f"Git source {source.source_id} is not ready: {final.detail}")


def load_state(path: Path) -> Dict[Path, Path]:
    if not _path_exists(path):
        return {}
    if path.is_symlink() or not path.is_file():
        raise ConfigError(f"State path is not an ordinary file: {_display(path)}")
    raw = _mapping(_read_json(path, "installer state"), "installer state")
    if raw.get("formatVersion") != 1:
        raise ConfigError("Installer state formatVersion must be 1.")
    links = _array(raw.get("links"), "installer state links")
    owned: Dict[Path, Path] = {}
    for index, value in enumerate(links):
        label = f"installer state links[{index}]"
        entry = _mapping(value, label)
        target = Path(_string(entry.get("target"), f"{label}.target"))
        source = Path(_string(entry.get("source"), f"{label}.source"))
        if not target.is_absolute() or not source.is_absolute():
            raise ConfigError(f"{label} paths must be absolute.")
        target = _lexical(target)
        source = _lexical(source)
        if not _is_within(target, HOME_ROOT) or target == HOME_ROOT:
            raise ConfigError(f"{label}.target is outside the home directory.")
        if target in owned:
            raise ConfigError(f"Duplicate state target: {_display(target)}")
        owned[target] = source
    return owned


def write_state(path: Path, owned: Mapping[Path, Path]) -> None:
    if _path_exists(path) and (path.is_symlink() or not path.is_file()):
        raise DotError(f"Refusing to replace non-file state path: {_display(path)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "formatVersion": 1,
        "links": [
            {"target": str(target), "source": str(owned[target])}
            for target in sorted(owned, key=str)
        ],
    }
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        dir=str(path.parent),
        text=True,
    )
    temporary_path = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass
        raise


def _confirm(prompt: str, assume_yes: bool) -> bool:
    if assume_yes:
        return True
    try:
        response = input(f"\n{prompt} [y/N] ").strip().lower()
    except EOFError:
        response = ""
    return response in ("y", "yes")


def command_plan(configuration: Configuration, links: Sequence[LinkSpec]) -> int:
    findings = collect_findings(configuration, links)
    _render_findings(findings, configuration.manual_steps, heading="Dotfiles plan")
    return 1 if _has_blockers(findings) else 0


def command_check(configuration: Configuration, links: Sequence[LinkSpec]) -> int:
    findings = collect_findings(configuration, links)
    failures = [finding for finding in findings if finding.status != "ok"]
    if not failures:
        print(f"Check passed: {len(findings)} managed items are correct.")
        for step in configuration.manual_steps:
            print(f"Manual: {step}")
        return 0
    _render_findings(findings, configuration.manual_steps, heading="Dotfiles check failed")
    return 1


def command_apply(
    configuration: Configuration,
    links: Sequence[LinkSpec],
    *,
    assume_yes: bool,
) -> int:
    findings = collect_findings(configuration, links)
    _render_findings(findings, configuration.manual_steps, heading="Dotfiles apply plan")
    if _has_blockers(findings):
        print("\nApply refused: resolve every conflict and blocked prerequisite first.")
        return 1
    if not _has_changes(findings):
        print("\nNo managed changes are required.")
        return 0
    if not _confirm("Apply these changes?", assume_yes):
        print("No changes applied.")
        return 1

    for source in configuration.git_sources:
        ensure_git_source(source)

    post_source_findings = collect_findings(configuration, links)
    if _has_blockers(post_source_findings):
        raise DotError("A conflict or missing prerequisite appeared after source update.")
    source_failures = [
        finding
        for finding in post_source_findings
        if finding.group == "sources" and finding.status != "ok"
    ]
    if source_failures:
        raise DotError("One or more pinned Git sources are still not ready.")

    for link in links:
        finding = inspect_link(link)
        if finding.status in ("conflict", "blocked"):
            raise DotError(f"Cannot create {_display(link.target)}: {finding.detail}")

    owned = load_state(configuration.state_file)
    created_count = 0
    for link in links:
        if _path_exists(link.target):
            continue
        link.target.parent.mkdir(parents=True, exist_ok=True)
        previous = owned.get(link.target)
        link_created = False
        try:
            link.target.symlink_to(link.source)
            link_created = True
            owned[link.target] = link.source
            write_state(configuration.state_file, owned)
        except BaseException:
            if link_created and _symlink_points_to(link.target, link.source):
                link.target.unlink()
            if previous is None:
                owned.pop(link.target, None)
            else:
                owned[link.target] = previous
            raise
        created_count += 1
        print(f"Linked {_display(link.target)} -> {_display(link.source)}")

    print(f"\nApply complete: created {created_count} managed link(s).")
    print("Run './dot check' to inspect the deployed state.")
    return 0


def _unlink_findings(owned: Mapping[Path, Path]) -> Tuple[Finding, ...]:
    findings: List[Finding] = []
    for target in sorted(owned, key=str):
        source = owned[target]
        if not _path_exists(target):
            findings.append(
                Finding(
                    "links",
                    "change",
                    _display(target),
                    "remove stale ownership record",
                )
            )
        elif _symlink_points_to(target, source):
            findings.append(
                Finding(
                    "links",
                    "change",
                    _display(target),
                    f"unlink recorded source {_display(source)}",
                )
            )
        else:
            findings.append(
                Finding(
                    "links",
                    "conflict",
                    _display(target),
                    "recorded target changed; it will not be removed",
                )
            )
    return tuple(findings)


def command_unlink(configuration: Configuration, *, assume_yes: bool) -> int:
    owned = load_state(configuration.state_file)
    if not owned:
        print("No installer-owned links are recorded.")
        print("Pinned source checkouts, if present, are unchanged.")
        return 0

    findings = _unlink_findings(owned)
    _render_findings(findings, (), heading="Dotfiles unlink plan")
    if _has_blockers(findings):
        print("\nUnlink refused: recorded targets changed and were left untouched.")
        return 1
    if not _confirm("Remove these installer-owned links?", assume_yes):
        print("No links removed.")
        return 1

    removed = 0
    for target, source in sorted(owned.items(), key=lambda item: str(item[0])):
        if not _path_exists(target):
            continue
        if _symlink_points_to(target, source):
            target.unlink()
            removed += 1
            continue
        raise DotError(
            f"Recorded target changed during unlink and was left untouched: "
            f"{_display(target)}"
        )

    if _path_exists(configuration.state_file):
        if configuration.state_file.is_symlink() or not configuration.state_file.is_file():
            raise DotError(
                f"Refusing to remove non-file state path: {_display(configuration.state_file)}"
            )
        configuration.state_file.unlink()

    print(f"\nUnlink complete: removed {removed} installer-owned link(s).")
    print("Pinned source checkouts and created directories were retained.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dot",
        description="Plan and manage this repository's dotfile links safely.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("plan", help="show changes without modifying the system")
    apply_parser = commands.add_parser("apply", help="apply the current safe plan")
    apply_parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="skip the confirmation prompt",
    )
    commands.add_parser("check", help="verify sources and links without changes")
    unlink_parser = commands.add_parser(
        "unlink",
        help="remove only links recorded as installer-owned",
    )
    unlink_parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="skip the confirmation prompt",
    )
    return parser


def main(arguments: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    options = parser.parse_args(arguments)
    try:
        configuration = load_configuration()
        links = desired_links(configuration)
        load_state(configuration.state_file)
        if options.command == "plan":
            return command_plan(configuration, links)
        if options.command == "apply":
            return command_apply(configuration, links, assume_yes=options.yes)
        if options.command == "check":
            return command_check(configuration, links)
        if options.command == "unlink":
            return command_unlink(configuration, assume_yes=options.yes)
        parser.error(f"Unknown command: {options.command}")
    except KeyboardInterrupt:
        print("\nInterrupted; no further changes were made.", file=sys.stderr)
        return 130
    except DotError as error:
        print(f"dot: {error}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"dot: filesystem error: {error}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
