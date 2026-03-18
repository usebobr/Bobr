from __future__ import annotations

import hashlib
import re
import time


def make_id(title: str, prefix: str = "BL") -> str:
    """Generate a hash-based ID like BL-a3f1 or CH-b2c4.

    Uses sha1(title + nanosecond timestamp) for uniqueness.
    4 hex chars = 65536 possibilities — sufficient for any project.
    """
    raw = f"{title.strip().lower()}{time.time_ns()}"
    digest = hashlib.sha1(raw.encode()).hexdigest()
    return f"{prefix}-{digest[:4]}"


def slug(title: str) -> str:
    """Convert title to filesystem-safe kebab-case slug.

    'Fix login bug' -> 'fix-login-bug'
    Truncated to 48 chars to keep paths sane.
    """
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:48]
