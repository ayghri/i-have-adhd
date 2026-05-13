<p align="center">
  <img src="https://em-content.zobj.net/source/apple/391/brain_1f9e0.png" width="120" />
</p>

<h1 align="center">i-have-adhd</h1>

<p align="center">
  <strong>Claude Code, but it stops burying the answer. No ADHD diagnosis needed.</strong>
</p>

<p align="center">
  <em>Action first. Steps numbered. No preamble. No "hope this helps!" No 600-word essay when you asked a yes/no question.</em>
</p>

<p align="center">
  <a href="#-the-pitch">The Pitch</a> •
  <a href="#-before--after">Before/After</a> •
  <a href="#-install-30-seconds">Install</a> •
  <a href="#-the-ten-rules">The Rules</a> •
  <a href="./INSTALL.md">Full guide</a>
</p>

---

## 🧠 The Pitch

You ask Claude Code a question.

It says **"Great question! Let me think about this..."** for three paragraphs before you find the actual command. By the time you've scrolled to it, you've forgotten what you were doing. You start scrolling Twitter. It's 4pm.

**This skill fixes that.**

One slash command, `/i-have-adhd`, and Claude Code reshapes every response so you can act on it:

- 🎯 **The first line is the answer.** Command, path, snippet. No warmup.
- 🔢 **Multi-step tasks get numbered.** One action per step. Bounded.
- 🧷 **State gets restated every turn.** "Step 3 of 5 done." Working memory is small. Stop pretending it isn't.
- ✂️ **Tangents get suppressed.** Second issue? Saved for a separate question. Not dumped on you mid-fix.
- 🏆 **Wins get shown, not buried.** "Login now works. Try `npm run dev`." Not "I've made some changes…"
- 🚫 **No preamble. No recap. No closers.** "Hope this helps!" is illegal here.

Ten rules. One markdown file. Zero hooks. Zero magic. Stars appreciated. ⭐

---

## ✨ Before / After

<table>
<tr>
<td width="50%" valign="top">

### 🌫️ Normal Claude

> Great question! Let's think about this. Your auth flow has a few moving pieces. You've got the middleware, the token verification, and the cookie handling. We could approach this in a few different ways.
>
> By the way, your dependency is also a bit out of date, you might want to look at that at some point.
>
> Let me know if you want to dig deeper into any of these!

*"Where do I click."* (you, after reading this)

</td>
<td width="50%" valign="top">

### 🎯 ADHD-friendly Claude

> Run `npm install jsonwebtoken@latest`, then edit `src/auth.ts:42`.
>
> 1. Open `src/auth.ts`
> 2. Replace `verifyToken` (lines 42–58) with the snippet below
> 3. Run `npm test -- auth.spec.ts`
>
> Next: paste the first failing line if any test fails.

*"Oh. Okay."* (you, actually doing the thing)

</td>
</tr>
<tr>
<td valign="top">

### 🌫️ Normal Claude

> I've made some changes to the auth flow. Among other things, I've updated the middleware and refactored the verification logic to be more robust. There may also be some implications for the session handling, but we can revisit that.
>
> Hope this helps! Let me know if anything is unclear. 🙂

</td>
<td valign="top">

### 🎯 ADHD-friendly Claude

> Step 3 of 5 done: middleware updated.
>
> Login now works with magic links. Try: `npm run dev`, open `/login`.
>
> Next: backfill the `last_login` column. Run the script?

</td>
</tr>
</table>

```
┌─────────────────────────────────────┐
│  PREAMBLE              ████████   0 │
│  CLOSERS               ████████   0 │
│  ACTION-FIRST LINES    ████████ 100%│
│  TANGENT SUPPRESSION   ████████  ON │
│  WORKING MEMORY LOAD   ████████  LO │
│  DOPAMINE PER REPLY    ████████  HI │
└─────────────────────────────────────┘
```

---

## 🚀 Install (30 seconds)

```bash
git clone https://github.com/ayghri/i-have-adhd ~/i-have-adhd
claude plugin marketplace add ~/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Then in any Claude Code session:

```
/i-have-adhd
```

Done. Every reply from here on is action-first, numbered, restated, no fluff.

**Stop with:** `stop adhd mode` or `normal mode`.

Want it in one repo only? Or auto-on every session? → [**INSTALL.md**](./INSTALL.md).

---

## 📜 The Ten Rules

The skill enforces these. Edit [`skills/i-have-adhd/SKILL.md`](./skills/i-have-adhd/SKILL.md) to tune.

| # | Rule | Why it exists |
|---|---|---|
| 1 | **Lead with the next action.** | Knowing ≠ doing. The friction between "got it" and "done it" is where ADHD work dies. |
| 2 | **Number multi-step tasks.** | One bounded action per step. No step contains "and then" twice. |
| 3 | **End with one concrete next action.** | Under two minutes. "Open the file" counts. |
| 4 | **Suppress tangents.** | A second issue mid-fix is how you forget the first. Save it as a separate question. |
| 5 | **Restate state every turn.** | Working memory can't hold "we're on step 3 of 5" between messages. |
| 6 | **Specific time estimates.** | "A bit of work" and "a few hours" register the same. Use minutes. |
| 7 | **Make wins visible.** | Dopamine is scarce. Buried wins don't register. |
| 8 | **Matter-of-fact errors.** | No "uh oh." State cause and fix. |
| 9 | **Cap lists at 5 items.** | Five ranked beats ten unranked. |
| 10 | **No preamble. No recap. No closers.** | "Great question," "Sure!," "Hope this helps!" all banned. Start with the answer. End when the answer is done. |

Five facts justify the rules. They're spelled out at the top of [SKILL.md](./skills/i-have-adhd/SKILL.md).

---

## 🔧 How It Works

No hooks. No background processes. No statusline writes. Three files do everything:

```
i-have-adhd/
├── .claude-plugin/
│   ├── plugin.json          # tells Claude Code this is a plugin
│   └── marketplace.json     # makes it installable via `claude plugin marketplace add`
├── commands/
│   └── i-have-adhd.md       # registers the /i-have-adhd slash command
└── skills/
    └── i-have-adhd/
        └── SKILL.md         # the ten rules
```

1. You run `/i-have-adhd`.
2. Claude Code loads the skill from `skills/i-have-adhd/SKILL.md`.
3. The frontmatter tells the model **when** to apply the rules (every response).
4. The body tells the model **how**.
5. Stays active for the session. Drop with "stop adhd mode" or "normal mode".

That's the whole thing. It's just a markdown file with attitude.

---

## 🤔 FAQ

**Is this just "be terse"?**
No. Terse is a vibe. This is ten specific rules tuned to how an ADHD brain reads, starts work, and runs out of dopamine. Action-first ≠ short.

**Will it break code review or long explanations?**
No. The skill has override rules: when you ask to "explain" or "walk me through," it goes long but still cuts the preamble and the closer. Headers stay so you can skim.

**Does it work without `/i-have-adhd`?**
Yes. Add a note to `~/.claude/CLAUDE.md` and it'll apply every session. See [INSTALL.md](./INSTALL.md#always-on-optional).

**Why not just put this in CLAUDE.md and skip the plugin?**
You can. The plugin form lets you toggle it on/off per session and share it across machines. Pick whichever feels right.

**Do I actually have ADHD to use this?**
No diagnosis required. If you've ever scrolled past three paragraphs of preamble looking for the command, this is for you.

---

## 🌱 Tuning

Edit `skills/i-have-adhd/SKILL.md`. Changes apply next time `/i-have-adhd` runs. If they don't, restart Claude Code.

The frontmatter `description` is what the model reads to decide when to engage. Keep it specific. The body is the rule set. Add, remove, rewrite. It's your brain.

---

## ⭐ Star This Repo

If this saved you one scroll past one "Great question!", that's a fair trade. Costs nothing. Helps a lot.

## Credits

The rules are loosely based on strategies from *The Adult ADHD Tool Kit* by J. Russell Ramsay and Anthony L. Rostain, adapted for how an LLM should *respond*, not how a human should organize their day.

## License

MIT.
