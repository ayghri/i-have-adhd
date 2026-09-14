# 安裝方法

<details>
<summary><strong>Antigravity (<code>agy</code>)</strong></summary>

### 安裝

```bash
agy plugin install https://github.com/ayghri/i-have-adhd
```

### 驗證

```bash
agy plugin list
```

### 更新

```bash
agy plugin uninstall i-have-adhd
agy plugin install https://github.com/ayghri/i-have-adhd
```

### 解除安裝

```bash
agy plugin uninstall i-have-adhd
```

也可以保留安裝並將其關閉：`agy plugin disable i-have-adhd`。

### 始終啟用（可選）

新增到 `~/.gemini/GEMINI.md`：

```markdown
## 輸出風格

讀者有 ADHD。請讓每條回覆都便於立即執行：

1. 先給出答案或下一步行動：命令、路徑或程式碼片段優先。
2. 為多步驟工作編號；每一步只包含一個明確的行動。
3. 最後給出一個能在兩分鐘內完成的下一步行動。
4. 先解決當前問題，再提出新問題。
5. 每輪重述進度（“5 步中的第 3 步已完成”）。
6. 用具體單位估算時間，絕不說“一會兒”。
7. 修改後說明現在可以正常工作的內容。
8. 出錯時說明位置、原因和修復方法，不誇大。
9. 列表最多包含 5 項。
10. 不要前言、回顧或結束語。

例外：使用者要求解釋時應充分說明。執行破壞性操作前先確認。連續三次修復失敗後停止，並指出可疑的假設。請求含糊時只問一個簡短問題。
```

</details>

<details>
<summary><strong>AstronClaw（自定義技能）</strong></summary>

AstronClaw 支援將 Markdown 檔案匯入為自定義技能。此方式使用現有的 `SKILL.md`；
上傳和管理入口參見[官方技能指南](https://github.com/iflytek/astronclaw-tutorial/blob/main/docs/guide/astronclaw/skills.md)。

以下步驟依據 AstronClaw 官方文件編寫，但尚未使用本技能進行實際測試。
啟用前，請檢查匯出的技能指令。

### 安裝

1. 下載[技能原始檔 SKILL.md](https://raw.githubusercontent.com/ayghri/i-have-adhd/main/skills/i-have-adhd/SKILL.md)，儲存為 `SKILL.md`，上傳前先閱讀檔案內容。
2. 在 AstronClaw 中開啟**我的技能**，選擇**新建**，上傳該 `.md` 檔案。
3. 確認匯入後的技能名稱為 `i-have-adhd`，透過**啟用/禁用**控制技能是否可用。

只需上傳技能 Markdown 檔案。上傳會將該檔案傳送給 AstronClaw；
本倉庫的外掛清單和鉤子不參與此安裝流程。

### 驗證與啟用

確認**我的技能**中出現 `i-have-adhd`，透過**下載**將匯入後的指令與原始技能對照檢查，
然後啟用並嘗試輸入：

```text
請在本次對話中使用 i-have-adhd 技能。說明如何在新資料夾中建立一個空的 Git 倉庫。
```

檢查回覆是否先給出行動，併為步驟編號。這是對匯入技能的手動檢查；
上傳成功本身不能證明回覆規則已經生效。

### 啟用說明

AstronClaw 支援指定呼叫和自動呼叫技能。官方指南未說明是否遵循
`disable-model-invocation: true`，因此不希望技能可用時，請使用**禁用**開關。
無需依賴 `/i-have-adhd` 斜槓命令。

技能要求助手在本次對話中保持該回復風格，直到你說 `stop adhd mode` 或
`normal mode`。這條指令不會更改平臺開關；如需開始不使用該技能的新會話，
請禁用技能並開啟新對話。

### 更新

下載最新的技能原始檔 `SKILL.md`。如果修改過已匯入的副本，請先使用**下載**
儲存備份。如需完整替換，請刪除舊的 `i-have-adhd` 條目，重新匯入檔案，
並在新對話中執行驗證提示詞。

### 解除安裝

在**我的技能**中選擇 `i-have-adhd`，點選**刪除**，然後開啟新對話。
如需保留已匯入的副本以便以後使用，可選擇**禁用**。

</details>

<details>
<summary><strong>Claude Code</strong></summary>

### 安裝

```bash
claude plugin marketplace add ayghri/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

輸入 `/i-have-adhd`。

### 驗證

```bash
claude plugin list
```

### 更新

```bash
claude plugin marketplace update i-have-adhd
```

### 解除安裝

```bash
claude plugin uninstall i-have-adhd
claude plugin marketplace remove i-have-adhd
```

也可以保留安裝並將其關閉：`claude plugin disable i-have-adhd`。

### 始終啟用（可選）

`SessionStart` 鉤子會在每次會話開始時載入完整規則，無需輸入 `/i-have-adhd`：

```bash
touch ~/.claude/.i-have-adhd-always
```

如果你使用自定義 Claude 配置目錄，請改為在其中建立標誌檔案：

```bash
touch "$CLAUDE_CONFIG_DIR/.i-have-adhd-always"
```

恢復為按需啟用：

```bash
rm ~/.claude/.i-have-adhd-always
```

該鉤子只在標誌檔案存在時觸發，因此僅安裝外掛不會改變任何行為。“stop adhd mode”仍可在當前會話中將其關閉。

</details>


<details>
<summary><strong>Codex</strong></summary>

### 安裝

```bash
codex plugin marketplace add ayghri/i-have-adhd --ref main
codex plugin add i-have-adhd@i-have-adhd
```

明確輸入 `$i-have-adhd` 來啟用此技能。Codex 不會自動呼叫它。

### 驗證

```bash
codex plugin list
```

### 更新

```bash
codex plugin marketplace upgrade i-have-adhd
codex plugin remove i-have-adhd
codex plugin add i-have-adhd@i-have-adhd
```

### 解除安裝

```bash
codex plugin remove i-have-adhd
codex plugin marketplace remove i-have-adhd
```

### 始終啟用（可選）

新增到 `~/.codex/AGENTS.md`：

```markdown
## 輸出風格

讀者有 ADHD。請讓每條回覆都便於立即執行：

1. 先給出答案或下一步行動：命令、路徑或程式碼片段優先。
2. 為多步驟工作編號；每一步只包含一個明確的行動。
3. 最後給出一個能在兩分鐘內完成的下一步行動。
4. 先解決當前問題，再提出新問題。
5. 每輪重述進度（“5 步中的第 3 步已完成”）。
6. 用具體單位估算時間，絕不說“一會兒”。
7. 修改後說明現在可以正常工作的內容。
8. 出錯時說明位置、原因和修復方法，不誇大。
9. 列表最多包含 5 項。
10. 不要前言、回顧或結束語。

例外：使用者要求解釋時應充分說明。執行破壞性操作前先確認。連續三次修復失敗後停止，並指出可疑的假設。請求含糊時只問一個簡短問題。
```

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

Gemini CLI 沒有外掛市場，因此有兩種原生方式：**自定義命令**（選擇啟用，呼叫前保持關閉）或**擴充套件**（安裝後始終啟用）。命令方式符合此技能的預設行為；除非希望每次會話都使用這些規則，否則請選擇命令方式。

### 安裝 (command, opt-in)

```bash
mkdir -p ~/.gemini/commands
curl -fsSL https://raw.githubusercontent.com/ayghri/i-have-adhd/main/skills/i-have-adhd/agents/gemini.toml \
  -o ~/.gemini/commands/i-have-adhd.toml
```

開始新會話並輸入 `/i-have-adhd`。它會在該會話中持續啟用。

### 安裝 (extension, always-on)

```bash
gemini extensions install https://github.com/ayghri/i-have-adhd
```

擴充套件會載入匯入完整技能的 `GEMINI.md`，因此規則從第一條訊息起生效。必須安裝 `git`。

### 驗證

```bash
gemini extensions list          # 擴充套件方式
ls ~/.gemini/commands           # command route: i-have-adhd.toml present
```

也可以在會話中輸入 `/`，確認列表中有 `i-have-adhd`。

### 更新

```bash
gemini extensions update i-have-adhd    # 擴充套件方式
# 命令方式：重新執行上面的 curl
```

### 解除安裝

```bash
gemini extensions uninstall i-have-adhd    # 擴充套件方式
rm ~/.gemini/commands/i-have-adhd.toml     # command route
```

</details>

<details>
<summary><strong>GitHub Copilot (VS Code and Copilot CLI)</strong></summary>

Copilot 原生讀取 Agent Skills：直接使用同一個 `SKILL.md`，無需轉換。它會掃描專案中的 `.github/skills/`、`.claude/skills/` 和 `.agents/skills/`，以及全域性的 `~/.copilot/skills/`、`~/.claude/skills/` 和 `~/.agents/skills/`。

### 安裝

```bash
npx skills add ayghri/i-have-adhd -a github-copilot        # 此專案
npx skills add ayghri/i-have-adhd -a github-copilot -g     # 所有專案
```

不使用 CLI 時，將技能資料夾複製到 Copilot 掃描的任一目錄：

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.copilot/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.copilot/skills/
```

### 驗證

在聊天輸入框中輸入 `/`，確認出現 `i-have-adhd`。或者：

```bash
npx skills list
npx skills ls -g    # 如果全域性安裝
```

### 更新

```bash
npx skills update i-have-adhd
```

也可以在 `git pull` 後重新複製該資料夾。

### 解除安裝

```bash
npx skills remove i-have-adhd
```

也可以從安裝所在的 skills 目錄刪除 `i-have-adhd` 資料夾。

### 啟用說明

Copilot 遵循 `disable-model-invocation`：與 Claude Code 相同，在呼叫技能前不會應用任何規則（已在 [#60](https://github.com/ayghri/i-have-adhd/pull/60) 中測試）。

### 始終啟用（可選）

將下面的內容新增到專案的 `.github/copilot-instructions.md`（Copilot 會在每次聊天中讀取）：

```markdown
## 輸出風格

讀者有 ADHD。請讓每條回覆都便於立即執行：

1. 先給出答案或下一步行動：命令、路徑或程式碼片段優先。
2. 為多步驟工作編號；每一步只包含一個明確的行動。
3. 最後給出一個能在兩分鐘內完成的下一步行動。
4. 先解決當前問題，再提出新問題。
5. 每輪重述進度（“5 步中的第 3 步已完成”）。
6. 用具體單位估算時間，絕不說“一會兒”。
7. 修改後說明現在可以正常工作的內容。
8. 出錯時說明位置、原因和修復方法，不誇大。
9. 列表最多包含 5 項。
10. 不要前言、回顧或結束語。

例外：使用者要求解釋時應充分說明。執行破壞性操作前先確認。連續三次修復失敗後停止，並指出可疑的假設。請求含糊時只問一個簡短問題。
```

</details>

<details>
<summary><strong>Hermes</strong></summary>

### 安裝

```bash
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd
```

輸入 `/i-have-adhd`。 The skill installs into `~/.hermes/skills/` and is exposed as a slash command at the next session start.

想先瀏覽內容？將此倉庫新增為技能源（“tap”），然後搜尋並安裝：

```bash
hermes skills tap add ayghri/i-have-adhd
hermes skills search adhd
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd
```

### 驗證

```bash
hermes skills list
```

### 更新

```bash
hermes skills update i-have-adhd
```

### 解除安裝

```bash
hermes skills uninstall i-have-adhd
```

也可以同時刪除 tap：`hermes skills tap remove ayghri/i-have-adhd`。

### 始終啟用（可選）

新增到工作目錄的 `AGENTS.md`（Hermes 按工作目錄載入），或新增到角色的 `SOUL.md` 以用於每次會話：

```markdown
## 輸出風格

讀者有 ADHD。請讓每條回覆都便於立即執行：

1. 先給出答案或下一步行動：命令、路徑或程式碼片段優先。
2. 為多步驟工作編號；每一步只包含一個明確的行動。
3. 最後給出一個能在兩分鐘內完成的下一步行動。
4. 先解決當前問題，再提出新問題。
5. 每輪重述進度（“5 步中的第 3 步已完成”）。
6. 用具體單位估算時間，絕不說“一會兒”。
7. 修改後說明現在可以正常工作的內容。
8. 出錯時說明位置、原因和修復方法，不誇大。
9. 列表最多包含 5 項。
10. 不要前言、回顧或結束語。

例外：使用者要求解釋時應充分說明。執行破壞性操作前先確認。連續三次修復失敗後停止，並指出可疑的假設。請求含糊時只問一個簡短問題。
```

</details>

<details>
<summary><strong>Kimi Code CLI</strong></summary>

### 安裝

啟動一個 Kimi Code 會話，然後：

1. 輸入 `/plugins`。
2. 選擇 **Custom**。
3. 貼上 `https://github.com/ayghri/i-have-adhd` 並 Enter。
4. 選擇 **Trust and install**。

使用斜槓命令 `/skill:i-have-adhd` 顯式呼叫此技能。

### 更新

在 Kimi Code 會話中輸入 `/plugins`，將游標移至 **I Have ADHD**，按 `R`。

### 解除安裝

在 Kimi Code 會話中輸入 `/plugins`，將游標移至 **I Have ADHD**，按 `D`。

</details>


<details>
<summary><strong>Pi</strong></summary>

Pi 實現了 Agent Skills 標準，因此可直接載入同一個 `SKILL.md`，無需轉換。Pi 的呼叫方式不同：使用 `/skill:<name>` 呼叫技能。

### 安裝

```bash
npx skills add ayghri/i-have-adhd -a pi -y
```

偏好檔案系統方式？Pi 會在 `~/.pi/agent/skills/` 和 `~/.agents/skills/`（全域性），以及 `.pi/skills/` 和 `.agents/skills/`（專案）中發現技能：

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.pi/agent/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.pi/agent/skills/
```

在 Pi 的 `settings.json` 中啟用技能斜槓命令：

```json
{ "enableSkillCommands": true }
```

開始新會話並輸入 `/skill:i-have-adhd`。

### 驗證

```bash
npx skills list
```

也可以在會話中輸入 `/skill:`，確認列表中有 `i-have-adhd`。

### 更新

```bash
npx skills update i-have-adhd
```

也可以在 `git pull` 後重新複製該資料夾。

### 解除安裝

```bash
npx skills remove i-have-adhd
```

也可以刪除 `~/.pi/agent/skills/i-have-adhd`。

### 始終啟用（可選）

新增到專案的 `AGENTS.md`：

```markdown
## 輸出風格

讀者有 ADHD。請讓每條回覆都便於立即執行：

1. 先給出答案或下一步行動：命令、路徑或程式碼片段優先。
2. 為多步驟工作編號；每一步只包含一個明確的行動。
3. 最後給出一個能在兩分鐘內完成的下一步行動。
4. 先解決當前問題，再提出新問題。
5. 每輪重述進度（“5 步中的第 3 步已完成”）。
6. 用具體單位估算時間，絕不說“一會兒”。
7. 修改後說明現在可以正常工作的內容。
8. 出錯時說明位置、原因和修復方法，不誇大。
9. 列表最多包含 5 項。
10. 不要前言、回顧或結束語。

例外：使用者要求解釋時應充分說明。執行破壞性操作前先確認。連續三次修復失敗後停止，並指出可疑的假設。請求含糊時只問一個簡短問題。
```

</details>


<details>
<summary><strong>Qwen Code</strong></summary>

### 安裝

```bash
qwen extensions install ayghri/i-have-adhd
```

Qwen Code 支援 GitHub 短路徑，並可將該倉庫安裝為原生擴充套件。擴充套件會發現 `skills/` 下的技能。

安裝擴充套件本身不會改變輸出，除非輸入 `/i-have-adhd` 顯式呼叫此技能。

### 驗證

```bash
qwen extensions list
```

然後啟動新的 Qwen Code 會話並執行：

```text
/skills
```

確認列表中出現 `i-have-adhd`。

### 更新

```bash
qwen extensions update i-have-adhd
```

### 解除安裝

```bash
qwen extensions uninstall i-have-adhd
```

</details>

<details>
<summary><strong>Zed</strong></summary>

Zed 的 Agent 原生讀取 Agent Skills：直接使用同一個 `SKILL.md`，無需轉換。（Zed 舊版的“Rules”已由 Skills 和 `AGENTS.md` 指令取代。）

### 安裝

在 Agent Panel 中開啟 Skills 管理器，選擇 **Create skill from URL**（命令面板中為 `agent: create skill from url`），然後貼上：

```
https://github.com/ayghri/i-have-adhd/blob/main/skills/i-have-adhd/SKILL.md
```

要用於所有專案，請儲存到 **User** 作用域；僅用於一個專案則儲存到 **Project** 作用域。然後在 Agent Panel 中輸入 `/i-have-adhd`。

偏好檔案系統方式？克隆倉庫並將技能資料夾放入使用者 skills 目錄：

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.agents/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.agents/skills/
```

### 驗證

在 Agent Panel 中開啟 Skills 管理器，確認列表中有 `i-have-adhd`。也可以輸入 `/` 並確認它出現。

### 更新

從同一 URL 重新匯入（會覆蓋），或在 `git pull` 後重新複製資料夾。

### 解除安裝

從 Skills 管理器中移除 `i-have-adhd`，或刪除 `~/.agents/skills/i-have-adhd`。

### 始終啟用（可選）

新增到個人的 `~/.config/zed/AGENTS.md`：

```markdown
## 輸出風格

讀者有 ADHD。請讓每條回覆都便於立即執行：

1. 先給出答案或下一步行動：命令、路徑或程式碼片段優先。
2. 為多步驟工作編號；每一步只包含一個明確的行動。
3. 最後給出一個能在兩分鐘內完成的下一步行動。
4. 先解決當前問題，再提出新問題。
5. 每輪重述進度（“5 步中的第 3 步已完成”）。
6. 用具體單位估算時間，絕不說“一會兒”。
7. 修改後說明現在可以正常工作的內容。
8. 出錯時說明位置、原因和修復方法，不誇大。
9. 列表最多包含 5 項。
10. 不要前言、回顧或結束語。

例外：使用者要求解釋時應充分說明。執行破壞性操作前先確認。連續三次修復失敗後停止，並指出可疑的假設。請求含糊時只問一個簡短問題。
```

</details>

<details>
<summary><strong>Cursor、OpenCode、Amp 及其他 agent-skills 執行環境</strong></summary>

適用於任何能讀取 Agent Skills 的執行環境。將 `-a <agent>` 替換為你的智慧體。

### 安裝

```bash
npx skills add ayghri/i-have-adhd                  # this workspace
npx skills add ayghri/i-have-adhd -g               # 所有專案
npx skills add ayghri/i-have-adhd -a cursor -y     # one agent only
npx skills add ayghri/i-have-adhd -a opencode -y
```

開啟新的智慧體聊天並輸入 `/i-have-adhd`。

不使用 CLI 時，將技能資料夾複製到智慧體掃描的路徑：

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.cursor/skills     # Cursor。OpenCode 使用 .agents/skills，其他智慧體使用其自身路徑
cp -R i-have-adhd/skills/i-have-adhd ~/.cursor/skills/
```

### 驗證

```bash
npx skills list
npx skills ls -g    # 如果全域性安裝
```

### 更新

```bash
npx skills update i-have-adhd
npx skills update -g    # 如果全域性安裝
```

### 解除安裝

```bash
npx skills remove i-have-adhd
npx skills remove i-have-adhd -g    # 如果全域性安裝
```

### 始終啟用（可選）

將此內容貼上到智慧體的持久規則檔案。Cursor：**Settings → Rules → User Rules**，或在 `.cursor/rules/` 下建立設定了 `alwaysApply: true` 的專案規則。OpenCode：`~/.config/opencode/AGENTS.md`。

```markdown
## 輸出風格

讀者有 ADHD。請讓每條回覆都便於立即執行：

1. 先給出答案或下一步行動：命令、路徑或程式碼片段優先。
2. 為多步驟工作編號；每一步只包含一個明確的行動。
3. 最後給出一個能在兩分鐘內完成的下一步行動。
4. 先解決當前問題，再提出新問題。
5. 每輪重述進度（“5 步中的第 3 步已完成”）。
6. 用具體單位估算時間，絕不說“一會兒”。
7. 修改後說明現在可以正常工作的內容。
8. 出錯時說明位置、原因和修復方法，不誇大。
9. 列表最多包含 5 項。
10. 不要前言、回顧或結束語。

例外：使用者要求解釋時應充分說明。執行破壞性操作前先確認。連續三次修復失敗後停止，並指出可疑的假設。請求含糊時只問一個簡短問題。
```
</details>


## 啟用機制

1. **已安裝但未呼叫。** 在 Claude Code、Qwen Code 和 Codex 中，只有明確呼叫技能後才會發生變化。Claude Code 和 Qwen Code 遵循 `SKILL.md` 中的 `disable-model-invocation: true`；Codex 遵循 `agents/openai.yaml` 中的 `policy.allow_implicit_invocation: false`。其他執行環境可能會在啟動時載入每個技能的描述，並自行啟用技能。
2. **明確呼叫技能。** 在 Claude Code 或 Qwen Code 中輸入 `/i-have-adhd`，在 Codex 中輸入 `$i-have-adhd`。規則將在該會話中啟用。輸入“stop adhd mode”或“normal mode”可將其關閉。
3. **建立 `~/.claude/.i-have-adhd-always`**（Claude Code）。`SessionStart` 鉤子會在每次會話中從第一條訊息起載入完整規則。
4. **新增上面的始終啟用片段**（其他執行環境）。這樣會將核心規則保留在智慧體的持久上下文中。

在 Claude Code、Qwen Code 和 Codex 中沒有中間狀態：未啟用就是關閉。

## 故障排除

**自動補全中沒有 `/i-have-adhd`。** 重啟智慧體。外掛索引在啟動時讀取。

**始終啟用標誌無效。** 更新外掛（`claude plugin marketplace update i-have-adhd`）並重啟。鉤子在啟動時讀取，且該標誌需要包含 `hooks/hooks.json` 的外掛版本。

**`claude plugin marketplace add` 失敗。** 使用 `owner/repo` 格式。本地路徑必須指向倉庫根目錄，而不是 `.claude-plugin/`。

**已安裝，但回覆仍有開場白。** 開啟新會話。如果仍然偏離，請收緊 `skills/i-have-adhd/SKILL.md` 中的措辭。

**想使用不同規則。** Fork 倉庫，編輯 `skills/i-have-adhd/SKILL.md`，然後換成你的副本：

```bash
claude plugin uninstall i-have-adhd            # 先移除上游副本：
claude plugin marketplace remove i-have-adhd   # fork 與上游使用相同名稱
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

重啟，然後再次呼叫 `/i-have-adhd`。

**執行 `npx skills add` 後找不到技能。** 開啟新的智慧體聊天。技能在會話開始時建立索引。確認資料夾位於智慧體掃描的位置（Cursor 為 `~/.cursor/skills/`，OpenCode 為 `.agents/skills/`），且 frontmatter 中的 `name` 與資料夾名稱一致。
