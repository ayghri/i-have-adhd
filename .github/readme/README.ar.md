<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">إجابات موجزة ومناسبة للمصابين باضطراب فرط الحركة وتشتت الانتباه. لا حاجة إلى تشخيص؛ يمكن للجميع استخدامها!</strong>
</p>
<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/ayghri/i-have-adhd?style=flat" alt="الترخيص"></a>
</p>

<p align="center">
  <a href="../../README.md" title="English" aria-label="English">🇬🇧</a> ·
  <a href="README.zh-CN.md" title="简体中文" aria-label="简体中文">🇨🇳</a> ·
  <a href="README.pt-BR.md" title="Português (Brasil)" aria-label="Português (Brasil)">🇧🇷</a> ·
  <a href="README.ja.md" title="日本語" aria-label="日本語">🇯🇵</a> ·
  <a href="README.vi.md" title="Tiếng Việt" aria-label="Tiếng Việt">🇻🇳</a> ·
  <a href="README.ko.md" title="한국어" aria-label="한국어">🇰🇷</a> ·
  <a href="README.th.md" title="ภาษาไทย" aria-label="ภาษาไทย">🇹🇭</a> ·
  <strong title="العربية" aria-label="العربية">🇸🇦</strong>
</p>

## التثبيت

انسخ النص التالي والصقه في موجّه سطر الأوامر:

```text
Install the i-have-adhd skill/plugin from https://github.com/ayghri/i-have-adhd, refer to the repo's AGENTS.md for instructions.
```

أو 🔗 [راجع تعليمات التثبيت](../install/INSTALL.ar.md).

## ماذا تفعل هذه المهارة؟

تمنع هذه المهارة مساعد البرمجة من إخفاء الإجابة وسط نص طويل: الإجراء أولاً، والخطوات مرقمة، ومن دون عبارات ختامية مثل «آمل أن يساعدك هذا!».

## ما الذي يتغير؟

<table>
<tr>
<td width="50%">

## قبل

> سؤال رائع! دعني أفكر في الأمر. يتكوّن مسار المصادقة لديك من عدة أجزاء مترابطة: البرمجية الوسيطة، والتحقق من الرمز، ومعالجة ملفات تعريف الارتباط. بالنظر إلى `src/auth.ts`، يبدو أن الدالة `verifyToken` (الأسطر 42–58 تقريبًا) تستخدم إصدارًا قديمًا من واجهة `jsonwebtoken`. يمكن تحديث الحزمة وإعادة كتابة الدالة، ثم تشغيل اختبارات المصادقة للتأكد من أن كل شيء يعمل. وبالمناسبة، قد يكون من المفيد أيضًا مراجعة إصدارات بقية الاعتماديات. آمل أن يساعدك هذا! أخبرني إن كنت تريد التعمق أكثر.

</td>

<td width="50%">

## بعد

> شغّل `npm install jsonwebtoken@latest`، ثم عدّل `src/auth.ts:42`.
>
> 1. افتح `src/auth.ts`
> 2. استبدل `verifyToken` (الأسطر 42–58) بالمقتطف أدناه
> 3. شغّل `npm test -- auth.spec.ts`
>
> الخطوة التالية: إذا فشل أي اختبار، الصق أول سطر من رسالة الخطأ.

</td>
</tr>
</table>

## القواعد العشر

تتكوّن المهارة من عشر قواعد. تجد النص الكامل في [SKILL.md](../../skills/i-have-adhd/SKILL.md).

1. ابدأ بالإجراء التالي.
2. رقّم المهام متعددة الخطوات.
3. اختم بخطوة عملية واحدة تالية.
4. تجنّب الخروج عن الموضوع.
5. أعد توضيح الحالة في كل رد.
6. قدّم تقديرات زمنية محددة بالدقائق، لا عبارات مبهمة مثل «قليلاً».
7. وضّح ما أصبح يعمل بعد التغيير.
8. اذكر الأخطاء بموضوعية.
9. اجعل القوائم في حدود خمسة عناصر.
10. لا مقدمات، ولا إعادة تلخيص، ولا عبارات ختامية.

## التخصيص

أنشئ نسخة متفرعة من المستودع، وعدّل `skills/i-have-adhd/SKILL.md`، ثم استخدم نسختك بدلاً من النسخة الأصلية:

```bash
claude plugin uninstall i-have-adhd            # إزالة النسخة الأصلية أولاً
claude plugin marketplace remove i-have-adhd   # النسخة المتفرعة والأصلية تحملان الاسم نفسه
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

أعد تشغيل Claude Code، ثم استدعِ `/i-have-adhd` مجددًا.

## شكر وتقدير

مستوحاة بصورة عامة من كتاب *The Adult ADHD Tool Kit* للمؤلفين J. Russell Ramsay وAnthony L. Rostain. وقد كُيّفت لتناسب طريقة استجابة نماذج اللغة الكبيرة، لا طريقة تنظيم الإنسان ليومه.

## الترخيص

MIT.

ضع نجمة ⭐ إذا وفّرت عليك تمرير الشاشة بعد عبارة «سؤال رائع!» ولو مرة واحدة.
