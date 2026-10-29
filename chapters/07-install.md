# 第7章 全プロジェクトへの導入 — ~/.claude に置く

## 1. この章のゴール

作った設定を `~/.claude/` に置いて、すべてのプロジェクトで使えるようにできる。

## 2. しくみ

第1〜6章では、設定を練習用フォルダの中（`~/claude-practice/`）に置いた。同じものを**ホームフォルダの `.claude/`**（`~/.claude/`）に置くと、どのプロジェクトを開いても読み込まれる。

```text
~/claude-practice/                    ~/.claude/
├── CLAUDE.md                ──▶      ├── CLAUDE.md
└── .claude/                          ├── rules/markdown.md
    ├── rules/markdown.md    ──▶      ├── skills/explain/SKILL.md
    ├── skills/explain/      ──▶      ├── agents/reviewer.md
    ├── agents/reviewer.md   ──▶      ├── hooks/guard_new_file.py
    ├── hooks/               ──▶      └── settings.json  ← ★既存の内容に追記
    └── settings.json        ──▶
```

`CLAUDE.md` だけは置き場所が変わる（練習用フォルダでは直下、`~/.claude/` では `.claude/` の中）。ほかは同じ構成のままコピーする。

どのプロジェクトを開いても、次の 2 つが両方読み込まれる。

```text
① ~/.claude/                ← すべてのプロジェクト共通（この章で入れる）
② <プロジェクト>/.claude/   ← そのプロジェクト固有の設定（あれば）
```

| 種類 | ①と②の両方にあるとき |
|---|---|
| CLAUDE.md・rules | 両方読み込まれる |
| skills・agents | 両方使える（同じ名前の agents は、プロジェクト側が優先） |
| settings.json の permissions・hooks | **合算**される（両方の deny が効く、など） |

出典: https://code.claude.com/docs/en/memory, https://code.claude.com/docs/en/settings, https://code.claude.com/docs/en/sub-agents

## 3. 作ってみる

作るもの: `~/.claude/` の中のファイル（第1〜6章で作ったものと同じ）

[examples/07-install/](../examples/07-install/) に、`~/.claude/` と同じ構成の完成例を用意してある。この中身を `~/.claude/` に入れる。

```text
examples/07-install/          ~/.claude/ に入れると
├── CLAUDE.md            ──▶  ~/.claude/CLAUDE.md
├── rules/markdown.md    ──▶  ~/.claude/rules/markdown.md
├── skills/explain/      ──▶  ~/.claude/skills/explain/
├── agents/reviewer.md   ──▶  ~/.claude/agents/reviewer.md
├── hooks/guard_new_file.py ▶ ~/.claude/hooks/guard_new_file.py
├── settings.windows.json ┐
└── settings.mac.json     ┴▶  自分の OS のほうを ~/.claude/settings.json にする
```

> ⚠ `~/.claude/` は、すべてのプロジェクトに影響する。先に今の中身を確かめ、`settings.json` はバックアップを取ってから変える。

1. **今の `~/.claude/` を確かめる。** すでに `CLAUDE.md` や `settings.json` がある場合は、上書きせずに中身を書き足す。`settings.json` は、先にコピーを取っておく（例: `settings.json.bak`）。
2. **`examples/07-install/` の中身を `~/.claude/` に入れる。** `CLAUDE.md`・`rules/`・`skills/`・`agents/`・`hooks/` を、同じ構成のまま入れる。第1〜6章で自分用に変えたものがあれば、練習用フォルダのほうから入れてもよい。
3. **`settings.json` を用意する。** 自分の OS のファイル（`settings.windows.json` か `settings.mac.json`）を `~/.claude/settings.json` として置く。すでに `settings.json` がある場合は、`permissions` と `hooks` の部分だけを書き足す。
4. **hook のパスを書き換える。** `settings.json` の `<.claude フォルダのパス>` を、`settings.json` を置いたフォルダのパスに書き換える（次の節）。

### hook のパスを書き換える

完成例の `settings.json` では、hook のパスが次のようになっている。

```json
"args": ["<.claude フォルダのパス>/hooks/guard_new_file.py"]
```

`<.claude フォルダのパス>` を、**`settings.json` を置いたフォルダ（`.claude` フォルダ）のパス**に書き換える。パスは VS Code で調べるのが確実。

1. VS Code のエクスプローラーで `~/.claude/settings.json` を右クリックし、「パスのコピー」を選ぶ。
2. コピーしたパスの最後の `settings.json` を消すと、`.claude` フォルダのパスになる。
3. **Windows の場合は、`\` を `/` に置き換える**（JSON の中では `\` をそのまま書けないため）。

| | コピーしたパス | 書き換えた後の `args` |
|---|---|---|
| Windows | `C:\Users\yamada\.claude\settings.json` | `"C:/Users/yamada/.claude/hooks/guard_new_file.py"` |
| Mac | `/Users/yamada/.claude/settings.json` | `"/Users/yamada/.claude/hooks/guard_new_file.py"` |

> ⚠ **書き換え忘れ・間違いに注意**: パスが間違っていると、hook のスクリプトが見つからず、Claude がファイルを書こうとするたびに**毎回ブロック**される（Python がスクリプトを見つけられないときに返す終了コード 2 が、hook では「ブロック」の意味になるため）。しかも、すべてのプロジェクトで起きる。書き換えたら、すぐに「試してみる」で確かめる。

**なぜ第6章と書き方が違うのか**: 第6章では `${CLAUDE_PROJECT_DIR}`（セッションを始めたプロジェクトのフォルダ）を使った。`~/.claude/hooks/` に置いた hook は、どのプロジェクトからでも同じ場所を指す必要があるので、`${CLAUDE_PROJECT_DIR}` は使えない。`settings.json` と同じフォルダを指す変数は用意されていないので、パスをそのまま書く。

> 💡 すでにある `settings.json` に書き足すときは、JSON の形が崩れないように気をつける（カンマの位置など）。崩れると設定全体が読めなくなる。

## 4. 試してみる

練習用フォルダ**ではない**、新しいフォルダを作って試す（例: `~/claude-check`）。VS Code でそのフォルダを開き、新しいセッションで次を試す。

| # | やること | 成功したときの結果 |
|---|---|---|
| 1 | `/context` を入力する | Memory files に `~/.claude/CLAUDE.md` が表示される |
| 2 | `/hooks` を入力する | PreToolUse に Write の hook が表示される |
| 3 | `/` を入力する | 一覧に `explain` が表示される |
| 4 | 「今使えるサブエージェントを一覧にして」と頼む | 一覧に `reviewer` が含まれる |
| 5 | 「todo.md に明日やることを3つ書いて」と頼む | 「New file」の確認ダイアログが出る（hook）。承認すると、チェックボックスと日付の形式で書かれる（rules） |

> 💡 5 の rules（`markdown.md`）は `paths` 付きなので、`/context` には表示されない。書かれた結果で確かめる。

うまくいかないときは、`/status` の Setting sources に User settings（`~/.claude/settings.json`）が表示されているかを確かめる。

**元に戻したいとき**: `~/.claude/` に入れたファイルを消し、`settings.json` をバックアップから戻す。

## 5. よくある疑問

<details>
<summary>Q. ~/.claude に置くと、Claude がホームフォルダの全ファイルに触れるようにならない？</summary>

ならない。`~/.claude/` は、Claude Code が**設定を読みに行く場所**で、Claude が触れるファイルの範囲とは関係ない。

Claude が確認なしで触れる範囲を決めるのは、**VS Code で開いたフォルダ**（作業フォルダ）。その外にあるファイルを読み書きしようとすると、確認が出る。

| VS Code で開くフォルダ | Claude が確認なしで触れる範囲 |
|---|---|
| ✅ `~/projects/app-a/` | app-a の中だけ |
| ⚠ `~/Documents/` | Documents の下のすべて |
| ⚠ ホームフォルダ | ホームフォルダの下のすべて |

作業するプロジェクトのフォルダを 1 つずつ開くのが安全。

出典: https://code.claude.com/docs/en/security
</details>

<details>
<summary>Q. プロジェクトにも .claude/ の設定があったら、どうなる？</summary>

両方とも読み込まれる（「しくみ」の表を参照）。

- CLAUDE.md は両方読み込まれる。内容が矛盾すると、どちらに従うかは決まっていない。`~/.claude/CLAUDE.md` に「プロジェクトの CLAUDE.md と矛盾したら、プロジェクトを優先する」と書いておくと迷わない。
- permissions のリストは合算される。プロジェクト側で `~/.claude/` の deny を取り消すことはできない。
</details>

<details>
<summary>Q. ~/.claude の設定は、サブエージェントにも効く？</summary>

効く。サブエージェントも CLAUDE.md や rules を読み込む。たとえば、`~/.claude/rules/` に「Python の公開関数には型ヒントを付ける」というルールがあると、reviewer の指摘に「あなたの Python ルールでも、公開関数には型ヒントとなっています」のように出てくることがある。

第4章で、人によって reviewer の出力が少しずつ違うのは、これも理由の 1 つ。
</details>

<details>
<summary>Q. settings.json と hooks フォルダは同じ場所にあるのに、hook のパスを相対パス（hooks/guard_new_file.py）で書いてはダメ？</summary>

ダメ。hook のコマンドは、settings.json の場所ではなく、**Claude が今作業しているプロジェクトのフォルダ**で実行される。相対パスは、そのフォルダからたどられる。

```text
~/projects/app-a を開いて作業中に、"hooks/guard_new_file.py" と書いた hook が動くと
  探しに行く場所: ~/projects/app-a/hooks/guard_new_file.py   ← ない
  本当の場所:     ~/.claude/hooks/guard_new_file.py
```

開くプロジェクトによって、たどる先が変わってしまう。だから `.claude` フォルダのパスをそのまま書く。

出典: https://code.claude.com/docs/en/hooks
</details>

<details>
<summary>Q. 導入した後、Claude がファイルを作ろうとすると毎回エラーになる</summary>

hook のパスが間違っている可能性が高い。エラーに `can't open file` や `No such file or directory` と出ていれば、hook のスクリプトが見つかっていない。

1. `~/.claude/settings.json` の `args` のパスを確かめる（`<.claude フォルダのパス>` のままになっていないか、Windows で `\` が残っていないか）。
2. そのパスに `guard_new_file.py` が本当にあるかを、VS Code のエクスプローラーで確かめる。

すぐに作業を続けたいときは、`~/.claude/settings.json` から `hooks` の部分を消せば、元どおりファイルを作れるようになる。
</details>

<details>
<summary>Q. 毎回手でコピーするのは面倒。自動化できる？</summary>

できる。設定の本体を 1 つのフォルダ（Git で管理するとよい）にまとめておき、次のことをするスクリプトを作る。

1. CLAUDE.md・rules・skills・agents・hooks を `~/.claude/` にコピーする
2. `~/.claude/settings.json` に、バックアップを取ってから `permissions` と `hooks` を書き足す（既存の設定は残す）
3. hook のパスを、`.claude` フォルダの実際のパスに書き換える
4. コピーしたものを記録しておき、解除するときは自分で入れたものだけを消す

`--dry-run`（何が変わるかを表示するだけ）を付けられるようにしておくと安心。本体を編集したら、スクリプトを実行し直すだけで反映できる。
</details>

## 6. 自分用に変える

**全プロジェクト共通にするものと、プロジェクトごとにするものを分けてみる。**

| 置き場所 | 向いているもの | 例 |
|---|---|---|
| `~/.claude/` | 自分の好み。どのプロジェクトでも変わらないもの | About me、答え方、explain、秘密情報の deny |
| `<プロジェクト>/.claude/` | そのプロジェクトの決まり。チームで共有したいもの | 使っている言語のルール、テストの書き方、整形の hook |

今の `~/.claude/` の中身を見て、プロジェクトごとにしたほうがよいものがあれば、そのプロジェクトの `.claude/` に移す。

## 7. 確認問題

<details>
<summary>Q1. ~/.claude/settings.json の hook のパスに `${CLAUDE_PROJECT_DIR}` を使わないのはなぜ？</summary>

`${CLAUDE_PROJECT_DIR}` は、セッションを始めたフォルダ（開いているプロジェクト）に置き換わる。`~/.claude/hooks/` に置いた hook は、どのプロジェクトからでも同じ場所を指す必要があるので、`.claude` フォルダのパスをそのまま書く。
</details>

<details>
<summary>Q2. ~/.claude/ に設定を入れた後、Claude が確認なしで触れるファイルの範囲は広がる？</summary>

広がらない。範囲を決めるのは VS Code で開いたフォルダ。`~/.claude/` は設定を読みに行く場所にすぎない。
</details>

<details>
<summary>Q3. ~/.claude/settings.json に deny を書いた。あるプロジェクトの .claude/settings.json で、その deny を取り消せる？</summary>

取り消せない。permissions のリストは合算されるので、どちらかに deny があれば効く。
</details>
