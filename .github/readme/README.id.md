<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">Output yang ramah ADHD. Tidak perlu diagnosis ADHD!</strong>
</p>
<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/ayghri/i-have-adhd?style=flat" alt="Lisensi"></a>
</p>

<p align="center">
  <a href="../../README.md" title="English" aria-label="English">🇬🇧</a> ·
  <a href="README.zh-CN.md" title="简体中文" aria-label="简体中文">🇨🇳</a> ·
  <a href="README.pt-BR.md" title="Português (Brasil)" aria-label="Português (Brasil)">🇧🇷</a> ·
  <a href="README.ja.md" title="日本語" aria-label="日本語">🇯🇵</a> ·
  <a href="README.vi.md" title="Tiếng Việt" aria-label="Tiếng Việt">🇻🇳</a> ·
  <a href="README.ko.md" title="한국어" aria-label="한국어">🇰🇷</a> ·
  <a href="README.th.md" title="ภาษาไทย" aria-label="ภาษาไทย">🇹🇭</a> ·
  <strong title="Bahasa Indonesia" aria-label="Bahasa Indonesia">🇮🇩</strong>
</p>


## Instalasi

Salin/tempel ke prompt CLI Anda:

```text
Install the i-have-adhd skill/plugin from https://github.com/ayghri/i-have-adhd, refer to the repo's AGENTS.md for instructions.
```

Atau 🔗 [lihat petunjuk instalasi](../../INSTALL.md).

## Apa yang dilakukan

Skill untuk asisten koding Anda yang mencegah jawaban terkubur dalam penjelasan panjang. Aksi dulu. Langkah bernomor. Tanpa "Semoga membantu!"


## Apa yang berubah


<table>
<tr>
<td width="50%">

## Sebelum

> Pertanyaan bagus! Coba saya pikirkan. Alur auth Anda punya beberapa bagian yang saling terkait: middleware, verifikasi token, dan penanganan cookie. Melihat `src/auth.ts`, fungsi `verifyToken` (sekitar baris 42–58) tampaknya masih menggunakan API `jsonwebtoken` yang lebih lama. Salah satu pendekatan adalah memperbarui package dan menulis ulang fungsi tersebut. Setelah perubahan, Anda sebaiknya menjalankan test auth untuk memastikan tidak ada yang rusak. Omong-omong, mungkin ada baiknya juga memeriksa versi dependency secara keseluruhan. Semoga membantu! Beri tahu saya kalau ingin membahas lebih dalam.

</td>

<td width="50%">

## Sesudah

> Jalankan `npm install jsonwebtoken@latest`, lalu edit `src/auth.ts:42`.
>
> 1. Buka `src/auth.ts`
> 2. Ganti `verifyToken` (baris 42–58) dengan snippet di bawah
> 3. Jalankan `npm test -- auth.spec.ts`
>
> Berikutnya: tempel baris error pertama jika ada test yang gagal.

</td>
</tr>
</table>


## Aturannya

10 aturan. Teks lengkap ada di [SKILL.md](../../skills/i-have-adhd/SKILL.md).

1. Mulai dengan aksi berikutnya.
2. Beri nomor untuk tugas bertahap.
3. Akhiri dengan satu langkah berikutnya yang konkret.
4. Hilangkan pembahasan yang menyimpang.
5. Nyatakan kembali status di setiap balasan.
6. Berikan estimasi waktu spesifik (dalam menit, bukan "sebentar").
7. Tampilkan hasil yang berhasil dicapai.
8. Jelaskan error apa adanya.
9. Batasi list maksimal 5 item.
10. Tanpa pembuka. Tanpa rekap. Tanpa basa-basi penutup.

## Sesuaikan

Fork repo ini, edit `skills/i-have-adhd/SKILL.md`, lalu ganti ke salinan Anda:

```bash
claude plugin uninstall i-have-adhd            # drop the upstream copy first:
claude plugin marketplace remove i-have-adhd   # fork and upstream share both names
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Restart Claude Code, lalu jalankan lagi `/i-have-adhd`.

## Kredit

Terinspirasi secara bebas dari *The Adult ADHD Tool Kit* karya J. Russell Ramsay dan Anthony L. Rostain. Diadaptasi untuk cara LLM seharusnya merespons, bukan cara manusia mengatur harinya.

## Lisensi

MIT.

Beri bintang ⭐ kalau ini membuat Anda tidak perlu scroll melewati satu lagi "Pertanyaan bagus!"
