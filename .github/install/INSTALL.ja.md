# インストール方法

<details>
<summary><strong>Antigravity (<code>agy</code>)</strong></summary>

### インストール

```bash
agy plugin install https://github.com/ayghri/i-have-adhd
```

### 確認

```bash
agy plugin list
```

### 更新

```bash
agy plugin uninstall i-have-adhd
agy plugin install https://github.com/ayghri/i-have-adhd
```

### アンインストール

```bash
agy plugin uninstall i-have-adhd
```

インストールしたまま無効にする場合は、`agy plugin disable i-have-adhd` を実行します。

### 常時有効（任意）

`~/.gemini/GEMINI.md` に追加します：

```markdown
## 出力スタイル

読み手には ADHD があります。すぐ行動に移せるよう、すべての回答を次のように構成してください：

1. 回答または次の行動から始める。コマンド、パス、スニペットを先に示す。
2. 複数手順の作業には番号を付け、1 ステップにつき 1 つの明確な行動にする。
3. 2 分以内にできる次の行動を 1 つ示して終える。
4. 新しい問題を挙げる前に、現在の問題を終わらせる。
5. 各ターンで進捗を言い直す（「5 ステップ中 3 ステップ完了」）。
6. 所要時間は具体的な単位で示し、「少し」とは言わない。
7. 変更後は、何が動くようになったかを示す。
8. エラーは場所、原因、修正方法を淡々と示す。
9. リストは最大 5 項目にする。
10. 前置き、要約、締めの言葉を入れない。

例外：説明を求められた場合は十分に説明する。破壊的な操作の前には確認する。修正に 3 回失敗したら止まり、疑わしい前提を明示する。依頼が曖昧なら短い質問を 1 つする。
```

</details>

<details>
<summary><strong>Claude Code</strong></summary>

### インストール

```bash
claude plugin marketplace add ayghri/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

`/i-have-adhd` と入力します。

### 確認

```bash
claude plugin list
```

### 更新

```bash
claude plugin marketplace update i-have-adhd
```

### アンインストール

```bash
claude plugin uninstall i-have-adhd
claude plugin marketplace remove i-have-adhd
```

インストールしたまま無効にする場合は、`claude plugin disable i-have-adhd` を実行します。

### 常時有効（任意）

`SessionStart` フックが各セッションの開始時に完全なルールセットを読み込むため、`/i-have-adhd` は不要です：

```bash
touch ~/.claude/.i-have-adhd-always
```

オンデマンドに戻す場合：

```bash
rm ~/.claude/.i-have-adhd-always
```

フックはフラグファイルが存在する場合のみ動作するため、プラグインをインストールしただけでは何も変わりません。設定ディレクトリを移動している場合は `$CLAUDE_CONFIG_DIR` が使われます。「stop adhd mode」と入力すれば、現在のセッションでは無効にできます。

</details>


<details>
<summary><strong>Codex</strong></summary>

### インストール

```bash
codex plugin marketplace add ayghri/i-have-adhd --ref main
codex plugin add i-have-adhd@i-have-adhd
```

`$i-have-adhd` を明示的に入力して有効化します。Codex がこのスキルを自動で呼び出すことはありません。

### 確認

```bash
codex plugin list
```

### 更新

```bash
codex plugin marketplace upgrade i-have-adhd
codex plugin remove i-have-adhd
codex plugin add i-have-adhd@i-have-adhd
```

### アンインストール

```bash
codex plugin remove i-have-adhd
codex plugin marketplace remove i-have-adhd
```

### 常時有効（任意）

`~/.codex/AGENTS.md` に追加します：

```markdown
## 出力スタイル

読み手には ADHD があります。すぐ行動に移せるよう、すべての回答を次のように構成してください：

1. 回答または次の行動から始める。コマンド、パス、スニペットを先に示す。
2. 複数手順の作業には番号を付け、1 ステップにつき 1 つの明確な行動にする。
3. 2 分以内にできる次の行動を 1 つ示して終える。
4. 新しい問題を挙げる前に、現在の問題を終わらせる。
5. 各ターンで進捗を言い直す（「5 ステップ中 3 ステップ完了」）。
6. 所要時間は具体的な単位で示し、「少し」とは言わない。
7. 変更後は、何が動くようになったかを示す。
8. エラーは場所、原因、修正方法を淡々と示す。
9. リストは最大 5 項目にする。
10. 前置き、要約、締めの言葉を入れない。

例外：説明を求められた場合は十分に説明する。破壊的な操作の前には確認する。修正に 3 回失敗したら止まり、疑わしい前提を明示する。依頼が曖昧なら短い質問を 1 つする。
```

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

Gemini CLI にはプラグインマーケットプレイスがないため、ネイティブな方法は 2 つあります。呼び出すまで無効な**カスタムコマンド**（オプトイン）と、インストール後は常時有効な**拡張機能**です。コマンド方式がこのスキルの既定の動作に合うため、すべてのセッションでルールを使いたい場合を除き、こちらを選んでください。

### インストール (command, opt-in)

```bash
mkdir -p ~/.gemini/commands
curl -fsSL https://raw.githubusercontent.com/ayghri/i-have-adhd/main/skills/i-have-adhd/agents/gemini.toml \
  -o ~/.gemini/commands/i-have-adhd.toml
```

新しいセッションを開始して `/i-have-adhd` と入力します。そのセッション中は有効のままです。

### インストール (extension, always-on)

```bash
gemini extensions install https://github.com/ayghri/i-have-adhd
```

拡張機能は完全なスキルをインポートする `GEMINI.md` を読み込むため、最初のメッセージからルールが適用されます。`git` のインストールが必要です。

### 確認

```bash
gemini extensions list          # 拡張機能方式
ls ~/.gemini/commands           # command route: i-have-adhd.toml present
```

または、セッションで `/` と入力し、`i-have-adhd` が一覧にあることを確認します。

### 更新

```bash
gemini extensions update i-have-adhd    # 拡張機能方式
# コマンド方式：上記の curl を再実行
```

### アンインストール

```bash
gemini extensions uninstall i-have-adhd    # 拡張機能方式
rm ~/.gemini/commands/i-have-adhd.toml     # command route
```

</details>

<details>
<summary><strong>GitHub Copilot (VS Code and Copilot CLI)</strong></summary>

Copilot は Agent Skills をネイティブに読み取るため、同じ `SKILL.md` を変換なしで使えます。プロジェクトでは `.github/skills/`、`.claude/skills/`、`.agents/skills/`、グローバルでは `~/.copilot/skills/`、`~/.claude/skills/`、`~/.agents/skills/` を検索します。

### インストール

```bash
npx skills add ayghri/i-have-adhd -a github-copilot        # このプロジェクト
npx skills add ayghri/i-have-adhd -a github-copilot -g     # すべてのプロジェクト
```

CLI を使わない場合は、Copilot が検索するいずれかのディレクトリにスキルフォルダーをコピーします：

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.copilot/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.copilot/skills/
```

### 確認

チャット入力欄に `/` と入力し、`i-have-adhd` が表示されることを確認します。または：

```bash
npx skills list
npx skills ls -g    # グローバルにインストールした場合
```

### 更新

```bash
npx skills update i-have-adhd
```

または、`git pull` の後にフォルダーを再度コピーします。

### アンインストール

```bash
npx skills remove i-have-adhd
```

または、配置先の skills ディレクトリから `i-have-adhd` フォルダーを削除します。

### 有効化に関する注意

Copilot は `disable-model-invocation` を尊重します。Claude Code と同様、スキルを呼び出すまで何も適用されません（[#60](https://github.com/ayghri/i-have-adhd/pull/60) で検証済み）。

### 常時有効（任意）

以下のブロックをプロジェクトの `.github/copilot-instructions.md` に追加します（Copilot はすべてのチャットでこれを読み込みます）：

```markdown
## 出力スタイル

読み手には ADHD があります。すぐ行動に移せるよう、すべての回答を次のように構成してください：

1. 回答または次の行動から始める。コマンド、パス、スニペットを先に示す。
2. 複数手順の作業には番号を付け、1 ステップにつき 1 つの明確な行動にする。
3. 2 分以内にできる次の行動を 1 つ示して終える。
4. 新しい問題を挙げる前に、現在の問題を終わらせる。
5. 各ターンで進捗を言い直す（「5 ステップ中 3 ステップ完了」）。
6. 所要時間は具体的な単位で示し、「少し」とは言わない。
7. 変更後は、何が動くようになったかを示す。
8. エラーは場所、原因、修正方法を淡々と示す。
9. リストは最大 5 項目にする。
10. 前置き、要約、締めの言葉を入れない。

例外：説明を求められた場合は十分に説明する。破壊的な操作の前には確認する。修正に 3 回失敗したら止まり、疑わしい前提を明示する。依頼が曖昧なら短い質問を 1 つする。
```

</details>

<details>
<summary><strong>Hermes</strong></summary>

### インストール

```bash
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd
```

`/i-have-adhd` と入力します。 The skill installs into `~/.hermes/skills/` and is exposed as a slash command at the next session start.

先に内容を確認したい場合は、このリポジトリをスキルソース（「tap」）として追加してから、検索してインストールします：

```bash
hermes skills tap add ayghri/i-have-adhd
hermes skills search adhd
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd
```

### 確認

```bash
hermes skills list
```

### 更新

```bash
hermes skills update i-have-adhd
```

### アンインストール

```bash
hermes skills uninstall i-have-adhd
```

tap も削除する場合は、`hermes skills tap remove ayghri/i-have-adhd` を実行します。

### 常時有効（任意）

作業ディレクトリの `AGENTS.md`（Hermes が作業ディレクトリごとに読み込みます）、または全セッション用のペルソナ `SOUL.md` に追加します：

```markdown
## 出力スタイル

読み手には ADHD があります。すぐ行動に移せるよう、すべての回答を次のように構成してください：

1. 回答または次の行動から始める。コマンド、パス、スニペットを先に示す。
2. 複数手順の作業には番号を付け、1 ステップにつき 1 つの明確な行動にする。
3. 2 分以内にできる次の行動を 1 つ示して終える。
4. 新しい問題を挙げる前に、現在の問題を終わらせる。
5. 各ターンで進捗を言い直す（「5 ステップ中 3 ステップ完了」）。
6. 所要時間は具体的な単位で示し、「少し」とは言わない。
7. 変更後は、何が動くようになったかを示す。
8. エラーは場所、原因、修正方法を淡々と示す。
9. リストは最大 5 項目にする。
10. 前置き、要約、締めの言葉を入れない。

例外：説明を求められた場合は十分に説明する。破壊的な操作の前には確認する。修正に 3 回失敗したら止まり、疑わしい前提を明示する。依頼が曖昧なら短い質問を 1 つする。
```

</details>

<details>
<summary><strong>Kimi Code CLI</strong></summary>

### インストール

Kimi Code セッションを開始してから、次を実行します：

1. `/plugins` を実行する。
2. **Custom** を選ぶ。
3. `https://github.com/ayghri/i-have-adhd` を貼り付けて Enter を押す。
4. **Trust and install** を選ぶ。

slash コマンド `/skill:i-have-adhd` を使って、このスキルを明示的に呼び出します。

### 更新

Kimi Code セッションで `/plugins` を実行し、**I Have ADHD** にカーソルを合わせて `R` を押します。

### アンインストール

Kimi Code セッションで `/plugins` を実行し、**I Have ADHD** にカーソルを合わせて `D` を押します。

</details>


<details>
<summary><strong>Pi</strong></summary>

Pi はこのリポジトリをネイティブパッケージとして検出します。`extensions/` がセッション永続モードを提供し、`skills/` が Agent Skills のエントリーポイントを提供します。

### インストール

```bash
pi install https://github.com/ayghri/i-have-adhd
```

新しい Pi セッションを開始します。現在のセッションで ADHD 向け出力を切り替えます：

```text
/i-have-adhd
```

モードが有効な間、フッターに `● ADHD ON` と表示されます。もう一度コマンドを実行するとオフになります。明示的に指定することもできます：

```text
/i-have-adhd on
/i-have-adhd off
stop adhd mode
```

Claude Code のフックと同様、この拡張はルールセットをリクエストごとにシステムプロンプトへ書き込む代わりに、会話に一度だけ追加し、コンパクションでルールセットが失われた後も再度追加します。

既存の Agent Skills コマンドはエイリアスとして引き続き使えます：

```text
/skill:i-have-adhd
```

デフォルトでモードを有効にした状態で新しい Pi セッションを開始します：

```bash
pi --adhd
```

### 確認

```bash
pi list
```

GitHub パッケージが一覧にあることを確認し、`/i-have-adhd` と入力してフッターに `● ADHD ON` が表示されることを確認します。

### 更新

```bash
pi update https://github.com/ayghri/i-have-adhd
```

または、`pi update --extensions` で固定されていないすべての Pi パッケージを更新します。

### アンインストール

```bash
pi remove https://github.com/ayghri/i-have-adhd
```

### 常時有効（任意）

Pi のエージェント設定ディレクトリにフラグファイルを作成します：

```bash
touch ~/.pi/agent/.i-have-adhd-always
```

この拡張は、新規・再開・フォーク・再読み込みのいずれのセッションでもこのフラグを確認します。現在のセッションで保存された選択はこのデフォルトより優先されるため、「stop adhd mode」を実行すればそのセッションでは無効のままになります。

オンデマンドに戻す場合：

```bash
rm ~/.pi/agent/.i-have-adhd-always
```

`PI_CODING_AGENT_DIR` が設定されている場合は、代わりにそのディレクトリに `.i-have-adhd-always` を置いてください。フラグを変更した後は `/reload` を実行するか、新しいセッションを開始してください。

</details>


<details>
<summary><strong>Qwen Code</strong></summary>

### インストール

```bash
qwen extensions install ayghri/i-have-adhd
```

Qwen Code は GitHub の短縮表記をサポートし、このリポジトリをネイティブ拡張機能としてインストールします。拡張機能は `skills/` 配下のスキルを検出します。

スキルを明示的に呼び出すには `/i-have-adhd` を入力します。拡張機能をインストールしただけでは、スキルを呼び出すまで出力は変わりません。

### 確認

```bash
qwen extensions list
```

次に新しい Qwen Code セッションを開始し、以下を実行します：

```text
/skills
```

一覧に `i-have-adhd` が表示されることを確認します。

### 更新

```bash
qwen extensions update i-have-adhd
```

### アンインストール

```bash
qwen extensions uninstall i-have-adhd
```

</details>

<details>
<summary><strong>Zed</strong></summary>

Zed の Agent は Agent Skills をネイティブに読み取るため、同じ `SKILL.md` を変換なしで使えます（従来の「Rules」は Skills と `AGENTS.md` の指示に置き換えられました）。

### インストール

Agent Panel で Skills マネージャーを開き、**Create skill from URL**（コマンドパレットでは `agent: create skill from url`）を選択して、次を貼り付けます：

```
https://github.com/ayghri/i-have-adhd/blob/main/skills/i-have-adhd/SKILL.md
```

すべてのプロジェクトで使う場合は **User** スコープ、1 つだけなら **Project** スコープに保存します。その後、Agent Panel で `/i-have-adhd` と入力します。

ファイルシステムを使う場合は、リポジトリをクローンし、ユーザーの skills ディレクトリにスキルフォルダーを配置します：

```bash
git clone https://github.com/ayghri/i-have-adhd
cp -R i-have-adhd/skills/i-have-adhd ~/.config/zed/skills/
```

### 確認

Agent Panel で Skills マネージャーを開き、`i-have-adhd` が一覧にあることを確認します。または、`/` と入力して表示されることを確認します。

### 更新

同じ URL から再インポート（上書き）するか、`git pull` の後にフォルダーを再度コピーします。

### アンインストール

Skills マネージャーから `i-have-adhd` を削除するか、`~/.config/zed/skills/i-have-adhd` を削除します。

### 常時有効（任意）

個人用の `~/.config/zed/AGENTS.md` に追加します：

```markdown
## 出力スタイル

読み手には ADHD があります。すぐ行動に移せるよう、すべての回答を次のように構成してください：

1. 回答または次の行動から始める。コマンド、パス、スニペットを先に示す。
2. 複数手順の作業には番号を付け、1 ステップにつき 1 つの明確な行動にする。
3. 2 分以内にできる次の行動を 1 つ示して終える。
4. 新しい問題を挙げる前に、現在の問題を終わらせる。
5. 各ターンで進捗を言い直す（「5 ステップ中 3 ステップ完了」）。
6. 所要時間は具体的な単位で示し、「少し」とは言わない。
7. 変更後は、何が動くようになったかを示す。
8. エラーは場所、原因、修正方法を淡々と示す。
9. リストは最大 5 項目にする。
10. 前置き、要約、締めの言葉を入れない。

例外：説明を求められた場合は十分に説明する。破壊的な操作の前には確認する。修正に 3 回失敗したら止まり、疑わしい前提を明示する。依頼が曖昧なら短い質問を 1 つする。
```

</details>

<details>
<summary><strong>Cursor、OpenCode、Amp、その他の agent-skills 対応環境</strong></summary>

Agent Skills を読み取るすべての環境で動作します。`-a <agent>` を使用するエージェントに置き換えてください。

### インストール

```bash
npx skills add ayghri/i-have-adhd                  # this workspace
npx skills add ayghri/i-have-adhd -g               # すべてのプロジェクト
npx skills add ayghri/i-have-adhd -a cursor -y     # one agent only
npx skills add ayghri/i-have-adhd -a opencode -y
```

新しいエージェントチャットで `/i-have-adhd` と入力します。

CLI を使わない場合は、エージェントが検索するパスにスキルフォルダーをコピーします：

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.cursor/skills     # Cursor。OpenCode は .agents/skills、その他はエージェント固有のパスを使用
cp -R i-have-adhd/skills/i-have-adhd ~/.cursor/skills/
```

### 確認

```bash
npx skills list
npx skills ls -g    # グローバルにインストールした場合
```

### 更新

```bash
npx skills update i-have-adhd
npx skills update -g    # グローバルにインストールした場合
```

### アンインストール

```bash
npx skills remove i-have-adhd
npx skills remove i-have-adhd -g    # グローバルにインストールした場合
```

### 常時有効（任意）

これをエージェントの永続ルールファイルに貼り付けます。Cursor：**Settings → Rules → User Rules**、または `.cursor/rules/` 配下のプロジェクトルールで `alwaysApply: true` を指定します。OpenCode：`~/.config/opencode/AGENTS.md`。

```markdown
## 出力スタイル

読み手には ADHD があります。すぐ行動に移せるよう、すべての回答を次のように構成してください：

1. 回答または次の行動から始める。コマンド、パス、スニペットを先に示す。
2. 複数手順の作業には番号を付け、1 ステップにつき 1 つの明確な行動にする。
3. 2 分以内にできる次の行動を 1 つ示して終える。
4. 新しい問題を挙げる前に、現在の問題を終わらせる。
5. 各ターンで進捗を言い直す（「5 ステップ中 3 ステップ完了」）。
6. 所要時間は具体的な単位で示し、「少し」とは言わない。
7. 変更後は、何が動くようになったかを示す。
8. エラーは場所、原因、修正方法を淡々と示す。
9. リストは最大 5 項目にする。
10. 前置き、要約、締めの言葉を入れない。

例外：説明を求められた場合は十分に説明する。破壊的な操作の前には確認する。修正に 3 回失敗したら止まり、疑わしい前提を明示する。依頼が曖昧なら短い質問を 1 つする。
```
</details>


## 有効化の仕組み

1. **インストール済み、未呼び出し。** Claude Code、Qwen Code、Codex では、明示的に呼び出すまで何も起きません。Claude Code と Qwen Code は `SKILL.md` の `disable-model-invocation: true` を、Codex は `agents/openai.yaml` の `policy.allow_implicit_invocation: false` を尊重します。その他の環境では、起動時に各スキルの説明を読み込み、自動で有効化する場合があります。
2. **明示的に呼び出す。** Claude Code と Qwen Code では `/i-have-adhd`、Codex では `$i-have-adhd` を入力します。そのセッションでルールが有効になります。「stop adhd mode」または「normal mode」で無効にできます。
3. **`~/.claude/.i-have-adhd-always` を作成する**（Claude Code）。`SessionStart` フックが、すべてのセッションで最初のメッセージから完全なルールセットを読み込みます。
4. **上記の常時有効スニペットを追加する**（その他の環境）。中核となるルールをエージェントの永続コンテキストに保持します。

Claude Code、Qwen Code、Codex では中間状態はありません。有効にしていなければ無効です。

## トラブルシューティング

**`/i-have-adhd` が自動補完に表示されない。** エージェントを再起動してください。プラグインのインデックスは起動時に読み込まれます。

**常時有効フラグが効かない。** プラグインを更新（`claude plugin marketplace update i-have-adhd`）して再起動してください。フックは起動時に読み込まれ、フラグには `hooks/hooks.json` を含むバージョンが必要です。

**`claude plugin marketplace add` が失敗する。** `owner/repo` 形式を使用してください。ローカルパスは `.claude-plugin/` ではなく、リポジトリのルートを指す必要があります。

**インストールしたが回答にまだ前置きが入る。** 新しいセッションを開いてください。それでも逸脱する場合は、`skills/i-have-adhd/SKILL.md` の文言をより厳密にしてください。

**別のルールを使いたい。** Fork して `skills/i-have-adhd/SKILL.md` を編集し、自分のコピーに切り替えます：

```bash
claude plugin uninstall i-have-adhd            # 先に上流のコピーを削除：
claude plugin marketplace remove i-have-adhd   # fork と上流はどちらも同じ名前を使用
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

再起動してから、`/i-have-adhd` をもう一度呼び出します。

**`npx skills add` の後にスキルが見つからない。** 新しいエージェントチャットを開始してください。スキルはセッション開始時にインデックス化されます。フォルダーがエージェントの検索先（Cursor は `~/.cursor/skills/`、OpenCode は `.agents/skills/`）に配置され、frontmatter の `name` がフォルダー名と一致していることを確認してください。
