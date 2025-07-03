#!/usr/bin/env python3
import re
import subprocess
import sys

CONVENTIONAL_PATTERN = r"^(feat|fix|chore|docs|style|refactor|perf|test)(\([\w\-]+\))?: .+"
ISSUE_REF_PATTERN = r"#\d{1,6}"

def get_commit_messages(base: str, head: str) -> list[str]:
    """Get commit messages between base and head (exclusive)"""
    try:
        result = subprocess.run(
            ["git", "log", "--pretty=%s", f"{base}..{head}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to get commit messages: {e.stderr}")
        sys.exit(1)

def validate_commit(message: str) -> list[str]:
    """Validate a single commit message and return error list"""
    errors = []
    if not re.match(CONVENTIONAL_PATTERN, message):
        errors.append("Not following Conventional Commits format.")
    if not re.search(ISSUE_REF_PATTERN, message):
        errors.append("Missing issue reference (e.g., #1234).")
    return errors

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    head = sys.argv[2] if len(sys.argv) > 2 else "HEAD"

    print(f"🔍 Validating commits from {base} to {head}...\n")

    messages = get_commit_messages(base, head)
    all_valid = True

    for i, msg in enumerate(messages, start=1):
        errors = validate_commit(msg)
        if errors:
            all_valid = False
            print(f"❌ Commit {i}: \"{msg}\"")
            for err in errors:
                print(f"   - {err}")
        else:
            print(f"✅ Commit {i}: \"{msg}\" passed.")

    if not all_valid:
        print("\n🚫 Some commits are invalid. Please fix them before merging.")
        sys.exit(1)
    else:
        print("\n🎉 All commits are valid!")

if __name__ == "__main__":
    main()
