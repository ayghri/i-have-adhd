<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">Respons yang ramah bagi kamu yang memiliki ADHD. Tanpa perlu diagnosis!</strong>
</p>
<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/aixinwudi/i-have-adhd-cn?style=flat" alt="Lisensi"></a>
</p>

<p align="center">
  <a href="../../README.md" title="English" aria-label="English">🇬🇧</a> ·
  <a href="README.zh-CN.md" title="简体中文" aria-label="简体中文">🇨🇳</a> ·
  <strong title="Bahasa Indonesia" aria-label="Bahasa Indonesia">🇮🇩</strong> ·
  <a href="README.ja.md" title="日本語" aria-label="日本語">🇯🇵</a> ·
  <a href="README.vi.md" title="Tiếng Việt" aria-label="Tiếng Việt">🇻🇳</a> ·
  <a href="README.ko.md" title="한국어" aria-label="한국어">🇰🇷</a> ·
  <a href="README.fa.md" title="فارسی" aria-label="فارسی">🇮🇷</a> ·
  <a href="README.th.md" title="ภาษาไทย" aria-label="ภาษาไทย">🇹🇭</a>
</p>


## Instalasi

🔗 [Panduan Instalasi](../install/INSTALL.id.md)

## Apa Fungsinya Sii?

Sebuah skill untuk asisten coding-mu yang mencegahnya mengubur jawaban di tengah teks. Aksi di awal. Langkah bernomor. Tanpa basa-basi seperti "Semoga membantu!"


## Apa yang Berubah??


<table>
<tr>
<td width="50%">

## Sebelumnya

> Pertanyaan bagus! Biarkan saya memikirkan ini. Alur autentikasi Anda memiliki beberapa bagian yang terlibat: middleware, verifikasi token, dan penanganan cookie. Melihat `src/auth.ts`, fungsi `verifyToken` (sekitar baris 42-58) sepertinya menggunakan API lama dari `jsonwebtoken`. Salah satu pendekatannya adalah memperbarui paket dan menulis ulang fungsi tersebut. Setelah perubahan, Anda perlu menjalankan tes autentikasi untuk memastikan tidak ada yang rusak. Ngomong-ngomong, mungkin ada baiknya meninjau ulang versi dependensi Anda secara keseluruhan. Semoga membantu! Beri tahu saya jika Anda ingin mendalami lebih lanjut.

</td>
<td width="50%">

## Sesudahnya

> Jalankan `npm install jsonwebtoken@latest` lalu edit `src/auth.ts:42`.
>
> 1. Buka `src/auth.ts`
> 2. Ganti `verifyToken` (baris 42–58) dengan cuplikan di bawah ini
> 3. Jalankan `npm test -- auth.spec.ts`
>
> Langkah selanjutnya: tempel baris error pertama jika ada tes yang gagal.

</td>
</tr>
</table>


## Aturannya

10 aturan. Teks lengkap ada di [SKILL.md](../../skills/i-have-adhd/SKILL.md).

1. Mulai dengan langkah selanjutnya.
2. Beri nomor pada tugas yang memiliki beberapa langkah.
3. Akhiri dengan langkah selanjutnya yang konkret.
4. Potong pembahasan yang melebar (tidak relevan).
5. Tegaskan kembali status terkini di setiap giliran.
6. Berikan estimasi waktu yang spesifik (dalam menit, bukan "sebentar").
7. Buat pencapaian terlihat jelas.
8. Laporkan error secara objektif.
9. Batasi daftar maksimal 5 item.
10. Tanpa pembukaan. Tanpa ringkasan ulang. Tanpa kalimat penutup.

## Sesuaikan (Kustomisasi)

Lakukan fork, edit `skills/i-have-adhd/SKILL.md`, dan ganti dengan salinan Anda sendiri:

```bash
claude plugin uninstall i-have-adhd            # hapus salinan upstream terlebih dahulu:
claude plugin marketplace remove i-have-adhd   # fork dan upstream menggunakan nama yang sama
claude plugin marketplace add <username-anda>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Mulai ulang Claude Code dan panggil `/i-have-adhd` lagi.

## Kredit

Terinspirasi secara bebas dari *The Adult ADHD Tool Kit* karya J. Russell Ramsay dan Anthony L. Rostain. Diadaptasi untuk cara LLM seharusnya merespons, bukan untuk cara seseorang mengatur harinya.

## Lisensi

MIT.

Beri ⭐ jika ini menyelamatkanmu dari harus menggulir layar melewati satu lagi "Pertanyaan bagus!"