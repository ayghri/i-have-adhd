# i-have-adhd — Kiro CLI installation guide

`kiro-skill.json` is the Kiro manifest. It tells Kiro where the skill lives
(`skills/`) and provides display metadata. Kiro does not require it to be
copied anywhere — the skill files themselves are what Kiro discovers.

## On-demand skill (install once, invoke with `/i-have-adhd`)

Copy the skill into your global Kiro skills directory so it is available in every
project:

```sh
mkdir -p ~/.kiro/skills/i-have-adhd
cp skills/i-have-adhd/SKILL.md ~/.kiro/skills/i-have-adhd/SKILL.md
```

Then invoke it in any Kiro session:

```
/i-have-adhd
```

The skill stays active for the rest of the session. Say "stop adhd mode" or
"normal mode" to turn it off.

## Always-on (inject ruleset at every agent spawn)

1. **Opt in** — create the flag file:

   ```sh
   touch ~/.kiro/.i-have-adhd-always
   ```

2. **Register the hook** — add the `agentSpawn` hook to your default agent
   config at `~/.kiro/agents/default.json` (create the file if it does not
   exist):

   ```json
   {
     "name": "default",
     "hooks": {
       "agentSpawn": [
         {
           "command": "/absolute/path/to/i-have-adhd/hooks/always-on-kiro.sh",
           "timeout_ms": 30000
         }
       ]
     }
   }
   ```

   The `"name"` field is required — Kiro rejects the config with an "invalid
   agent config" error if it is missing. `timeout_ms` is optional (default
   30 000 ms) but recommended to set explicitly.

   Replace `/absolute/path/to/i-have-adhd` with the actual clone location,
   e.g. `~/projects/i-have-adhd`.

3. **Verify** — start a new Kiro session. The first response should include
   the `ADHD MODE ACTIVE` notice.

4. **Opt out** — delete the flag file:

   ```sh
   rm ~/.kiro/.i-have-adhd-always
   ```

## Per-workspace skill (workspace-local, not global)

Place the skill inside the workspace and Kiro discovers it automatically:

```sh
mkdir -p .kiro/skills/i-have-adhd
cp /path/to/i-have-adhd/skills/i-have-adhd/SKILL.md .kiro/skills/i-have-adhd/SKILL.md
```

Invoke with `/i-have-adhd` while working in that project.
