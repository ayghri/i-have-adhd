# 安装方法

<details>
<summary><strong>Antigravity (<code>agy</code>)</strong></summary>

### 安装

```bash
agy plugin install https://github.com/ayghri/i-have-adhd
```

### 验证

```bash
agy plugin list
```

### 更新

```bash
agy plugin uninstall i-have-adhd
agy plugin install https://github.com/ayghri/i-have-adhd
```

### 卸载

```bash
agy plugin uninstall i-have-adhd
```

也可以保留安装并将其关闭：`agy plugin disable i-have-adhd`。

### 始终启用（可选）

添加到 `~/.gemini/GEMINI.md`：

```markdown
## 输出风格

读者有 ADHD。请让每条回复都便于立即执行：

1. 先给出答案或下一步行动：命令、路径或代码片段优先。
2. 为多步骤工作编号；每一步只包含一个明确的行动。
3. 最后给出一个能在两分钟内完成的下一步行动。
4. 先解决当前问题，再提出新问题。
5. 每轮重述进度（“5 步中的第 3 步已完成”）。
6. 用具体单位估算时间，绝不说“一会儿”。
7. 修改后说明现在可以正常工作的内容。
8. 出错时说明位置、原因和修复方法，不夸大。
9. 列表最多包含 5 项。
10. 不要前言、回顾或结束语。

例外：用户要求解释时应充分说明。执行破坏性操作前先确认。连续三次修复失败后停止，并指出可疑的假设。请求含糊时只问一个简短问题。
```

</details>

<details>
<summary><strong>AstronClaw（自定义技能）</strong></summary>

AstronClaw 支持将 Markdown 文件导入为自定义技能。此方式使用现有的 `SKILL.md`；
上传和管理入口参见[官方技能指南](https://github.com/iflytek/astronclaw-tutorial/blob/main/docs/guide/astronclaw/skills.md)。

以下步骤依据 AstronClaw 官方文档编写，但尚未使用本技能进行实际测试。
启用前，请检查导出的技能指令。

### 安装

1. 下载[技能源文件 SKILL.md](https://raw.githubusercontent.com/ayghri/i-have-adhd/main/skills/i-have-adhd/SKILL.md)，保存为 `SKILL.md`，上传前先阅读文件内容。
2. 在 AstronClaw 中打开**我的技能**，选择**新建**，上传该 `.md` 文件。
3. 确认导入后的技能名称为 `i-have-adhd`，通过**启用/禁用**控制技能是否可用。

只需上传技能 Markdown 文件。上传会将该文件发送给 AstronClaw；
本仓库的插件清单和钩子不参与此安装流程。

### 验证与启用

确认**我的技能**中出现 `i-have-adhd`，通过**下载**将导入后的指令与原始技能对照检查，
然后启用并尝试输入：

```text
请在本次对话中使用 i-have-adhd 技能。说明如何在新文件夹中创建一个空的 Git 仓库。
```

检查回复是否先给出行动，并为步骤编号。这是对导入技能的手动检查；
上传成功本身不能证明回复规则已经生效。

### 启用说明

AstronClaw 支持指定调用和自动调用技能。官方指南未说明是否遵循
`disable-model-invocation: true`，因此不希望技能可用时，请使用**禁用**开关。
无需依赖 `/i-have-adhd` 斜杠命令。

技能要求助手在本次对话中保持该回复风格，直到你说 `stop adhd mode` 或
`normal mode`。这条指令不会更改平台开关；如需开始不使用该技能的新会话，
请禁用技能并开启新对话。

### 更新

下载最新的技能源文件 `SKILL.md`。如果修改过已导入的副本，请先使用**下载**
保存备份。如需完整替换，请删除旧的 `i-have-adhd` 条目，重新导入文件，
并在新对话中运行验证提示词。

### 卸载

在**我的技能**中选择 `i-have-adhd`，点击**删除**，然后开启新对话。
如需保留已导入的副本以便以后使用，可选择**禁用**。

</details>

<details>
<summary><strong>Claude Code</strong></summary>

### 安装

```bash
claude plugin marketplace add ayghri/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

输入 `/i-have-adhd`。

### 验证

```bash
claude plugin list
```

### 更新

```bash
claude plugin marketplace update i-have-adhd
```

### 卸载

```bash
claude plugin uninstall i-have-adhd
claude plugin marketplace remove i-have-adhd
```

也可以保留安装并将其关闭：`claude plugin disable i-have-adhd`。

### 始终启用（可选）

`SessionStart` 钩子会在每次会话开始时加载完整规则，无需输入 `/i-have-adhd`：

```bash
touch ~/.claude/.i-have-adhd-always
```

如果你使用自定义 Claude 配置目录，请改为在其中创建标志文件：

```bash
touch "$CLAUDE_CONFIG_DIR/.i-have-adhd-always"
```

恢复为按需启用：

```bash
rm ~/.claude/.i-have-adhd-always
```

该钩子只在标志文件存在时触发，因此仅安装插件不会改变任何行为。“stop adhd mode”仍可在当前会话中将其关闭。

</details>


<details>
<summary><strong>Codex</strong></summary>

### 安装

```bash
codex plugin marketplace add ayghri/i-have-adhd --ref main
codex plugin add i-have-adhd@i-have-adhd
```

明确输入 `$i-have-adhd` 来启用此技能。Codex 不会自动调用它。

### 验证

```bash
codex plugin list
```

### 更新

```bash
codex plugin marketplace upgrade i-have-adhd
codex plugin remove i-have-adhd
codex plugin add i-have-adhd@i-have-adhd
```

### 卸载

```bash
codex plugin remove i-have-adhd
codex plugin marketplace remove i-have-adhd
```

### 始终启用（可选）

添加到 `~/.codex/AGENTS.md`：

```markdown
## 输出风格

读者有 ADHD。请让每条回复都便于立即执行：

1. 先给出答案或下一步行动：命令、路径或代码片段优先。
2. 为多步骤工作编号；每一步只包含一个明确的行动。
3. 最后给出一个能在两分钟内完成的下一步行动。
4. 先解决当前问题，再提出新问题。
5. 每轮重述进度（“5 步中的第 3 步已完成”）。
6. 用具体单位估算时间，绝不说“一会儿”。
7. 修改后说明现在可以正常工作的内容。
8. 出错时说明位置、原因和修复方法，不夸大。
9. 列表最多包含 5 项。
10. 不要前言、回顾或结束语。

例外：用户要求解释时应充分说明。执行破坏性操作前先确认。连续三次修复失败后停止，并指出可疑的假设。请求含糊时只问一个简短问题。
```

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

Gemini CLI 没有插件市场，因此有两种原生方式：**自定义命令**（选择启用，调用前保持关闭）或**扩展**（安装后始终启用）。命令方式符合此技能的默认行为；除非希望每次会话都使用这些规则，否则请选择命令方式。

### 安装（命令方式，按需启用）

```bash
mkdir -p ~/.gemini/commands
curl -fsSL https://raw.githubusercontent.com/ayghri/i-have-adhd/main/skills/i-have-adhd/agents/gemini.toml \
  -o ~/.gemini/commands/i-have-adhd.toml
```

开始新会话并输入 `/i-have-adhd`。它会在该会话中持续启用。

### 安装（扩展方式，始终启用）

```bash
gemini extensions install https://github.com/ayghri/i-have-adhd
```

扩展会加载导入完整技能的 `GEMINI.md`，因此规则从第一条消息起生效。必须安装 `git`。

### 验证

```bash
gemini extensions list          # 扩展方式
ls ~/.gemini/commands           # 命令方式：应存在 i-have-adhd.toml
```

也可以在会话中输入 `/`，确认列表中有 `i-have-adhd`。

### 更新

```bash
gemini extensions update i-have-adhd    # 扩展方式
# 命令方式：重新运行上面的 curl
```

### 卸载

```bash
gemini extensions uninstall i-have-adhd    # 扩展方式
rm ~/.gemini/commands/i-have-adhd.toml     # 命令方式
```

</details>

<details>
<summary><strong>GitHub Copilot (VS Code and Copilot CLI)</strong></summary>

Copilot 原生读取 Agent Skills：直接使用同一个 `SKILL.md`，无需转换。它会扫描项目中的 `.github/skills/`、`.claude/skills/` 和 `.agents/skills/`，以及全局的 `~/.copilot/skills/`、`~/.claude/skills/` 和 `~/.agents/skills/`。

### 安装

```bash
npx skills add ayghri/i-have-adhd -a github-copilot        # 此项目
npx skills add ayghri/i-have-adhd -a github-copilot -g     # 所有项目
```

不使用 CLI 时，将技能文件夹复制到 Copilot 扫描的任一目录：

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.copilot/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.copilot/skills/
```

### 验证

在聊天输入框中输入 `/`，确认出现 `i-have-adhd`。或者：

```bash
npx skills list
npx skills ls -g    # 如果全局安装
```

### 更新

```bash
npx skills update i-have-adhd
```

也可以在 `git pull` 后重新复制该文件夹。

### 卸载

```bash
npx skills remove i-have-adhd
```

也可以从安装所在的 skills 目录删除 `i-have-adhd` 文件夹。

### 启用说明

Copilot 遵循 `disable-model-invocation`：与 Claude Code 相同，在调用技能前不会应用任何规则（已在 [#60](https://github.com/ayghri/i-have-adhd/pull/60) 中测试）。

### 始终启用（可选）

将下面的内容添加到项目的 `.github/copilot-instructions.md`（Copilot 会在每次聊天中读取）：

```markdown
## 输出风格

读者有 ADHD。请让每条回复都便于立即执行：

1. 先给出答案或下一步行动：命令、路径或代码片段优先。
2. 为多步骤工作编号；每一步只包含一个明确的行动。
3. 最后给出一个能在两分钟内完成的下一步行动。
4. 先解决当前问题，再提出新问题。
5. 每轮重述进度（“5 步中的第 3 步已完成”）。
6. 用具体单位估算时间，绝不说“一会儿”。
7. 修改后说明现在可以正常工作的内容。
8. 出错时说明位置、原因和修复方法，不夸大。
9. 列表最多包含 5 项。
10. 不要前言、回顾或结束语。

例外：用户要求解释时应充分说明。执行破坏性操作前先确认。连续三次修复失败后停止，并指出可疑的假设。请求含糊时只问一个简短问题。
```

</details>

<details>
<summary><strong>Hermes</strong></summary>

### 安装

```bash
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd
```

输入 `/i-have-adhd`。技能会安装到 `~/.hermes/skills/`，并在下次会话启动时作为斜杠命令生效。

想先浏览内容？将此仓库添加为技能源（“tap”），然后搜索并安装：

```bash
hermes skills tap add ayghri/i-have-adhd
hermes skills search adhd
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd
```

### 验证

```bash
hermes skills list
```

### 更新

```bash
hermes skills update i-have-adhd
```

### 卸载

```bash
hermes skills uninstall i-have-adhd
```

也可以同时删除 tap：`hermes skills tap remove ayghri/i-have-adhd`。

### 始终启用（可选）

添加到工作目录的 `AGENTS.md`（Hermes 按工作目录加载），或添加到角色的 `SOUL.md` 以用于每次会话：

```markdown
## 输出风格

读者有 ADHD。请让每条回复都便于立即执行：

1. 先给出答案或下一步行动：命令、路径或代码片段优先。
2. 为多步骤工作编号；每一步只包含一个明确的行动。
3. 最后给出一个能在两分钟内完成的下一步行动。
4. 先解决当前问题，再提出新问题。
5. 每轮重述进度（“5 步中的第 3 步已完成”）。
6. 用具体单位估算时间，绝不说“一会儿”。
7. 修改后说明现在可以正常工作的内容。
8. 出错时说明位置、原因和修复方法，不夸大。
9. 列表最多包含 5 项。
10. 不要前言、回顾或结束语。

例外：用户要求解释时应充分说明。执行破坏性操作前先确认。连续三次修复失败后停止，并指出可疑的假设。请求含糊时只问一个简短问题。
```

</details>

<details>
<summary><strong>Kimi Code CLI</strong></summary>

### 安装

启动一个 Kimi Code 会话，然后：

1. 输入 `/plugins`。
2. 选择 **Custom**。
3. 粘贴 `https://github.com/ayghri/i-have-adhd` 并 Enter。
4. 选择 **Trust and install**。

使用斜杠命令 `/skill:i-have-adhd` 显式调用此技能。

### 更新

在 Kimi Code 会话中输入 `/plugins`，将光标移至 **I Have ADHD**，按 `R`。

### 卸载

在 Kimi Code 会话中输入 `/plugins`，将光标移至 **I Have ADHD**，按 `D`。

</details>


<details>
<summary><strong>OpenCode</strong></summary>

OpenCode 将此仓库作为服务端插件加载：`.opencode/plugins/i-have-adhd.mjs` 注册 `skills/` 入口点和 `/i-have-adhd` 命令，并在启用始终启用模式时注入规则。OpenCode 也会原生读取 `skills/`，因此即使没有插件，技能本身仍然可用——插件额外提供的是 `/i-have-adhd` 命令和始终启用标志。

### 安装

克隆仓库并让 OpenCode 指向该插件。使用绝对路径可以让所有项目共享同一份检出：

```bash
git clone https://github.com/ayghri/i-have-adhd ~/.config/opencode/vendor/i-have-adhd
```

将以下内容加入你的 `opencode.json`（全局：`~/.config/opencode/opencode.json`）：

```json
{ "plugin": ["/absolute/path/to/i-have-adhd/.opencode/plugins/i-have-adhd.mjs"] }
```

也可以直接在检出目录中运行 OpenCode——仓库根目录自带已接好插件的 `opencode.json`。

开启新会话，并为该会话启用 ADHD 友好输出：

```text
/i-have-adhd
```

规则持续生效，直到输入 `stop adhd mode` 或 `normal mode`。

### 验证

启动 OpenCode，输入 `/`，确认命令列表中出现 `i-have-adhd`。

### 更新

```bash
git -C ~/.config/opencode/vendor/i-have-adhd pull
```

### 卸载

从 `opencode.json` 中移除 `plugin` 条目。

### 始终启用（可选）

```bash
touch ~/.config/opencode/.i-have-adhd-always
```

标志存在期间，插件会在每一轮把完整规则追加到系统提示——相当于 Claude Code `SessionStart` 钩子的 OpenCode 版本。`stop adhd mode` 或 `normal mode` 可在当前会话中停用；删除该标志即可永久关闭始终启用：

```bash
rm ~/.config/opencode/.i-have-adhd-always
```

</details>


<details>
<summary><strong>Pi</strong></summary>

Pi 将此仓库识别为原生包：`extensions/` 提供会话级持久模式，`skills/` 保留 Agent Skills 入口点。

### 安装

```bash
pi install https://github.com/ayghri/i-have-adhd
```

开启新的 Pi 会话，为当前会话切换 ADHD 友好输出：

```text
/i-have-adhd
```

模式生效期间，页脚会显示 `● ADHD ON`。再次运行该命令即可关闭，也可以明确指定：

```text
/i-have-adhd on
/i-have-adhd off
stop adhd mode
```

与 Claude Code 的钩子类似，扩展只把规则集加入一次对话，而不是在每次请求时重写系统提示，并在压缩丢弃后重新注入。

现有的 Agent Skills 命令仍作为别名可用：

```text
/skill:i-have-adhd
```

以默认启用模式开启新的 Pi 会话：

```bash
pi --adhd
```

### 验证

```bash
pi list
```

确认列表中出现该 GitHub 包，然后输入 `/i-have-adhd`，检查页脚是否显示 `● ADHD ON`。

### 更新

```bash
pi update https://github.com/ayghri/i-have-adhd
```

或使用 `pi update --extensions` 更新所有未固定版本的 Pi 包。

### 卸载

```bash
pi remove https://github.com/ayghri/i-have-adhd
```

### 始终启用（可选）

在 Pi 的智能体配置目录中创建标志文件：

```bash
touch ~/.pi/agent/.i-have-adhd-always
```

扩展会在每个新建、恢复、分叉或重载的会话中检查该标志。当前会话已保存的选择优先于此默认值，因此 `stop adhd mode` 仍可让该会话保持关闭。

恢复为按需启用：

```bash
rm ~/.pi/agent/.i-have-adhd-always
```

### 配置文件（可选）

在 Pi 的智能体配置目录中创建 `~/.pi/agent/i-have-adhd.json`：

```json
{
  "alwaysOn": true,
  "hideStatus": true
}
```

- `alwaysOn`：每个会话都以规则启用开始——与 `.i-have-adhd-always` 标志文件等效，标志文件仍然可用
- `hideStatus`：隐藏 `● ADHD ON` 状态栏条目；规则和 `/i-have-adhd` 命令仍然有效

该文件在扩展启动时读取一次，修改后需重启 Pi。当前会话已保存的选择优先于 `alwaysOn`，因此 `stop adhd mode` 仍可让该会话保持关闭。

如果设置了 `PI_CODING_AGENT_DIR`，请改为在该目录中放置 `.i-have-adhd-always`。修改标志后运行 `/reload` 或开启新会话。

</details>


<details>
<summary><strong>Oh My Pi (OMP)</strong></summary>

### 安装

```bash
omp plugin marketplace add ayghri/i-have-adhd
omp plugin install --scope user i-have-adhd@i-have-adhd
```

开启新的 OMP 会话并运行 `/i-have-adhd` 切换模式。

### 更新

```bash
omp plugin marketplace update i-have-adhd
omp plugin upgrade --scope user i-have-adhd@i-have-adhd
```

### 卸载

```bash
omp plugin uninstall --scope user i-have-adhd@i-have-adhd
omp plugin marketplace remove i-have-adhd
```

</details>


<details>
<summary><strong>Qwen Code</strong></summary>

### 安装

```bash
qwen extensions install ayghri/i-have-adhd
```

Qwen Code 支持 GitHub 短路径，并可将该仓库安装为原生扩展。扩展会发现 `skills/` 下的技能。

安装扩展本身不会改变输出，除非输入 `/i-have-adhd` 显式调用此技能。

### 验证

```bash
qwen extensions list
```

然后启动新的 Qwen Code 会话并运行：

```text
/skills
```

确认列表中出现 `i-have-adhd`。

### 更新

```bash
qwen extensions update i-have-adhd
```

### 卸载

```bash
qwen extensions uninstall i-have-adhd
```

</details>

<details>
<summary><strong>Zed</strong></summary>

Zed 的 Agent 原生读取 Agent Skills：直接使用同一个 `SKILL.md`，无需转换。（Zed 旧版的“Rules”已由 Skills 和 `AGENTS.md` 指令取代。）

### 安装

在 Agent Panel 中打开 Skills 管理器，选择 **Create skill from URL**（命令面板中为 `agent: create skill from url`），然后粘贴：

```
https://github.com/ayghri/i-have-adhd/blob/main/skills/i-have-adhd/SKILL.md
```

要用于所有项目，请保存到 **User** 作用域；仅用于一个项目则保存到 **Project** 作用域。然后在 Agent Panel 中输入 `/i-have-adhd`。

偏好文件系统方式？克隆仓库并将技能文件夹放入用户 skills 目录：

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.agents/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.agents/skills/
```

### 验证

在 Agent Panel 中打开 Skills 管理器，确认列表中有 `i-have-adhd`。也可以输入 `/` 并确认它出现。

### 更新

从同一 URL 重新导入（会覆盖），或在 `git pull` 后重新复制文件夹。

### 卸载

从 Skills 管理器中移除 `i-have-adhd`，或删除 `~/.agents/skills/i-have-adhd`。

### 始终启用（可选）

添加到个人的 `~/.config/zed/AGENTS.md`：

```markdown
## 输出风格

读者有 ADHD。请让每条回复都便于立即执行：

1. 先给出答案或下一步行动：命令、路径或代码片段优先。
2. 为多步骤工作编号；每一步只包含一个明确的行动。
3. 最后给出一个能在两分钟内完成的下一步行动。
4. 先解决当前问题，再提出新问题。
5. 每轮重述进度（“5 步中的第 3 步已完成”）。
6. 用具体单位估算时间，绝不说“一会儿”。
7. 修改后说明现在可以正常工作的内容。
8. 出错时说明位置、原因和修复方法，不夸大。
9. 列表最多包含 5 项。
10. 不要前言、回顾或结束语。

例外：用户要求解释时应充分说明。执行破坏性操作前先确认。连续三次修复失败后停止，并指出可疑的假设。请求含糊时只问一个简短问题。
```

</details>

<details>
<summary><strong>Cursor、Amp 及其他 agent-skills 运行环境</strong></summary>

适用于任何能读取 Agent Skills 的运行环境。将 `-a <agent>` 替换为你的智能体。

### 安装

```bash
npx skills add ayghri/i-have-adhd                  # 当前项目
npx skills add ayghri/i-have-adhd -g               # 所有项目
npx skills add ayghri/i-have-adhd -a cursor -y     # 仅一个智能体
npx skills add ayghri/i-have-adhd -a opencode -y
```

开启新的智能体聊天并输入 `/i-have-adhd`。

不使用 CLI 时，将技能文件夹复制到智能体扫描的路径：

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.cursor/skills     # Cursor。OpenCode 使用 .agents/skills，其他智能体使用其自身路径
cp -R i-have-adhd/skills/i-have-adhd ~/.cursor/skills/
```

### 验证

```bash
npx skills list
npx skills ls -g    # 如果全局安装
```

### 更新

```bash
npx skills update i-have-adhd
npx skills update -g    # 如果全局安装
```

### 卸载

```bash
npx skills remove i-have-adhd
npx skills remove i-have-adhd -g    # 如果全局安装
```

### 始终启用（可选）

将此内容粘贴到智能体的持久规则文件。Cursor：**Settings → Rules → User Rules**，或在 `.cursor/rules/` 下创建设置了 `alwaysApply: true` 的项目规则。OpenCode：`~/.config/opencode/AGENTS.md`。

```markdown
## 输出风格

读者有 ADHD。请让每条回复都便于立即执行：

1. 先给出答案或下一步行动：命令、路径或代码片段优先。
2. 为多步骤工作编号；每一步只包含一个明确的行动。
3. 最后给出一个能在两分钟内完成的下一步行动。
4. 先解决当前问题，再提出新问题。
5. 每轮重述进度（“5 步中的第 3 步已完成”）。
6. 用具体单位估算时间，绝不说“一会儿”。
7. 修改后说明现在可以正常工作的内容。
8. 出错时说明位置、原因和修复方法，不夸大。
9. 列表最多包含 5 项。
10. 不要前言、回顾或结束语。

例外：用户要求解释时应充分说明。执行破坏性操作前先确认。连续三次修复失败后停止，并指出可疑的假设。请求含糊时只问一个简短问题。
```
</details>


## 启用机制

1. **已安装但未调用。** 在 Claude Code、Qwen Code 和 Codex 中，只有明确调用技能后才会发生变化。Claude Code 和 Qwen Code 遵循 `SKILL.md` 中的 `disable-model-invocation: true`；Codex 遵循 `agents/openai.yaml` 中的 `policy.allow_implicit_invocation: false`。其他运行环境可能会在启动时加载每个技能的描述，并自行启用技能。
2. **明确调用技能。** 在 Claude Code 或 Qwen Code 中输入 `/i-have-adhd`，在 Codex 中输入 `$i-have-adhd`。规则将在该会话中启用。输入“stop adhd mode”或“normal mode”可将其关闭。
3. **创建 `~/.claude/.i-have-adhd-always`**（Claude Code）。`SessionStart` 钩子会在每次会话中从第一条消息起加载完整规则。
4. **添加上面的始终启用片段**（其他运行环境）。这样会将核心规则保留在智能体的持久上下文中。

在 Claude Code、Qwen Code 和 Codex 中没有中间状态：未启用就是关闭。

## 故障排除

**自动补全中没有 `/i-have-adhd`。** 重启智能体。插件索引在启动时读取。

**始终启用标志无效。** 更新插件（`claude plugin marketplace update i-have-adhd`）并重启。钩子在启动时读取，且该标志需要包含 `hooks/hooks.json` 的插件版本。

**`claude plugin marketplace add` 失败。** 使用 `owner/repo` 格式。本地路径必须指向仓库根目录，而不是 `.claude-plugin/`。

**已安装，但回复仍有开场白。** 开启新会话。如果仍然偏离，请收紧 `skills/i-have-adhd/SKILL.md` 中的措辞。

**想使用不同规则。** Fork 仓库，编辑 `skills/i-have-adhd/SKILL.md`，然后换成你的副本：

```bash
claude plugin uninstall i-have-adhd            # 先移除上游副本：
claude plugin marketplace remove i-have-adhd   # fork 与上游使用相同名称
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

重启，然后再次调用 `/i-have-adhd`。

**执行 `npx skills add` 后找不到技能。** 开启新的智能体聊天。技能在会话开始时建立索引。确认文件夹位于智能体扫描的位置（Cursor 为 `~/.cursor/skills/`，OpenCode 为 `.agents/skills/`），且 frontmatter 中的 `name` 与文件夹名称一致。
