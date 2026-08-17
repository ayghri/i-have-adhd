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

恢复为按需启用：

```bash
rm ~/.claude/.i-have-adhd-always
```

该钩子只在标志文件存在时触发，因此仅安装插件不会改变任何行为。如果移动了配置目录，它会遵循 `$CLAUDE_CONFIG_DIR`。“stop adhd mode”仍可在当前会话中将其关闭。

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

### 安装 (command, opt-in)

```bash
mkdir -p ~/.gemini/commands
curl -fsSL https://raw.githubusercontent.com/ayghri/i-have-adhd/main/skills/i-have-adhd/agents/gemini.toml \
  -o ~/.gemini/commands/i-have-adhd.toml
```

开始新会话并输入 `/i-have-adhd`。它会在该会话中持续启用。

### 安装 (extension, always-on)

```bash
gemini extensions install https://github.com/ayghri/i-have-adhd
```

扩展会加载导入完整技能的 `GEMINI.md`，因此规则从第一条消息起生效。必须安装 `git`。

### 验证

```bash
gemini extensions list          # 扩展方式
ls ~/.gemini/commands           # command route: i-have-adhd.toml present
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
rm ~/.gemini/commands/i-have-adhd.toml     # command route
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

输入 `/i-have-adhd`。 The skill installs into `~/.hermes/skills/` and is exposed as a slash command at the next session start.

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
<summary><strong>Pi</strong></summary>

Pi 会将此仓库识别为原生软件包：`extensions/` 提供会话持久模式，`skills/` 继续提供 Agent Skills 入口。

### 安装

```bash
pi install https://github.com/ayghri/i-have-adhd
```

启动新的 Pi 会话。为当前会话切换 ADHD 友好输出：

```text
/i-have-adhd
```

模式启用期间，页脚会显示 `● ADHD ON`。再次运行该命令即可关闭，也可以显式指定：

```text
/i-have-adhd on
/i-have-adhd off
stop adhd mode
```

与 Claude Code 的钩子类似，该扩展只在会话中添加一次规则，而不是每次请求都重写系统提示词，并在压缩（compaction）导致规则丢失后重新添加。

现有的 Agent Skills 命令仍可作为别名使用：

```text
/skill:i-have-adhd
```

以默认启用该模式的方式启动新的 Pi 会话：

```bash
pi --adhd
```

### 验证

```bash
pi list
```

确认列表中包含该 GitHub 软件包，然后输入 `/i-have-adhd` 并检查页脚是否显示 `● ADHD ON`。

### 更新

```bash
pi update https://github.com/ayghri/i-have-adhd
```

也可以用 `pi update --extensions` 更新所有未锁定版本的 Pi 软件包。

### 卸载

```bash
pi remove https://github.com/ayghri/i-have-adhd
```

### 始终启用（可选）

在 Pi 的代理配置目录中创建一个标志文件：

```bash
touch ~/.pi/agent/.i-have-adhd-always
```

该扩展会在每次新建、恢复、分叉或重新加载的会话中检查此标志。当前会话中已保存的选择优先于此默认值，因此 "stop adhd mode" 仍会让该会话保持关闭。

恢复为按需启用：

```bash
rm ~/.pi/agent/.i-have-adhd-always
```

如果设置了 `PI_CODING_AGENT_DIR`，请改为将 `.i-have-adhd-always` 放在该目录下。更改标志后，请运行 `/reload` 或开始新会话。

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
cp -R i-have-adhd/skills/i-have-adhd ~/.config/zed/skills/
```

### 验证

在 Agent Panel 中打开 Skills 管理器，确认列表中有 `i-have-adhd`。也可以输入 `/` 并确认它出现。

### 更新

从同一 URL 重新导入（会覆盖），或在 `git pull` 后重新复制文件夹。

### 卸载

从 Skills 管理器中移除 `i-have-adhd`，或删除 `~/.config/zed/skills/i-have-adhd`。

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
<summary><strong>Cursor、OpenCode、Amp 及其他 agent-skills 运行环境</strong></summary>

适用于任何能读取 Agent Skills 的运行环境。将 `-a <agent>` 替换为你的智能体。

### 安装

```bash
npx skills add ayghri/i-have-adhd                  # this workspace
npx skills add ayghri/i-have-adhd -g               # 所有项目
npx skills add ayghri/i-have-adhd -a cursor -y     # one agent only
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
