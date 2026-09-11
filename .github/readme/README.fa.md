<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">خروجی‌های سازگار با ADHD. نیازی به تشخیص پزشکی نیست!</strong>
</p>
<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/ayghri/i-have-adhd?style=flat" alt="مجوز"></a>
</p>

<p align="center">
  <strong title="فارسی" aria-label="فارسی">🇮🇷</strong> ·
  <a href="../../README.md" title="English" aria-label="English">🇬🇧</a> ·
  <a href="README.zh-CN.md" title="简体中文" aria-label="简体中文">🇨🇳</a> ·
  <a href="README.pt-BR.md" title="Português (Brasil)" aria-label="Português (Brasil)">🇧🇷</a> ·
  <a href="README.ja.md" title="日本語" aria-label="日本語">🇯🇵</a> ·
  <a href="README.vi.md" title="Tiếng Việt" aria-label="Tiếng Việt">🇻🇳</a> ·
  <a href="README.ko.md" title="한국어" aria-label="한국어">🇰🇷</a> ·
  <a href="README.th.md" title="ภาษาไทย" aria-label="ภาษาไทย">🇹🇭</a>
</p>


## نصب
به طور خلاصه، در اکثر ابزارها می‌توانید با دستور زیر شروع کنید:

```text
Install the i-have-adhd skill/plugin from https://github.com/ayghri/i-have-adhd, refer to the repo's AGENTS.md for instructions.
```

🔗 [مشاهده راهنمای نصب](../install/INSTALL.fa.md)


## این مهارت چه کار می‌کند؟

یک افزونه برای دستیار برنامه‌نویسی شما که جلوی پنهان شدن جواب لابه‌لای متن‌های طولانی را می‌گیرد. اول اقدام، بعد توضیح. مراحل شماره‌گذاری شده. بدون جملاتی مثل «امیدوارم مفید بوده باشه!»


## تفاوت قبل و بعد


<table>
<tr>
<td width="50%">

## قبل

> سؤال خیلی خوبیه! بذار فکر کنم. جریان احراز هویت تو چند تا بخش داره: میان‌افزار، بررسی توکن و مدیریت کوکی. اگه به `src/auth.ts` نگاه کنی، تابع `verifyToken` (حدود خط ۴۲ تا ۵۸) انگار از API قدیمی `jsonwebtoken` استفاده می‌کنه. یکی از راه‌ها اینه که پکیج رو آپدیت کنی و اون تابع رو دوباره بنویسی. بعد از تغییر هم باید تست‌های auth رو اجرا کنی تا مطمئن بشی چیزی خراب نشده. راستی شاید بد نباشه یه نگاهی هم به نسخه وابستگی‌هات بندازی. امیدوارم کمک کرده باشه! اگه خواستی بیشتر بررسی کنیم بگو.

</td>
<td width="50%">

## بعد

> اجرا کن `npm install jsonwebtoken@latest`، بعد `src/auth.ts:42` رو ویرایش کن.
>
> 1. فایل `src/auth.ts` رو باز کن
> 2. تابع `verifyToken` (خط ۴۲–۵۸) رو با قطعه‌کد زیر جایگزین کن
> 3. اجرا کن `npm test -- auth.spec.ts`
>
> مرحله بعد: اگه تستی فیل شد، اولین خط خطا رو بفرست.

</td>
</tr>
</table>


## قوانین

۱۰ قانون ساده. متن کامل در [SKILL.md](../../skills/i-have-adhd/SKILL.md).

1. همیشه با اقدام بعدی شروع کن.
2. کارهای چندمرحله‌ای را شماره‌گذاری کن.
3. هر پاسخ را با یک قدم مشخص تمام کن.
4. از حاشیه رفتن پرهیز کن.
5. هر دور وضعیت فعلی را دوباره بیان کن.
6. زمان تخمینی دقیق بده (دقیقه، نه «یه کم»).
7. پیشرفت‌ها را واضح نشان بده.
8. خطاها را بدون احساسات گزارش کن.
9. لیست‌ها حداکثر ۵ مورد.
10. بدون مقدمه، بدون خلاصه، بدون جمله پایانی.


## شخصی‌سازی

ریپو را فورک کنید، فایل `skills/i-have-adhd/SKILL.md` را ویرایش کنید، سپس نسخه خودتان را جایگزین کنید:

```bash
claude plugin uninstall i-have-adhd            # اول نسخه اصلی رو حذف کن:
claude plugin marketplace remove i-have-adhd   # فورک و نسخه اصلی اسم مشترک دارند
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Claude Code را ری‌استارت کنید و دوباره `/i-have-adhd` را صدا بزنید.


## اعتبارها

برگرفته از کتاب *The Adult ADHD Tool Kit* نوشته J. Russell Ramsay و Anthony L. Rostain. این مهارت برای نحوه پاسخ‌دهی مدل‌های زبانی طراحی شده، نه برای سازمان‌دهی زندگی روزمره افراد.


## مجوز

MIT.

اگه باعث شد حتی یک بار کمتر اسکرول کنی و یک «سؤال خوبیه!» رو رد کنی، ستاره ⭐ بده.
