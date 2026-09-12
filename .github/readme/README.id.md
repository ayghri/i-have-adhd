<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">Output yang ramah ADHD. Tanpa perlu diagnosis ADHD!</strong>
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

Atau 🔗 [lihat panduan instalasi](../../INSTALL.md) (bahasa Inggris)

## Apa yang dilakukannya

Sebuah skill untuk asisten coding Anda yang mencegahnya mengubur jawaban. Aksi dulu. Langkah diberi nomor. Tanpa "Semoga membantu!"


## Apa yang berubah


<table>
<tr>
<td width="50%">

## Sebelum

> Pertanyaan bagus! Coba saya pikirkan dulu. Alur autentikasi Anda punya beberapa bagian yang saling terkait: middleware, verifikasi token, dan penanganan cookie. Melihat `src/auth.ts`, fungsi `verifyToken` (sekitar baris 42-58) sepertinya masih memakai API `jsonwebtoken` versi lama. Salah satu pendekatannya adalah memperbarui paket tersebut dan menulis ulang fungsi itu. Setelah melakukan perubahan, Anda sebaiknya menjalankan tes autentikasi untuk memastikan tidak ada yang rusak. Oh ya, mungkin Anda juga ingin meninjau versi dependensi Anda secara keseluruhan. Semoga membantu! Beri tahu saya kalau mau membahasnya lebih dalam.

</td>

<td width="50%">

## Sesudah

> Jalankan `npm install jsonwebtoken@latest`, lalu edit `src/auth.ts:42`.
>
> 1. Buka `src/auth.ts`
> 2. Ganti `verifyToken` (baris 42–58) dengan potongan kode di bawah
> 3. Jalankan `npm test -- auth.spec.ts`
>
> Berikutnya: tempelkan baris kegagalan pertama jika ada tes yang gagal.

</td>
</tr>
</table>


## Aturannya

10 aturan. Teks lengkapnya ada di [SKILL.md](../../skills/i-have-adhd/SKILL.md).

1. Mulai dengan aksi berikutnya.
2. Beri nomor untuk tugas multi-langkah.
3. Akhiri dengan satu langkah berikutnya yang konkret.
4. Singkirkan bahasan yang menyimpang.
5. Nyatakan ulang status di setiap giliran.
6. Estimasi waktu yang spesifik (dalam menit, bukan "sebentar").
7. Tampilkan hasil yang sudah dicapai.
8. Laporkan error secara lugas.
9. Batasi daftar maksimal 5 item.
10. Tanpa pembuka. Tanpa rekap. Tanpa basa-basi penutup.

## Sesuaikan

Fork, edit `skills/i-have-adhd/SKILL.md`, lalu pasang salinan Anda:

```bash
claude plugin uninstall i-have-adhd            # drop the upstream copy first:
claude plugin marketplace remove i-have-adhd   # fork and upstream share both names
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Mulai ulang Claude Code, lalu panggil `/i-have-adhd` lagi.

## Kredit

Terinspirasi secara bebas dari *The Adult ADHD Tool Kit* karya J. Russell Ramsay dan Anthony L. Rostain. Diadaptasi untuk cara sebuah LLM sebaiknya merespons, bukan cara manusia sebaiknya mengatur harinya.

## Lisensi

MIT.

Beri ⭐ kalau ini menghemat satu kali scroll melewati satu "Pertanyaan bagus!"
