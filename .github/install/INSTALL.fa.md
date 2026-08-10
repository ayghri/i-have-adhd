# راهنمای نصب

<details>
<summary><strong>Antigravity (<code>agy</code>)</strong></summary>

### نصب

```bash
agy plugin install https://github.com/ayghri/i-have-adhd
```

### تایید نصب

```bash
agy plugin list
```

### به‌روزرسانی

```bash
agy plugin uninstall i-have-adhd
agy plugin install https://github.com/ayghri/i-have-adhd
```

### حذف

```bash
agy plugin uninstall i-have-adhd
```

یا آن را نصب نگه داشته و غیرفعال کنید: `agy plugin disable i-have-adhd`.

### همیشه فعال (اختیاری)

قسمت زیر را به فایل `~/.gemini/GEMINI.md` اضافه کنید:

```markdown
## سبک خروجی

خواننده دارای ADHD است. هر پاسخ را طوری تنظیم کنید که قابل اجرا باشد:

1. با پاسخ یا اقدام بعدی شروع کنید: ابتدا دستور، مسیر یا قطعه‌کد.
2. کارهای چندمرحله‌ای را شماره‌گذاری کنید؛ در هر مرحله یک اقدام مشخص و محدود.
3. با یک اقدام بعدی که در کمتر از دو دقیقه قابل انجام است پایان دهید.
4. موضوع فعلی را پیش از مطرح کردن موضوع جدید تمام کنید.
5. پیشرفت را در هر مرحله بازگو کنید ("مرحله ۳ از ۵ انجام شد").
6. تخمین زمان را با واحدهای ملموس بیان کنید، هرگز از "یک کم" استفاده نکنید.
7. پس از اعمال تغییر، نشان دهید چه چیزی الان کار می‌کند.
8. خطاها: محل، علت و راه حل را بیان کنید. بدون حاشیه و اغراق.
9. فهرست‌ها را به حداکثر ۵ مورد محدود کنید.
10. بدون مقدمه، بدون خلاصه، بدون کلمات پایانی.

استثناها: وقتی درخواست توضیح شد، به‌طور کامل توضیح دهید. قبل از اقدامات مخرب تایید بگیرید. پس از سه اصلاح ناموفق، متوقف شوید و فرض مشکوک را نام ببرید. اگر درخواست مبهم است، یک سوال کوتاه بپرسید.
```

</details>

<details>
<summary><strong>Claude Code</strong></summary>

### نصب

```bash
claude plugin marketplace add ayghri/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

عبارت `/i-have-adhd` را تایپ کنید.

### تایید نصب

```bash
claude plugin list
```

### به‌روزرسانی

```bash
claude plugin marketplace update i-have-adhd
```

### حذف

```bash
claude plugin uninstall i-have-adhd
claude plugin marketplace remove i-have-adhd
```

یا آن را نصب نگه داشته و غیرفعال کنید: `claude plugin disable i-have-adhd`.

### همیشه فعال (اختیاری)

یک هوک (hook) `SessionStart` مجموعه کامل قوانین را در شروع هر نشست بارگذاری می‌کند و نیازی به `/i-have-adhd` نیست:

```bash
touch ~/.claude/.i-have-adhd-always
```

بازگشت به حالت فقط در صورت درخواست (on-demand):

```bash
rm ~/.claude/.i-have-adhd-always
```

این هوک تنها در صورتی اجرا می‌شود که فایل پرچم (flag) وجود داشته باشد، بنابراین نصب پلاگین به تنهایی چیزی را تغییر نمی‌دهد. اگر مسیر تنظیمات خود را تغییر داده باشید، از `$CLAUDE_CONFIG_DIR` پشتیبانی می‌کند. عبارت "stop adhd mode" همچنان آن را برای نشست فعلی غیرفعال می‌کند.

</details>


<details>
<summary><strong>Codex</strong></summary>

### نصب

```bash
codex plugin marketplace add ayghri/i-have-adhd --ref main
codex plugin add i-have-adhd@i-have-adhd
```

با تایپ `$i-have-adhd` مهارت را صراحتاً فراخوانی کنید. Codex آن را به طور خودکار فعال نمی‌کند.

### تایید نصب

```bash
codex plugin list
```

### به‌روزرسانی

```bash
codex plugin marketplace upgrade i-have-adhd
codex plugin remove i-have-adhd
codex plugin add i-have-adhd@i-have-adhd
```

### حذف

```bash
codex plugin remove i-have-adhd
codex plugin marketplace remove i-have-adhd
```

### همیشه فعال (اختیاری)

به فایل `~/.codex/AGENTS.md` اضافه کنید:

```markdown
## سبک خروجی

خواننده دارای ADHD است. هر پاسخ را طوری تنظیم کنید که قابل اجرا باشد:

1. با پاسخ یا اقدام بعدی شروع کنید: ابتدا دستور، مسیر یا قطعه‌کد.
2. کارهای چندمرحله‌ای را شماره‌گذاری کنید؛ در هر مرحله یک اقدام مشخص و محدود.
3. با یک اقدام بعدی که در کمتر از دو دقیقه قابل انجام است پایان دهید.
4. موضوع فعلی را پیش از مطرح کردن موضوع جدید تمام کنید.
5. پیشرفت را در هر مرحله بازگو کنید ("مرحله ۳ از ۵ انجام شد").
6. تخمین زمان را با واحدهای ملموس بیان کنید، هرگز از "یک کم" استفاده نکنید.
7. پس از اعمال تغییر، نشان دهید چه چیزی الان کار می‌کند.
8. خطاها: محل، علت و راه حل را بیان کنید. بدون حاشیه و اغراق.
9. فهرست‌ها را به حداکثر ۵ مورد محدود کنید.
10. بدون مقدمه، بدون خلاصه، بدون کلمات پایانی.

استثناها: وقتی درخواست توضیح شد، به‌طور کامل توضیح دهید. قبل از اقدامات مخرب تایید بگیرید. پس از سه اصلاح ناموفق، متوقف شوید و فرض مشکوک را نام ببرید. اگر درخواست مبهم است، یک سوال کوتاه بپرسید.
```

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

ابزار Gemini CLI مارکت پلاگین ندارد، بنابراین دو روش بومی وجود دارد: یک **دستور سفارشی** (با انتخاب کاربر، تا زمان فراخوانی غیرفعال است) یا یک **افزونه** (پس از نصب، همیشه فعال است). روش دستور با حالت پیش‌فرض این skill مطابقت دارد؛ مگر اینکه بخواهید قوانین در هر نشست اعمال شوند، این روش را انتخاب کنید.

### نصب (دستور، با انتخاب کاربر)

```bash
mkdir -p ~/.gemini/commands
curl -fsSL https://raw.githubusercontent.com/ayghri/i-have-adhd/main/skills/i-have-adhd/agents/gemini.toml \
  -o ~/.gemini/commands/i-have-adhd.toml
```

یک نشست جدید شروع کرده و `/i-have-adhd` را تایپ کنید. برای آن نشست فعال می‌ماند.

### نصب (افزونه، همیشه فعال)

```bash
gemini extensions install https://github.com/ayghri/i-have-adhd
```

افزونه فایل `GEMINI.md` را بارگذاری می‌کند که مهارت کامل را وارد می‌نماید، بنابراین قوانین از اولین پیام اعمال می‌شوند. ابزار `git` باید نصب باشد.

### تایید نصب

```bash
gemini extensions list          # روش افزونه
ls ~/.gemini/commands           # روش دستور: وجود i-have-adhd.toml
```

یا در یک نشست `/` را تایپ کرده و تایید کنید که `i-have-adhd` در لیست قرار دارد.

### به‌روزرسانی

```bash
gemini extensions update i-have-adhd    # روش افزونه
# روش دستور: اجرای مجدد دستور curl بالا
```

### حذف

```bash
gemini extensions uninstall i-have-adhd    # روش افزونه
rm ~/.gemini/commands/i-have-adhd.toml     # روش دستور
```

</details>

<details>
<summary><strong>GitHub Copilot (VS Code and Copilot CLI)</strong></summary>

ابزار Copilot مهارت‌های دستیار (Agent Skills) را به صورت بومی می‌خواند: همان فایل `SKILL.md` بدون نیاز به تبدیل. این ابزار مسیرهای `.github/skills/`، `.claude/skills/` و `.agents/skills/` را در پروژه، و مسیرهای `~/.copilot/skills/`، `~/.claude/skills/` و `~/.agents/skills/` را به صورت سراسری اسکن می‌کند.

### نصب

```bash
npx skills add ayghri/i-have-adhd -a github-copilot        # این پروژه
npx skills add ayghri/i-have-adhd -a github-copilot -g     # همه پروژه‌ها
```

بدون CLI، پوشه مهارت را در هر دایرکتوری که Copilot اسکن می‌کند کپی کنید:

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.copilot/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.copilot/skills/
```

### تایید نصب

در ورودی چت `/` را تایپ کنید و تایید نمایید که `i-have-adhd` ظاهر می‌شود. یا:

```bash
npx skills list
npx skills ls -g    # در صورت نصب سراسری
```

### به‌روزرسانی

```bash
npx skills update i-have-adhd
```

یا بعد از `git pull` پوشه را دوباره کپی کنید.

### حذف

```bash
npx skills remove i-have-adhd
```

یا پوشه `i-have-adhd` را از دایرکتوری مهارت‌هایی که در آن قرار گرفته حذف کنید.

### نکته فعال‌سازی

ابزار Copilot از `disable-model-invocation` پشتیبانی می‌کند: تا زمانی که مهارت را فراخوانی نکنید هیچ تغییری اعمال نمی‌شود، همانند Claude Code (تست‌شده در [#60](https://github.com/ayghri/i-have-adhd/pull/60)).

### همیشه فعال (اختیاری)

قطعه‌کد زیر را به فایل `.github/copilot-instructions.md` در پروژه اضافه کنید (Copilot آن را در هر چت می‌خواند):

```markdown
## سبک خروجی

خواننده دارای ADHD است. هر پاسخ را طوری تنظیم کنید که قابل اجرا باشد:

1. با پاسخ یا اقدام بعدی شروع کنید: ابتدا دستور، مسیر یا قطعه‌کد.
2. کارهای چندمرحله‌ای را شماره‌گذاری کنید؛ در هر مرحله یک اقدام مشخص و محدود.
3. با یک اقدام بعدی که در کمتر از دو دقیقه قابل انجام است پایان دهید.
4. موضوع فعلی را پیش از مطرح کردن موضوع جدید تمام کنید.
5. پیشرفت را در هر مرحله بازگو کنید ("مرحله ۳ از ۵ انجام شد").
6. تخمین زمان را با واحدهای ملموس بیان کنید، هرگز از "یک کم" استفاده نکنید.
7. پس از اعمال تغییر، نشان دهید چه چیزی الان کار می‌کند.
8. خطاها: محل، علت و راه حل را بیان کنید. بدون حاشیه و اغراق.
9. فهرست‌ها را به حداکثر ۵ مورد محدود کنید.
10. بدون مقدمه، بدون خلاصه، بدون کلمات پایانی.

استثناها: وقتی درخواست توضیح شد، به‌طور کامل توضیح دهید. قبل از اقدامات مخرب تایید بگیرید. پس از سه اصلاح ناموفق، متوقف شوید و فرض مشکوک را نام ببرید. اگر درخواست مبهم است، یک سوال کوتاه بپرسید.
```

</details>


<details>
<summary><strong>Hermes</strong></summary>

### نصب

```bash
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd
```

عبارت `/i-have-adhd` را تایپ کنید. مهارت در `~/.hermes/skills/` نصب شده و در شروع نشست بعدی به عنوان یک دستور اسلش (slash command) در دسترس خواهد بود.

ترجیح می‌دهید ابتدا مرور کنید؟ این مخزن را به عنوان منبع مهارت (یک "tap") اضافه کرده، سپس جستجو و نصب کنید:

```bash
hermes skills tap add ayghri/i-have-adhd
hermes skills search adhd
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd
```

### تایید نصب

```bash
hermes skills list
```

### به‌روزرسانی

```bash
hermes skills update i-have-adhd
```

### حذف

```bash
hermes skills uninstall i-have-adhd
```

یا tap را نیز حذف کنید: `hermes skills tap remove ayghri/i-have-adhd`.

### همیشه فعال (اختیاری)

به فایل `AGENTS.md` در دایرکتوری کاری خود اضافه کنید (Hermes آن را برای هر دایرکتوری کاری بارگذاری می‌کند)، یا برای همه نشست‌ها به فایل شخصیت `SOUL.md` خود اضافه کنید:

```markdown
## سبک خروجی

خواننده دارای ADHD است. هر پاسخ را طوری تنظیم کنید که قابل اجرا باشد:

1. با پاسخ یا اقدام بعدی شروع کنید: ابتدا دستور، مسیر یا قطعه‌کد.
2. کارهای چندمرحله‌ای را شماره‌گذاری کنید؛ در هر مرحله یک اقدام مشخص و محدود.
3. با یک اقدام بعدی که در کمتر از دو دقیقه قابل انجام است پایان دهید.
4. موضوع فعلی را پیش از مطرح کردن موضوع جدید تمام کنید.
5. پیشرفت را در هر مرحله بازگو کنید ("مرحله ۳ از ۵ انجام شد").
6. تخمین زمان را با واحدهای ملموس بیان کنید، هرگز از "یک کم" استفاده نکنید.
7. پس از اعمال تغییر، نشان دهید چه چیزی الان کار می‌کند.
8. خطاها: محل، علت و راه حل را بیان کنید. بدون حاشیه و اغراق.
9. فهرست‌ها را به حداکثر ۵ مورد محدود کنید.
10. بدون مقدمه، بدون خلاصه، بدون کلمات پایانی.

استثناها: وقتی درخواست توضیح شد، به‌طور کامل توضیح دهید. قبل از اقدامات مخرب تایید بگیرید. پس از سه اصلاح ناموفق، متوقف شوید و فرض مشکوک را نام ببرید. اگر درخواست مبهم است، یک سوال کوتاه بپرسید.
```

</details>

<details>
<summary><strong>Kimi Code CLI</strong></summary>

### نصب

یک نشست Kimi Code را شروع کنید، سپس:

1. دستور `/plugins` را اجرا کنید.
2. گزینه **Custom** را انتخاب کنید.
3. آدرس `https://github.com/ayghri/i-have-adhd` را پیست کرده و `Enter` را فشار دهید.
4. گزینه **Trust and install** را انتخاب کنید.

از دستور اسلش `/skill:i-have-adhd` برای فراخوانی صریح مهارت استفاده کنید.

### به‌روزرسانی

دستور `/plugins` در نشست Kimi Code، انتقال نشانگر روی **I Have ADHD**، کلید `R` را فشار دهید.

### حذف

دستور `/plugins` در نشست Kimi Code، انتقال نشانگر روی **I Have ADHD**، کلید `D` را فشار دهید.


</details>

<details>
<summary><strong>Pi</strong></summary>

ابزار Pi این مخزن را به عنوان یک پکیج بومی شناسایی می‌کند: `extensions/` حالت پایدار در نشست را ارائه می‌دهد و `skills/` نقطه ورود Agent Skills را در دسترس نگه می‌دارد.

### نصب

```bash
pi install https://github.com/ayghri/i-have-adhd
```

یک نشست جدید Pi شروع کنید. خروجی سازگار با ADHD را برای نشست فعلی تغییر دهید (تاتگل کنید):

```text
/i-have-adhd
```

پانویس در زمان فعال بودن این حالت عبارت `● ADHD ON` را نشان می‌دهد. دستور را دوباره اجرا کنید تا خاموش شود، یا صریح باشید:

```text
/i-have-adhd on
/i-have-adhd off
stop adhd mode
```

مانند هوک Claude Code، این افزونه مجموعه قوانین را یک بار به گفتگو اضافه می‌کند به جای اینکه دستورالعمل سیستم را در هر درخواست بازنویسی کند، و پس از حذف آن طی فشرده‌سازی (compaction)، دوباره آن را اضافه می‌کند.

دستور موجود Agent Skills همچنان به عنوان یک نام مستعار (alias) در دسترس است:

```text
/skill:i-have-adhd
```

یک نشست جدید Pi را با فعال بودن پیش‌فرض این حالت شروع کنید:

```bash
pi --adhd
```

### تایید نصب

```bash
pi list
```

تایید کنید که پکیج GitHub در لیست است، سپس `/i-have-adhd` را تایپ کرده و بررسی کنید که `● ADHD ON` در پانویس ظاهر شود.

### به‌روزرسانی

```bash
pi update https://github.com/ayghri/i-have-adhd
```

یا هر پکیج سنجاق‌نشده Pi را با `pi update --extensions` به‌روزرسانی کنید.

### حذف

```bash
pi remove https://github.com/ayghri/i-have-adhd
```

### همیشه فعال (اختیاری)

یک پرچم در دایرکتوری تنظیمات دستیار Pi ایجاد کنید:

```bash
touch ~/.pi/agent/.i-have-adhd-always
```

این افزونه پرچم را در هر نشست جدید، ازسرگرفته‌شده، فورک‌شده یا بازبارگذاری‌شده بررسی می‌کند. انتخاب ذخیره‌شده برای نشست فعلی بر این پیش‌فرض اولویت دارد، بنابراین عبارت `stop adhd mode` آن نشست را غیرفعال نگه می‌دارد.

بازگشت به حالت در صورت درخواست (on-demand):

```bash
rm ~/.pi/agent/.i-have-adhd-always
```

اگر `PI_CODING_AGENT_DIR` تنظیم شده است، فایل `.i-have-adhd-always` را در آن دایرکتوری قرار دهید. پس از تغییر پرچم، دستور `/reload` را اجرا کرده یا یک نشست جدید شروع کنید.

</details>


<details>
<summary><strong>Qwen Code</strong></summary>

### نصب

```bash
qwen extensions install ayghri/i-have-adhd
```

ابزار Qwen Code از میانبر GitHub پشتیبانی کرده و مخزن را به عنوان یک افزونه بومی نصب می‌کند. این افزونه مهارت موجود در `skills/` را شناسایی می‌نماید.

برای فراخوانی صریح مهارت، عبارت `/i-have-adhd` را تایپ کنید. نصب افزونه تا زمانی که مهارت فراخوانی نشود، خروجی را تغییر نمی‌دهد.

### تایید نصب

```bash
qwen extensions list
```

سپس یک نشست جدید Qwen Code را شروع کرده و اجرا کنید:

```text
/skills
```

تایید کنید که `i-have-adhd` در لیست ظاهر می‌شود.

### به‌روزرسانی

```bash
qwen extensions update i-have-adhd
```

### حذف

```bash
qwen extensions uninstall i-have-adhd
```

</details>

<details>
<summary><strong>Zed</strong></summary>

دستیار Zed مهارت‌های دستیار (Agent Skills) را به صورت بومی می‌خواند: همان فایل `SKILL.md` بدون نیاز به تبدیل. ("Rules" قدیمی‌تر Zed با Skills و دستورالعمل‌های `AGENTS.md` جایگزین شده‌اند.)

### نصب

در پنل دستیار (Agent Panel)، مدیریت Skills را باز کرده و **Create skill from URL** را انتخاب کنید (همچنین در پالت دستورات به صورت `agent: create skill from url` در دسترس است)، سپس پیست کنید:

```
https://github.com/ayghri/i-have-adhd/blob/main/skills/i-have-adhd/SKILL.md
```

آن را در محدوده **User** برای همه پروژه‌ها، یا محدوده **Project** برای یک پروژه ذخیره کنید. سپس `/i-have-adhd` را در پنل دستیار تایپ کنید.

ترجیح می‌دهید از سیستم فایل استفاده کنید؟ مخزن را کلون کرده و پوشه مهارت را در دایرکتوری مهارت‌های کاربر خود قرار دهید:

```bash
git clone https://github.com/ayghri/i-have-adhd
cp -R i-have-adhd/skills/i-have-adhd ~/.config/zed/skills/
```

### تایید نصب

مدیریت Skills را در پنل دستیار باز کرده و تایید کنید که `i-have-adhd` لیست شده است. یا `/` را تایپ کرده و تایید کنید که ظاهر می‌شود.

### به‌روزرسانی

از همان URL دوباره وارد کنید (جایگزین می‌شود)، یا پس از `git pull` پوشه را دوباره کپی کنید.

### حذف

عبارت `i-have-adhd` را از مدیریت Skills حذف کنید، یا `~/.config/zed/skills/i-have-adhd` را پاک نمایید.

### همیشه فعال (اختیاری)

به فایل شخصی `~/.config/zed/AGENTS.md` اضافه کنید:

```markdown
## سبک خروجی

خواننده دارای ADHD است. هر پاسخ را طوری تنظیم کنید که قابل اجرا باشد:

1. با پاسخ یا اقدام بعدی شروع کنید: ابتدا دستور، مسیر یا قطعه‌کد.
2. کارهای چندمرحله‌ای را شماره‌گذاری کنید؛ در هر مرحله یک اقدام مشخص و محدود.
3. با یک اقدام بعدی که در کمتر از دو دقیقه قابل انجام است پایان دهید.
4. موضوع فعلی را پیش از مطرح کردن موضوع جدید تمام کنید.
5. پیشرفت را در هر مرحله بازگو کنید ("مرحله ۳ از ۵ انجام شد").
6. تخمین زمان را با واحدهای ملموس بیان کنید، هرگز از "یک کم" استفاده نکنید.
7. پس از اعمال تغییر، نشان دهید چه چیزی الان کار می‌کند.
8. خطاها: محل، علت و راه حل را بیان کنید. بدون حاشیه و اغراق.
9. فهرست‌ها را به حداکثر ۵ مورد محدود کنید.
10. بدون مقدمه، بدون خلاصه، بدون کلمات پایانی.

استثناها: وقتی درخواست توضیح شد، به‌طور کامل توضیح دهید. قبل از اقدامات مخرب تایید بگیرید. پس از سه اصلاح ناموفق، متوقف شوید و فرض مشکوک را نام ببرید. اگر درخواست مبهم است، یک سوال کوتاه بپرسید.
```

</details>

<details>
<summary><strong>Cursor, OpenCode, Amp, and any other agent-skills harness</strong></summary>

با هر محیطی که مهارت‌های دستیار (agent skills) را می‌خواند کار می‌کند. عبارت `-a <agent>` را با دستیار خود جایگزین کنید.

### نصب

```bash
npx skills add ayghri/i-have-adhd                  # این فضای کاری
npx skills add ayghri/i-have-adhd -g               # همه پروژه‌ها
npx skills add ayghri/i-have-adhd -a cursor -y     # فقط یک دستیار
npx skills add ayghri/i-have-adhd -a opencode -y
```

در چت دستیار جدید، `/i-have-adhd` را تایپ کنید.

بدون CLI، پوشه مهارت را در هر مسیری که دستیار شما اسکن می‌کند کپی کنید:

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.cursor/skills     # Cursor. از .agents/skills برای OpenCode یا مسیر اختصاصی دستیار خود استفاده کنید
cp -R i-have-adhd/skills/i-have-adhd ~/.cursor/skills/
```

### تایید نصب

```bash
npx skills list
npx skills ls -g    # در صورت نصب سراسری
```

### به‌روزرسانی

```bash
npx skills update i-have-adhd
npx skills update -g    # در صورت نصب سراسری
```

### حذف

```bash
npx skills remove i-have-adhd
npx skills remove i-have-adhd -g    # در صورت نصب سراسری
```

### همیشه فعال (اختیاری)

این متن را در فایل قوانین پایدار دستیار خود پیست کنید. Cursor: **Settings → Rules → User Rules**، یا یک قانون پروژه در مسیر `.cursor/rules/` با `alwaysApply: true`. OpenCode: `~/.config/opencode/AGENTS.md`.

```markdown
## سبک خروجی

خواننده دارای ADHD است. هر پاسخ را طوری تنظیم کنید که قابل اجرا باشد:

1. با پاسخ یا اقدام بعدی شروع کنید: ابتدا دستور، مسیر یا قطعه‌کد.
2. کارهای چندمرحله‌ای را شماره‌گذاری کنید؛ در هر مرحله یک اقدام مشخص و محدود.
3. با یک اقدام بعدی که در کمتر از دو دقیقه قابل انجام است پایان دهید.
4. موضوع فعلی را پیش از مطرح کردن موضوع جدید تمام کنید.
5. پیشرفت را در هر مرحله بازگو کنید ("مرحله ۳ از ۵ انجام شد").
6. تخمین زمان را با واحدهای ملموس بیان کنید، هرگز از "یک کم" استفاده نکنید.
7. پس از اعمال تغییر، نشان دهید چه چیزی الان کار می‌کند.
8. خطاها: محل، علت و راه حل را بیان کنید. بدون حاشیه و اغراق.
9. فهرست‌ها را به حداکثر ۵ مورد محدود کنید.
10. بدون مقدمه، بدون خلاصه، بدون کلمات پایانی.

استثناها: وقتی درخواست توضیح شد، به‌طور کامل توضیح دهید. قبل از اقدامات مخرب تایید بگیرید. پس از سه اصلاح ناموفق، متوقف شوید و فرض مشکوک را نام ببرید. اگر درخواست مبهم است، یک سوال کوتاه بپرسید.
```
</details>


## نحوه کارکرد فعال‌سازی

1. **نصب‌شده، اما فراخوانی نمیشود.** در Claude Code، Qwen Code و Codex تا زمانی که مهارت را به طور صریح فراخوانی نکنید، هیچ اتفاقی نمی‌افتد. Claude Code و Qwen Code از تنظیم `disable-model-invocation: true` در `SKILL.md` پیروی می‌کنند؛ Codex از `policy.allow_implicit_invocation: false` در `agents/openai.yaml` پیروی می‌کند. سایر محیط‌ها ممکن است توضیحات هر مهارت را در هنگام راه‌اندازی بارگذاری کرده و خودشان مهارت را فعال کنند.
2. **آن را صراحتاً فراخوانی می‌کنید.** عبارت `/i-have-adhd` را در Claude Code یا Qwen Code، یا `$i-have-adhd` را در Codex تایپ کنید. قوانین برای آن نشست فعال می‌مانند. عبارت "stop adhd mode" یا "normal mode" آن‌ها را خاموش می‌کند.
3. **ایجاد فایل `~/.claude/.i-have-adhd-always`** (در Claude Code). یک هوک `SessionStart` مجموعه کامل قوانین را از اولین پیام در هر نشست بارگذاری می‌کند.
4. **افزودن قطعه‌کد همیشه فعال بالا** (سایر محیط‌ها). قوانین اصلی را در زمینه (context) پایدار دستیار شما نگه می‌دارد.

در Claude Code، Qwen Code و Codex هیچ حالت میانه‌ای وجود ندارد: اگر آن را روشن نکرده باشید، خاموش است.

## عیب‌یابی

**عدم وجود `/i-have-adhd` در تکمیل خودکار.** دستیار را مجدداً راه‌اندازی کنید. نمایه پلاگین در زمان راه‌اندازی خوانده می‌شود.

**بی‌اثر بودن پرچم همیشه فعال.** پلاگین را به‌روزرسانی کنید (`claude plugin marketplace update i-have-adhd`) و مجدداً راه‌اندازی کنید. هوک‌ها در زمان راه‌اندازی خوانده می‌شوند و پرچم نیاز به نسخه‌ای از پلاگین دارد که شامل `hooks/hooks.json` باشد.

**ناموفق بودن `claude plugin marketplace add`.** از فرمت `owner/repo` استفاده کنید. مسیر محلی باید به ریشه مخزن اشاره کند، نه `.claude-plugin/`.

**نصب شده اما پاسخ‌ها همچنان دارای مقدمه هستند.** یک نشست جدید باز کنید. اگر همچنان انحراف وجود دارد، عبارت‌ها در `skills/i-have-adhd/SKILL.md` را دقیق‌تر کنید.

**قوانین متفاوت میخواهید.** مخزن را فورک کنید، `skills/i-have-adhd/SKILL.md` را ویرایش کنید، سپس نسخه خود را جایگزین نمایید:

```bash
claude plugin uninstall i-have-adhd            # ابتدا نسخه اصلی (upstream) را حذف کنید:
claude plugin marketplace remove i-have-adhd   # فورک و نسخه اصلی نام یکسانی دارند
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

مجدداً راه‌اندازی کرده، سپس `/i-have-adhd` را دوباره فراخوانی کنید.

**قابل نمایش نبودن مهارت پس از `npx skills add`.** یک چت جدید با دستیار شروع کنید. مهارت‌ها در شروع نشست نمایه می‌شوند. تایید کنید که پوشه در مسیری که دستیار شما اسکن می‌کند قرار گرفته باشد (`~/.cursor/skills/` برای Cursor، و `.agents/skills/` برای OpenCode) و نام `name` در frontmatter با نام پوشه مطابقت داشته باشد.
