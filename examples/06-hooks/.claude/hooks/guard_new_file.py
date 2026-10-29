"""PreToolUse(Write) フック: 新しいファイルを作る前に確認を求める。

既存ファイルの上書きは確認しない。~/.claude 配下と一時フォルダは対象外。
"""
import json
import os
import sys
import tempfile
from pathlib import Path

# 確認しないフォルダ（Claude がメモなどを保存する場所）
EXEMPT_DIRS = [Path.home() / ".claude", Path(tempfile.gettempdir())]


def is_exempt(path: Path) -> bool:
    resolved = path.resolve()
    return any(resolved.is_relative_to(d.resolve()) for d in EXEMPT_DIRS)


def main() -> None:
    # Claude Code から、ツールの情報が JSON で標準入力に渡される
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return  # 読めないときは何もしない（通常の権限チェックに任せる）
    if data.get("tool_name") != "Write":
        return
    raw = (data.get("tool_input") or {}).get("file_path", "")
    if not raw:
        return
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = Path(data.get("cwd") or os.getcwd()) / path
    if path.exists() or is_exempt(path):
        return  # 既存ファイル・対象外のフォルダ → 何も出力しない
    # 新しいファイル → 「確認する（ask）」と Claude Code に返す
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": f"New file: {path}",
    }}))


if __name__ == "__main__":
    main()
