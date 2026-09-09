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

インストールしたまま無効化する場合：`agy plugin disable i-have-adhd`

### 常時有効（任意）

`~/.gemini/GEMINI.md` に追加：

```markdown
## 出力スタイル

読み手はADHDです。すぐ行動に移せるよう、すべての回答を以下のように構成してください：

1. 答えや次に取るべき行動から始める：コマンド、パス、コードスニペットを最優先で提示する。
2. 複数ステップの作業には番号を付ける（1ステップにつき明確な行動1つ）。
3. 2分以内に完了できる具体的な次の行動を1つ提示して終える。
4. 新しい論点を挙げる前に、現在の問題を解決して終わらせる。
5. ターンごとに進捗を明記する（例: 「5ステップ中3ステップ完了」）。
6. 所要時間は「少し」などの曖昧な表現を使わず、分単位などの具体的な数値で示す。
7. 変更後は、何が動作するようになったかを目に見える形で示す。
8. エラーは場所・原因・修正方法を淡々と伝える（大げさな表現は避ける）。
9. リストは最大5項目までに抑える。
10. 前置き、要約、締めの挨拶は入れない。

例外規定：解説を求められた場合は十分に説明する。破壊的な操作を行う前には必ず確認を取る。修正に3回失敗した場合は一度停止し、前提条件のどこに誤りがあるかを指摘する。指示が曖昧な場合は短い質問を1つだけ行う。
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

インストールしたまま無効化する場合：`claude plugin disable i-have-adhd`

### 常時有効（任意）

`SessionStart` フックが毎セッション開始時に完全なルールセットを読み込むため、`/i-have-adhd` の入力が不要になります：

```bash
touch ~/.claude/.i-have-adhd-always
```

カスタムの Claude 設定ディレクトリを使用している場合は、代わりにそこにフラグファイルを作成します：

```bash
touch "$CLAUDE_CONFIG_DIR/.i-have-adhd-always"
```

手動呼び出し（オンデマンド）に戻す場合：

```bash
rm ~/.claude/.i-have-adhd-always
```

フックはフラグファイルが存在する場合にのみ動作するため、プラグインをインストールしただけでは動作に影響しません。現在のセッションでのみ無効化したい場合は `stop adhd mode` と入力してください。

</details>


<details>
<summary><strong>Codex</strong></summary>

### インストール

```bash
codex plugin marketplace add ayghri/i-have-adhd --ref main
codex plugin add i-have-adhd@i-have-adhd
```

`$i-have-adhd` と明示的に入力してスキルを呼び出します。Codex が自動で有効化することはありません。

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

`~/.codex/AGENTS.md` に追加：

```markdown
## 出力スタイル

読み手はADHDです。すぐ行動に移せるよう、すべての回答を以下のように構成してください：

1. 答えや次に取るべき行動から始める：コマンド、パス、コードスニペットを最優先で提示する。
2. 複数ステップの作業には番号を付ける（1ステップにつき明確な行動1つ）。
3. 2分以内に完了できる具体的な次の行動を1つ提示して終える。
4. 新しい論点を挙げる前に、現在の問題を解決して終わらせる。
5. ターンごとに進捗を明記する（例: 「5ステップ中3ステップ完了」）。
6. 所要時間は「少し」などの曖昧な表現を使わず、分単位などの具体的な数値で示す。
7. 変更後は、何が動作するようになったかを目に見える形で示す。
8. エラーは場所・原因・修正方法を淡々と伝える（大げさな表現は避ける）。
9. リストは最大5項目までに抑える。
10. 前置き、要約、締めの挨拶は入れない。

例外規定：解説を求められた場合は十分に説明する。破壊的な操作を行う前には必ず確認を取る。修正に3回失敗した場合は一度停止し、前提条件のどこに誤りがあるかを指摘する。指示が曖昧な場合は短い質問を1つだけ行う。
```

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

Gemini CLI にはプラグインマーケットプレイスがないため、公式には2つの導入方法があります。**カスタムコマンド**（オプトイン形式。呼び出すまでオフ）または **拡張機能**（インストール後は常時有効）です。このスキルの標準的な動作に合わせるなら、コマンド方式が適しています。全セッションで常にルールを適用したい場合以外は、コマンド方式を選んでください。

### インストール（コマンド方式、オプトイン）

```bash
mkdir -p ~/.gemini/commands
curl -fsSL https://raw.githubusercontent.com/ayghri/i-have-adhd/main/skills/i-have-adhd/agents/gemini.toml \
  -o ~/.gemini/commands/i-have-adhd.toml
```

新しいセッションを開始して `/i-have-adhd` と入力します。そのセッション中は有効な状態が続きます。

### インストール（拡張機能方式、常時有効）

```bash
gemini extensions install https://github.com/ayghri/i-have-adhd
```

拡張機能が `GEMINI.md` を読み込み、そこから完全なスキルがインポートされるため、最初のメッセージからルールが適用されます。`git` のインストールが必要です。

### 確認

```bash
gemini extensions list          # 拡張機能方式
ls ~/.gemini/commands           # コマンド方式: i-have-adhd.toml が存在することを確認
```

または、セッション内で `/` と入力し、一覧に `i-have-adhd` が表示されることを確認します。

### 更新

```bash
gemini extensions update i-have-adhd    # 拡張機能方式
# コマンド方式: 上記の curl コマンドを再実行
```

### アンインストール

```bash
gemini extensions uninstall i-have-adhd    # 拡張機能方式
rm ~/.gemini/commands/i-have-adhd.toml     # コマンド方式
```

</details>

<details>
<summary><strong>GitHub Copilot (VS Code および Copilot CLI)</strong></summary>

Copilot は Agent Skills をネイティブに読み込むため、変換不要でそのまま `SKILL.md` を利用できます。プロジェクト内では `.github/skills/`、`.claude/skills/`、`.agents/skills/` を、グローバル環境では `~/.copilot/skills/`、`~/.claude/skills/`、`~/.agents/skills/` をスキャンします。

### インストール

```bash
npx skills add ayghri/i-have-adhd -a github-copilot        # このプロジェクトのみ
npx skills add ayghri/i-have-adhd -a github-copilot -g     # 全プロジェクト共通
```

CLI を使わない場合は、Copilot がスキャンするいずれかのディレクトリにスキルフォルダーをコピーします：

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

Copilot は設定項目の `disable-model-invocation` に従います。Claude Code と同様に、スキルを明示的に呼び出すまでルールは適用されません（[#60](https://github.com/ayghri/i-have-adhd/pull/60) で検証済み）。

### 常時有効（任意）

プロジェクト内の `.github/copilot-instructions.md` に以下のブロックを追加します（Copilot はすべてのチャット開始時にこれを読み込みます）：

```markdown
## 出力スタイル

読み手はADHDです。すぐ行動に移せるよう、すべての回答を以下のように構成してください：

1. 答えや次に取るべき行動から始める：コマンド、パス、コードスニペットを最優先で提示する。
2. 複数ステップの作業には番号を付ける（1ステップにつき明確な行動1つ）。
3. 2分以内に完了できる具体的な次の行動を1つ提示して終える。
4. 新しい論点を挙げる前に、現在の問題を解決して終わらせる。
5. ターンごとに進捗を明記する（例: 「5ステップ中3ステップ完了」）。
6. 所要時間は「少し」などの曖昧な表現を使わず、分単位などの具体的な数値で示す。
7. 変更後は、何が動作するようになったかを目に見える形で示す。
8. エラーは場所・原因・修正方法を淡々と伝える（大げさな表現は避ける）。
9. リストは最大5項目までに抑える。
10. 前置き、要約、締めの挨拶は入れない。

例外規定：解説を求められた場合は十分に説明する。破壊的な操作を行う前には必ず確認を取る。修正に3回失敗した場合は一度停止し、前提条件のどこに誤りがあるかを指摘する。指示が曖昧な場合は短い質問を1つだけ行う。
```

</details>

<details>
<summary><strong>Hermes</strong></summary>

### インストール

```bash
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd
```

`/i-have-adhd` と入力します。スキルは `~/.hermes/skills/` にインストールされ、次回のセッション開始時からスラッシュコマンドとして利用可能になります。

先に内容を確認したい場合は、このリポジトリをスキルソース（「tap」）として追加してから検索・インストールすることもできます：

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

tap も削除する場合：`hermes skills tap remove ayghri/i-have-adhd`

### 常時有効（任意）

作業ディレクトリ内の `AGENTS.md`（Hermes が作業ディレクトリごとに読み込みます）、または全セッション共通のペルソナ設定 `SOUL.md` に追加：

```markdown
## 出力スタイル

読み手はADHDです。すぐ行動に移せるよう、すべての回答を以下のように構成してください：

1. 答えや次に取るべき行動から始める：コマンド、パス、コードスニペットを最優先で提示する。
2. 複数ステップの作業には番号を付ける（1ステップにつき明確な行動1つ）。
3. 2分以内に完了できる具体的な次の行動を1つ提示して終える。
4. 新しい論点を挙げる前に、現在の問題を解決して終わらせる。
5. ターンごとに進捗を明記する（例: 「5ステップ中3ステップ完了」）。
6. 所要時間は「少し」などの曖昧な表現を使わず、分単位などの具体的な数値で示す。
7. 変更後は、何が動作するようになったかを目に見える形で示す。
8. エラーは場所・原因・修正方法を淡々と伝える（大げさな表現は避ける）。
9. リストは最大5項目までに抑える。
10. 前置き、要約、締めの挨拶は入れない。

例外規定：解説を求められた場合は十分に説明する。破壊的な操作を行う前には必ず確認を取る。修正に3回失敗した場合は一度停止し、前提条件のどこに誤りがあるかを指摘する。指示が曖昧な場合は短い質問を1つだけ行う。
```

</details>

<details>
<summary><strong>Kimi Code CLI</strong></summary>

### インストール

Kimi Code のセッションを開始し、以下の手順を実行します：

1. `/plugins` を実行する。
2. **Custom** を選択する。
3. `https://github.com/ayghri/i-have-adhd` を貼り付けて `Enter` を押す。
4. **Trust and install** を選択する。

スラッシュコマンド `/skill:i-have-adhd` を使用することで、スキルを明示的に呼び出します。

### 更新

Kimi Code セッション内で `/plugins` を実行し、**I Have ADHD** にカーソルを合わせて `R` を押します。

### アンインストール

Kimi Code セッション内で `/plugins` を実行し、**I Have ADHD** にカーソルを合わせて `D` を押します。

</details>

<details>
<summary><strong>OpenCode</strong></summary>

OpenCode はこのリポジトリをサーバープラグインとして読み込みます。`.opencode/plugins/i-have-adhd.mjs` が `skills/` のエントリーポイントと `/i-have-adhd` コマンドを登録し、常時有効化されている場合はルールセットを注入します。また、OpenCode は `skills/` をネイティブにも読み込めるため、プラグインなしでもスキル自体は動作します（プラグインを追加すると `/i-have-adhd` コマンドと常時有効化フラグが使えるようになります）。

### インストール

リポジトリをクローンし、OpenCode からプラグインを指定します。絶対パスを指定すると、すべてのプロジェクトで単一のチェックアウトを共有できます：

```bash
git clone https://github.com/ayghri/i-have-adhd ~/.config/opencode/vendor/i-have-adhd
```

`opencode.json`（グローバル設定: `~/.config/opencode/opencode.json`）に追加：

```json
{ "plugin": ["/absolute/path/to/i-have-adhd/.opencode/plugins/i-have-adhd.mjs"] }
```

または、チェックアウト先から直接 OpenCode を起動します。ルート直下の `opencode.json` にプラグインが設定済みです。

新しいセッションを開始し、そのセッションでADHDフレンドリーな出力を有効化：

```text
/i-have-adhd
```

`stop adhd mode` または `normal mode` と入力するまでルールが維持されます。

### 確認

OpenCode を起動して `/` と入力し、コマンド一覧に `i-have-adhd` が表示されることを確認します。

### 更新

```bash
git -C ~/.config/opencode/vendor/i-have-adhd pull
```

### アンインストール

`opencode.json` から `plugin` のエントリーを削除します。

### 常時有効（任意）

```bash
touch ~/.config/opencode/.i-have-adhd-always
```

フラグファイルが存在する間、プラグインは毎ターンシステムプロンプトの末尾に完全なルールセットを追加します（Claude Code の `SessionStart` フックに相当）。`stop adhd mode` や `normal mode` で現在のセッションのみ無効化できます。常時有効を完全に解除する場合はフラグファイルを削除してください：

```bash
rm ~/.config/opencode/.i-have-adhd-always
```

</details>


<details>
<summary><strong>Pi</strong></summary>

Pi はこのリポジトリをネイティブパッケージとして認識します。`extensions/` がセッション持続モードを提供し、`skills/` によって Agent Skills のエントリーポイントも引き続き利用できます。

### インストール

```bash
pi install https://github.com/ayghri/i-have-adhd
```

新しい Pi セッションを開始し、現在のセッションでADHDフレンドリー出力を切り替えます：

```text
/i-have-adhd
```

有効化中はフッターに `● ADHD ON` と表示されます。もう一度コマンドを実行するとオフになります。明示的に指定することも可能です：

```text
/i-have-adhd on
/i-have-adhd off
stop adhd mode
```

Claude Code のフックと同様、拡張機能は毎リクエストでシステムプロンプトを書き換えるのではなく、会話コンテキストに一度だけルールセットを追加します（コンパクション等で消えた場合は再追加されます）。

既存の Agent Skills コマンドもエイリアスとして利用可能です：

```text
/skill:i-have-adhd
```

デフォルトで有効化した状態で新しい Pi セッションを開始する場合：

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

または、`pi update --extensions` で固定されていない全 Pi パッケージを一括更新します。

### アンインストール

```bash
pi remove https://github.com/ayghri/i-have-adhd
```

### 常時有効（任意）

Pi のエージェント設定ディレクトリにフラグファイルを作成：

```bash
touch ~/.pi/agent/.i-have-adhd-always
```

拡張機能は、セッションの新規作成・再開・フォーク・リロード時にこのフラグを確認します。現在のセッションで明示的に切り替えた設定が優先されるため、`stop adhd mode` を実行すればそのセッション内では無効化されたままになります。

オンデマンドに戻す場合：

```bash
rm ~/.pi/agent/.i-have-adhd-always
```

### 設定ファイル（任意）

Pi のエージェント設定ディレクトリに `~/.pi/agent/i-have-adhd.json` を作成します：

```json
{
  "alwaysOn": true,
  "hideStatus": true
}
```

- `alwaysOn`：すべてのセッションをルール有効の状態で開始します。従来の `.i-have-adhd-always` フラグファイルも引き続き使えます。
- `hideStatus`：ステータスバーの `● ADHD ON` 表示を隠します。ルールと `/i-have-adhd` コマンドは引き続き機能します。

設定は拡張機能の起動時に一度だけ読み込まれるため、変更後は Pi を再起動してください。現在のセッションに保存された選択は `alwaysOn` より優先されるため、`stop adhd mode` を実行するとそのセッションでは無効のままになります。

`PI_CODING_AGENT_DIR` が設定されている場合は、そのディレクトリ内に `.i-have-adhd-always` を配置してください。フラグを変更した後は `/reload` を実行するか、新しいセッションを開始してください。

</details>


<details>
<summary><strong>Oh My Pi (OMP)</strong></summary>

### インストール

```bash
omp plugin marketplace add ayghri/i-have-adhd
omp plugin install --scope user i-have-adhd@i-have-adhd
```

新しい OMP セッションを開始し、`/i-have-adhd` を実行してモードを切り替えます。

### 更新

```bash
omp plugin marketplace update i-have-adhd
omp plugin upgrade --scope user i-have-adhd@i-have-adhd
```

### アンインストール

```bash
omp plugin uninstall --scope user i-have-adhd@i-have-adhd
omp plugin marketplace remove i-have-adhd
```

</details>


<details>
<summary><strong>Qwen Code</strong></summary>

### インストール

```bash
qwen extensions install ayghri/i-have-adhd
```

Qwen Code は GitHub の短縮記法に対応しており、このリポジトリをネイティブ拡張機能としてインストール可能です。拡張機能は `skills/` 配下のスキルを自動検出します。

スキルを明示的に呼び出すには `/i-have-adhd` と入力します。拡張機能をインストールしても、スキルを呼び出すまで出力の変化はありません。

### 確認

```bash
qwen extensions list
```

次に新しい Qwen Code セッションを開始し、以下を実行：

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

Zed の Agent は Agent Skills をネイティブに読み込むため、変換不要でそのまま `SKILL.md` を利用できます（Zed の以前の「Rules」は、Skills と `AGENTS.md` の指示に置き換えられました）。

### インストール

Agent Panel で Skills マネージャーを開き、**Create skill from URL**（コマンドパレットでは `agent: create skill from url`）を選択して、以下を貼り付けます：

```
https://github.com/ayghri/i-have-adhd/blob/main/skills/i-have-adhd/SKILL.md
```

全プロジェクト共通で使う場合は **User** スコープ、現在のプロジェクトのみなら **Project** スコープで保存します。その後、Agent Panel で `/i-have-adhd` と入力します。

ファイルシステムを直接使う場合は、リポジトリをクローンしてユーザースキルディレクトリにスキルフォルダーを配置：

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

個人用の `~/.config/zed/AGENTS.md` に追加：

```markdown
## 出力スタイル

読み手はADHDです。すぐ行動に移せるよう、すべての回答を以下のように構成してください：

1. 答えや次に取るべき行動から始める：コマンド、パス、コードスニペットを最優先で提示する。
2. 複数ステップの作業には番号を付ける（1ステップにつき明確な行動1つ）。
3. 2分以内に完了できる具体的な次の行動を1つ提示して終える。
4. 新しい論点を挙げる前に、現在の問題を解決して終わらせる。
5. ターンごとに進捗を明記する（例: 「5ステップ中3ステップ完了」）。
6. 所要時間は「少し」などの曖昧な表現を使わず、分単位などの具体的な数値で示す。
7. 変更後は、何が動作するようになったかを目に見える形で示す。
8. エラーは場所・原因・修正方法を淡々と伝える（大げさな表現は避ける）。
9. リストは最大5項目までに抑える。
10. 前置き、要約、締めの挨拶は入れない。

例外規定：解説を求められた場合は十分に説明する。破壊的な操作を行う前には必ず確認を取る。修正に3回失敗した場合は一度停止し、前提条件のどこに誤りがあるかを指摘する。指示が曖昧な場合は短い質問を1つだけ行う。
```

</details>

<details>
<summary><strong>Cursor、Amp、その他の agent-skills 対応環境</strong></summary>

agent-skills を読み込めるすべての環境で動作します。`-a <agent>` の部分を、使用するエージェント名に置き換えてください。

### インストール

```bash
npx skills add ayghri/i-have-adhd                  # このプロジェクトのみ
npx skills add ayghri/i-have-adhd -g               # 全プロジェクト共通
npx skills add ayghri/i-have-adhd -a cursor -y     # 特定のエージェントのみ
npx skills add ayghri/i-have-adhd -a opencode -y
```

新しいエージェントチャットで `/i-have-adhd` と入力します。

CLI を使わない場合は、エージェントがスキャンするパスにスキルフォルダーをコピー：

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.cursor/skills     # Cursorの場合。OpenCodeなら .agents/skills、その他は各固有パス
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

エージェントの永続ルール設定ファイルに以下を貼り付けます。

Cursor の場合：**Settings → Rules → User Rules**、または `.cursor/rules/` 配下のプロジェクトルールで `alwaysApply: true` を設定。

OpenCode の場合：`~/.config/opencode/AGENTS.md`。

```markdown
## 出力スタイル

読み手はADHDです。すぐ行動に移せるよう、すべての回答を以下のように構成してください：

1. 答えや次に取るべき行動から始める：コマンド、パス、コードスニペットを最優先で提示する。
2. 複数ステップの作業には番号を付ける（1ステップにつき明確な行動1つ）。
3. 2分以内に完了できる具体的な次の行動を1つ提示して終える。
4. 新しい論点を挙げる前に、現在の問題を解決して終わらせる。
5. ターンごとに進捗を明記する（例: 「5ステップ中3ステップ完了」）。
6. 所要時間は「少し」などの曖昧な表現を使わず、分単位などの具体的な数値で示す。
7. 変更後は、何が動作するようになったかを目に見える形で示す。
8. エラーは場所・原因・修正方法を淡々と伝える（大げさな表現は避ける）。
9. リストは最大5項目までに抑える。
10. 前置き、要約、締めの挨拶は入れない。

例外規定：解説を求められた場合は十分に説明する。破壊的な操作を行う前には必ず確認を取る。修正に3回失敗した場合は一度停止し、前提条件のどこに誤りがあるかを指摘する。指示が曖昧な場合は短い質問を1つだけ行う。
```
</details>


## 有効化の仕組み

1. **インストール済み・未呼び出しの状態**：Claude Code、Qwen Code、Codex では、スキルを明示的に呼び出すまで何も起こりません。Claude Code と Qwen Code は `SKILL.md` 内の設定項目である `disable-model-invocation: true` に従い、Codex は `agents/openai.yaml` 内の `policy.allow_implicit_invocation: false` に従います。その他の環境では、起動時にすべてのスキルの説明文を読み込み、自動で有効化する場合があります。
2. **明示的に呼び出す**：Claude Code や Qwen Code では `/i-have-adhd`、Codex では `$i-have-adhd` と入力します。そのセッション中はルールが有効になります。`stop adhd mode` または `normal mode` でオフにできます。
3. **`~/.claude/.i-have-adhd-always` を作成する**（Claude Code）：`SessionStart` フックにより、すべてのセッションで最初のメッセージから完全なルールセットが読み込まれます。
4. **上記の常時有効スニペットを追加する**（その他の環境）：エージェントの永続コンテキスト内に中核ルールを保持します。

Claude Code、Qwen Code、Codex には中間状態がありません。有効化していなければオフのままです。

## トラブルシューティング

**`/i-have-adhd` が自動補完に表示されない →** エージェントを再起動してください。プラグインのインデックスは起動時に読み込まれます。

**常時有効フラグが効かない →** プラグインを更新（`claude plugin marketplace update i-have-adhd`）して再起動してください。フックは起動時に読み込まれるほか、フラグの認識には `hooks/hooks.json` が含まれるバージョンが必要です。

**`claude plugin marketplace add` が失敗する →** `owner/repo` 形式を使用してください。ローカルパスを指定する場合は `.claude-plugin/` ではなくリポジトリのルートを指す必要があります。

**インストールしたのに回答に前置きが入る →** 新しいセッションを開いてください。それでも指示から逸脱する場合は、`skills/i-have-adhd/SKILL.md` の文言をより厳格に調整してください。

**自分好みのルールに変更したい →** Fork して `skills/i-have-adhd/SKILL.md` を編集し、自分のコピーに差し替えます：

```bash
claude plugin uninstall i-have-adhd            # 先に本家のコピーを削除
claude plugin marketplace remove i-have-adhd   # Fork版と本家で名前が重複するため
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

再起動してから、`/i-have-adhd` をもう一度呼び出してください。

**`npx skills add` の後にスキルが見つからない →** 新しいエージェントチャットを開始してください。スキルはセッション開始時にインデックス化されます。フォルダーがエージェントのスキャン対象パス（Cursor なら `~/.cursor/skills/`、OpenCode なら `.agents/skills/`）に正しく配置されていること、および frontmatter の `name` がフォルダー名と一致していることを確認してください。
