<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">ADHD ရှိသူတွေ ဖတ်ရလွယ်အောင် ရေးပေးတဲ့ အဖြေတွေ။ ADHD လို့ ဆရာဝန်ပြောထားဖို့ မလိုပါဘူး!</strong>
</p>
<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/ayghri/i-have-adhd?style=flat" alt="လိုင်စင်"></a>
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
  <strong title="မြန်မာ" aria-label="မြန်မာ">🇲🇲</strong>
</p>


## ထည့်သွင်းနည်း

CLI prompt ထဲကို copy/paste လုပ်ပါ:

```text
Install the i-have-adhd skill/plugin from https://github.com/ayghri/i-have-adhd, refer to the repo's AGENTS.md for instructions.
```

ဒါမှမဟုတ် 🔗 [ထည့်သွင်းနည်း အပြည့်အစုံကို ကြည့်ပါ](../../INSTALL.md)။

## ဘာလုပ်ပေးလဲ

သင့် coding assistant က အဖြေကို စာတွေကြားမှာ မြှုပ်မထားအောင် တားပေးတဲ့ skill တစ်ခုပါ။ လုပ်ရမှာကို အရင်ပြောတယ်။ အဆင့်တွေကို နံပါတ်တပ်တယ်။ "Hope this helps!" မရှိဘူး။

[Kacper Rutkiewicz | AI Made Simple](https://youtu.be/NEl8kPWZP_Y) က ဒီ skill ရဲ့ version အဟောင်းကို ကောင်းကောင်း ရှင်းပြထားပါတယ်။

## ဘာတွေ ပြောင်းသွားလဲ


<table>
<tr>
<td width="50%">

## မသုံးခင်

> Great question! ဒါကို စဉ်းစားကြည့်ရအောင်။ သင့် auth flow မှာ အစိတ်အပိုင်း အတော်များများ ရှိပါတယ်: middleware၊ token verification နဲ့ cookie handling တို့ပါ။ `src/auth.ts` ကို ကြည့်ရင် `verifyToken` function (line 42-58 ဝန်းကျင်) က `jsonwebtoken` API အဟောင်းကို သုံးထားသလို ရှိပါတယ်။ နည်းလမ်းတစ်ခုကတော့ package ကို update လုပ်ပြီး အဲ့ function ကို ပြန်ရေးတာပါ။ ပြင်ပြီးရင် ဘာမှ မပျက်ဘူးဆိုတာ သေချာဖို့ auth test တွေကို run သင့်ပါတယ်။ စကားမစပ်၊ dependency version တွေကိုလည်း ကြည့်ချင်ကြည့်နိုင်ပါတယ်။ Hope this helps! ပိုသိချင်ရင် ပြောပါ။

</td>

<td width="50%">

## သုံးပြီးနောက်

> token validation ကို update လုပ်ဖို့ `src/auth.ts:42` ကို ပြင်ပါ။
>
> 1. `src/auth.ts` ကို ဖွင့်ပါ
> 2. `verifyToken` (line 42–58) ကို အောက်က snippet နဲ့ အစားထိုးပါ
> 3. `npm test -- auth.spec.ts` ကို run ပါ
>
> နောက်တစ်ဆင့်: test ကျရင် ပထမဆုံး ကျတဲ့ စာကြောင်းကို paste လုပ်ပါ။

</td>
</tr>
</table>


## စည်းမျဉ်းများ

စည်းမျဉ်း ၁၀ ခု ရှိပါတယ်။ အပြည့်အစုံကို [SKILL.md](../../skills/i-have-adhd/SKILL.md) မှာ ဖတ်ပါ။

1. လုပ်ရမယ့် နောက်တစ်ဆင့်ကို အရင်ပြောပါ။
2. အဆင့်များတဲ့ အလုပ်ကို နံပါတ်တပ်ပါ။
3. လက်တွေ့လုပ်လို့ရတဲ့ နောက်တစ်ဆင့် တစ်ခုနဲ့ အဆုံးသတ်ပါ။
4. ဘေးထွက်အကြောင်းအရာတွေ မထည့်ပါနဲ့။
5. လက်ရှိအခြေအနေကို reply တိုင်းမှာ ပြန်ပြောပါ။
6. အချိန်ခန့်မှန်းချက်ကို တိတိကျကျ ပြောပါ ("ခဏလေး" မဟုတ်ဘဲ မိနစ်နဲ့)။
7. ပြီးသွားတဲ့ အလုပ်ကို မြင်သာအောင် ပြပါ။
8. Error တွေကို ဖြစ်ရပ်အတိုင်း ပြောပါ။
9. စာရင်းတစ်ခုကို ၅ ခုအထိပဲ ပြပါ။
10. အစပျိုးစကား မလို၊ ပြန်အကျဉ်းချုပ် မလို၊ နှုတ်ဆက်စကား မလို။

## စိတ်ကြိုက်ပြင်ရန်

Fork လုပ်ပြီး `skills/i-have-adhd/SKILL.md` ကို ပြင်ပါ။ ပြီးရင် သင့် copy ကို အစားထိုးပါ:

```bash
claude plugin uninstall i-have-adhd            # drop the upstream copy first:
claude plugin marketplace remove i-have-adhd   # fork and upstream share both names
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Coding assistant ကို ပြန်စပြီး `/i-have-adhd` ကို ပြန်ခေါ်ပါ။

## Credits

J. Russell Ramsay နဲ့ Anthony L. Rostain ရေးတဲ့ *The Adult ADHD Tool Kit* ကို အကြမ်းဖျင်း အခြေခံထားပါတယ်။ လူတစ်ယောက် သူ့နေ့ရက်ကို ဘယ်လိုစီစဉ်ရမလဲ ဆိုတာအတွက် မဟုတ်ဘဲ LLM က ဘယ်လိုတုံ့ပြန်သင့်လဲ ဆိုတာအတွက် ပြင်ဆင်ထားတာပါ။

## လိုင်စင်

[MIT](../../LICENSE)။

"Great question!" တစ်ခုကို scroll ကျော်ရတာ တစ်ခါလောက် သက်သာသွားရင် Star ⭐ ပေးခဲ့ပါ။
