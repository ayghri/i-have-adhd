<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">ADHS-freundliche Antworten. Keine ADHS-Diagnose nötig!</strong>
</p>
<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/ayghri/i-have-adhd?style=flat" alt="License"></a>
</p>

<p align="center">
  <a href="../../README.md" title="English" aria-label="English">🇬🇧</a> ·
  <a href="README.zh-CN.md" title="简体中文" aria-label="简体中文">🇨🇳</a> ·
  <a href="README.es.md" title="Español" aria-label="Español">🇪🇸</a> ·
  <a href="README.pt-BR.md" title="Português (Brasil)" aria-label="Português (Brasil)">🇧🇷</a> ·
  <a href="README.ja.md" title="日本語" aria-label="日本語">🇯🇵</a> ·
  <a href="README.vi.md" title="Tiếng Việt" aria-label="Tiếng Việt">🇻🇳</a> ·
  <a href="README.ko.md" title="한국어" aria-label="한국어">🇰🇷</a> ·
  <a href="README.fa.md" title="فارسی" aria-label="فارسی">🇮🇷</a> ·
  <a href="README.th.md" title="ภาษาไทย" aria-label="ภาษาไทย">🇹🇭</a> ·
  <a href="README.ar.md" title="العربية" aria-label="العربية">🇸🇦</a> ·
  <a href="README.fr.md" title="Français" aria-label="Français">🇫🇷</a> ·
  <strong title="Deutsch" aria-label="Deutsch">🇩🇪</strong>
</p>


## Installation

In den Prompt deiner CLI kopieren:

```text
Install the i-have-adhd skill/plugin from https://github.com/ayghri/i-have-adhd, refer to the repo's AGENTS.md for instructions.
```

Oder 🔗 [sieh dir die Installationsanleitung an](../../INSTALL.md) (auf Englisch).

## Was es macht

Ein Skill für deinen Coding-Assistenten, der verhindert, dass die Antwort im Text untergeht. Zuerst die Aktion. Nummerierte Schritte. Kein „Ich hoffe, das hilft!“

[Kacper Rutkiewicz | AI Made Simple](https://youtu.be/NEl8kPWZP_Y) hat eine gute Analyse einer früheren Version des Skills gemacht (auf Englisch).
## Was sich ändert


<table>
<tr>
<td width="50%">

## Vorher

> Gute Frage! Lass mich kurz darüber nachdenken. Dein Auth-Flow besteht aus mehreren beweglichen Teilen: der Middleware, der Token-Verifizierung und dem Cookie-Handling. Wenn man sich `src/auth.ts` ansieht, scheint die Funktion `verifyToken` (etwa Zeilen 42–58) eine ältere `jsonwebtoken`-API zu verwenden. Ein Ansatz wäre, das Paket zu aktualisieren und die Funktion neu zu schreiben. Nach der Änderung solltest du die Auth-Tests laufen lassen, um sicherzugehen, dass nichts kaputtgeht. Übrigens könntest du dir auch mal deine Abhängigkeitsversionen insgesamt anschauen. Ich hoffe, das hilft! Sag Bescheid, wenn du tiefer einsteigen willst.

</td>

<td width="50%">

## Nachher

> Bearbeite `src/auth.ts:42`, um die Token-Validierung zu aktualisieren.
>
> 1. Öffne `src/auth.ts`
> 2. Ersetze `verifyToken` (Zeilen 42–58) durch das Snippet unten
> 3. Führe `npm test -- auth.spec.ts` aus
>
> Als Nächstes: Füge die erste fehlschlagende Zeile ein, falls ein Test fehlschlägt.

</td>
</tr>
</table>


## Die Regeln

10 Regeln. Vollständiger Text in [SKILL.md](../../skills/i-have-adhd/SKILL.md) (auf Englisch).

1. Mit der nächsten Aktion beginnen.
2. Mehrstufige Aufgaben nummerieren.
3. Mit genau einem konkreten nächsten Schritt enden.
4. Abschweifungen unterdrücken.
5. Den aktuellen Stand in jeder Antwort wiederholen.
6. Konkrete Zeitangaben (Minuten, nicht „ein bisschen“).
7. Erfolge sichtbar machen.
8. Fehler sachlich benennen.
9. Listen auf 5 Punkte begrenzen.
10. Keine Einleitung. Keine Zusammenfassung. Keine Schlussfloskeln.

## Anpassen

Forken, `skills/i-have-adhd/SKILL.md` bearbeiten und dann deine Kopie einsetzen:

```bash
claude plugin uninstall i-have-adhd            # zuerst die Upstream-Kopie entfernen:
claude plugin marketplace remove i-have-adhd   # Fork und Upstream haben beide Namen gemeinsam
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Starte deinen Coding-Assistenten neu und rufe dann `/i-have-adhd` erneut auf.

## Credits

Lose angelehnt an *The Adult ADHD Tool Kit* von J. Russell Ramsay und Anthony L. Rostain. Angepasst darauf, wie ein LLM antworten sollte, nicht darauf, wie ein Mensch seinen Tag organisieren sollte.

## Lizenz

[MIT](../../LICENSE).

Gib einen Stern ⭐, wenn es dir auch nur ein einziges Scrollen an einem „Gute Frage!“ vorbei erspart hat.
