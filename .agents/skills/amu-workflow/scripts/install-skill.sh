#!/usr/bin/env bash
set -euo pipefail

TARGET_PATH="${1:-$(pwd)}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_AI="$SKILL_ROOT/assets/scaffold/.ai"
TARGET_ROOT="$(cd "$TARGET_PATH" && pwd)"
TARGET_AI="$TARGET_ROOT/.ai"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

copied=0
backed_up=0
skipped=0

ensure_dir() {
  mkdir -p "$1"
}

copy_file_safe() {
  local source="$1"
  local destination="$2"
  local protect_existing="$3"
  ensure_dir "$(dirname "$destination")"
  if [[ -e "$destination" ]]; then
    if [[ "$protect_existing" == "true" ]]; then
      skipped=$((skipped + 1))
      echo "skip protected: $destination"
      return
    fi
    cp "$destination" "$destination.bak-$TIMESTAMP"
    backed_up=$((backed_up + 1))
  fi
  cp "$source" "$destination"
  copied=$((copied + 1))
}

ensure_dir "$TARGET_AI"
for dir in rules requirements playbooks archive tmp artifacts; do
  ensure_dir "$TARGET_AI/$dir"
done

for file in "$SOURCE_AI"/*; do
  [[ -f "$file" ]] || continue
  name="$(basename "$file")"
  protect="false"
  case "$name" in
    MEMORY.md|DECISIONS.md|HANDOFF.md) protect="true" ;;
  esac
  copy_file_safe "$file" "$TARGET_AI/$name" "$protect"
done

for dir in rules playbooks tmp artifacts; do
  for file in "$SOURCE_AI/$dir"/*; do
    [[ -f "$file" ]] || continue
    copy_file_safe "$file" "$TARGET_AI/$dir/$(basename "$file")" "false"
  done
done

for dir in requirements archive; do
  for file in "$SOURCE_AI/$dir"/*; do
    [[ -f "$file" ]] || continue
    destination="$TARGET_AI/$dir/$(basename "$file")"
    if [[ -e "$destination" ]]; then
      skipped=$((skipped + 1))
      echo "skip protected: $destination"
    else
      cp "$file" "$destination"
      copied=$((copied + 1))
    fi
  done
done

echo "amu-workflow scaffold installed."
echo "Target: $TARGET_AI"
echo "Copied: $copied"
echo "Backed up: $backed_up"
echo "Skipped protected existing files: $skipped"
