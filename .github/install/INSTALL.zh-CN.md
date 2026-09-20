# 安装方法

本仓库是 [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) 的中文 fork：[aixinwudi/i-have-adhd-cn](https://github.com/aixinwudi/i-have-adhd-cn)。下面所有命令都用这个地址；换成你自己的 fork 时，把仓库地址改掉即可。

<details>
<summary><strong>Antigravity (<code>agy</code>)</strong></summary>

### 安装

```bash
agy plugin install https://github.com/aixinwudi/i-have-adhd-cn
```

### 验证

```bash
agy plugin list
```

### 更新

```bash
agy plugin uninstall i-have-adhd
agy plugin install https://github.com/aixinwudi/i-have-adhd-cn
```

### 卸载

```bash
agy plugin uninstall i-have-adhd
```

也可以保留安装但先关掉它：`agy plugin disable i-have-adhd`。

### 始终启用（可选）

添加到 `~/.gemini/GEMINI.md`：

```markdown
## 输出风格

读者有 ADHD。把每一条回复都塑造成可以直接执行的样子：

1. 先给答案或下一步行动：命令、路径或代码片段放在最前面。
2. 多步骤工作要编号；每一步一个边界清楚的动作。
3. 以唯一一个下一步收尾，两分钟内能做完。
4. 先把当前问题收尾，再提新问题。
5. 每一轮重述进度（“5 步中的第 3 步完成”）。
6. 用具体单位给时间估计，绝不说“一点”。
7. 一次改动之后，说明现在什么能用了。
8. 报错时说清位置、原因和修复方式，不带情绪。
9. 列表最多 5 项。
10. 不写开场白、不写回顾、不写结束语。

例外情况：要求解释时完整解释。破坏性操作前先确认。连续三次修不好就停下来，指出可疑的假设。请求有歧义时，只问一个简短的问题。

另外：始终用简体中文回复；用户使用其他语言时跟随用户的语言。
```

</details>

<details>
<summary><strong>AstronClaw（自定义技能）</strong></summary>

AstronClaw 支持把 Markdown 文件导入为自定义技能。这条路线直接复用仓库里现成的 `SKILL.md`；上传和管理入口见它的[官方技能指南](https://github.com/iflytek/astronclaw-tutorial/blob/main/docs/guide/astronclaw/skills.md)。

下面的步骤依照 AstronClaw 的文档写成，但没有用本技能实测过。启用前请先检查导入后的指令内容。

### 安装

1. 下载[标准 SKILL.md](https://raw.githubusercontent.com/aixinwudi/i-have-adhd-cn/main/skills/i-have-adhd/SKILL.md)，保存为 `SKILL.md`。上传前先看一遍内容。
2. 在 AstronClaw 中打开 **我的技能 (My skills)**，点 **新建 (New)**，上传这个 `.md` 文件。
3. 确认导入的技能名为 `i-have-adhd`。用 **启用/禁用 (Enable/Disable)** 控制它是否可用。

只需要技能 Markdown 文件。上传会把该文件发送到 AstronClaw；仓库里的插件清单和 hooks 不参与这条安装路线。

### 验证与启用

确认 **我的技能** 里出现 `i-have-adhd`。可以用 **下载 (Download)** 导出导入后的指令，和原始技能对比，然后启用并试一句：

```text
本次对话使用 i-have-adhd 技能。说明如何在新文件夹里创建一个空的 Git 仓库。
```

检查回复是否先给行动、步骤是否编号。这是对导入技能的人工检查；只上传成功并不能证明它的输出规则已经生效。

### 启用说明

AstronClaw 同时支持显式请求和自动调用技能。它的文档没有说明是否遵循 `disable-model-invocation: true`，所以不想要这个技能时，直接用 **禁用**。不需要依赖 `/i-have-adhd` 斜杠命令。

技能会要求助手在本次对话里保持这种风格，直到你说“停止 ADHD 模式”或“正常模式”。这个指令不会改变平台的开关；想彻底不用，就禁用技能并开一个新对话。

### 更新

下载最新的标准 `SKILL.md`。如果你改过导入的那份，先用 **下载 (Download)** 备份。想要干净替换，就删掉旧的 `i-have-adhd` 条目，重新导入，然后在新对话里跑一次验证用的提示词。

### 卸载

在 **我的技能** 里选中 `i-have-adhd`，点 **删除 (Delete)**，然后开一个新对话。想留着以后再用就点 **禁用**。

</details>

<details>
<summary><strong>Claude Code</strong></summary>

### 安装

```bash
claude plugin marketplace add aixinwudi/i-have-adhd-cn
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

也可以保留安装但先关掉它：`claude plugin disable i-have-adhd`。

### 始终启用（可选）

`SessionStart` hook 会在每个会话开始时载入完整规则，不需要 `/i-have-adhd`：

```bash
touch ~/.claude/.i-have-adhd-always
```

如果你用的是自定义 Claude 配置目录，就在那个目录里创建标记文件：

```bash
touch "$CLAUDE_CONFIG_DIR/.i-have-adhd-always"
```

改回按需启用：

```bash
rm ~/.claude/.i-have-adhd-always
```

只有标记文件存在时 hook 才会触发，所以单是安装插件不会改变任何行为。当前会话里说“停止 ADHD 模式”依然可以关掉它。

</details>

<details>
<summary><strong>Codex</strong></summary>

### 安装

```bash
codex plugin marketplace add aixinwudi/i-have-adhd-cn --ref main
codex plugin add i-have-adhd@i-have-adhd
```

输入 `$i-have-adhd` 显式调用这个技能。Codex 不会自动启用它。

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

读者有 ADHD。把每一条回复都塑造成可以直接执行的样子：

1. 先给答案或下一步行动：命令、路径或代码片段放在最前面。
2. 多步骤工作要编号；每一步一个边界清楚的动作。
3. 以唯一一个下一步收尾，两分钟内能做完。
4. 先把当前问题收尾，再提新问题。
5. 每一轮重述进度（“5 步中的第 3 步完成”）。
6. 用具体单位给时间估计，绝不说“一点”。
7. 一次改动之后，说明现在什么能用了。
8. 报错时说清位置、原因和修复方式，不带情绪。
9. 列表最多 5 项。
10. 不写开场白、不写回顾、不写结束语。

例外情况：要求解释时完整解释。破坏性操作前先确认。连续三次修不好就停下来，指出可疑的假设。请求有歧义时，只问一个简短的问题。

另外：始终用简体中文回复；用户使用其他语言时跟随用户的语言。
```

</details>

<details>
<summary><strong>Grok (<code>grok</code>)</strong></summary>

Grok 直接加载仓库里已有的插件和技能文件，不需要单独的 Grok 清单。从 GitHub 直接安装，启用插件，然后调用技能。有两个 Grok 特有的步骤：`--trust`（不加它 hooks 和技能都不会生效）和 `grok plugin enable`（插件默认关闭，启用后才生效）。

### 安装

```bash
grok plugin install aixinwudi/i-have-adhd-cn --trust
grok plugin enable i-have-adhd
```

开一个新的 Grok 会话，输入 `/i-have-adhd`。Grok 遵循 `disable-model-invocation: true`，所以在调用技能或打开始终启用之前，不会有任何变化。

### 验证

```bash
grok plugin list
grok plugin details i-have-adhd
```

确认 `i-have-adhd` 已列出、已启用，并且显示一个技能加 hooks。

### 更新

```bash
grok plugin update i-have-adhd
```

### 卸载

```bash
grok plugin uninstall i-have-adhd --confirm
```

也可以保留安装但先关掉它：`grok plugin disable i-have-adhd`。

### 始终启用（可选）

把下面的块加到 `~/.grok/AGENTS.md`，或者放进 `~/.grok/rules/i-have-adhd.md`（Grok 在会话开始时会读这两处）：

```markdown
## 输出风格

读者有 ADHD。把每一条回复都塑造成可以直接执行的样子：

1. 先给答案或下一步行动：命令、路径或代码片段放在最前面。
2. 多步骤工作要编号；每一步一个边界清楚的动作。
3. 以唯一一个下一步收尾，两分钟内能做完。
4. 先把当前问题收尾，再提新问题。
5. 每一轮重述进度（“5 步中的第 3 步完成”）。
6. 用具体单位给时间估计，绝不说“一点”。
7. 一次改动之后，说明现在什么能用了。
8. 报错时说清位置、原因和修复方式，不带情绪。
9. 列表最多 5 项。
10. 不写开场白、不写回顾、不写结束语。

例外情况：要求解释时完整解释。破坏性操作前先确认。连续三次修不好就停下来，指出可疑的假设。请求有歧义时，只问一个简短的问题。

另外：始终用简体中文回复；用户使用其他语言时跟随用户的语言。
```

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

Gemini CLI 没有插件市场，所以有两条原生路线：**自定义命令**（按需启用，你不调用就不生效）或 **扩展**（安装后始终启用）。命令路线符合本技能的默认姿态；除非你想每个会话都生效，否则选它。

### 安装（命令方式，按需启用）

```bash
mkdir -p ~/.gemini/commands
curl -fsSL https://raw.githubusercontent.com/aixinwudi/i-have-adhd-cn/main/skills/i-have-adhd/agents/gemini.toml \
  -o ~/.gemini/commands/i-have-adhd.toml
```

开一个新会话，输入 `/i-have-adhd`。它在本次会话里持续生效。

### 安装（扩展方式，始终启用）

```bash
gemini extensions install https://github.com/aixinwudi/i-have-adhd-cn
```

扩展会加载 `GEMINI.md`，而后者导入了完整技能，所以从第一条消息起规则就生效。需要先装好 `git`。

### 验证

```bash
gemini extensions list          # 扩展方式
ls ~/.gemini/commands           # 命令方式：i-have-adhd.toml 已存在
```

或者在会话里输入 `/`，确认列表里出现 `i-have-adhd`。

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

Copilot 原生读取 Agent Skills：同一个 `SKILL.md`，不需要转换。它会扫描项目里的 `.github/skills/`、`.claude/skills/` 和 `.agents/skills/`，以及全局的 `~/.copilot/skills/`、`~/.claude/skills/`、`~/.agents/skills/`。

### 安装

```bash
npx skills add aixinwudi/i-have-adhd-cn -a github-copilot        # 当前项目
npx skills add aixinwudi/i-have-adhd-cn -a github-copilot -g     # 所有项目
```

不用 CLI 的话，把技能目录复制到 Copilot 会扫描的任意位置：

```bash
git clone https://github.com/aixinwudi/i-have-adhd-cn i-have-adhd
mkdir -p ~/.copilot/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.copilot/skills/
```

### 验证

在聊天输入框里输入 `/`，确认出现 `i-have-adhd`。或者：

```bash
npx skills list
npx skills ls -g    # 全局安装时
```

### 更新

```bash
npx skills update i-have-adhd
```

或者 `git pull` 之后重新复制目录。

### 卸载

```bash
npx skills remove i-have-adhd
```

或者从它所在的技能目录里删除 `i-have-adhd` 文件夹。

### 启用说明

Copilot 遵循 `disable-model-invocation`：在你调用技能之前不会有任何变化，和 Claude Code 一样（已在 [#60](https://github.com/aixinwudi/i-have-adhd-cn/pull/60) 测试）。

### 始终启用（可选）

把下面的块加到项目的 `.github/copilot-instructions.md`（Copilot 每次聊天都会读它）：

```markdown
## 输出风格

读者有 ADHD。把每一条回复都塑造成可以直接执行的样子：

1. 先给答案或下一步行动：命令、路径或代码片段放在最前面。
2. 多步骤工作要编号；每一步一个边界清楚的动作。
3. 以唯一一个下一步收尾，两分钟内能做完。
4. 先把当前问题收尾，再提新问题。
5. 每一轮重述进度（“5 步中的第 3 步完成”）。
6. 用具体单位给时间估计，绝不说“一点”。
7. 一次改动之后，说明现在什么能用了。
8. 报错时说清位置、原因和修复方式，不带情绪。
9. 列表最多 5 项。
10. 不写开场白、不写回顾、不写结束语。

例外情况：要求解释时完整解释。破坏性操作前先确认。连续三次修不好就停下来，指出可疑的假设。请求有歧义时，只问一个简短的问题。

另外：始终用简体中文回复；用户使用其他语言时跟随用户的语言。
```

</details>

<details>
<summary><strong>Hermes</strong></summary>

### 安装

```bash
hermes skills install aixinwudi/i-have-adhd-cn/skills/i-have-adhd
```

输入 `/i-have-adhd`。技能会装到 `~/.hermes/skills/`，并在下一个会话开始时作为斜杠命令出现。

想先看看再装？把这个仓库添加为技能源（一个 "tap"），然后搜索并安装：

```bash
hermes skills tap add aixinwudi/i-have-adhd-cn
hermes skills search adhd
hermes skills install aixinwudi/i-have-adhd-cn/skills/i-have-adhd
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

也可以顺便移除 tap：`hermes skills tap remove aixinwudi/i-have-adhd-cn`。

### 始终启用（可选）

加到工作目录里的 `AGENTS.md`（Hermes 按工作目录加载），或者加到 persona 的 `SOUL.md` 让每个会话都生效：

```markdown
## 输出风格

读者有 ADHD。把每一条回复都塑造成可以直接执行的样子：

1. 先给答案或下一步行动：命令、路径或代码片段放在最前面。
2. 多步骤工作要编号；每一步一个边界清楚的动作。
3. 以唯一一个下一步收尾，两分钟内能做完。
4. 先把当前问题收尾，再提新问题。
5. 每一轮重述进度（“5 步中的第 3 步完成”）。
6. 用具体单位给时间估计，绝不说“一点”。
7. 一次改动之后，说明现在什么能用了。
8. 报错时说清位置、原因和修复方式，不带情绪。
9. 列表最多 5 项。
10. 不写开场白、不写回顾、不写结束语。

例外情况：要求解释时完整解释。破坏性操作前先确认。连续三次修不好就停下来，指出可疑的假设。请求有歧义时，只问一个简短的问题。

另外：始终用简体中文回复；用户使用其他语言时跟随用户的语言。
```

</details>

<details>
<summary><strong>Kimi Code CLI</strong></summary>

### 安装

先进入一个 Kimi Code 会话，然后：

1. 运行 `/plugins`。
2. 选择 **Custom**。
3. 粘贴 `https://github.com/aixinwudi/i-have-adhd-cn` 并按 `Enter`。
4. 选择 **Trust and install**。

用斜杠命令 `/skill:i-have-adhd` 显式调用技能。

### 更新

在 Kimi Code 会话里运行 `/plugins`，光标移到 **I Have ADHD**，按 `R`。

### 卸载

在 Kimi Code 会话里运行 `/plugins`，光标移到 **I Have ADHD**，按 `D`。

</details>

<details>
<summary><strong>OpenCode</strong></summary>

OpenCode 把这个仓库作为服务端插件加载：`.opencode/plugins/i-have-adhd.mjs` 注册 `skills/` 入口和 `/i-have-adhd` 命令，并在开启始终启用时注入规则。OpenCode 也能原生读取 `skills/`，所以没有插件时技能依然可用——插件额外提供的是 `/i-have-adhd` 命令和始终启用开关。

### 安装

克隆仓库，让 OpenCode 指向插件。用绝对路径可以让所有项目共用一份检出：

```bash
git clone https://github.com/aixinwudi/i-have-adhd-cn ~/.config/opencode/vendor/i-have-adhd
```

加到你的 `opencode.json`（全局配置在 `~/.config/opencode/opencode.json`）：

```json
{ "plugin": ["/absolute/path/to/i-have-adhd/.opencode/plugins/i-have-adhd.mjs"] }
```

也可以直接从检出目录里运行 OpenCode——仓库根目录的 `opencode.json` 已经接好插件。

开一个新会话，为本次会话打开 ADHD 友好输出：

```text
/i-have-adhd
```

规则会一直生效，直到你说“停止 ADHD 模式”或“正常模式”。

### 验证

启动 OpenCode，输入 `/`，确认命令列表里出现 `i-have-adhd`。

### 更新

```bash
git -C ~/.config/opencode/vendor/i-have-adhd pull
```

### 卸载

从 `opencode.json` 里删掉那个 `plugin` 条目。

### 始终启用（可选）

```bash
touch ~/.config/opencode/.i-have-adhd-always
```

标记文件存在期间，插件每一轮都会把完整规则追加到 system prompt —— 也就是 OpenCode 版的 Claude Code `SessionStart` hook。说“停止 ADHD 模式”或“正常模式”会为当前会话关掉它；删除标记文件则永久关闭始终启用：

```bash
rm ~/.config/opencode/.i-have-adhd-always
```

</details>

<details>
<summary><strong>Pi</strong></summary>

Pi 把这个仓库识别为原生包：`extensions/` 提供会话内的持久模式，`skills/` 保留 Agent Skills 入口。

### 安装

```bash
pi install https://github.com/aixinwudi/i-have-adhd-cn
```

开一个新的 Pi 会话。为当前会话切换 ADHD 友好输出：

```text
/i-have-adhd
```

模式开启时页脚显示 `● ADHD 已开启`。再运行一次命令可以关掉，也可以明确指定：

```text
/i-have-adhd on
/i-have-adhd off
stop adhd mode
```

和 Claude Code 的 hook 一样，扩展只把规则往对话里加一次，而不是每个请求都重写 system prompt；上下文压缩把它丢掉之后会重新加一次。

原有的 Agent Skills 命令仍然作为别名可用：

```text
/skill:i-have-adhd
```

启动一个默认开启该模式的新 Pi 会话：

```bash
pi --adhd
```

### 验证

```bash
pi list
```

确认列出了这个 GitHub 包，然后输入 `/i-have-adhd`，检查页脚是否出现 `● ADHD 已开启`。

### 更新

```bash
pi update https://github.com/aixinwudi/i-have-adhd-cn
```

或者用 `pi update --extensions` 更新所有未锁版本的 Pi 包。

### 卸载

```bash
pi remove https://github.com/aixinwudi/i-have-adhd-cn
```

### 始终启用（可选）

在 Pi 的 agent 配置目录里创建标记文件：

```bash
touch ~/.pi/agent/.i-have-adhd-always
```

扩展会在每个新建、恢复、fork 或重新加载的会话里检查这个标记。当前会话里保存过的选择优先于这个默认值，所以说“停止 ADHD 模式”会保持该会话关闭。

改回按需启用：

```bash
rm ~/.pi/agent/.i-have-adhd-always
```

### 配置文件（可选）

在 Pi 的 agent 配置目录里创建 `~/.pi/agent/i-have-adhd.json`：

```json
{
  "alwaysOn": true,
  "hideStatus": true
}
```

- `alwaysOn`：每个会话启动时规则就生效——和 `.i-have-adhd-always` 标记文件效果一样，标记文件也仍然有效
- `hideStatus`：隐藏状态栏里的 `● ADHD 已开启` 条目；规则和 `/i-have-adhd` 命令照常工作

配置文件只在扩展启动时读一次，改完要重启 Pi。当前会话里保存过的选择优先于 `alwaysOn`，所以说“停止 ADHD 模式”会保持该会话关闭。

如果设置了 `PI_CODING_AGENT_DIR`，就把 `.i-have-adhd-always` 放在那个目录里。改动标记后运行 `/reload` 或开一个新会话。

</details>

<details>
<summary><strong>Oh My Pi (OMP)</strong></summary>

### 安装

```bash
omp plugin marketplace add aixinwudi/i-have-adhd-cn
omp plugin install --scope user i-have-adhd@i-have-adhd
```

开一个新的 OMP 会话，运行 `/i-have-adhd` 切换模式。

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
qwen extensions install aixinwudi/i-have-adhd-cn
```

Qwen Code 支持 GitHub 简写形式，会把仓库装成原生扩展。扩展会在 `skills/` 下发现这个技能。

输入 `/i-have-adhd` 显式调用技能。只安装扩展、不调用技能，输出不会有变化。

### 验证

```bash
qwen extensions list
```

然后开一个新的 Qwen Code 会话并运行：

```text
/skills
```

确认列表里出现 `i-have-adhd`。

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

Zed 的 Agent 原生读取 Agent Skills，用的是同一套 SKILL.md 格式，不需要转换。注意 Zed 旧版的 "Rules" 已经被 Skills 和 AGENTS.md 指令取代。

### 安装

在 Agent Panel 里打开 Skills 管理器，选择 **Create skill from URL**（命令面板里是 `agent: create skill from url`），然后粘贴：

```
https://github.com/aixinwudi/i-have-adhd-cn/blob/main/skills/i-have-adhd/SKILL.md
```

保存时选 **User** 作用域可对所有项目生效，选 **Project** 只对一个项目生效。然后在 Agent Panel 里输入 `/i-have-adhd`。

更想直接放文件？克隆仓库，把技能目录放进你的用户技能目录：

```bash
git clone https://github.com/aixinwudi/i-have-adhd-cn i-have-adhd
mkdir -p ~/.agents/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.agents/skills/
```

### 验证

在 Agent Panel 里打开 Skills 管理器，确认列出了 `i-have-adhd`。或者输入 `/`，确认它出现在列表里。

### 更新

从同一个 URL 重新导入（会覆盖），或者 `git pull` 之后重新复制目录。

### 卸载

从 Skills 管理器里移除 `i-have-adhd`，或者删除 `~/.agents/skills/i-have-adhd`。

### 始终启用（可选）

加到你的个人 `~/.config/zed/AGENTS.md`：

```markdown
## 输出风格

读者有 ADHD。把每一条回复都塑造成可以直接执行的样子：

1. 先给答案或下一步行动：命令、路径或代码片段放在最前面。
2. 多步骤工作要编号；每一步一个边界清楚的动作。
3. 以唯一一个下一步收尾，两分钟内能做完。
4. 先把当前问题收尾，再提新问题。
5. 每一轮重述进度（“5 步中的第 3 步完成”）。
6. 用具体单位给时间估计，绝不说“一点”。
7. 一次改动之后，说明现在什么能用了。
8. 报错时说清位置、原因和修复方式，不带情绪。
9. 列表最多 5 项。
10. 不写开场白、不写回顾、不写结束语。

例外情况：要求解释时完整解释。破坏性操作前先确认。连续三次修不好就停下来，指出可疑的假设。请求有歧义时，只问一个简短的问题。

另外：始终用简体中文回复；用户使用其他语言时跟随用户的语言。
```

</details>
<details>
<summary><strong>Cursor、Amp 及其他 agent-skills 运行环境</strong></summary>

任何能读取 agent skills 的运行环境都可以用。把 `-a <agent>` 换成你的工具。

### 安装

```bash
npx skills add aixinwudi/i-have-adhd-cn                  # 当前工作区
npx skills add aixinwudi/i-have-adhd-cn -g               # 所有项目
npx skills add aixinwudi/i-have-adhd-cn -a cursor -y     # 只装给一个 agent
npx skills add aixinwudi/i-have-adhd-cn -a opencode -y
```

在新的 agent 对话里输入 `/i-have-adhd`。

不用 CLI 的话，把技能目录复制到你的 agent 会扫描的路径：

```bash
git clone https://github.com/aixinwudi/i-have-adhd-cn i-have-adhd
mkdir -p ~/.cursor/skills     # Cursor。OpenCode 用 .agents/skills，其他 agent 用各自的路径
cp -R i-have-adhd/skills/i-have-adhd ~/.cursor/skills/
```

### 验证

```bash
npx skills list
npx skills ls -g    # 全局安装时
```

### 更新

```bash
npx skills update i-have-adhd
npx skills update -g    # 全局安装时
```

### 卸载

```bash
npx skills remove i-have-adhd
npx skills remove i-have-adhd -g    # 全局安装时
```

### 始终启用（可选）

把下面这块贴进你的 agent 的常驻规则文件。Cursor：**Settings → Rules → User Rules**，或者放在 `.cursor/rules/` 下并加 `alwaysApply: true` 的项目规则。OpenCode：`~/.config/opencode/AGENTS.md`。

```markdown
## 输出风格

读者有 ADHD。把每一条回复都塑造成可以直接执行的样子：

1. 先给答案或下一步行动：命令、路径或代码片段放在最前面。
2. 多步骤工作要编号；每一步一个边界清楚的动作。
3. 以唯一一个下一步收尾，两分钟内能做完。
4. 先把当前问题收尾，再提新问题。
5. 每一轮重述进度（“5 步中的第 3 步完成”）。
6. 用具体单位给时间估计，绝不说“一点”。
7. 一次改动之后，说明现在什么能用了。
8. 报错时说清位置、原因和修复方式，不带情绪。
9. 列表最多 5 项。
10. 不写开场白、不写回顾、不写结束语。

例外情况：要求解释时完整解释。破坏性操作前先确认。连续三次修不好就停下来，指出可疑的假设。请求有歧义时，只问一个简短的问题。

另外：始终用简体中文回复；用户使用其他语言时跟随用户的语言。
```

</details>

## 启用机制

1. **只安装，不调用。** 在 Claude Code、Qwen Code、Codex 和 Grok 里，你不显式调用技能就什么都不会发生。Claude Code、Qwen Code 和 Grok 遵循 `SKILL.md` 里的 `disable-model-invocation: true`；Codex 遵循 `agents/openai.yaml` 里的 `policy.allow_implicit_invocation: false`。其他运行环境可能会在启动时读取每个技能的描述，并自行激活技能。
2. **你显式调用。** 在 Claude Code、Qwen Code 或 Grok 里输入 `/i-have-adhd`，在 Codex 里输入 `$i-have-adhd`。规则在本次会话内持续生效。说“停止 ADHD 模式”或“正常模式”可以关掉。
3. **你创建 `~/.claude/.i-have-adhd-always`**（Claude Code）。`SessionStart` hook 从第一条消息起就载入完整规则，每个会话都如此。
4. **你添加上面的始终启用片段**（Grok、Codex 和其他运行环境）。Grok 会读 `~/.grok/AGENTS.md` 和 `~/.grok/rules/*.md`。这样能把核心规则放进 agent 的常驻上下文。

在 Claude Code、Qwen Code、Codex 和 Grok 里没有中间状态：你没打开，它就是关的。

## 故障排除

**自动补全里没有 `/i-have-adhd`。** 重启 agent。插件索引只在启动时读取。在 Grok 上还要运行 `grok plugin enable i-have-adhd`，并确认安装时用了 `--trust`。

**始终启用标记不生效。** 更新插件（`claude plugin marketplace update i-have-adhd`）并重启。hooks 在启动时读取，而这个标记需要带 `hooks/hooks.json` 的插件版本。Grok 不读 `~/.claude/.i-have-adhd-always`；把始终启用块放进 `~/.grok/AGENTS.md` 或 `~/.grok/rules/i-have-adhd.md`。

**`claude plugin marketplace add` 失败。** 用 `owner/repo` 形式。本地路径必须指向仓库根目录，不能指向 `.claude-plugin/`。

**`grok plugin install` 看起来什么都没发生。** 加上 `--trust`，然后运行 `grok plugin enable i-have-adhd`，再开一个新会话。缺少这两步，Grok 插件会一直处于关闭且不受信任的状态。

**装上了，回复还是先讲一堆废话。** 开一个新会话。如果还是飘，就去收紧 `skills/i-have-adhd/SKILL.md` 里的措辞。

**想要不一样的规则。** Fork 仓库，编辑 `skills/i-have-adhd/SKILL.md`，然后换上你的副本：

```bash
claude plugin uninstall i-have-adhd            # 先移除上游副本：
claude plugin marketplace remove i-have-adhd   # fork 与上游同名
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

重启，然后重新调用 `/i-have-adhd`。

**`npx skills add` 之后找不到技能。** 开一个新的 agent 对话。技能索引在会话开始时建立。确认目录落在你的 agent 会扫描的位置（Cursor 是 `~/.cursor/skills/`，OpenCode 是 `.agents/skills/`），并且 frontmatter 里的 `name` 和目录名一致。
