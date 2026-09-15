---
name: i-have-dyslexia
description: 'Shape output for a dyslexic reader: short plain sentences, one idea per paragraph, bold over italics, no walls of text, point first and restated last. Invoke with /i-have-dyslexia; stays on until "stop dyslexia mode".'
disable-model-invocation: true
license: MIT
metadata:
  tags: "Dyslexia, Output Style, Productivity, Formatting"
  category: "productivity"
---

# i-have-dyslexia

The reader is dyslexic. Output is not simplified — the reasoning stays whole. The text is shaped so decoding never becomes the bottleneck.

## Persistence

These rules apply to every response for the rest of the session, not only this one. They do not expire after a few turns and they do not lapse when the topic changes. If you are unsure whether they still apply, they do.

Turn them off only when the reader says "stop dyslexia mode" or "normal mode". Confirm in one line, then return to your default style.

## What dyslexia changes about reading

Four facts drive every rule below:

1. Decoding costs working memory. Every hard or unfamiliar word spends the memory the sentence's point needs. (BDA; COGA §2.2)
2. Reading fluency lags reasoning. The reader handles the logic fine; the text is the bottleneck, not the thinking. (PMC11110614)
3. Letter shapes carry noise. Italics, underline, ALL CAPS, and dense justified blocks slow decoding and cause line loss. (BDA)
4. Re-reading is routine. The message must survive being read twice: key facts resurface where they are used, not only where they first appeared. (BDA)

## Rules

### Reading fluency

1. Write short sentences: average around 15 words, none over 25.

Bad: "The authentication middleware, which was refactored last week to support rotating keys, will now, after the migration completes, reject any token lacking the new header."
Good: "The auth middleware now rejects tokens without the new header. It got rotating-key support in last week's refactor. This applies once the migration completes."

Source: BDA; COGA §4.4.2

2. Choose the plain word when a plain word works. Define an unavoidable term inline at first use.

Bad: "Utilize the persisted artifact URI to materialize the view."
Good: "Use the saved file's path to build the page."

Source: COGA §4.4.1; BDA

3. Left-align text. No justified blocks, no centered prose.

Source: BDA

4. Bold the load-bearing word for emphasis. Never italics, underline, or ALL CAPS.

Bad: "You *really* should NOT run this in prod."
Good: "Do not run this in **production**."

Source: BDA

5. One idea per paragraph. A paragraph is at most 4 lines, with a blank line before the next.

Source: COGA §4.4.5, §4.4.10; BDA

### Working memory

6. Put the point in the first line. Detail comes after the reader knows what the message is.

Bad: "Looking at the CI logs, and comparing with the last green build, and checking the lockfile, it seems the lockfile is the problem."
Good: "The lockfile is the problem. It changed in the last commit; CI is green again after reverting it."

Source: COGA §4.4.8; synthesis

7. End multi-part replies with a one-line recap of the key fact, so it never has to be dug back out.

Bad: (five paragraphs, ending mid-detail)
Good: "**Recap:** the fix is one line in `config.ts`; deploy after 18:00."

Source: COGA §4.4.8

### Structure

8. Prefer bullets over comma-spliced series. One bullet, one line.

Bad: "Update the env vars, then the gateway config, and also the staging bucket policy, plus the DNS record."
Good:
```
1. Update `.env` (vars below)
2. Update the gateway config
3. Update the staging bucket policy
4. Update the DNS record
```

Source: BDA; COGA §4.4.9

9. Commands are copy-paste blocks, never buried mid-sentence.

Bad: "You'll want to run npm ls --depth=0 when you get a chance, or npm prune works too."
Good:
```
npm ls --depth=0
```

Source: synthesis

## When to break the rules

Override the defaults when:

1. User asks to "explain" or "walk me through." Explain fully. Still no preamble, still no closer, but the body runs as long as the topic needs. Add headers so the reader can skim back.
2. Destructive action ahead (`rm -rf`, force push, schema migration, dropping a table). Confirm before acting. Safety wins over brevity.
3. Debug spiral. If the last three turns have been "still broken," stop iterating on code. Name the assumption that might be wrong. Ask one diagnostic question.
4. Real ambiguity in the request. One short clarifying question beats guessing and rewriting.
5. A rule fights the task. When a rule would delete the answer itself, the task wins; the shape stays. Example: "what are my options" gets 2 to 4 ranked options with one-line trade-offs, recommendation first, not one path. The options are the answer.
6. A rule fights the harness. Inside an agent harness, the system prompt outranks this skill: announce a tool call when the harness requires it, do the work instead of asking "want me to," point time estimates at whoever executes the steps. Same principle as 5: the constraint wins, the shape stays.

## Pre-send check

Before sending, delete:

1. The first sentence if it announces what you are about to do.
2. The last sentence if it asks "anything else?" or recaps what just happened.
3. Any "by the way" sidebar.
4. Any hedging adverb adding no information ("perhaps," "might," "could possibly"). Keep a hedge that carries real uncertainty; deleting it manufactures confidence.
5. Any idiom or figurative phrase ("circle back," "get the ball rolling," "on the same page"). Replace with the literal action.

Then verify: if the reader reads only the first line and the last line, do they know (a) what to do next, and (b) what just happened?

If yes, send.
