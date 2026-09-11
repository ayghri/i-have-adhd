<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">ADHD-अनुकूल जवाफहरू। ADHD को निदान आवश्यक छैन!</strong>
</p>
<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/ayghri/i-have-adhd?style=flat" alt="लाइसेन्स"></a>
</p>

<p align="center">
  <a href="../../README.md" title="English" aria-label="English">🇬🇧</a> ·
  <a href="README.zh-CN.md" title="简体中文" aria-label="简体中文">🇨🇳</a> ·
  <a href="README.pt-BR.md" title="Português (Brasil)" aria-label="Português (Brasil)">🇧🇷</a> ·
  <a href="README.ja.md" title="日本語" aria-label="日本語">🇯🇵</a> ·
  <a href="README.vi.md" title="Tiếng Việt" aria-label="Tiếng Việt">🇻🇳</a> ·
  <a href="README.ko.md" title="한국어" aria-label="한국어">🇰🇷</a> ·
  <a href="README.th.md" title="ภาษาไทย" aria-label="ภาษาไทย">🇹🇭</a> ·
  <strong title="नेपाली" aria-label="नेपाली">🇳🇵</strong>
</p>

## स्थापना

CLI prompt मा यो text copy/paste गर्नुहोस्:

```text
Install the i-have-adhd skill/plugin from https://github.com/ayghri/i-have-adhd, refer to the repo's AGENTS.md for instructions.
```

वा 🔗 [स्थापना निर्देशन हेर्नुहोस्](../../INSTALL.md) (अङ्ग्रेजीमा)।

## यसले के गर्छ

तपाईंको coding assistant ले मुख्य उत्तरलाई लामो व्याख्याभित्र गाड्न नदिने skill। पहिले गर्नुपर्ने काम। क्रमाङ्कित चरणहरू। “यसले मद्दत गर्छ भन्ने आशा छ!” जस्ता अनावश्यक वाक्य छैनन्।

## के परिवर्तन हुन्छ

<table>
<tr>
<td width="50%">

## प्रयोगअघि

> राम्रो प्रश्न! यसबारे सोचौँ। तपाईंको authentication flow मा middleware, token verification र cookie handling जस्ता केही भाग छन्। `src/auth.ts` हेर्दा `verifyToken` function (लगभग 42–58 लाइन) ले `jsonwebtoken` को पुरानो API प्रयोग गरिरहेको जस्तो देखिन्छ। एउटा उपाय package update गरेर function फेरि लेख्नु हो। परिवर्तनपछि केही बिग्रिएको छैन भनेर auth tests चलाउनुपर्छ। साथै dependency versions पनि समग्रमा जाँच्न सक्नुहुन्छ। यसले मद्दत गर्छ भन्ने आशा छ! अझ गहिरो हेर्न चाहनुहुन्छ भने भन्नुहोस्।

</td>

<td width="50%">

## प्रयोगपछि

> `npm install jsonwebtoken@latest` चलाउनुहोस्, त्यसपछि `src/auth.ts:42` सम्पादन गर्नुहोस्।
>
> 1. `src/auth.ts` खोल्नुहोस्
> 2. `verifyToken` (लाइन 42–58) लाई तलको snippet ले बदल्नुहोस्
> 3. `npm test -- auth.spec.ts` चलाउनुहोस्
>
> अर्को कदम: कुनै test असफल भए पहिलो failing line paste गर्नुहोस्।

</td>
</tr>
</table>

## नियमहरू

१० वटा नियम। पूरा text [SKILL.md](../../skills/i-have-adhd/SKILL.md) मा छ।

1. अर्को गर्नुपर्ने कामबाट सुरु गर्नुहोस्।
2. धेरै चरण भएको कामलाई क्रमाङ्कित गर्नुहोस्।
3. एउटा ठोस अर्को कदममा अन्त्य गर्नुहोस्।
4. प्रसङ्गबाहिरका कुरा हटाउनुहोस्।
5. प्रत्येक turn मा हालको अवस्था फेरि स्पष्ट गर्नुहोस्।
6. समयको अनुमान ठोस रूपमा दिनुहोस् (मिनेटमा, “अलि समय” होइन)।
7. भएको प्रगति स्पष्ट देखिने बनाउनुहोस्।
8. त्रुटि तथ्यगत र सीधा रूपमा बताउनुहोस्।
9. सूचीलाई बढीमा ५ वस्तुमा सीमित गर्नुहोस्।
10. प्रस्तावना छैन। पुनरावलोकन छैन। अनावश्यक समापन छैन।

## आफूअनुसार मिलाउनुहोस्

Repository fork गर्नुहोस्, `skills/i-have-adhd/SKILL.md` सम्पादन गर्नुहोस्, त्यसपछि आफ्नो copy प्रयोग गर्नुहोस्:

```bash
claude plugin uninstall i-have-adhd            # पहिले upstream copy हटाउनुहोस्:
claude plugin marketplace remove i-have-adhd   # fork र upstream दुवैको नाम एउटै छ
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Claude Code restart गर्नुहोस्, त्यसपछि `/i-have-adhd` फेरि चलाउनुहोस्।

## श्रेय

J. Russell Ramsay र Anthony L. Rostain को *The Adult ADHD Tool Kit* बाट प्रेरित। मानिसले आफ्नो दिन कसरी व्यवस्थित गर्ने भन्ने होइन, LLM ले कसरी जवाफ दिनुपर्छ भन्नेअनुसार रूपान्तरण गरिएको हो।

## लाइसेन्स

MIT।

यसले तपाईंलाई एउटा “राम्रो प्रश्न!” पार गर्न स्क्रोल गर्नबाट बचायो भने Star ⭐ दिनुहोस्।
