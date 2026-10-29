# 第3章 skills — 呼び出せる手順と知識

## 1. この章のゴール

skill を作って、`/名前` で呼び出したり、Claude に自動で使わせたりできる。

## 2. しくみ

skill は、**決まった手順や知識をまとめたもの**。呼び出し方は 2 通りある。

```text
① 自分で呼ぶ
   あなた: /explain HTTP
      │
      ▼
   Claude Code: explain の SKILL.md を読み込み、$ARGUMENTS を "HTTP" に置き換えて Claude に渡す
      │
      ▼
   Claude: SKILL.md の手順どおりに答える

② Claude が自動で使う
   あなた:「DNS とは？」
      │
      ▼
   Claude: 各 skill の description（説明文）を見て、「explain が合う」と判断する
      │
      ▼
   Claude: explain の SKILL.md を読み込み、その手順どおりに答える
```

| 項目 | 内容 |
|---|---|
| 読み込まれるとき | description（説明文）は毎回。本文は、`/名前` で呼んだとき、または Claude が必要と判断したときだけ |
| 置き場所 | `.claude/skills/<名前>/SKILL.md`（そのプロジェクトだけ）、`~/.claude/skills/<名前>/SKILL.md`（すべてのプロジェクト。第7章） |
| 誰が判断するか | 自分（`/名前`）、または **Claude**（description を見て判断） |
| トークンへの影響 | 普段は description だけなので小さい。本文は使うときだけ |
| 強さ | **お願い**。Claude が読んで従う指示 |

第2章の rules との違いは、**誰が読み込みを決めるか**。rules は Claude Code がファイルのパスで機械的に決める。skills は自分か Claude が決める。

出典: https://code.claude.com/docs/en/slash-commands

## 3. 作ってみる

作るもの: `~/claude-practice/.claude/skills/explain/SKILL.md`

1. 練習用フォルダの中に `.claude/skills/explain/` フォルダを作る（`~/claude-practice/.claude/skills/explain/`）。
2. その中に `SKILL.md` を作り、次の内容を書く（完成例: [examples/03-skills/.claude/skills/explain/SKILL.md](../examples/03-skills/.claude/skills/explain/SKILL.md)）。

```markdown
---
name: explain
description: 知らない用語や技術を、要約・図・例の3つで説明する。「〜とは？」「〜の違いは？」と聞かれたときに使う。
argument-hint: <説明してほしいこと>
---

次のことを説明する: $ARGUMENTS

空なら、何を説明してほしいかを聞く。

次の形で、短く説明する。
1. **要約** — 2〜3行で、何なのか・なぜ大事なのか。
2. **図** — テキストの図。横幅は70文字以内。
3. **例** — 身近なたとえか、最小限のコード・コマンド。
```

| 部分 | 意味 |
|---|---|
| `name` | skill の名前。`/explain` で呼び出せるようになる。フォルダ名と同じにする |
| `description` | **Claude が自動で使うかを判断する材料**。「何をするか」と「いつ使うか」を書く |
| `argument-hint` | `/explain` と入力したときに表示されるヒント |
| `$ARGUMENTS` | `/explain HTTP` の「HTTP」の部分に置き換わる |

3. 保存したら、Claude Code で**新しいセッション**を開く。

> 💡 1 つの skill は 1 つのフォルダになっている。手順が長くなったら、同じフォルダにテンプレートや参考資料のファイルを追加で置ける。

## 4. 試してみる

| # | やること | 成功したときの結果 |
|---|---|---|
| 1 | `/` を入力する | 一覧に `explain` が表示される |
| 2 | `/explain HTTP` と入力する | 要約・図・例の 3 つの形で説明される |
| 3 | `/` を付けずに「DNS とは？」と聞く | Claude が explain を自動で使い、同じ 3 つの形で説明される |

**勝手に使われないようにしてみる**: SKILL.md の frontmatter に次の 1 行を足し、新しいセッションで 3 をもう一度試す。

```markdown
disable-model-invocation: true
```

今度は Claude が自動で使わなくなり、普通の説明の形に戻る。`/explain DNS` と入力すれば、自分で呼び出すことはできる。確かめたら、この行を消しておく。

> 💡 3 で自動で使われないこともある。Claude は description を見て判断するので、description に「〜とは？と聞かれたときに使う」のように**いつ使うか**をはっきり書くと、使われやすくなる。

## 5. よくある疑問

<details>
<summary>Q. 「commands（スラッシュコマンド）」と skills は何が違う？</summary>

今の Claude Code では、commands は skills に統合されている。`.claude/commands/explain.md` と `.claude/skills/explain/SKILL.md` は、どちらも `/explain` になり、同じように動く。

| | `.claude/commands/<名前>.md` | `.claude/skills/<名前>/SKILL.md` |
|---|---|---|
| 形 | ファイル 1 枚 | フォルダ（補助ファイルも置ける） |
| `/名前` で呼べる | ✅ | ✅ |
| Claude が自動で使う | ✅（初期設定） | ✅（初期設定） |

古い形式の commands も引き続き使えるが、新しく作るなら skills がおすすめ（公式ドキュメントも skills を勧めている）。

出典: https://code.claude.com/docs/en/slash-commands
</details>

<details>
<summary>Q. skills も / で呼べるの？ 自動で使われるものだと思っていた</summary>

どちらもできる。初期設定では、**自分が `/名前` で呼ぶことも、Claude が自動で使うことも**できる。frontmatter で、どちらか片方だけにできる。

| 設定 | 自分が `/名前` で呼ぶ | Claude が自動で使う | 向いているもの |
|---|---|---|---|
| 何も書かない | ✅ | ✅ | 説明の仕方など、勝手に使われても困らないもの |
| `disable-model-invocation: true` | ✅ | ❌ | 自分が頼んだときだけ動いてほしい手順（例: 作業のまとめを作る） |
| `user-invocable: false` | ❌（一覧に出ない） | ✅ | 背景知識など、自分で呼ぶ必要がないもの |
</details>

<details>
<summary>Q. rules と skills は、どう使い分ける？</summary>

| | rules | skills |
|---|---|---|
| 読み込みを決めるのは | Claude Code（ファイルのパスで機械的に） | 自分（`/名前`）か Claude（話の内容で判断） |
| 確実さ | 一致するファイルを触れば必ず読み込まれる | Claude が使わないと判断することもある |
| 向いている内容 | 特定の種類のファイルを書くときの短いルール | 手順・説明の形・長めの知識 |

「`.md` を書くときは必ずこの形式」なら rules。「説明してと頼まれたら、この形で」なら skills。
</details>

## 6. 自分用に変える

ふだん Claude に**同じような頼み方を何度もしていること**を 1 つ、skill にしてみる。

例:

- `/summary` — 貼り付けたメモを「決まったこと・やること・未決事項」にまとめる
- `/error` — 貼り付けたエラーメッセージの原因と直し方を、可能性の高い順に 3 つ挙げる
- explain の形を変える — 「4. 注意点」を足す、例を Python のコードにする、など

作ったら、`/名前` で呼んで確かめる。勝手に使われると困るものには `disable-model-invocation: true` を付ける。

## 7. 確認問題

<details>
<summary>Q1. skill の description には、何を書くとよい？ それはなぜ？</summary>

「何をするか」と「いつ使うか」。Claude は description を見て、自動で使うかどうかを判断するため。
</details>

<details>
<summary>Q2. 「.md を書くときは、日付を必ず YYYY-MM-DD にする」。rules と skills のどちらが向いている？</summary>

rules。`.md` ファイルを扱えば必ず読み込まれる。skills だと、Claude が使わないと判断することがある。
</details>
