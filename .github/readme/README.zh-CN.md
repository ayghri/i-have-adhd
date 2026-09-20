<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">对 ADHD 友好的输出。无需确诊 ADHD！</strong>
</p>
<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/aixinwudi/i-have-adhd-cn?style=flat" alt="License"></a>
</p>

<p align="center">
  <strong title="简体中文" aria-label="简体中文">🇨🇳</strong> ·
  <a href="README.en.md" title="English" aria-label="English">🇬🇧</a> ·
  <a href="README.es.md" title="Español" aria-label="Español">🇪🇸</a> ·
  <a href="README.pt-BR.md" title="Português (Brasil)" aria-label="Português (Brasil)">🇧🇷</a> ·
  <a href="README.ja.md" title="日本語" aria-label="日本語">🇯🇵</a> ·
  <a href="README.vi.md" title="Tiếng Việt" aria-label="Tiếng Việt">🇻🇳</a> ·
  <a href="README.ko.md" title="한국어" aria-label="한국어">🇰🇷</a> ·
  <a href="README.fa.md" title="فارسی" aria-label="فارسی">🇮🇷</a> ·
  <a href="README.th.md" title="ภาษาไทย" aria-label="ภาษาไทย">🇹🇭</a> ·
  <a href="README.ar.md" title="العربية" aria-label="العربية">🇸🇦</a>
</p>


## 这个中文版改了什么

- **上游项目**：[ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd)。本仓库是它的中文 fork：[aixinwudi/i-have-adhd-cn](https://github.com/aixinwudi/i-have-adhd-cn)。
- **默认用简体中文回复。** 上游版本是英文规则，装上后模型倾向于跟着用英文回答；这里的技能文件全部改成了中文，并明确写了语言规则：默认中文，用户换语言就跟着换，代码、命令、路径和报错原文不翻译。
- **所有会注入到模型上下文里的文字都翻成了中文**：技能正文、hook 注入的横幅、OpenCode 插件与命令、Gemini 命令、Pi/OMP 扩展、各家插件清单里的描述。
- **英文原文保留**：`README.en` 与 `INSTALL.en` 分别在 [.github/readme/](README.en.md) 和 [.github/install/](../install/INSTALL.en.md)。

只想要中文输出、不想要其他改动的，直接装这个 fork 就行。

## 安装

复制粘贴到你的 CLI 对话框：

```text
从 https://github.com/aixinwudi/i-have-adhd-cn 安装 i-have-adhd 技能/插件，具体步骤参考仓库的 AGENTS.md。
```

Codex 里的最短路径（本仓库地址）：

```text
codex plugin marketplace add aixinwudi/i-have-adhd-cn --ref main
codex plugin add i-have-adhd@i-have-adhd
```

然后输入 `$i-have-adhd` 调用。其他运行环境（Claude Code、Grok、Gemini、Copilot、Zed、OpenCode、Pi、OMP、Qwen、Kimi 等）见 🔗 [安装说明](../install/INSTALL.zh-CN.md)。

## 功能

一个给编程助手用的技能，让它别把答案埋进长篇大论。行动优先。步骤编号。不说“希望这能帮到你！”

[Kacper Rutkiewicz | AI Made Simple](https://youtu.be/NEl8kPWZP_Y) 讲解过这个技能的早期版本。

## 有什么变化


<table>
<tr>
<td width="50%">

## 之前

> 问得好！让我想一想。你的身份验证流程包含几个环节：中间件、令牌验证和 Cookie 处理。查看 `src/auth.ts` 后，`verifyToken` 函数（大约第 42–58 行）似乎使用了旧版 `jsonwebtoken` API。一种做法是升级这个包并重写该函数。完成修改后，你需要运行身份验证测试，确认没有破坏任何功能。顺便一提，你可能还想整体检查一下依赖版本。希望这能帮到你！如果你想进一步研究，请告诉我。

</td>

<td width="50%">

## 之后

> 运行 `npm install jsonwebtoken@latest`，然后编辑 `src/auth.ts:42`。
>
> 1. 打开 `src/auth.ts`
> 2. 将 `verifyToken`（第 42–58 行）替换为下面的代码片段
> 3. 运行 `npm test -- auth.spec.ts`
>
> 下一步：如果有测试失败，请粘贴第一行报错。

</td>
</tr>
</table>


## 规则

10 条规则。完整内容见 [SKILL.md](../../skills/i-have-adhd/SKILL.md)。

1. 先说下一步行动。
2. 多步骤任务使用编号。
3. 以一个具体的下一步收尾。
4. 抑制离题内容。
5. 每轮重述当前状态。
6. 给出具体的时间估计（以分钟计，不说“一会儿”）。
7. 让完成的工作看得见。
8. 就事论事地报告错误。
9. 每个列表最多 5 项。
10. 不写开场白、回顾或结束语。

另外一条本 fork 新增的规则：默认用简体中文输出；用户使用其他语言时跟随用户的语言，代码、命令、路径和报错原文保持原样。

## 自定义

Fork 此仓库，编辑 `skills/i-have-adhd/SKILL.md`，然后换成你的副本：

```bash
claude plugin uninstall i-have-adhd            # 先移除上游副本：
claude plugin marketplace remove i-have-adhd   # fork 与上游使用相同名称
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

改完 `skills/i-have-adhd/SKILL.md` 后，别忘了同步 Cursor 用的镜像文件：

```bash
cp skills/i-have-adhd/SKILL.md .cursor/skills/i-have-adhd/SKILL.md
```

重启你的编程助手，然后再次调用 `/i-have-adhd`。

想把默认语言改回英文，就删掉 `SKILL.md` 里的“输出语言”小节，或者在那一节里写上你想要的语言。

## 致谢

内容大致参考 J. Russell Ramsay 和 Anthony L. Rostain 所著的 *The Adult ADHD Tool Kit*。本技能针对 LLM 应如何回应进行了改编，而不是教人们如何安排日常生活。

## 许可证

[MIT](../../LICENSE)。

如果它帮你省下一次滚动、少看一句“问得好！”，请点个 Star ⭐
