# 第5章 permissions — 許可・確認・禁止を強制する

## 1. この章のゴール

settings.json の permissions で、コマンドやファイルの読み取りを確認・禁止できる。

## 2. しくみ

第1〜4章で作ったものは、どれも Claude が読んで従う「**お願い**」だった。permissions は、Claude Code（プログラム）が判定する「**強制**」。

```text
Claude:「Bash ツールで git push を実行したい」
   │  依頼するだけ（Claude は PC を直接操作できない）
   ▼
Claude Code: settings.json の permissions と照らし合わせる
   ├─ deny に一致 → 実行しない
   ├─ ask  に一致 → 確認ダイアログを出す
   ├─ allow に一致 → 確認なしで実行する
   └─ どれにも一致しない → 初期設定の動き
```

| 種類 | 動き | 使いどころ |
|---|---|---|
| `deny` | 実行させない | 絶対にやらせたくないこと |
| `ask` | 毎回確認ダイアログを出す | やってよいかを毎回自分で判断したいこと |
| `allow` | 確認なしで実行する | 毎回聞かれると面倒な安全なこと |

同じ操作に複数のルールが一致したら、**deny → ask → allow の順に優先**される。

| 項目 | 内容 |
|---|---|
| 書く場所 | `.claude/settings.json`（そのプロジェクト）、`~/.claude/settings.json`（すべてのプロジェクト。第7章） |
| 読み込まれるとき | セッション開始時。セッション中にファイルを変更しても、自動で読み込み直される |
| 誰が判断するか | **Claude Code**（プログラム）。Claude は読まない |
| トークンへの影響 | なし（Claude に渡されないため） |
| 強さ | **強制** |

### ルールの書き方

`ツール名(対象)` の形で書く。

| ルール | 意味 |
|---|---|
| `Bash(git push)` | `git push` というコマンド（引数なし） |
| `Bash(git push *)` | `git push` で始まるコマンド（`git push origin main` など） |
| `Read(**/.env)` | どのフォルダにある `.env` でも、読むこと |
| `Edit(src/**)` | `src/` フォルダの下のファイルを編集すること |

出典: https://code.claude.com/docs/en/permissions, https://code.claude.com/docs/en/settings

## 3. 作ってみる

作るもの: `~/claude-practice/.claude/settings.json`

1. 練習用フォルダの `.claude/` の中に `settings.json` を作り、次の内容を書く（完成例: [examples/05-permissions/.claude/settings.json](../examples/05-permissions/.claude/settings.json)）。

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
  }
}
```

| ルール | 意味 |
|---|---|
| `Read(**/.env)` の deny | `.env`（API キーやパスワードを書くことが多いファイル）を読ませない |
| `rm` の ask | ファイルを削除する前に確認する |

> 💡 **Windows の場合**: Claude Code は Bash ツールのほかに **PowerShell ツール**も使うことがある。`Bash(...)` だけだと、PowerShell で実行されたときに止まらないので、`PowerShell(...)` のルールも書いている。PowerShell ではファイルの削除に `Remove-Item` も使うので、それも書いた。Mac では PowerShell のルールは使われないが、書いておいても問題ない。

> 💡 settings.json は厳密な JSON。コメントや、最後の要素の後ろのカンマ（`,`）は書けない。

2. 保存すると、実行中のセッションにもすぐ反映される。念のため、新しいセッションを開いて試すと確実。

## 4. 試してみる

先に、試すためのダミーのファイルを作っておく。ターミナルで練習用フォルダ（`~/claude-practice/`）に移動して、次を実行する。

```bash
echo "test" > dummy.txt
echo "TEST=1" > .env
```

中身はどちらもダミーなので、万が一ルールが効かなくても問題ない。

| # | やること | 成功したときの結果 |
|---|---|---|
| 1 | `/status` を入力する | Setting sources に Shared project settings（`~/claude-practice/.claude/settings.json`）が表示される |
| 2 | 「dummy.txt を削除して」と頼む | 確認ダイアログが出る（ask）。拒否しても承認してもよい |
| 3 | 「.env の中身を読んで、内容を教えて」と頼む | Read ツールでの読み取りが拒否される（deny） |

> 💡 3 では、Read ツールが拒否された後、Claude が `cat .env` のような**コマンドで読もうとする**ことがある。`Read(...)` のルールは Read ツールを止めるもので、Bash のコマンドは止めない。これは permissions の限界の 1 つ（第8章「既知の制限」）。中身はダミーなので問題ない。

## 5. よくある疑問

<details>
<summary>Q. CLAUDE.md に「git push しない」と書くのと、何が違う？</summary>

| | CLAUDE.md | permissions |
|---|---|---|
| 誰が判断するか | Claude（読んで従う） | Claude Code（プログラム） |
| 守られるか | 守られないことがある（指示しだいで破られる） | 必ず効く |
| 向いていること | 方針や好み（答え方・確認の仕方） | 絶対にやらせたくないこと |

両方に書くのがおすすめ。CLAUDE.md に書いておくと、Claude は最初からやろうとしない。permissions に書いておくと、もし Claude がやろうとしても止まる。
</details>

<details>
<summary>Q. 「Write ツール」「Bash ツール」ってなに？</summary>

Claude は、あなたの PC を直接操作できない。「このファイルを書きたい」「このコマンドを実行したい」と**ツールの使用を依頼し**、それを Claude Code が実行する。permissions が「強制」できるのは、すべての操作がこの Claude Code を通るから。

| ツール | やること | ルールの例 |
|---|---|---|
| Read | ファイルを読む | `Read(**/.env)` |
| Write | ファイルを新しく作る、または丸ごと上書きする | `Write(docs/**)` |
| Edit | ファイルの一部を書き換える | `Edit(src/**)` |
| Bash | コマンドを実行する | `Bash(git push *)` |
| PowerShell | PowerShell のコマンドを実行する（Windows） | `PowerShell(Remove-Item *)` |
| WebFetch | Web ページを読む | `WebFetch(domain:example.com)` |

VS Code の Claude Code のパネルでは、「Write hello.py」「Bash git status」のように、使ったツールが折りたたまれた行で表示される。
</details>

<details>
<summary>Q. settings.json はいつ読み込まれる？ 複数あったらどうなる？</summary>

セッション開始時に読み込まれ、その後もファイルが監視されている。変更すると、**実行中のセッションにも自動で反映**される。

settings.json は複数の場所に置ける。上にあるものほど優先される。

| 優先 | 場所 | 範囲 |
|---|---|---|
| 1 | 組織の管理設定 | 会社が配布するもの |
| 2 | `.claude/settings.local.json` | そのプロジェクト・自分だけ（Git で共有しない） |
| 3 | `.claude/settings.json` | そのプロジェクト（Git で共有できる） |
| 4 | `~/.claude/settings.json` | すべてのプロジェクト |

`deny` や `ask` のような**リストは、上書きではなく合算**される。`~/.claude/settings.json` の deny と `.claude/settings.json` の deny は、両方とも効く。

出典: https://code.claude.com/docs/en/settings
</details>

<details>
<summary>Q. VS Code の「コミット」「同期」ボタンで git push したときも止まる？</summary>

止まらない。permissions が効くのは、**Claude が Claude Code を通して実行するとき**だけ。

```text
① VS Code のボタンで push
   あなた ──▶ VS Code ──▶ git          ← Claude Code は関わらない

② Claude に push させる
   あなた ──▶ Claude ──▶ Claude Code ──▶ git
                          ↑ permissions が効くのはここ
```

自分の操作も含めて止めたい場合は、Git 自体の仕組み（Git の hook や、GitHub のブランチ保護）を使う。
</details>

## 6. 自分用に変える

### 例: 破壊的な git コマンドを止める

変更を取り消せなくなる git コマンドは、deny に入れておくと安心。

**Mac の場合**

```json
"deny": [
  "Bash(git push --force*)",
  "Bash(git push -f*)",
  "Bash(git reset --hard*)",
  "Bash(git clean -f*)",
  "Bash(git checkout -- *)",
  "Bash(git branch -D *)"
]
```

**Windows の場合**（Bash に加えて PowerShell でも止める）

```json
"deny": [
  "Bash(git push --force*)",
  "Bash(git push -f*)",
  "Bash(git reset --hard*)",
  "Bash(git clean -f*)",
  "Bash(git checkout -- *)",
  "Bash(git branch -D *)",
  "PowerShell(git push --force*)",
  "PowerShell(git push -f*)",
  "PowerShell(git reset --hard*)",
  "PowerShell(git clean -f*)",
  "PowerShell(git checkout -- *)",
  "PowerShell(git branch -D *)"
]
```

| コマンド | 何が起きるか |
|---|---|
| `git push --force` / `-f` | リモートの履歴を上書きする。ほかの人のコミットが消えることがある |
| `git reset --hard` | コミットしていない変更をすべて捨てる |
| `git clean -f` | Git で管理していないファイルを削除する |
| `git checkout -- <ファイル>` | そのファイルの、コミットしていない変更を捨てる |
| `git branch -D` | マージしていないブランチも強制的に削除する |

- 自分で実行したいときは、Claude に頼まずにターミナルで実行する。Claude に実行させたい場面がある場合は、deny ではなく ask にする。
- `git push` 自体を止めたい場合は、`"Bash(git push)"` と `"Bash(git push *)"` を書く。

### そのほかの例

次のどれかをやってみる。

- **ask を足す**: パッケージの追加・削除の前に確認する。`"Bash(npm install *)"`、`"Bash(pip install *)"` など
- **deny を足す**: 読ませたくないファイルを足す。`"Read(~/.ssh/**)"`（SSH の鍵）、`"Read(**/.env.*)"`（`.env.local` など）
- **allow を足す**: 毎回確認されて面倒な、安全なコマンドを足す。`"Bash(git status)"`、`"Bash(git diff *)"` など

足したら、それぞれ試して効いているかを確かめる。

## 7. 確認問題

<details>
<summary>Q1. 同じコマンドが deny と allow の両方に一致した。どうなる？</summary>

実行されない。deny → ask → allow の順に優先される。
</details>

<details>
<summary>Q2. `Read(**/.env)` を deny に書いた。Claude が `cat .env` を実行したら止まる？</summary>

止まらない。`Read(...)` は Read ツールのルールで、Bash のコマンドには一致しない。止めたい場合は、CLAUDE.md で「.env は読まない」とお願いしておく、第6章の hooks でコマンドの中身を調べる、などを組み合わせる。
</details>

<details>
<summary>Q3. permissions を書いた settings.json は、Claude（AI）が読んでいる？</summary>

読んでいない。読んで判定しているのは Claude Code（プログラム）。だから「お願い」ではなく「強制」になり、トークンも使わない。
</details>
