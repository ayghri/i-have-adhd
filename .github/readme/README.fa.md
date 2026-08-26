<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">خروجی‌های ADHD پسند. برای استفاده به تشخیص پزشک نیازی ندارید!</strong>
</p>
<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/ayghri/i-have-adhd?style=flat" alt="مجوز"></a>
</p>

<p align="center">
  <a href="../../README.md" title="English" aria-label="English">🇬🇧</a> ·
  <a href="README.zh-CN.md" title="简体中文" aria-label="简体中文">🇨🇳</a> ·
  <a href="README.pt-BR.md" title="Português (Brasil)" aria-label="Português (Brasil)">🇧🇷</a> ·
  <a href="README.ja.md" title="日本語" aria-label="日本語">🇯🇵</a> ·
  <a href="README.vi.md" title="Tiếng Việt" aria-label="Tiếng Việt">🇻🇳</a> ·
  <a href="README.ko.md" title="한국어" aria-label="한국어">🇰🇷</a> ·
  <strong title="فارسی" aria-label="فارسی">🇮🇷</strong>
</p>


## نصب

🔗 [راهنمای نصب](../install/INSTALL.fa.md)

## عملکرد

مهارتی برای دستیار برنامه‌نویسی شما که مانع از مدفون کردن پاسخ در میان توضیحات اضافی می‌شود. اقدام در ابتدا. مراحل شماره‌گذاری‌شده. بدون «امیدوارم این کمک کند!»


## تغییرات


<table>
<tr>
<td width="50%">

## قبل

> سوال خوبی است! اجازه دهید در این مورد فکر کنم. جریان احراز هویت شما چند بخش متحرک دارد: میان‌افزار (middleware)، تایید توکن، و مدیریت کوکی‌ها. با نگاهی به `src/auth.ts`، به نظر می‌رسد تابع `verifyToken` (حدود خطوط 42-58) از API قدیمی‌تر `jsonwebtoken` استفاده می‌کند. یک روش این است که پکیج را به‌روزرسانی کرده و آن تابع را بازنویسی کنید. پس از اعمال تغییرات، بهتر است تست‌های احراز هویت را اجرا کنید تا مطمئن شوید چیزی خراب نشده است. ضمناً، شاید بخواهید نگاهی هم به نسخه‌های وابستگی‌های خود به‌طور کلی بیندازید. امیدوارم این کمک کند! اگر می‌خواهید عمیق‌تر بررسی کنیم اطلاع دهید.

</td>

<td width="50%">

## بعد

> دستور `npm install jsonwebtoken@latest` را اجرا کنید، سپس `src/auth.ts:42` را ویرایش کنید.
>
> 1. فایل `src/auth.ts` را باز کنید
> 2. قسمت `verifyToken` (خطوط 42–58) را با قطعه‌کد زیر جایگزین کنید
> 3. دستور `npm test -- auth.spec.ts` را اجرا کنید
>
> گام بعدی: در صورت رد شدن هر تست، اولین خط خطا را پیست کنید.

</td>
</tr>
</table>


## قوانین

10 قانون. متن کامل در [SKILL.md](../../skills/i-have-adhd/SKILL.md).

1. شروع با اقدام بعدی.
2. شماره‌گذاری کارهای چندمرحله‌ای.
3. پایان با یک گام بعدی ملموس.
4. جلوگیری از حاشیه‌پردازی.
5. بازگویی وضعیت در هر مرحله.
6. تخمین زمان دقیق (به دقیقه، نه «یک کم»).
7. نمایش ملموس موفقیت‌ها.
8. بیان واقع‌بینانه و بدون حاشیه خطاها.
9. محدود کردن فهرست‌ها به 5 مورد.
10. بدون مقدمه. بدون جمع‌بندی. بدون کلمات پایانی.

## سفارشی‌سازی

مخزن را فورک (Fork) کنید، فایل `skills/i-have-adhd/SKILL.md` را ویرایش کنید، سپس نسخه خود را جایگزین نمایید:

```bash
claude plugin uninstall i-have-adhd            # ابتدا نسخه اصلی (upstream) را حذف کنید:
claude plugin marketplace remove i-have-adhd   # فورک و نسخه اصلی نام یکسانی دارند
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

کلاد کد (Claude Code) را مجدداً راه‌اندازی کرده و سپس `/i-have-adhd` را دوباره فراخوانی کنید.

## قدردانی

با الهام از کتاب *The Adult ADHD Tool Kit* نوشته J. Russell Ramsay و Anthony L. Rostain. برای نحوه پاسخ‌دهی یک مدل زبانی (LLM) تطبیق داده شده است، نه برای نحوه سازماندهی روزمره یک انسان.

## مجوز

MIT.

اگر این افزونه باعث شد حتی یک بار از اسکرول کردن و رد شدن از جملاتی مثل «سوال خوبی است!» نجات پیدا کنید، ستاره ⭐ بدهید.
