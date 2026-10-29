# 第2章 rules — 特定のファイルを触るときだけのルール

## 1. この章のゴール

`paths` を使って、特定の種類のファイルを扱うときだけ読み込まれるルールを作れる。

## 2. しくみ

```text
あなた:「todo.md に明日やることを書いて」
   │
   ▼
Claude: Write ツールで todo.md を書こうとする
   │
   ▼
Claude Code: ファイルのパス "todo.md" を、各ルールの paths と照らし合わせる
   │  "**/*.md" に一致 → markdown.md の中身を Claude への指示として追加する
   ▼
Claude: markdown.md のルール（チェックボックス・日付の形式）に沿って書く
```

| 項目 | 内容 |
|---|---|
| 読み込まれるとき | `paths` に一致するファイルを、Claude が Read / Write / Edit ツールで扱ったとき（`cat` などで 1 ファイルを読んだときも） |
| `paths` を書かない場合 | セッション開始時に毎回読み込まれる（CLAUDE.md と同じ扱い） |
| 置き場所 | `.claude/rules/`（そのプロジェクトだけ）、`~/.claude/rules/`（すべてのプロジェクト。第7章） |
| 誰が判断するか | **Claude Code**（プログラム）がパスを機械的に照らし合わせる。Claude が「読むべきか」を判断しているのではない |
| トークンへの影響 | 一致するファイルを扱うまで読み込まれないので、CLAUDE.md に全部書くより少なくて済む |
| 強さ | **お願い**。読み込まれた後は、CLAUDE.md と同じく Claude が読んで従う指示 |

rules は「実行」されるものではない。中身の文章が、Claude への指示に**追加される**だけ。

出典: https://code.claude.com/docs/en/memory

## 3. 作ってみる

作るもの: `~/claude-practice/.claude/rules/markdown.md`

1. 練習用フォルダの中に `.claude/rules/` フォルダを作る（`~/claude-practice/.claude/rules/`）。
2. その中に `markdown.md` を作り、次の内容を書く（完成例: [examples/02-rules/.claude/rules/markdown.md](../examples/02-rules/.claude/rules/markdown.md)）。

```markdown
---
paths:
  - "**/*.md"
---

# Markdown ファイルの書き方
- 見出しは `##` から始める（`#` はファイルのタイトルの 1 つだけ）。
- TODO はチェックボックスで書く: `- [ ] やること`
- 日付は `YYYY-MM-DD` の形で書く。
- 表やコードブロックの前後には空行を入れる。
```

| 部分 | 意味 |
|---|---|
| `---` で囲んだ部分 | frontmatter（設定の部分）。**ファイルの 1 行目**から書く |
| `paths:` | このルールを読み込む対象のファイル。`"**/*.md"` は「どのフォルダにある `.md` ファイルでも」という意味 |
| それより下 | Claude へのルール本文 |

3. 保存したら、Claude Code で**新しいセッション**を開く。

> 💡 `.claude` のように `.` で始まるフォルダは、Mac の Finder や Windows のエクスプローラーでは隠しフォルダとして表示されないことがある。VS Code のエクスプローラーなら表示される。

## 4. 試してみる

`paths` 付きのルールは、読み込まれても `/context` には表示されない。そこで、**書かれた結果**で確かめる。結果だけでは判断しにくいので、確かめるあいだだけ「目印」のルールを 1 行足しておく。

1. `markdown.md` の最後に、次の 1 行を一時的に足す。

```markdown
- ファイルの最終行に `<!-- markdown rule -->` と書く。
```

2. 新しいセッションを開き、次を試す。

| # | やること | 成功したときの結果 |
|---|---|---|
| 1 | 「todo.md に明日やることを3つ書いて」と頼む | TODO が `- [ ] 〜` のチェックボックスで、日付が `2026-10-23` のような形で書かれ、最終行に `<!-- markdown rule -->` がある |
| 2 | 新しいセッションで「todo.txt に明日やることを3つ書いて」と頼む | `.txt` は `paths` に一致しないので、最終行に `<!-- markdown rule -->` が**ない** |

3. 確かめたら、目印の 1 行を消しておく。

> 💡 1 では、第1章の CLAUDE.md（新しいファイルを作る前に確認する）が効いて、作る前に確認されるはず。承認して進める。

> 💡 チェックボックスや日付の形式は、ルールがなくても Claude がたまたま同じ形で書くことがある。目印の行は、ルールがなければまず書かれないので、読み込まれたかどうかをはっきり区別できる。

## 5. よくある疑問

<details>
<summary>Q. rules は何をきっかけに読み込まれる？</summary>

`paths` があるルールは、`paths` に一致するファイルを Claude が **Read / Write / Edit ツールで扱ったとき**に読み込まれる。`cat` や `head` で 1 つのファイルを読んだときも読み込まれる。

逆に言うと、**ファイルを触るまでは読み込まれない**。たとえば「Markdown の書き方を教えて」と聞いただけでは、`.md` ファイルを扱っていないので読み込まれない。

判断しているのは Claude Code（プログラム）で、ファイルのパスとパターンを機械的に照らし合わせているだけ。

出典: https://code.claude.com/docs/en/memory
</details>

<details>
<summary>Q. CLAUDE.md に書くのと何が違う？</summary>

| | CLAUDE.md | rules（`paths` あり） |
|---|---|---|
| 読み込まれるとき | 毎回 | 一致するファイルを扱ったときだけ |
| トークン | 毎回かかる | 必要なときだけかかる |
| 向いている内容 | どんな作業でも守ってほしいこと | 特定の種類のファイルだけのルール |

Markdown の書き方は、Python のコードを書いているときには必要ない。必要なときだけ読み込まれるように rules に分けると、CLAUDE.md を短く保てる。
</details>

<details>
<summary>Q. paths にはどんな書き方ができる？</summary>

| パターン | 一致するもの |
|---|---|
| `**/*.md` | どのフォルダにある `.md` ファイルでも |
| `*.md` | プロジェクトの直下にある `.md` ファイルだけ |
| `docs/**/*` | `docs/` フォルダの下にあるすべてのファイル |
| `src/**/*.{ts,tsx}` | `src/` の下の `.ts` と `.tsx` ファイル |

複数のパターンは、`paths:` の下に `- "..."` を並べて書く。

出典: https://code.claude.com/docs/en/memory
</details>

<details>
<summary>Q. .md 以外のファイルしか触っていないのに、markdown.md が効いている</summary>

frontmatter（`---` で囲んだ部分）が正しく書けていない可能性がある。`paths` が認識されないと、毎回読み込まれるルールとして扱われることがある。次を確かめる。

- 1 行目が `---` で始まっているか（前に空行や文字がないか）
- `paths:` の下の行が、スペースで字下げされているか
- パターンを `"` で囲んでいるか
</details>

## 6. 自分用に変える

次のどちらかをやってみる。

- **markdown.md にルールを 1 つ足す**。例:「箇条書きの文末に句点（。）を付けない」「表の見出し行は太字にしない」
- **別の種類のファイル用のルールを作る**。例: `~/claude-practice/.claude/rules/python.md` に `paths: "**/*.py"` と「コメントは日本語で書く」を書き、Python のファイルを作らせて確かめる

## 7. 確認問題

<details>
<summary>Q1. `paths: "**/*.md"` のルールは、「README の書き方のコツを教えて」と聞いただけで読み込まれる？</summary>

読み込まれない。rules が読み込まれるのは、一致するファイルを Claude が Read / Write / Edit などで扱ったとき。質問しただけでは、ファイルを扱っていない。
</details>

<details>
<summary>Q2. rules を読み込むかどうかを決めているのは、Claude と Claude Code のどちら？</summary>

Claude Code（プログラム）。ファイルのパスと `paths` のパターンを機械的に照らし合わせている。
</details>

<details>
<summary>Q3. 「Python のコードを書くときは型ヒントを付ける」というルール。CLAUDE.md と rules のどちらに書くのがよい？</summary>

rules（`paths: "**/*.py"`）。Python のファイルを扱うときだけ必要なルールなので、毎回読み込まれる CLAUDE.md に書くとトークンの無駄になる。
</details>
