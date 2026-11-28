<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">Mga sagot na angkop sa ADHD. Hindi kailangan ng ADHD diagnosis!</strong>
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
  <strong title="Tagalog" aria-label="Tagalog">🇵🇭</strong>
</p>


## Pag-install

Kopyahin at i-paste sa prompt ng iyong CLI:

```text
Install the i-have-adhd skill/plugin from https://github.com/ayghri/i-have-adhd, refer to the repo's AGENTS.md for instructions.
```

O 🔗 [tingnan ang mga tagubilin sa pag-install](../../INSTALL.md) (sa Ingles).

## Ano ang ginagawa nito

Isang *skill* para sa iyong coding assistant na pumipigil dito na ibaon ang sagot. Aksyon muna. May bilang ang mga hakbang. Walang "Sana nakatulong ito!"

Gumawa si [Kacper Rutkiewicz | AI Made Simple](https://youtu.be/NEl8kPWZP_Y) ng magandang paliwanag tungkol sa naunang bersyon ng *skill* (sa Ingles).
## Ano ang nagbabago


<table>
<tr>
<td width="50%">

## Bago

> Magandang tanong! Pag-isipan ko muna ito. Maraming gumagalaw na bahagi ang iyong auth flow: ang middleware, ang pag-verify ng token, at ang paghawak ng cookie. Kung titingnan ang `src/auth.ts`, mukhang lumang API ng `jsonwebtoken` ang ginagamit ng function na `verifyToken` (mga linya 42-58). Isang paraan ay i-update ang package at isulat muli ang function na iyon. Pagkatapos ng pagbabago, dapat mong patakbuhin ang mga auth test para matiyak na walang nasira. Siya nga pala, baka gusto mo ring silipin ang mga bersyon ng lahat ng iyong dependency. Sana nakatulong ito! Sabihan mo lang ako kung gusto mong pag-aralan pa ito nang mas malalim.

</td>

<td width="50%">

## Pagkatapos

> I-edit ang `src/auth.ts:42` para i-update ang token validation.
>
> 1. Buksan ang `src/auth.ts`
> 2. Palitan ang `verifyToken` (mga linya 42–58) ng snippet sa ibaba
> 3. Patakbuhin ang `npm test -- auth.spec.ts`
>
> Susunod: kung may pumalyang test, i-paste ang unang linya ng error.

</td>
</tr>
</table>


## Ang mga patakaran

10 patakaran. Buong teksto sa [SKILL.md](../../skills/i-have-adhd/SKILL.md) (sa Ingles).

1. Unahin ang susunod na aksyon.
2. Lagyan ng bilang ang mga gawaing maraming hakbang.
3. Magtapos sa isang konkretong susunod na hakbang.
4. Iwasan ang paglihis sa paksa.
5. Ipaalala ang kasalukuyang estado sa bawat sagot.
6. Tiyak na tantiya ng oras (minuto, hindi "sandali").
7. Ipakita ang mga tagumpay.
8. Sabihin ang mga error nang diretso, walang drama.
9. Hanggang 5 item lang bawat listahan.
10. Walang pambungad. Walang recap. Walang pangwakas.

## I-customize

I-fork, i-edit ang `skills/i-have-adhd/SKILL.md`, saka ipalit ang sarili mong kopya:

```bash
claude plugin uninstall i-have-adhd            # alisin muna ang kopya mula sa upstream:
claude plugin marketplace remove i-have-adhd   # magkapareho ng dalawang pangalan ang fork at upstream
claude plugin marketplace add <iyong-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

I-restart ang iyong coding assistant, saka tawagin muli ang `/i-have-adhd`.

## Pagkilala

Maluwag na hango sa *The Adult ADHD Tool Kit* nina J. Russell Ramsay at Anthony L. Rostain. Inangkop para sa kung paano dapat sumagot ang isang LLM, hindi kung paano dapat ayusin ng isang tao ang kanyang araw.

## Lisensya

[MIT](../../LICENSE).

Bigyan ng star ⭐ kung nailigtas ka nito kahit minsan sa pag-scroll lampas sa isang "Magandang tanong!"
