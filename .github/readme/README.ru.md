<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">ADHD-дружелюбные ответы. Диагноз СДВГ не требуется!</strong>
</p>
<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/ayghri/i-have-adhd?style=flat" alt="License"></a>
</p>


<p align="center">
  <a href="../../README.md" title="English" aria-label="English">🇬🇧</a> · <a href="README.es.md" title="Español" aria-label="Español">🇪🇸</a> ·
  <a href="README.zh-CN.md" title="简体中文" aria-label="简体中文">🇨🇳</a> ·
  <a href="README.id.md" title="Bahasa Indonesia" aria-label="Bahasa Indonesia">🇮🇩</a> ·
  <a href="README.pt-BR.md" title="Português (Brasil)" aria-label="Português (Brasil)">🇧🇷</a> ·
  <a href="README.ja.md" title="日本語" aria-label="日本語">🇯🇵</a> ·
  <a href="README.vi.md" title="Tiếng Việt" aria-label="Tiếng Việt">🇻🇳</a> ·
  <a href="README.ko.md" title="한국어" aria-label="한국어">🇰🇷</a> ·
  <a href="README.fa.md" title="فارسی" aria-label="فارسی">🇮🇷</a> ·
  <a href="README.th.md" title="ภาษาไทย" aria-label="ภาษาไทย">🇹🇭</a> ·
  <a href="README.ar.md" title="العربية" aria-label="العربية">🇸🇦</a> ·
  <a href="README.fr.md" title="Français" aria-label="Français">🇫🇷</a> ·
  <strong title="Русский" aria-label="Русский">🇷🇺</strong>
</p>



## Установка

Скопируйте и вставьте в ваш CLI-промпт:

```text
Install the i-have-adhd skill/plugin from https://github.com/ayghri/i-have-adhd, refer to the repo's AGENTS.md for instructions.
```

Или 🔗 [ознакомьтесь с инструкциями по установке](../INSTALL.md).

## Что это делает

Навык для вашего AI-помощника, который не дает ему прятать ответ. Сначала действие. Шаги пронумерованы. Никаких «Надеюсь, это поможет!».

[Kacper Rutkiewicz | AI Made Simple](https://youtu.be/NEl8kPWZP_Y) сделал отличный разбор ранней версии этого навыка.

## Что изменится

<table>
<tr>
<td width="50%">

## До
> Отличный вопрос! Давайте подумаю. В вашем процессе авторизации есть несколько движущихся частей: промежуточное ПО, проверка токена и обработка куки. Глядя на `src/auth.ts`, функция `verifyToken` (примерно строки 42-58), похоже, использует устаревший API `jsonwebtoken`. Одним из вариантов было бы обновить пакет и переписать эту функцию. После внесения изменений вам стоит запустить тесты авторизации, чтобы убедиться, что ничего не сломалось. Кстати, вам также может быть полезно проверить версии зависимостей в целом. Надеюсь, это поможет! Дайте знать, если хотите копнуть глубже.

</td>
<td width="50%">

## После
> Отредактируйте `src/auth.ts:42`, чтобы обновить валидацию токена.
>
> 1. Откройте `src/auth.ts`
> 2. Замените `verifyToken` (строки 42–58) фрагментом кода ниже
> 3. Запустите `npm test -- auth.spec.ts`
>
> Далее: пришлите первую строку с ошибкой, если какой-либо тест не пройдет.

</td>
</tr>
</table>

## Правила

10 правил. Полный текст в [SKILL.md](../skills/i-have-adhd/SKILL.md).

1. Начинайте со следующего действия.
2. Нумеруйте многошаговые задачи.
3. Заканчивайте одним конкретным следующим шагом.
4. Подавляйте отступления от темы.
5. Обновляйте текущий статус в каждом ответе.
6. Конкретные оценки времени (в минутах, а не «немного»).
7. Делайте успехи заметными.
8. Сообщайте об ошибках сухо и по делу.
9. Ограничивайте списки до 5 пунктов.
10. Без вступлений. Без итогов. Без прощаний.

## Настройка

Форкните, отредактируйте `skills/i-have-adhd/SKILL.md`, затем замените версию:

```bash
claude plugin uninstall i-have-adhd            # сначала удалите версию из upstream:
claude plugin marketplace remove i-have-adhd   # форк и upstream используют одно имя
claude plugin marketplace add <ваш-пользователь>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Перезапустите вашего AI-помощника, затем снова вызовите `/i-have-adhd`.

## Благодарности

Вдохновлено книгой *The Adult ADHD Tool Kit* (Дж. Рассел Рэмзи и Энтони Л. Ростейн). Адаптировано под формат ответов LLM, а не под организацию дня человеком.

## Лицензия

[MIT](../LICENSE).

Ставьте ⭐, если это сэкономило вам один скролл мимо фразы «Отличный вопрос!».
