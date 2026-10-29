# 第6章 hooks — 条件付きで強制する・後処理をする

## 1. この章のゴール

hook を作って、ツールを使う前に条件付きで確認を出したり、使った後に処理を動かしたりできる。

## 2. しくみ

hook は、**Claude がツールを使う直前・直後などに、Claude Code が自動で実行するスクリプト**。permissions と同じく「**強制**」だが、permissions より細かい条件で判定できる。

```text
Claude:「Write ツールで hello.py を作りたい」
   │
   ▼
Claude Code: settings.json の hooks を見る
   PreToolUse（ツールを使う前）の matcher が "Write" に一致 → スクリプトを実行
   │  標準入力に JSON を渡す
   │  {"tool_name": "Write", "tool_input": {"file_path": ".../hello.py"}, ...}
   ▼
guard_new_file.py:
   ファイルはすでにある？ ── ある → 何も出力しない（いつもどおり進む）
                         └─ ない → {"permissionDecision": "ask", ...} を出力
   │
   ▼
Claude Code: 確認ダイアログを出す「New file: .../hello.py」
```

| 項目 | 内容 |
|---|---|
| 登録する場所 | settings.json の `hooks`（第5章と同じファイル） |
| 動くとき | 登録したイベントのとき（下の表） |
| 誰が判断するか | **Claude Code** がスクリプトを実行し、その出力に従う |
| トークンへの影響 | 基本的になし（スクリプトの出力を Claude に渡す場合だけ使う） |
| 強さ | **強制** |

### 主なイベント

| イベント | タイミング | 使い道の例 |
|---|---|---|
| `PreToolUse` | ツールを使う**前** | 条件付きで止める・確認する（この章で作る） |
| `PostToolUse` | ツールを使った**後** | ファイルを書いた後に自動で整形する |
| `SessionStart` | セッション開始時 | Claude に毎回伝えたい情報を渡す |
| `UserPromptSubmit` | あなたがメッセージを送ったとき | メッセージの内容をチェックする |

### hook が返せる判定（PreToolUse）

| 出力 | 意味 |
|---|---|
| `"permissionDecision": "deny"` | 実行させない |
| `"permissionDecision": "ask"` | 確認ダイアログを出す |
| 何も出力しない | 通常の権限チェックに任せる（**許可したことにはならない**） |

出典: https://code.claude.com/docs/en/hooks

### permissions との違い

permissions は、ツールの**引数の文字列**がパターンに一致するかで判定する。hook は**プログラムなので、何でも調べられる**。

たとえば「**新しいファイルを作るときだけ**確認したい」。Claude は、ファイルを新しく作るときも、既存のファイルを丸ごと書き直すときも、同じ Write ツールを使う。引数（ファイルのパス）だけでは区別できないので、permissions では書けない。hook なら、「そのファイルがすでにあるか」を調べてから判定できる。

## 3. 作ってみる

作るもの: `~/claude-practice/.claude/hooks/guard_new_file.py` と、`~/claude-practice/.claude/settings.json` への `hooks` の追記

1. 練習用フォルダの中に `.claude/hooks/` フォルダを作り（`~/claude-practice/.claude/hooks/`）、[examples/06-hooks/.claude/hooks/guard_new_file.py](../examples/06-hooks/.claude/hooks/guard_new_file.py) をコピーする。

中身のポイントは次のとおり（全体は完成例を見る）。

```python
# Claude Code から、ツールの情報が JSON で標準入力に渡される
data = json.loads(sys.stdin.buffer.read().decode("utf-8"))
...
if path.exists() or is_exempt(path):
    return  # 既存ファイル・対象外のフォルダ → 何も出力しない
# 新しいファイル → 「確認する（ask）」と Claude Code に返す
print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "permissionDecisionReason": f"New file: {path}",
}}))
```

| 工夫 | 理由 |
|---|---|
| `~/.claude` と一時フォルダは対象外 | Claude がメモなどを保存するたびに確認が出ないように |
| 標準入力を UTF-8 として読む | 日本語のファイル名でも文字化けしないように（特に Windows） |
| 読めない入力なら何もしない | hook のバグで作業が止まらないように |

2. 第5章で作った `~/claude-practice/.claude/settings.json` に、`hooks` を追記する。追記した後の全体は次のとおり。

**Windows の場合**（完成例: [settings.windows.json](../examples/06-hooks/.claude/settings.windows.json)）

```json
{
  "permissions": {
    "deny": [
      "Read(**/.env)"
    ],
    "ask": [
      "Bash(rm *)",
      "PowerShell(rm *)",
      "PowerShell(Remove-Item *)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/guard_new_file.py"]
          }
        ]
      }
    ]
  }
}
```

**Mac の場合**（完成例: [settings.mac.json](../examples/06-hooks/.claude/settings.mac.json)）: 上と同じで、`"command": "python"` を `"command": "python3"` にする。

| 部分 | 意味 |
|---|---|
| `"PreToolUse"` | ツールを使う前に動かす |
| `"matcher": "Write"` | Write ツールのときだけ動かす（`"Edit\|Write"` のように複数も書ける） |
| `"command"` と `"args"` | 実行するプログラムと引数。`python guard_new_file.py` を実行するのと同じ |
| `${CLAUDE_PROJECT_DIR}` | セッションを始めたフォルダ（ここでは `~/claude-practice`）に置き換わる |

> 💡 **OS による違い**: Windows には `python3` というコマンドがないことが多く、Mac には `python` がないことが多い。自分の PC で `python --version` / `python3 --version` のどちらが動くかで決める。

3. 保存したら、新しいセッションを開く。

## 4. 試してみる

| # | やること | 成功したときの結果 |
|---|---|---|
| 1 | `/hooks` を入力する | PreToolUse に Write の hook が表示される |
| 2 | 「hello.py を作って。中身は print('hello') だけ」と頼む | 理由に「**New file: …hello.py**」と書かれた確認ダイアログが出る。承認する |
| 3 | 「hello.py の中身を print('hi') に丸ごと書き直して」と頼む | 「New file」の確認ダイアログは**出ない**（hello.py はもうあるため） |

> 💡 2 では、確認が 2 回出ることがある。1 回目は、第1章の CLAUDE.md（ファイルを作る前に確認する）を読んだ Claude が**チャットで聞いてくる**もの（お願い）。2 回目は、hook による**確認ダイアログ**（強制）。お願いと強制の違いを、ここで並べて見られる。

> 💡 3 で、「New file」とは別の確認ダイアログが出ることがある。それは、Claude Code の権限モードによる通常の確認。「New file: …」と書かれていなければ、hook の確認ではない。

**スクリプトだけを試す**（任意）: hook は普通の Python スクリプトなので、ターミナルで JSON を渡して動きを確かめられる。練習用フォルダで次を実行する（Mac は `python3`）。

```bash
echo '{"tool_name": "Write", "tool_input": {"file_path": "new.txt"}}' | python .claude/hooks/guard_new_file.py
```

`new.txt` がまだなければ `"permissionDecision": "ask"` を含む JSON が表示される。`file_path` を `hello.py`（すでにあるファイル）にすると、何も表示されない。

## 5. よくある疑問

<details>
<summary>Q. permissions で足りないのは、どんなとき？</summary>

| やりたいこと | permissions | hook |
|---|---|---|
| `rm` の前に確認する | ✅ `Bash(rm *)` | できるが不要 |
| **新しいファイル**を作るときだけ確認する | ❌（引数の文字列だけでは判定できない） | ✅ ファイルがあるかを調べる |
| コマンドの**どこかに** `.env` が含まれていたら止める | ❌（先頭からのパターンしか書けない） | ✅ 文字列を調べる |
| ファイルを書いた**後**に整形する | ❌（止める・確認するしかできない） | ✅ PostToolUse |

単純な「このコマンドは確認・禁止」は permissions、条件付きの判定や後処理は hook、と使い分ける。
</details>

<details>
<summary>Q. ファイルを書くたびに、毎回 ruff format（コード整形）を実行したい。skill と hook のどちら？</summary>

hook（PostToolUse）。「毎回必ず同じコマンドを実行する」のは、AI が判断する必要のない機械的な作業。skill にすると Claude が使い忘れることがあるが、hook なら毎回確実に動く。

```json
"PostToolUse": [
  {
    "matcher": "Edit|Write",
    "hooks": [
      { "type": "command", "command": "python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/ruff_format.py"] }
    ]
  }
]
```

`ruff_format.py` では、標準入力の JSON から `tool_input.file_path` を取り出し、`.py` なら `ruff format <ファイル>` を実行する。

> 💡 VS Code の「保存時にフォーマット」は、Claude がファイルを書き換えたときには動かない（エディタで保存したことにならないため）。
</details>

<details>
<summary>Q. hook から skill を動かせる？</summary>

直接は動かせない。hook が実行するのは、コマンドやスクリプト。ただし、次の 2 つの方法がある。

| 方法 | 内容 |
|---|---|
| hook から Claude に一言伝える | hook の出力に `additionalContext` を入れると、その文章が Claude に渡る。Claude がそれを読んで skill を使うかは、Claude の判断 |
| skill の中に hook を書く | skill の frontmatter に `hooks:` を書くと、その skill が使われた時点から hook が有効になる |

出典: https://code.claude.com/docs/en/hooks
</details>

<details>
<summary>Q. Claude が `echo "x" > new.txt` のようなコマンドでファイルを作ったら？</summary>

この hook は動かない。`matcher` が `Write` なので、Bash ツールでのファイル作成は対象外。止めたい場合は、`"matcher": "Bash"` の hook を別に作り、コマンドの中身を調べる（第8章「既知の制限」）。
</details>

<details>
<summary>Q. hook が動いていないようだ</summary>

次の順に確かめる。

1. `/hooks` に登録が表示されているか。表示されなければ、settings.json の書き方（JSON の形、`hooks` の位置）を見直す。
2. 「スクリプトだけを試す」の手順で、スクリプト単体が動くか。`python` / `python3` が見つからないエラーなら、`"command"` を自分の PC で動く方に直す。
3. スクリプトのパスが正しいか（`~/claude-practice/.claude/hooks/guard_new_file.py` にあるか）。
</details>

## 6. 自分用に変える

次のどれかをやってみる。

- **確認しないフォルダを足す**: `EXEMPT_DIRS` に、確認なしで作ってよいフォルダ（例: 練習用フォルダの `tmp/`）を足す
- **SessionStart の hook を作る**: セッション開始時に Claude へ情報を渡す。SessionStart の hook がコマンドで出力した文章は、Claude に伝わる

```json
"SessionStart": [
  {
    "hooks": [
      { "type": "command", "command": "echo 今日は金曜日なので、作業の終わりに来週やることをまとめて。" }
    ]
  }
]
```

新しいセッションで何か聞いて、Claude がその内容を踏まえているかを確かめる。

## 7. 確認問題

<details>
<summary>Q1. 「新しいファイルを作るときだけ確認したい」を permissions ではなく hook で作ったのはなぜ？</summary>

Write ツールは、新しく作るときも既存のファイルを書き直すときも同じなので、引数の文字列だけでは区別できない。hook ならファイルがあるかを調べてから判定できる。
</details>

<details>
<summary>Q2. PreToolUse の hook が何も出力しなかった。そのツールの使用は許可される？</summary>

許可されたことにはならない。何も出力しないのは「hook としては何も言わない」という意味で、そのあと通常の権限チェック（permissions や権限モード）に任される。
</details>

<details>
<summary>Q3. 「ファイルを書くたびに整形したい」。PreToolUse と PostToolUse のどちらを使う？</summary>

PostToolUse。ファイルが書かれた**後**でないと、整形するファイルがまだできていない。
</details>
