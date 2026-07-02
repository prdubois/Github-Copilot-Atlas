#!/usr/bin/env python3
"""
Atlas Agent Prompt Synchronizer

Takes a master Atlas agent file and updates all other Atlas*.agent.md files
in the same folder to match the master's content, preserving only the 
model: line from each target file.

Usage:
    python sync_atlas_agents.py <master_file>
    python sync_atlas_agents.py AtlasGPT.agent.md
    python sync_atlas_agents.py AtlasGPT.agent.md --dry-run
"""

import argparse
import re
from pathlib import Path


def extract_model_line(content: str) -> str:
    """Extract the model: line from YAML frontmatter."""
    match = re.search(r'^model:.*$', content, re.MULTILINE)
    if not match:
        raise ValueError("No 'model:' line found in frontmatter")
    return match.group(0)


def replace_model_line(content: str, new_model_line: str) -> str:
    """Replace the model: line in content with a new one."""
    return re.sub(r'^model:.*$', new_model_line, content, count=1, flags=re.MULTILINE)


def sync_agents(master_path: str, dry_run: bool = False):
    master = Path(master_path)
    if not master.exists():
        print(f"ERROR: Master file not found: {master}")
        return

    master_content = master.read_text(encoding='utf-8')
    master_model = extract_model_line(master_content)
    folder = master.parent

    # Find all Atlas*.agent.md files in the same folder
    atlas_files = sorted(folder.glob("Atlas*.agent.md"))
    targets = [f for f in atlas_files if f.name != master.name]

    if not targets:
        print(f"No other Atlas*.agent.md files found in {folder}")
        return

    print(f"Master: {master.name}")
    print(f"Master model: {master_model}")
    print(f"Found {len(targets)} target file(s) to sync:")
    print()

    for target in targets:
        target_content = target.read_text(encoding='utf-8')
        try:
            target_model = extract_model_line(target_content)
        except ValueError:
            print(f"  SKIP {target.name} — no model: line found")
            continue

        # Take master content, replace master's model line with target's model line
        synced_content = replace_model_line(master_content, target_model)

        if synced_content == target_content:
            print(f"  OK   {target.name} — already in sync")
        else:
            if dry_run:
                print(f"  WOULD UPDATE {target.name} — {target_model}")
            else:
                target.write_text(synced_content, encoding='utf-8')
                print(f"  UPDATED {target.name} — {target_model}")

    print()
    print("Done." if not dry_run else "Dry run complete. No files modified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync Atlas agent prompts from a master file.")
    parser.add_argument("master", help="Path to the master Atlas agent file")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    args = parser.parse_args()
    sync_agents(args.master, args.dry_run)
