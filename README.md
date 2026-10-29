# Claude Code 設定ワークブック

Claude Code の設定（CLAUDE.md・rules・skills・agents・permissions・hooks）を、1つずつ作って試しながら理解し、最後に自分用の共通設定として全プロジェクトに導入するまでのハンズオン教材。

## 対象読者

- VS Code と Git を普段使っている
- Claude Code は使ったことがある、またはこれから使う
- Claude Code の設定ファイルは書いたことがない

Mac・Windows のどちらでも進められる。OS によって違うところは、その場で注記している。

## この教材を終えるとできること

- 自分用の共通設定を一から作り、`~/.claude/` に導入して、すべてのプロジェクトで使える
- 「お願い」（CLAUDE.md・rules・skills・agents）と「強制」（permissions・hooks）の違いを説明し、使い分けられる

## 目次

| 章 | テーマ | 作るもの | 目安 |
|---|---|---|---|
| [0](chapters/00-setup.md) | はじめに・準備 | 練習用フォルダ | 15分 |
| [1](chapters/01-claude-md.md) | CLAUDE.md | `CLAUDE.md` | 20分 |
| [2](chapters/02-rules.md) | rules | `rules/markdown.md` | 20分 |
| [3](chapters/03-skills.md) | skills | `skills/explain/SKILL.md` | 20分 |
| [4](chapters/04-agents.md) | agents | `agents/reviewer.md` | 30分 |
| [5](chapters/05-permissions.md) | permissions | `settings.json`（deny・ask） | 20分 |
| [6](chapters/06-hooks.md) | hooks | `hooks/guard_new_file.py` | 30分 |
| [7](chapters/07-install.md) | 全プロジェクトへの導入 | `~/.claude/` へのコピー | 20分 |
| [8](chapters/08-summary.md) | まとめ | — | 10分 |

## 各章の進め方

各章は同じ形になっている。

1. **この章のゴール** — 終わったらできること
2. **しくみ** — 図と、読み込まれるタイミング
3. **作ってみる** — 手順どおりにファイルを作る（完成例は `examples/`）
4. **試してみる** — 「これを頼んで、こうなれば成功」
5. **よくある疑問** — つまずきやすいところ
6. **自分用に変える** — 完成例を自分好みに書き換える
7. **確認問題** — 理解できたかを自分で確かめる

途中でやめても、そこまでで作ったものは使える状態になっている。

## フォルダ構成

```text
claude-code-workbook/
├── README.md       このファイル
├── chapters/       各章の本文
└── examples/       各章の完成例（練習用フォルダに置くときと同じパス構成。07-install だけは ~/.claude/ と同じ構成）
```

## 安全に試すために

- 演習は、必ず**練習用のフォルダ**で行う（第0章で作る）。
- 削除や読み取りの演習では、その場で作る**ダミーのファイル**だけを使う。
- 第7章までは、設定は練習用フォルダの `.claude/` の中だけに置くので、ほかのプロジェクトには影響しない。
