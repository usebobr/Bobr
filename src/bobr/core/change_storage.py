from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path

import frontmatter

from bobr.core.change import ARTIFACT_FILENAMES, ARTIFACT_ORDER, Change, ChangeStatus


def changes_dir(bobr_dir: Path) -> Path:
    return bobr_dir / "specs" / "changes"


def archive_dir(bobr_dir: Path) -> Path:
    return changes_dir(bobr_dir) / "archive"


def change_dir(bobr_dir: Path, name: str) -> Path:
    return changes_dir(bobr_dir) / name


def read_change(change_path: Path) -> Change:
    """Read change metadata from proposal.md frontmatter."""
    proposal = change_path / "proposal.md"
    if not proposal.exists():
        raise FileNotFoundError(f"No proposal.md in {change_path}")
    post = frontmatter.load(str(proposal))
    return Change.from_frontmatter(dict(post.metadata))


def write_change_meta(change_path: Path, change: Change, body: str = "") -> None:
    """Write/update change metadata in proposal.md frontmatter, preserving body."""
    proposal = change_path / "proposal.md"
    change.updated = datetime.now(timezone.utc)

    if proposal.exists():
        post = frontmatter.load(str(proposal))
        # Preserve existing body if no new body given
        if not body:
            body = post.content
    post = frontmatter.Post(body, **change.to_frontmatter())
    change_path.mkdir(parents=True, exist_ok=True)
    with open(proposal, "w") as f:
        f.write(frontmatter.dumps(post))
        f.write("\n")


def list_changes(bobr_dir: Path) -> list[Change]:
    """List all active (non-archived) changes."""
    cdir = changes_dir(bobr_dir)
    if not cdir.exists():
        return []
    result = []
    for d in sorted(cdir.iterdir()):
        if not d.is_dir() or d.name == "archive":
            continue
        try:
            result.append(read_change(d))
        except (FileNotFoundError, KeyError):
            continue
    return result


def list_archived_changes(bobr_dir: Path) -> list[Change]:
    """List archived changes."""
    adir = archive_dir(bobr_dir)
    if not adir.exists():
        return []
    result = []
    for d in sorted(adir.iterdir()):
        if not d.is_dir():
            continue
        try:
            result.append(read_change(d))
        except (FileNotFoundError, KeyError):
            continue
    return result


def find_change(bobr_dir: Path, name: str) -> Path | None:
    """Find a change directory by name (checks active then archive)."""
    path = change_dir(bobr_dir, name)
    if path.is_dir() and (path / "proposal.md").exists():
        return path
    apath = archive_dir(bobr_dir) / name
    if apath.is_dir() and (apath / "proposal.md").exists():
        return apath
    return None


def get_existing_artifacts(change_path: Path) -> list[str]:
    """Return list of artifact names that exist in the change directory."""
    return [
        name
        for name in ARTIFACT_ORDER
        if (change_path / ARTIFACT_FILENAMES[name]).exists()
    ]


def get_next_artifact(change_path: Path) -> str | None:
    """Return the next artifact to create, or None if all exist."""
    existing = get_existing_artifacts(change_path)
    for name in ARTIFACT_ORDER:
        if name not in existing:
            return name
    return None


def write_artifact(change_path: Path, artifact: str, content: str = "") -> Path:
    """Write an artifact file. Returns the path written."""
    filename = ARTIFACT_FILENAMES[artifact]
    path = change_path / filename
    path.write_text(content + "\n" if content else "")
    return path


def parse_tasks(change_path: Path) -> dict:
    """Parse tasks.md and return counts of done/total tasks."""
    tasks_file = change_path / "tasks.md"
    if not tasks_file.exists():
        return {"total": 0, "done": 0}

    text = tasks_file.read_text()
    total = 0
    done = 0
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- [x]") or stripped.startswith("- [X]"):
            total += 1
            done += 1
        elif stripped.startswith("- [ ]"):
            total += 1
    return {"total": total, "done": done}


def archive_change(bobr_dir: Path, change_path: Path) -> Path:
    """Move change directory to archive/. Returns new path."""
    adir = archive_dir(bobr_dir)
    adir.mkdir(parents=True, exist_ok=True)
    dest = adir / change_path.name
    shutil.move(str(change_path), str(dest))
    return dest


def sync_delta_specs(bobr_dir: Path, change_path: Path) -> list[str]:
    """Sync delta spec files from change to main specs.

    Any .md files in the change directory that are NOT standard artifacts
    (proposal.md, design.md, tasks.md) are treated as delta specs.
    They get copied to .bobr/specs/<change-name>/spec.md (or merged).

    Returns list of synced spec names.
    """
    standard = set(ARTIFACT_FILENAMES.values())
    specs_dir = bobr_dir / "specs"
    synced = []

    for f in change_path.iterdir():
        if not f.is_file() or f.suffix != ".md" or f.name in standard:
            continue
        # Delta spec: copy to specs/<spec-name>/spec.md
        spec_name = f.stem  # e.g. "auth-module" from "auth-module.md"
        target_dir = specs_dir / spec_name
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / "spec.md"

        if target.exists():
            # Append delta to existing spec with separator
            existing = target.read_text()
            delta = f.read_text()
            target.write_text(
                f"{existing}\n\n---\n\n<!-- Delta from {change_path.name} -->\n\n{delta}"
            )
        else:
            shutil.copy2(str(f), str(target))
        synced.append(spec_name)

    return synced
