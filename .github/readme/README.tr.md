<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">DEHB dostu çıktılar. DEHB tanısı gerekmez!</strong>
</p>
<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/ayghri/i-have-adhd?style=flat" alt="Lisans"></a>
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
  <strong title="Türkçe" aria-label="Türkçe">🇹🇷</strong>
</p>


## Kurulum

CLI isteminize kopyalayıp yapıştırın:

```text
Install the i-have-adhd skill/plugin from https://github.com/ayghri/i-have-adhd, refer to the repo's AGENTS.md for instructions.
```

Ya da 🔗 [kurulum talimatlarına göz atın](../../INSTALL.md).

## Ne işe yarar

Kodlama asistanınız için, yanıtı gereksiz ayrıntıların altında ezmesini engelleyen bir skill. Önce eylem gelir. Adımlar numaralıdır. “Umarım yardımcı olur!” yok.

[Kacper Rutkiewicz | AI Made Simple](https://youtu.be/NEl8kPWZP_Y), skill'in önceki bir sürümünü güzelce açıklıyor.

## Neleri değiştirir


<table>
<tr>
<td width="50%">

## Önce

> Harika soru! Bir düşüneyim. Kimlik doğrulama akışınızda birkaç hareketli parça var: middleware, token doğrulama ve çerez yönetimi. `src/auth.ts` dosyasına baktığımda, `verifyToken` işlevi (yaklaşık 42-58. satırlar) eski bir `jsonwebtoken` API'si kullanıyor gibi görünüyor. Bir seçenek, paketi güncellemek ve bu işlevi yeniden yazmak olurdu. Değişikliği yaptıktan sonra hiçbir şeyin bozulmadığını doğrulamak için kimlik doğrulama testlerini çalıştırmanız gerekir. Bu arada, bağımlılık sürümlerinize genel olarak da göz atmak isteyebilirsiniz. Umarım yardımcı olur! Daha ayrıntılı incelemek isterseniz haber verin.

</td>

<td width="50%">

## Sonra

> `npm install jsonwebtoken@latest` komutunu çalıştırın, ardından `src/auth.ts` dosyasının 42. satırını düzenleyin.
>
> 1. `src/auth.ts` dosyasını açın
> 2. `verifyToken` işlevini (42-58. satırlar) aşağıdaki kod parçacığıyla değiştirin
> 3. `npm test -- auth.spec.ts` komutunu çalıştırın
>
> Sıradaki adım: Herhangi bir test başarısız olursa, başarısız olan ilk satırı yapıştırın.

</td>
</tr>
</table>


## Kurallar

10 kural. Tam metin için [SKILL.md](../../skills/i-have-adhd/SKILL.md) dosyasına bakın.

1. Bir sonraki eylemle başlayın.
2. Birden fazla adım içeren görevleri numaralandırın.
3. Tek bir somut sonraki adımla bitirin.
4. Konu dışına çıkmayın.
5. Her turda durumu yeniden belirtin.
6. Dakika cinsinden net zaman tahminleri verin; “birazdan” demeyin.
7. Kazanımları görünür kılın.
8. Hataları olduğu gibi, doğrudan ifade edin.
9. Listeleri 5 maddeyle sınırlayın.
10. Ön söz yok. Özet yok. Kapanış yok.

## Özelleştirin

Fork oluşturun, `skills/i-have-adhd/SKILL.md` dosyasını düzenleyin, ardından kendi kopyanızı kullanın:

```bash
claude plugin uninstall i-have-adhd            # önce upstream kopyasını kaldırın:
claude plugin marketplace remove i-have-adhd   # fork ve upstream aynı adı paylaşır
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Kodlama asistanınızı yeniden başlatın, ardından `/i-have-adhd` komutunu yeniden çağırın.

## Teşekkürler

J. Russell Ramsay ve Anthony L. Rostain'in *The Adult ADHD Tool Kit* kitabından serbestçe uyarlanmıştır. Bir insanın gününü nasıl düzenlemesi gerektiğine değil, bir LLM'nin nasıl yanıt vermesi gerektiğine uyarlanmıştır.

## Lisans

[MIT](../../LICENSE).

Bir “Harika soru!” ifadesini geçmek için kaydırmanız gereken mesafeyi azalttıysa ⭐ ile yıldız verin.
