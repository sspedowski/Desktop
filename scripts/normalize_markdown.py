#!/usr/bin/env python3
"""
Repo-wide doc cleanup for two targets + README spot-check tweaks.

Usage (PowerShell examples):
  # Dry-run (no writes), default workspace root
  python scripts/normalize_markdown.py --check \
    --targets START_HERE.md MASTER_JUSTICE_FILE_COPILOT_INSTRUCTIONS.md README.md

  # Apply changes
  python scripts/normalize_markdown.py \
    --targets START_HERE.md MASTER_JUSTICE_FILE_COPILOT_INSTRUCTIONS.md README.md

Notes:
  - Aggressive wrapping enabled for all except README.md (light touch there).
  - Preserves fenced code blocks and avoids wrapping URLs/HTML/table lines.
"""

import argparse
import os
import re
import sys
import textwrap
from typing import Dict, List


WRAP_WIDTH = 80


def read(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def write(path: str, data: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)


def normalize_markdown(md: str, aggressive_wrap: bool = True) -> str:
    lines = md.splitlines()
    out: List[str] = []
    in_code = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # Code fence toggling
        if re.match(r"^\s*```", line):
            # ensure blank line before opening fence
            if not in_code:
                if out and out[-1].strip() != "":
                    out.append("")
            in_code = not in_code
            out.append(line.rstrip())
            i += 1
            continue

        if in_code:
            out.append(line.rstrip())
            i += 1
            continue

        # Emphasis-as-heading -> real heading
        m_bold_head = re.match(r"^\s*\*\*(.+?)\*\*\s*$", line)
        if m_bold_head:
            line = f"### {m_bold_head.group(1).strip()}"

        # Headings: ensure blank line before and after
        if re.match(r"^#{1,6}\s", line):
            if out and out[-1].strip() != "":
                out.append("")
            out.append(line.rstrip())
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if nxt.strip() != "" and not re.match(r"^\s*```", nxt):
                out.append("")
            i += 1
            continue

        # List bullets: normalize * and + to -
        if re.match(r"^\s*[*+]\s+", line):
            line = re.sub(r"^\s*[*+]\s+", lambda m: re.sub(r"[^ ]", " ", m.group(0))[:-1] + "- ", line)

        # Ordered lists: force 1.
        if re.match(r"^\s*\d+\.\s+", line):
            indent = re.match(r"^(\s*)\d+\.\s+", line).group(1)
            content = re.sub(r"^\s*\d+\.\s+", "", line)
            line = f"{indent}1. {content}"

        # Ensure blank line before list blocks
        if re.match(r"^\s*-\s+", line) or re.match(r"^\s*1\.\s+", line):
            if out and out[-1].strip() != "":
                out.append("")
            out.append(line.rstrip())
            i += 1
            continue

        # Wrap long paragraphs cautiously
        if aggressive_wrap:
            if (
                "http://" in line
                or "https://" in line
                or line.strip().startswith(">")
                or line.strip().startswith("|")
                or re.match(r"^\s*<.+?>\s*$", line)
            ):
                out.append(line.rstrip())
            else:
                if line.strip() != "":
                    wrapped = textwrap.fill(
                        line.strip(),
                        width=WRAP_WIDTH,
                        break_long_words=False,
                        break_on_hyphens=False,
                    )
                    out.extend(wrapped.splitlines())
                else:
                    out.append("")
        else:
            out.append(line.rstrip())

        i += 1

    # Second pass: ensure blank line after closing fences and after lists
    lines2 = out
    out2: List[str] = []
    in_code = False
    for j, line in enumerate(lines2):
        if re.match(r"^\s*```", line):
            in_code = not in_code
            out2.append(line)
            if not in_code:
                nxt = lines2[j + 1] if j + 1 < len(lines2) else ""
                if nxt.strip() != "":
                    out2.append("")
            continue
        out2.append(line)
        if not in_code:
            if re.match(r"^\s*-\s+", line) or re.match(r"^\s*1\.\s+", line):
                nxt = lines2[j + 1] if j + 1 < len(lines2) else ""
                if nxt.strip() != "" and not (
                    re.match(r"^\s*-\s+", nxt) or re.match(r"^\s*1\.\s+", nxt)
                ):
                    out2.append("")

    # Trim trailing excess blank lines (at most one)
    while len(out2) >= 2 and out2[-1].strip() == "" and out2[-2].strip() == "":
        out2.pop()

    return "\n".join(out2) + "\n"


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="Normalize markdown files")
    parser.add_argument(
        "--root",
        default=os.getcwd(),
        help="Workspace root; defaults to CWD",
    )
    parser.add_argument(
        "--targets",
        nargs="+",
        required=True,
        help="List of markdown files (relative to root) to normalize",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Do not write changes; just report diffs",
    )
    args = parser.parse_args(argv)

    root = args.root
    targets = args.targets

    changes: Dict[str, str] = {}
    for rel in targets:
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            changes[rel] = "missing"
            continue
        original = read(path)
        aggressive = os.path.basename(rel) != "README.md"
        normalized = normalize_markdown(original, aggressive_wrap=aggressive)
        if normalized != original:
            if not args.check:
                write(path, normalized)
            changes[rel] = "updated"
        else:
            changes[rel] = "no changes"

    # Print a compact report
    for rel, status in changes.items():
        print(f"{rel}: {status}")

    # Exit non-zero if check mode and updates would occur
    if args.check and any(s == "updated" for s in changes.values()):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
