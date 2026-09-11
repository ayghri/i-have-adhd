# كيفية التثبيت

<details>
<summary><strong>Antigravity (<code>agy</code>)</strong></summary>

### تثبيت

```bash
agy plugin install https://github.com/ayghri/i-have-adhd
```

### تحقق

```bash
agy plugin list
```

### تحديث

```bash
agy plugin uninstall i-have-adhd
agy plugin install https://github.com/ayghri/i-have-adhd
```

### إلغاء التثبيت

```bash
agy plugin uninstall i-have-adhd
```

أو أبقِه مثبتًا وأوقف تشغيله: `agy plugin disable i-have-adhd`.

### تشغيل دائمًا (اختياري)

أضف إلى `~/.gemini/GEMINI.md`:

```markdown
## أسلوب الإجابة

القارئ مصاب باضطراب فرط الحركة وتشتت الانتباه. صُغ كل إجابة بحيث يمكن تنفيذها مباشرة:

1. ابدأ بالإجابة أو الإجراء التالي: الأمر أو المسار أو المقتطف أولاً.
2. رقّم العمل متعدد الخطوات، واجعل كل خطوة إجراءً واحدًا محددًا.
3. اختم بإجراء تالٍ واحد يمكن تنفيذه في أقل من دقيقتين.
4. أنهِ المشكلة الحالية قبل طرح مشكلة جديدة.
5. أعد توضيح التقدم في كل رد ("اكتملت الخطوة 3 من 5").
6. قدّم تقديرات زمنية بوحدات محددة، ولا تقل "قليلاً".
7. وضّح ما أصبح يعمل بعد إجراء أي تغيير.
8. عند حدوث خطأ، اذكر مكانه وسببه وطريقة إصلاحه بلا تهويل.
9. اجعل القوائم في حدود خمسة عناصر.
10. لا مقدمات، ولا إعادة تلخيص، ولا عبارات ختامية.

الاستثناءات: اشرح بالتفصيل عندما يُطلب منك ذلك. اطلب التأكيد قبل الإجراءات المدمرة. بعد ثلاث محاولات إصلاح فاشلة، توقّف وحدد الافتراض المشكوك فيه. إذا كان الطلب ملتبسًا، فاطرح سؤالاً قصيرًا واحدًا.
```

</details>

<details>
<summary><strong>AstronClaw (custom skill)</strong></summary>

يدعم AstronClaw استيراد ملف Markdown كمهارة مخصصة. تستخدم هذه الطريقة
ملف `SKILL.md` الحالي؛ راجع [دليل المهارات الرسمي ](https://github.com/iflytek/astronclaw-tutorial/blob/main/docs/guide/astronclaw/skills.md)
للتحكم في التحميل والإدارة.

يتبع هذا الإجراء وثائق AstronClaw، لكنه لم يُختبر مع
هذه المهارة. تحقق من التعليمات المصدرة قبل تمكينها.

### تثبيت

1. قم بتنزيل [SKILL.md](https://raw.githubusercontent.com/ayghri/i-have-adhd/main/skills/i-have-adhd/SKILL.md) الأساسي واحفظه باسم `SKILL.md`. قم بمراجعة محتوياته قبل التحميل.
2. في AstronClaw، افتح **我的技能 (مهاراتي)**، واختر **新建 (جديد)**، وقم بتحميل ملف `.md`.
3. تأكد من تسمية المهارة المستوردة `i-have-adhd`. استخدم **启用/禁用 (تمكين/تعطيل)** للتحكم في مدى توفره.

لا يلزم سوى ملف المهارة بصيغة Markdown. يؤدي التحميل إلى إرسال هذا الملف إلى AstronClaw؛
لا تعد بيانات البرنامج الإضافي للمستودع وخطافاته جزءًا من هذا الإعداد.

### التحقق والتنشيط

تأكد من ظهور `i-have-adhd` في **مهاراتي**. استخدم **下载 (تنزيل)** للمراجعة
التعليمات المستوردة مقابل المهارة الأصلية، ثم قم بتمكينها وحاول:

```text
Use the i-have-adhd skill for this conversation. Explain how to create an empty Git repository in a new folder.
```

تأكد من أن الرد يبدأ بإجراء ويرقّم الخطوات. هذا هو
فحص يدوي للمهارة المستوردة؛ لا يتم التحقق من التحميل الناجح وحده
أن قواعد الاستجابة الخاصة به يتم تطبيقها.

### مذكرة التنشيط

يدعم AstronClaw كلاً من الطلبات الصريحة واستدعاء المهارات تلقائيًا.
لا يحدد دليله ما إذا كان يحترم `disable-model-invocation: true` أم لا،
لذا استخدم **تعطيل** عندما لا تريد أن تكون المهارة متاحة. ليست هناك حاجة
للاعتماد على أمر يبدأ بشرطة مائلة `/i-have-adhd`.

تطلب المهارة من المساعد الحفاظ على أسلوب المحادثة حتى
أنت تقول `stop adhd mode` أو `normal mode`. لا تغيّر هذه التعليمات حالة التفعيل في المنصة؛ عطّل المهارة وابدأ
محادثة جديدة لبدء جلسة من دونها.

### تحديث

قم بتنزيل أحدث إصدار من ملف `SKILL.md` الأساسي. إذا قمت بتخصيص النسخة المستوردة،
استخدم **下载 (تنزيل)** للاحتفاظ بنسخة احتياطية أولاً. للحصول على بديل نظيف، احذف
إدخال `i-have-adhd` القديم، وكرر عملية الاستيراد، وقم بتشغيل مطالبة التحقق
في محادثة جديدة.

### إلغاء التثبيت

في **مهاراتي**، حدد `i-have-adhd` واختر **删除 (حذف)**، ثم ابدأ
محادثة جديدة. للاحتفاظ بالنسخة المستوردة لوقت لاحق، اختر **تعطيل** بدلاً من ذلك.

</details>

<details>
<summary><strong>Claude Code</strong></summary>

### تثبيت

```bash
claude plugin marketplace add ayghri/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

اكتب `/i-have-adhd`.

### تحقق

```bash
claude plugin list
```

### تحديث

```bash
claude plugin marketplace update i-have-adhd
```

### إلغاء التثبيت

```bash
claude plugin uninstall i-have-adhd
claude plugin marketplace remove i-have-adhd
```

أو أبقِه مثبتًا وأوقف تشغيله: `claude plugin disable i-have-adhd`.

### تشغيل دائمًا (اختياري)

يقوم الخطاف `SessionStart` بتحميل مجموعة القواعد الكاملة في بداية كل جلسة، ولا حاجة إلى `/i-have-adhd`:

```bash
touch ~/.claude/.i-have-adhd-always
```

إذا كنت تستخدم دليل تكوين Claude مخصصًا، فقم بإنشاء العلامة هناك بدلاً من ذلك:

```bash
touch "$CLAUDE_CONFIG_DIR/.i-have-adhd-always"
```

للعودة إلى التفعيل عند الطلب:

```bash
rm ~/.claude/.i-have-adhd-always
```

يتم تشغيل الخطاف فقط عند وجود ملف العلامة، لذا فإن تثبيت المكون الإضافي لا يغير شيئًا من تلقاء نفسه. لا يزال "إيقاف وضع adhd" يقوم بإيقاف تشغيله للجلسة الحالية.

</details>


<details>
<summary><strong>Codex</strong></summary>

### تثبيت

```bash
codex plugin marketplace add ayghri/i-have-adhd --ref main
codex plugin add i-have-adhd@i-have-adhd
```

قم باستدعاء المهارة بشكل صريح عن طريق كتابة `$i-have-adhd`. لن يفعّلها Codex تلقائيًا.

### تحقق

```bash
codex plugin list
```

### تحديث

```bash
codex plugin marketplace upgrade i-have-adhd
codex plugin remove i-have-adhd
codex plugin add i-have-adhd@i-have-adhd
```

### إلغاء التثبيت

```bash
codex plugin remove i-have-adhd
codex plugin marketplace remove i-have-adhd
```

### تشغيل دائمًا (اختياري)

أضف إلى `~/.codex/AGENTS.md`:

```markdown
## أسلوب الإجابة

القارئ مصاب باضطراب فرط الحركة وتشتت الانتباه. صُغ كل إجابة بحيث يمكن تنفيذها مباشرة:

1. ابدأ بالإجابة أو الإجراء التالي: الأمر أو المسار أو المقتطف أولاً.
2. رقّم العمل متعدد الخطوات، واجعل كل خطوة إجراءً واحدًا محددًا.
3. اختم بإجراء تالٍ واحد يمكن تنفيذه في أقل من دقيقتين.
4. أنهِ المشكلة الحالية قبل طرح مشكلة جديدة.
5. أعد توضيح التقدم في كل رد ("اكتملت الخطوة 3 من 5").
6. قدّم تقديرات زمنية بوحدات محددة، ولا تقل "قليلاً".
7. وضّح ما أصبح يعمل بعد إجراء أي تغيير.
8. عند حدوث خطأ، اذكر مكانه وسببه وطريقة إصلاحه بلا تهويل.
9. اجعل القوائم في حدود خمسة عناصر.
10. لا مقدمات، ولا إعادة تلخيص، ولا عبارات ختامية.

الاستثناءات: اشرح بالتفصيل عندما يُطلب منك ذلك. اطلب التأكيد قبل الإجراءات المدمرة. بعد ثلاث محاولات إصلاح فاشلة، توقّف وحدد الافتراض المشكوك فيه. إذا كان الطلب ملتبسًا، فاطرح سؤالاً قصيرًا واحدًا.
```

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

لا يوجد لدى Gemini CLI سوق للمكونات الإضافية، لذلك هناك طريقان أصليان: **أمر مخصص** (اختياري، ويبقى معطلاً حتى تستدعيه) أو **ملحق** (يتم تشغيله دائمًا بمجرد تثبيته). يتطابق مسار الأمر مع الوضع الافتراضي لهذه المهارة؛ اختره إلا إذا كنت تريد القواعد في كل جلسة.

### التثبيت (الأمر، الاشتراك)

```bash
mkdir -p ~/.gemini/commands
curl -fsSL https://raw.githubusercontent.com/ayghri/i-have-adhd/main/skills/i-have-adhd/agents/gemini.toml \
  -o ~/.gemini/commands/i-have-adhd.toml
```

ابدأ جلسة جديدة، اكتب `/i-have-adhd`. يبقى في تلك الجلسة.

### التثبيت (ملحق، قيد التشغيل دائمًا)

```bash
gemini extensions install https://github.com/ayghri/i-have-adhd
```

يقوم الملحق بتحميل `GEMINI.md`، الذي يستورد المهارة الكاملة، وبالتالي يتم تطبيق القواعد من الرسالة الأولى. يجب تثبيت `git`.

### تحقق

```bash
gemini extensions list          # طريقة الامتداد
ls ~/.gemini/commands           # طريقة الأمر: ملف i-have-adhd.toml موجود
```

أو اكتب `/` في الجلسة وتأكد من إدراج `i-have-adhd`.

### تحديث

```bash
gemini extensions update i-have-adhd    # طريقة الامتداد
# طريقة الأمر: أعد تشغيل أمر curl أعلاه
```

### إلغاء التثبيت

```bash
gemini extensions uninstall i-have-adhd    # طريقة الامتداد
rm ~/.gemini/commands/i-have-adhd.toml     # command route
```

</details>

<details>
<summary><strong>GitHub Copilot (VS Code and Copilot CLI)</strong></summary>

يقرأ Copilot مهارات الوكيل محليًا: نفس `SKILL.md`، بدون تحويل. فهو يقوم بمسح `.github/skills/`، و`.claude/skills/`، و`.agents/skills/` في المشروع، و`~/.copilot/skills/`، و`~/.claude/skills/`، و`~/.agents/skills/` عالميًا.

### تثبيت

```bash
npx skills add ayghri/i-have-adhd -a github-copilot        # هذا المشروع
npx skills add ayghri/i-have-adhd -a github-copilot -g     # جميع المشاريع
```

بدون واجهة سطر الأوامر (CLI)، انسخ مجلد المهارات إلى أي دليل يقوم Copilot بمسحه:

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.copilot/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.copilot/skills/
```

### تحقق

اكتب `/` في مدخلات الدردشة وأكد ظهور `i-have-adhd`. أو:

```bash
npx skills list
npx skills ls -g    # إذا ثُبّتت عالميًا
```

### تحديث

```bash
npx skills update i-have-adhd
```

أو أعد نسخ المجلد بعد `git pull`.

### إلغاء التثبيت

```bash
npx skills remove i-have-adhd
```

أو احذف المجلد `i-have-adhd` من دليل المهارات الذي نسخته إليه.

### مذكرة التنشيط

يحترم Copilot `disable-model-invocation`: لا شيء ينطبق حتى تقوم باستدعاء المهارة، مثل Claude Code (تم اختباره في [#60](https://github.com/ayghri/i-have-adhd/pull/60)).

### تشغيل دائمًا (اختياري)

أضف الكتلة أدناه إلى `.github/copilot-instructions.md` في المشروع (يقرأها برنامج Copilot في كل محادثة):

```markdown
## أسلوب الإجابة

القارئ مصاب باضطراب فرط الحركة وتشتت الانتباه. صُغ كل إجابة بحيث يمكن تنفيذها مباشرة:

1. ابدأ بالإجابة أو الإجراء التالي: الأمر أو المسار أو المقتطف أولاً.
2. رقّم العمل متعدد الخطوات، واجعل كل خطوة إجراءً واحدًا محددًا.
3. اختم بإجراء تالٍ واحد يمكن تنفيذه في أقل من دقيقتين.
4. أنهِ المشكلة الحالية قبل طرح مشكلة جديدة.
5. أعد توضيح التقدم في كل رد ("اكتملت الخطوة 3 من 5").
6. قدّم تقديرات زمنية بوحدات محددة، ولا تقل "قليلاً".
7. وضّح ما أصبح يعمل بعد إجراء أي تغيير.
8. عند حدوث خطأ، اذكر مكانه وسببه وطريقة إصلاحه بلا تهويل.
9. اجعل القوائم في حدود خمسة عناصر.
10. لا مقدمات، ولا إعادة تلخيص، ولا عبارات ختامية.

الاستثناءات: اشرح بالتفصيل عندما يُطلب منك ذلك. اطلب التأكيد قبل الإجراءات المدمرة. بعد ثلاث محاولات إصلاح فاشلة، توقّف وحدد الافتراض المشكوك فيه. إذا كان الطلب ملتبسًا، فاطرح سؤالاً قصيرًا واحدًا.
```

</details>


<details>
<summary><strong>Hermes</strong></summary>

### تثبيت

```bash
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd
```

اكتب `/i-have-adhd`. يتم تثبيت المهارة في `~/.hermes/skills/` ويتم عرضها كأمر يبدأ بشرطة مائلة في بداية الجلسة التالية.

هل تفضل التصفح أولا؟ أضف هذا المستودع كمصدر للمهارات (tap)، ثم ابحث وقم بتثبيت:

```bash
hermes skills tap add ayghri/i-have-adhd
hermes skills search adhd
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd
```

### تحقق

```bash
hermes skills list
```

### تحديث

```bash
hermes skills update i-have-adhd
```

### إلغاء التثبيت

```bash
hermes skills uninstall i-have-adhd
```

أو ولإزالة مصدر المهارات أيضًا: `hermes skills tap remove ayghri/i-have-adhd`.

### تشغيل دائمًا (اختياري)

أضف إلى `AGENTS.md` في دليل العمل الخاص بك (يقوم Hermes بتحميله لكل دليل عمل)، أو إلى شخصيتك `SOUL.md` لكل جلسة:

```markdown
## أسلوب الإجابة

القارئ مصاب باضطراب فرط الحركة وتشتت الانتباه. صُغ كل إجابة بحيث يمكن تنفيذها مباشرة:

1. ابدأ بالإجابة أو الإجراء التالي: الأمر أو المسار أو المقتطف أولاً.
2. رقّم العمل متعدد الخطوات، واجعل كل خطوة إجراءً واحدًا محددًا.
3. اختم بإجراء تالٍ واحد يمكن تنفيذه في أقل من دقيقتين.
4. أنهِ المشكلة الحالية قبل طرح مشكلة جديدة.
5. أعد توضيح التقدم في كل رد ("اكتملت الخطوة 3 من 5").
6. قدّم تقديرات زمنية بوحدات محددة، ولا تقل "قليلاً".
7. وضّح ما أصبح يعمل بعد إجراء أي تغيير.
8. عند حدوث خطأ، اذكر مكانه وسببه وطريقة إصلاحه بلا تهويل.
9. اجعل القوائم في حدود خمسة عناصر.
10. لا مقدمات، ولا إعادة تلخيص، ولا عبارات ختامية.

الاستثناءات: اشرح بالتفصيل عندما يُطلب منك ذلك. اطلب التأكيد قبل الإجراءات المدمرة. بعد ثلاث محاولات إصلاح فاشلة، توقّف وحدد الافتراض المشكوك فيه. إذا كان الطلب ملتبسًا، فاطرح سؤالاً قصيرًا واحدًا.
```

</details>

<details>
<summary><strong>Kimi Code CLI</strong></summary>

### تثبيت

ابدأ جلسة Kimi Code، ثم:

1. قم بتشغيل `/plugins`.
2. اختر **مخصص**.
3. الصق `https://github.com/ayghri/i-have-adhd` ثم اضغط على `Enter`.
4. اختر **الثقة والتثبيت**.

استخدم الأمر الذي يبدأ بشرطة مائلة `/skill:i-have-adhd` لاستدعاء المهارة بشكل صريح.

### تحديث

`/plugins` في جلسة Kimi Code، ضع المؤشر على **I Have ADHD**، ثم اضغط على `R`.

### إلغاء التثبيت

`/plugins` في جلسة Kimi Code، ضع المؤشر على **I Have ADHD**، ثم اضغط على `D`.


</details>

<details>
<summary><strong>OpenCode</strong></summary>

يقوم OpenCode بتحميل هذا المستودع كمكون إضافي للخادم: يسجل `.opencode/plugins/i-have-adhd.mjs` نقطة إدخال `skills/` والأمر `/i-have-adhd`، ويضيف مجموعة القواعد عند تمكين التشغيل الدائم. يقرأ OpenCode أيضًا `skills/` محليًا، لذلك تظل المهارة تعمل حتى بدون المكون الإضافي - يضيف المكون الإضافي أمر `/i-have-adhd` وعلامة التشغيل الدائم.

### تثبيت

استنسخ المستودع ووجّه OpenCode إلى المكوّن الإضافي. يتيح المسار المطلق استخدام نسخة محلية واحدة في جميع المشاريع:

```bash
git clone https://github.com/ayghri/i-have-adhd ~/.config/opencode/vendor/i-have-adhd
```

أضف إلى `opencode.json` (العالمي: `~/.config/opencode/opencode.json`):

```json
{ "plugin": ["/absolute/path/to/i-have-adhd/.opencode/plugins/i-have-adhd.mjs"] }
```

أو شغّل OpenCode من نسخة المستودع المحلية؛ إذ يحتوي ملف `opencode.json` في الجذر على إعداد المكوّن الإضافي مسبقًا.

ابدأ جلسة جديدة وفعّل نمط الإجابات المناسبة لاضطراب فرط الحركة وتشتت الانتباه:

```text
/i-have-adhd
```

تظل القواعد سارية حتى `stop adhd mode` أو `normal mode`.

### تحقق

ابدأ تشغيل OpenCode، واكتب `/`، وتأكد من ظهور `i-have-adhd` في قائمة الأوامر.

### تحديث

```bash
git -C ~/.config/opencode/vendor/i-have-adhd pull
```

### إلغاء التثبيت

قم بإزالة إدخال `plugin` من `opencode.json`.

### تشغيل دائمًا (اختياري)

```bash
touch ~/.config/opencode/.i-have-adhd-always
```

أثناء وجود العلامة، يضيف المكوّن الإضافي مجموعة القواعد الكاملة إلى موجّه النظام في كل رد - وهو ما يعادل OpenCode لخطاف Claude Code `SessionStart`. يقوم `stop adhd mode` أو `normal mode` بتعطيله للجلسة الحالية؛ احذف العلامة لتعطيل التشغيل الدائم:

```bash
rm ~/.config/opencode/.i-have-adhd-always
```

</details>


<details>
<summary><strong>Pi</strong></summary>

يكتشف Pi هذا المستودع كحزمة أصلية: يوفر `extensions/` الوضع المستمر للجلسة ويحتفظ `skills/` بنقطة إدخال مهارات الوكيل متاحة.

### تثبيت

```bash
pi install https://github.com/ayghri/i-have-adhd
```

ابدأ جلسة Pi جديدة. تبديل الإخراج المناسب لـ ADHD للجلسة الحالية:

```text
/i-have-adhd
```

يُظهر التذييل `● ADHD ON` أثناء تنشيط الوضع. شغّل الأمر مرة أخرى لتعطيله، أو حدّد الحالة صراحةً:

```text
/i-have-adhd on
/i-have-adhd off
stop adhd mode
```

مثل خطاف Claude Code، يضيف الامتداد مجموعة القواعد إلى المحادثة مرة واحدة بدلاً من إعادة كتابة موجه النظام عند كل طلب، ويضيفها مرة أخرى إذا أزالتها عملية ضغط السياق.

يظل أمر مهارات الوكيل الحالي متاحًا كاسم مستعار:

```text
/skill:i-have-adhd
```

ابدأ جلسة Pi جديدة مع تمكين الوضع افتراضيًا:

```bash
pi --adhd
```

### تحقق

```bash
pi list
```

تأكد من إدراج حزمة GitHub، ثم اكتب `/i-have-adhd` وتأكد من ظهور `● ADHD ON` في التذييل.

### تحديث

```bash
pi update https://github.com/ayghri/i-have-adhd
```

أو قم بتحديث كل حزمة Pi غير المثبّتة بإصدار محدد باستخدام `pi update --extensions`.

### إلغاء التثبيت

```bash
pi remove https://github.com/ayghri/i-have-adhd
```

### تشغيل دائمًا (اختياري)

قم بإنشاء علامة في دليل تكوين وكيل Pi:

```bash
touch ~/.pi/agent/.i-have-adhd-always
```

يتحقق الامتداد من العلامة في كل جلسة جديدة أو مستأنفة أو متشعبة أو مُعاد تحميلها. يفوز الاختيار المحفوظ للجلسة الحالية على هذا الإعداد الافتراضي، لذا فإن `stop adhd mode` يبقي تلك الجلسة معطلة.

للعودة إلى التفعيل عند الطلب:

```bash
rm ~/.pi/agent/.i-have-adhd-always
```

### ملف التكوين (اختياري)

قم بإنشاء `~/.pi/agent/i-have-adhd.json` في دليل تكوين وكيل Pi:

```json
{
  "alwaysOn": true,
  "hideStatus": true
}
```

- `alwaysOn`: ابدأ كل جلسة مع القواعد النشطة - مثل ملف العلامة `.i-have-adhd-always`، الذي لا يزال يعمل
- `hideStatus`: احتفظ بإدخال شريط الحالة `● ADHD ON` مخفيًا؛ لا تزال القواعد والأمر `/i-have-adhd` تعمل

اقرأ مرة واحدة عند بدء تشغيل الامتداد، لذا أعد تشغيل Pi بعد تغييره. يفوز الاختيار المحفوظ للجلسة الحالية على `alwaysOn`، لذا فإن `stop adhd mode` يبقي تلك الجلسة معطلة.

إذا تم تعيين `PI_CODING_AGENT_DIR`، فضع `.i-have-adhd-always` في هذا الدليل بدلاً من ذلك. قم بتشغيل `/reload` أو ابدأ جلسة جديدة بعد تغيير العلامة.

</details>


<details>
<summary><strong>Oh My Pi (OMP)</strong></summary>

### تثبيت

```bash
omp plugin marketplace add ayghri/i-have-adhd
omp plugin install --scope user i-have-adhd@i-have-adhd
```

ابدأ جلسة OMP جديدة وقم بتشغيل `/i-have-adhd` لتبديل الوضع.

### تحديث

```bash
omp plugin marketplace update i-have-adhd
omp plugin upgrade --scope user i-have-adhd@i-have-adhd
```

### إلغاء التثبيت

```bash
omp plugin uninstall --scope user i-have-adhd@i-have-adhd
omp plugin marketplace remove i-have-adhd
```

</details>


<details>
<summary><strong>Qwen Code</strong></summary>

### تثبيت

```bash
qwen extensions install ayghri/i-have-adhd
```

يدعم Qwen Code اختصار GitHub ويقوم بتثبيت المستودع كملف
امتداد أصلي. يكتشف الامتداد المهارة تحت `skills/`.

اكتب `/i-have-adhd` لاستدعاء المهارة بشكل صريح. تثبيت الامتداد
لا يغير الإخراج حتى يتم استدعاء المهارة.

### تحقق

```bash
qwen extensions list
```

ثم ابدأ جلسة Qwen Code جديدة وقم بتشغيل:

```text
/skills
```

تأكد من ظهور `i-have-adhd` في القائمة.

### تحديث

```bash
qwen extensions update i-have-adhd
```

### إلغاء التثبيت

```bash
qwen extensions uninstall i-have-adhd
```

</details>

<details>
<summary><strong>Zed</strong></summary>

يقرأ وكيل Zed مهارات الوكيل أصلاً باستخدام نفس تنسيق SKILL.md دون تحويل. لاحظ أنه تم استبدال "قواعد" Zed الأقدم بالمهارات جنبًا إلى جنب مع تعليمات AGENTS.md.

### تثبيت

في لوحة الوكيل، افتح مدير المهارات واختر **إنشاء مهارة من عنوان URL** (أيضًا في لوحة الأوامر باسم `agent: create skill from url`)، ثم الصق:

```
https://github.com/ayghri/i-have-adhd/blob/main/skills/i-have-adhd/SKILL.md
```

احفظها في نطاق **المستخدم** لجميع المشاريع، أو في نطاق **المشروع** لمشروع واحد. ثم اكتب `/i-have-adhd` في لوحة الوكيل.

تفضل نظام الملفات؟ استنسخ المستودع وأسقط مجلد المهارات في دليل مهارات المستخدم الخاص بك:

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.agents/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.agents/skills/
```

### تحقق

افتح مدير المهارات في لوحة الوكلاء وتأكد من إدراج `i-have-adhd`. أو اكتب `/` وأكد ظهوره.

### تحديث

أعد الاستيراد من نفس عنوان URL (الكتابة فوق)، أو أعد نسخ المجلد بعد `git pull`.

### إلغاء التثبيت

قم بإزالة `i-have-adhd` من مدير المهارات، أو قم بحذف `~/.agents/skills/i-have-adhd`.

### تشغيل دائمًا (اختياري)

أضف إلى `~/.config/zed/AGENTS.md` الشخصية الخاصة بك:

```markdown
## أسلوب الإجابة

القارئ مصاب باضطراب فرط الحركة وتشتت الانتباه. صُغ كل إجابة بحيث يمكن تنفيذها مباشرة:

1. ابدأ بالإجابة أو الإجراء التالي: الأمر أو المسار أو المقتطف أولاً.
2. رقّم العمل متعدد الخطوات، واجعل كل خطوة إجراءً واحدًا محددًا.
3. اختم بإجراء تالٍ واحد يمكن تنفيذه في أقل من دقيقتين.
4. أنهِ المشكلة الحالية قبل طرح مشكلة جديدة.
5. أعد توضيح التقدم في كل رد ("اكتملت الخطوة 3 من 5").
6. قدّم تقديرات زمنية بوحدات محددة، ولا تقل "قليلاً".
7. وضّح ما أصبح يعمل بعد إجراء أي تغيير.
8. عند حدوث خطأ، اذكر مكانه وسببه وطريقة إصلاحه بلا تهويل.
9. اجعل القوائم في حدود خمسة عناصر.
10. لا مقدمات، ولا إعادة تلخيص، ولا عبارات ختامية.

الاستثناءات: اشرح بالتفصيل عندما يُطلب منك ذلك. اطلب التأكيد قبل الإجراءات المدمرة. بعد ثلاث محاولات إصلاح فاشلة، توقّف وحدد الافتراض المشكوك فيه. إذا كان الطلب ملتبسًا، فاطرح سؤالاً قصيرًا واحدًا.
```

</details>

<details>
<summary><strong>Cursor, Amp, and any other agent-skills harness</strong></summary>

يعمل مع أي بيئة تدعم مهارات الوكيل. استبدل `<agent>` باسم وكيلك في الخيار `-a`.

### تثبيت

```bash
npx skills add ayghri/i-have-adhd                  # مساحة العمل هذه
npx skills add ayghri/i-have-adhd -g               # جميع المشاريع
npx skills add ayghri/i-have-adhd -a cursor -y     # وكيل واحد فقط
npx skills add ayghri/i-have-adhd -a opencode -y
```

في محادثة جديدة مع الوكيل، اكتب `/i-have-adhd`.

بدون واجهة سطر الأوامر (CLI)، انسخ مجلد المهارات إلى أي مسار يقوم وكيلك بمسحه ضوئيًا:

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.cursor/skills     # استخدم .agents/skills مع OpenCode أو المسار الخاص بوكيلك
cp -R i-have-adhd/skills/i-have-adhd ~/.cursor/skills/
```

### تحقق

```bash
npx skills list
npx skills ls -g    # إذا ثُبّتت عالميًا
```

### تحديث

```bash
npx skills update i-have-adhd
npx skills update -g    # إذا ثُبّتت عالميًا
```

### إلغاء التثبيت

```bash
npx skills remove i-have-adhd
npx skills remove i-have-adhd -g    # إذا ثُبّتت عالميًا
```

### تشغيل دائمًا (اختياري)

الصق هذا في ملف القواعد الثابتة لوكيلك. في Cursor: **الإعدادات → القواعد → قواعد المستخدم**، أو قاعدة مشروع ضمن `.cursor/rules/` مع `alwaysApply: true`. وفي OpenCode: `~/.config/opencode/AGENTS.md`.

```markdown
## أسلوب الإجابة

القارئ مصاب باضطراب فرط الحركة وتشتت الانتباه. صُغ كل إجابة بحيث يمكن تنفيذها مباشرة:

1. ابدأ بالإجابة أو الإجراء التالي: الأمر أو المسار أو المقتطف أولاً.
2. رقّم العمل متعدد الخطوات، واجعل كل خطوة إجراءً واحدًا محددًا.
3. اختم بإجراء تالٍ واحد يمكن تنفيذه في أقل من دقيقتين.
4. أنهِ المشكلة الحالية قبل طرح مشكلة جديدة.
5. أعد توضيح التقدم في كل رد ("اكتملت الخطوة 3 من 5").
6. قدّم تقديرات زمنية بوحدات محددة، ولا تقل "قليلاً".
7. وضّح ما أصبح يعمل بعد إجراء أي تغيير.
8. عند حدوث خطأ، اذكر مكانه وسببه وطريقة إصلاحه بلا تهويل.
9. اجعل القوائم في حدود خمسة عناصر.
10. لا مقدمات، ولا إعادة تلخيص، ولا عبارات ختامية.

الاستثناءات: اشرح بالتفصيل عندما يُطلب منك ذلك. اطلب التأكيد قبل الإجراءات المدمرة. بعد ثلاث محاولات إصلاح فاشلة، توقّف وحدد الافتراض المشكوك فيه. إذا كان الطلب ملتبسًا، فاطرح سؤالاً قصيرًا واحدًا.
```
</details>


## كيف يعمل التنشيط

1. **تم التثبيت، ولم يتم استدعاؤه.** في Claude Code، وQwen Code، وCodex، لا يحدث شيء حتى تقوم باستدعاء المهارة بشكل صريح. يحترم Claude Code وQwen Code `disable-model-invocation: true` في `SKILL.md`؛ ويحترم Codex `policy.allow_implicit_invocation: false` في `agents/openai.yaml`. قد تقوم الأدوات الأخرى بتحميل وصف كل مهارة عند بدء التشغيل وتنشيط المهارة نفسها.
2. **أنت تستدعيه بشكل صريح.** اكتب `/i-have-adhd` في Claude Code أو Qwen Code، أو `$i-have-adhd` في Codex. تبقى القواعد سارية لتلك الجلسة. يؤدي `stop adhd mode` أو `normal mode` إلى تعطيل الوضع.
3. **أنشئ `~/.claude/.i-have-adhd-always`** (في Claude Code). يقوم الخطاف `SessionStart` بتحميل مجموعة القواعد الكاملة من الرسالة الأولى، في كل جلسة.
4. **أضف مقتطف التشغيل الدائم أعلاه** (أدوات أخرى). يحافظ على القواعد الأساسية في السياق المستمر لوكيلك.

في Claude Code، وQwen Code، وCodex، لا يوجد حل وسط: إذا لم تقم بتشغيله، فسيتم إيقاف تشغيله.

## استكشاف الأخطاء وإصلاحها

**`/i-have-adhd` ليس في وضع الإكمال التلقائي.** أعد تشغيل الوكيل. تتم قراءة فهرس البرنامج المساعد عند بدء التشغيل.

**علامة التشغيل دائمًا ليس لها أي تأثير.** قم بتحديث البرنامج المساعد (`claude plugin marketplace update i-have-adhd`) وأعد التشغيل. تتم قراءة الخطافات عند بدء التشغيل، ويتطلب ملف العلامة إصدارًا من المكوّن الإضافي يتضمن `hooks/hooks.json`.

**فشل `claude plugin marketplace add`.** استخدم نموذج `owner/repo`. يجب أن يشير المسار المحلي إلى جذر الريبو، وليس إلى `.claude-plugin/`.

**تم التثبيت ولكن الردود لا تزال تبدأ بمقدمة.** افتح جلسة جديدة. إذا استمرت الإجابات في مخالفة القواعد، فشدّد الصياغة في `skills/i-have-adhd/SKILL.md`.

**تريد قواعد مختلفة.** أنشئ نسخة متفرعة، وقم بتحرير `skills/i-have-adhd/SKILL.md`، ثم استبدل النسخة الأصلية بنسختك:

```bash
claude plugin uninstall i-have-adhd            # أزل النسخة الأصلية أولاً
claude plugin marketplace remove i-have-adhd   # النسخة المتفرعة والأصلية تحملان الاسم نفسه
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

أعد التشغيل، ثم أعد استدعاء `/i-have-adhd`.

**المهارة مفقودة بعد `npx skills add`.** ابدأ محادثة وكيل جديد. تتم فهرسة المهارات عند بداية الجلسة. تأكد من وجود المجلد في المسار الذي يفحصه وكيلك (`~/.cursor/skills/` لـ Cursor، `.agents/skills/` لـ OpenCode) وأن بيانات الواجهة الأمامية `name` تتطابق مع اسم المجلد.
