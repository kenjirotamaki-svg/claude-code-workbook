# 第0章 はじめに・準備

## 1. この章のゴール

練習用のフォルダを用意し、Claude Code にいまどんな設定が読み込まれているかを確認できる。

## 2. Claude Code の設定の全体像

この教材では、次の 6 つを 1 つずつ作る。

```text
            ┌──────────── お願い（Claude が読んで従う）────────────┐
            │                                                      │
 第1章  CLAUDE.md   … 毎回読み込まれる個人ルール                    │
 第2章  rules       … 特定のファイルを触るときだけ読み込まれるルール │
 第3章  skills      … 呼び出せる手順・知識                          │
 第4章  agents      … 作業を任せる別の Claude                       │
            └──────────────────────────────────────────────────────┘
            ┌──────────── 強制（Claude Code が必ず実行する）────────┐
 第5章  permissions … コマンドやファイルの読み取りを確認・禁止する  │
 第6章  hooks       … ツールを使う前後に、スクリプトを自動で動かす  │
            └──────────────────────────────────────────────────────┘
 第7章  ~/.claude/ に置いて、すべてのプロジェクトで使えるようにする
```

- **Claude**（AI）と **Claude Code**（あなたの PC で動くプログラム）は別のもの。
- 「お願い」は Claude が読んで従う指示なので、守られないこともある。
- 「強制」は Claude Code というプログラムが判定するので、必ず効く。

この違いが、教材全体を通して大事になる。

## 3. 準備する

### 前提

| 必要なもの | 確認のしかた |
|---|---|
| VS Code と Claude Code（拡張機能） | VS Code のサイドバーに Claude のアイコンがある |
| Git | ターミナルで `git --version` |
| Python 3（第6章で使う） | Windows: `python --version` / Mac: `python3 --version` |

### 練習用フォルダを作る

ターミナル（Windows は Git Bash、Mac はターミナル）で次を実行する。

```bash
mkdir ~/claude-practice
```

- フォルダの名前と場所は自由。ただし、**ほかのプロジェクトの中には作らない**。

### VS Code で開く

1. VS Code で「ファイル」→「フォルダーを開く」から `claude-practice` を開く。
2. Claude Code のパネルを開く。
3. フォルダを信頼するかを聞かれたら、承認する。

## 4. 試してみる

Claude Code のパネルで、次のコマンドを入力してみる。今は何も作っていないので、「何もない」ことを確認しておくのが目的。

| やること | 見るところ | 今の状態 |
|---|---|---|
| `/context` を入力する | Memory files | 練習用フォルダの直下（`~/claude-practice/CLAUDE.md`）の CLAUDE.md は表示されない |
| `/status` を入力する | Setting sources | 練習用フォルダの設定（Shared project settings。`~/claude-practice/.claude/settings.json`）は表示されない |
| `/hooks` を入力する | 登録されている hook | 練習用フォルダの hook は登録されていない |
| 「今使えるサブエージェントを一覧にして」と頼む | Claude の返答 | 練習用フォルダのサブエージェント（`~/claude-practice/.claude/agents/`）はない |

> 💡 この教材で作る設定は、第7章までは練習用フォルダ（`~/claude-practice/`）の中だけに置く。練習用フォルダ以外の場所の設定が表示されるのは問題ない（下の「よくある疑問」を参照）。

## 5. よくある疑問

<details>
<summary>Q. まだ何も作っていないのに、/context の Memory files にファイルが表示されている</summary>

練習用フォルダ以外の場所にある設定が読み込まれている。よくあるのは次のもの。

| 表示されるファイル | 何か |
|---|---|
| `~/.claude/CLAUDE.md` | すべてのプロジェクトで読み込まれる、あなた個人のルール（第7章で扱う） |
| `MEMORY.md` など | Claude が自動で書き留めているメモ（auto memory） |
| 組織の CLAUDE.md | 会社が配布している設定（ある場合） |

どれもそのままでかまわない。ただし、第1章の「比べてみる」では、これらの影響も混ざることを覚えておく。
</details>

<details>
<summary>Q. /status の Setting sources に、すでに設定ファイルが表示されている</summary>

練習用フォルダ以外の設定ファイルが読み込まれている。

| 表示 | ファイル | 何か |
|---|---|---|
| User settings | `~/.claude/settings.json` | すべてのプロジェクトで使われる、あなた個人の設定（第7章で扱う） |
| Managed settings | 組織が配布した設定 | 会社が管理している設定（ある場合） |

練習用フォルダの設定（Shared project settings）は、第5章で `~/claude-practice/.claude/settings.json` を作ると表示されるようになる。
</details>

<details>
<summary>Q. /hooks に、すでに hook が登録されている</summary>

`~/.claude/settings.json` や、インストールしたプラグインで登録されている hook が表示されている。練習用フォルダの hook は、第6章で作る。
</details>

<details>
<summary>Q. サブエージェントの一覧に、作っていないものが出てくる</summary>

Claude Code に最初から入っている組み込みのサブエージェント（Explore・Plan・general-purpose など）や、`~/.claude/agents/`・プラグインのサブエージェントが表示されている。練習用フォルダのサブエージェントは、第4章で作る。
</details>

<details>
<summary>Q. /agents と入力したら「The /agents wizard has been removed.」と表示された</summary>

サブエージェントを対話的に作る `/agents` の画面は、なくなった。サブエージェントは、`.claude/agents/`（そのプロジェクト）か `~/.claude/agents/`（すべてのプロジェクト）にファイルを直接置いて作る（第4章）。使えるサブエージェントを確かめたいときは、Claude に「今使えるサブエージェントを一覧にして」と頼む。
</details>

## 6. 進め方のヒント

- 各章は「**作る → 試す → 疑問を解消する**」の 1 サイクルで完結する。
- 設定を変えたら、**新しいセッション**を開いて試すのが確実（読み込まれるのはセッション開始時のものが多い）。
- 完成例は `examples/` にある。自分で書くのが大変なら、コピーしてから書き換えてよい。
- 途中でやめても、そこまでで作ったものは使える状態になっている。
