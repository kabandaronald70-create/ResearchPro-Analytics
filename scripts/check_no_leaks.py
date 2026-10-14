"""
ResearchPro Analytics — Pre-commit safety check.

Scans notebooks and markdown exports for raw identifiers or restricted
data that must never be committed to a public repository.

Usage (from project root):
    python scripts/check_no_leaks.py

Exit codes:
    0 — all targets are clean
    1 — at least one target contains a leak marker
    2 — a required target file is missing
"""

from __future__ import annotations

import sys
from pathlib import Path

# ---------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TARGETS = [
    "notebooks/02_dataset_assessment_public.ipynb",
    "notebooks/03_data_inspection.ipynb",
    "notebooks/02_dataset_assessment_public.md",
]

# Strings that must NEVER appear in a committed public file.
# Includes real survey IDs plus a sentinel used by the questionnaire.
LEAK_MARKERS = [
    "004e93d7552248ed95d8bc3ec21bdbdb",
    "H1650506",
    "complete Roster&",
]

# ---------------------------------------------------------------
# Check
# ---------------------------------------------------------------

def check_file(path: Path) -> tuple[bool, dict[str, int]]:
    """Return (is_clean, {marker: count}) for one file."""
    if not path.exists():
        return False, {}

    text = path.read_text(encoding="utf-8", errors="replace")
    hits = {m: text.count(m) for m in LEAK_MARKERS if m in text}
    return not hits, hits


def main() -> int:
    print("PRE-COMMIT SAFETY CHECK")
    print("=" * 70)

    any_leak = False
    any_missing = False

    for rel in TARGETS:
        path = PROJECT_ROOT / rel

        if not path.exists():
            print(f"\n{rel}")
            print("-" * 70)
            print("  MISSING — cannot verify")
            any_missing = True
            continue

        clean, hits = check_file(path)

        print(f"\n{rel}")
        print("-" * 70)
        print(f"  Size: {path.stat().st_size:,} bytes")

        if clean:
            print("  ✅ CLEAN")
        else:
            any_leak = True
            print("  ❌ LEAK DETECTED")
            for marker, count in hits.items():
                print(f"     {marker[:48]:<50} FOUND {count}x")

    print("\n" + "=" * 70)

    if any_missing and not any_leak:
        print("Result: some targets missing (see above)")
        return 2
    if any_leak:
        print("Result: ❌ NOT READY — scrub the flagged files before committing")
        return 1

    print("Result: ✅ READY TO COMMIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())