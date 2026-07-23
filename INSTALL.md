# Install i-have-adhd for Antigravity

Ten skill został stworzony z myślą o systemie Antigravity i pozwala sformatować odpowiedzi asystenta w sposób dostosowany dla osób z ADHD.

## Instalacja

### Metoda 1: Instalator skryptowy (Rekomendowana)

Sklonuj to repozytorium na swój dysk i uruchom dołączony skrypt instalacyjny:

```bash
git clone https://github.com/merx666/i-have-adhd-antigravity.git
cd i-have-adhd-antigravity
./install.sh
```
Skrypt automatycznie przekopiuje pliki do katalogu `~/.gemini/config/skills/i-have-adhd-antigravity`.

### Metoda 2: Menedżer wtyczek Antigravity

Możesz zainstalować ten skill używając wbudowanego menedżera pluginów Antigravity:

```bash
agy plugin install https://github.com/merx666/i-have-adhd-antigravity
```

### Metoda 3: Instalacja Ręczna

Jeśli wolisz zrobić to ręcznie, skopiuj odpowiedni folder do konfiguracji Gemini:

```bash
git clone https://github.com/merx666/i-have-adhd-antigravity.git
mkdir -p ~/.gemini/config/skills
cp -R i-have-adhd-antigravity/skills/i-have-adhd ~/.gemini/config/skills/i-have-adhd-antigravity
```

---

## Jak aktywować

W nowej sesji w Antigravity wpisz `/i-have-adhd` aby aktywować tryb dla danej konwersacji. 
Aby wyłączyć, wpisz "stop adhd mode".

### Zawsze włączony (Opcjonalnie)

Dodaj poniższy fragment do pliku `~/.gemini/GEMINI.md`, aby reguły działały domyślnie od pierwszej wiadomości:

```markdown
## Output style

The reader has ADHD. Shape every response so it can be acted on:

1. Lead with the answer or next action: command, path, or snippet first.
2. Number multi-step work; one bounded action per step.
3. End with one next action doable in under two minutes.
4. Finish the current issue before raising a new one.
5. Restate progress each turn ("step 3 of 5 done").
6. Give time estimates in concrete units, never "a bit".
7. After a change, show what now works.
8. Errors: state location, cause, and fix. No drama.
9. Cap lists at 5 items.
10. No preamble, no recaps, no closers.

Exceptions: explain fully when asked to explain. Confirm before destructive actions. After three failed fixes, stop and name the doubtful assumption. If the request is ambiguous, ask one short question.
```

---

<details>
<summary><strong>Inne systemy (Claude Code, Codex, Zed, Hermes, Pi, itp.)</strong></summary>

Repozytorium to może być także zainstalowane we frameworkach opartych o standard Agent Skills. Użyj ogólnych narzędzi do instalacji skilli (np. `npx skills add merx666/i-have-adhd-antigravity`). W przypadku Claude Code:
```bash
claude plugin marketplace add merx666/i-have-adhd-antigravity
claude plugin install i-have-adhd@i-have-adhd-antigravity
```
</details>
