<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">Des réponses adaptées au TDAH. Pas besoin de diagnostic TDAH !</strong>
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
  <strong title="Français" aria-label="Français">🇫🇷</strong>
</p>


## Installation

Copiez-collez dans le prompt de votre CLI :

```text
Install the i-have-adhd skill/plugin from https://github.com/ayghri/i-have-adhd, refer to the repo's AGENTS.md for instructions.
```

Ou 🔗 [consultez les instructions d'installation](../../INSTALL.md) (en anglais).

## Ce que ça fait

Une *skill* pour votre assistant de code qui l'empêche de noyer la réponse. L'action d'abord. Des étapes numérotées. Fini les « J'espère que cela vous aide ! »

[Kacper Rutkiewicz | AI Made Simple](https://youtu.be/NEl8kPWZP_Y) a publié un bon décryptage d'une version antérieure de la *skill* (en anglais).
## Ce qui change


<table>
<tr>
<td width="50%">

## Avant

> Excellente question ! Laissez-moi y réfléchir. Votre flux d'authentification comporte plusieurs rouages : le middleware, la vérification du token et la gestion des cookies. Si l'on regarde `src/auth.ts`, la fonction `verifyToken` (autour des lignes 42-58) semble utiliser une ancienne API de `jsonwebtoken`. Une approche possible serait de mettre à jour le package et de réécrire cette fonction. Une fois la modification effectuée, il faudrait lancer les tests d'authentification pour vérifier que rien ne casse. Au fait, vous pourriez aussi jeter un œil aux versions de vos dépendances de manière générale. J'espère que cela vous aide ! N'hésitez pas à me dire si vous voulez approfondir.

</td>

<td width="50%">

## Après

> Modifiez `src/auth.ts:42` pour mettre à jour la validation du token.
>
> 1. Ouvrez `src/auth.ts`
> 2. Remplacez `verifyToken` (lignes 42–58) par l'extrait ci-dessous
> 3. Lancez `npm test -- auth.spec.ts`
>
> Prochaine étape : collez la première ligne d'erreur si un test échoue.

</td>
</tr>
</table>


## Les règles

10 règles. Texte complet dans [SKILL.md](../../skills/i-have-adhd/SKILL.md) (en anglais).

1. Commencer par la prochaine action.
2. Numéroter les tâches en plusieurs étapes.
3. Terminer par une seule prochaine étape concrète.
4. Supprimer les digressions.
5. Rappeler l'avancement à chaque réponse.
6. Des estimations de temps précises (en minutes, pas « un moment »).
7. Rendre les réussites visibles.
8. Des erreurs annoncées sans drame.
9. Limiter les listes à 5 éléments.
10. Pas de préambule. Pas de récap. Pas de formule de fin.

## Personnaliser

Forkez le dépôt, modifiez `skills/i-have-adhd/SKILL.md`, puis installez votre copie à la place :

```bash
claude plugin uninstall i-have-adhd            # retirez d'abord la copie d'origine :
claude plugin marketplace remove i-have-adhd   # le fork et l'original partagent ces deux noms
claude plugin marketplace add <votre-nom-utilisateur>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Redémarrez votre assistant de code, puis relancez `/i-have-adhd`.

## Crédits

Librement inspiré de *The Adult ADHD Tool Kit* de J. Russell Ramsay et Anthony L. Rostain. Adapté à la façon dont un LLM devrait répondre, et non à la façon dont un humain devrait organiser sa journée.

## Licence

[MIT](../../LICENSE).

Laissez une étoile ⭐ si ça vous a évité, ne serait-ce qu'une fois, de scroller au-delà d'un « Excellente question ! »
