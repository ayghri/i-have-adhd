# Cara Menginstal

<details>
<summary><strong>Antigravity (<code>agy</code>)</strong></summary>

### Instalasi

```bash
agy plugin install https://github.com/aixinwudi/i-have-adhd-cn
```

### Verifikasi

```bash
agy plugin list
```

### Pembaruan

```bash
agy plugin uninstall i-have-adhd
agy plugin install https://github.com/aixinwudi/i-have-adhd-cn
```

### Uninstal

```bash
agy plugin uninstall i-have-adhd
```

Atau biarkan terinstal tetapi nonaktifkan: `agy plugin disable i-have-adhd`.

### Selalu Aktif (opsional)

Tambahkan ke `~/.gemini/GEMINI.md`:

```markdown
## Gaya Respons

Pembaca ini memiliki ADHD. Susun setiap respons agar mudah ditindaklanjuti, jangan bertele-tele yaaa:

1. Mulailah dengan jawaban atau langkah selanjutnya: perintah, jalur file, atau cuplikan kode terlebih dahulu.
2. Beri nomor pada pekerjaan yang memiliki beberapa langkah; batasi satu tindakan jelas per langkah.
3. Akhiri dengan satu tindakan selanjutnya yang bisa diselesaikan dalam waktu kurang dari dua menit.
4. Selesaikan masalah saat ini sebelum membahas masalah lain.
5. Tegaskan kembali progres di setiap giliran (misalnya, "langkah 3 dari 5 selesai").
6. Berikan estimasi waktu dalam satuan yang konkret, jangan pernah menggunakan kata seperti "sebentar".
7. Setelah ada perubahan, tunjukkan apa yang sekarang berhasil berfungsi.
8. Error: jelaskan lokasi, penyebab, dan solusinya, tanpa basa-basi.
9. Batasi daftar hanya hingga 5 item.
10. Tanpa pembukaan, ringkasan ulang, atau salam penutup.

Pengecualian: jelaskan secara lengkap jika diminta. Konfirmasi sebelum melakukan tindakan yang bersifat destruktif. Setelah tiga kali percobaan perbaikan yang gagal, berhentilah dan identifikasi asumsi yang meragukan. Jika permintaan ambigu, ajukan satu pertanyaan singkat.
```

</details>

<details>
<summary><strong>Claude Code</strong></summary>

### Instalasi

```bash
claude plugin marketplace add aixinwudi/i-have-adhd-cn
claude plugin install i-have-adhd@i-have-adhd
```

Ketik `/i-have-adhd`.

### Verifikasi

```bash
claude plugin list
```

### Pembaruan

```bash
claude plugin marketplace update i-have-adhd
```

### Uninstal

```bash
claude plugin uninstall i-have-adhd
claude plugin marketplace remove i-have-adhd
```

Atau biarkan terinstal tetapi nonaktifkan: `claude plugin disable i-have-adhd`.

### Selalu Aktif (opsional)

Hook `SessionStart` akan memuat semua aturan di awal setiap sesi; Anda tidak perlu lagi mengetik `/i-have-adhd`:

```bash
touch ~/.claude/.i-have-adhd-always
```

Jika Anda menggunakan direktori konfigurasi kustom untuk Claude, buat file penanda (flag) di dalamnya:

```bash
touch "$CLAUDE_CONFIG_DIR/.i-have-adhd-always"
```

Untuk kembali ke mode sesuai permintaan (on-demand):

```bash
rm ~/.claude/.i-have-adhd-always
```

Hook ini hanya berjalan ketika file penanda ada, jadi menginstal plugin saja tidak akan mengubah apa pun. Perintah "stop adhd mode" tetap akan menonaktifkannya di sesi saat ini.

</details>

<details>
<summary><strong>Codex</strong></summary>

### Instalasi

```bash
codex plugin marketplace add aixinwudi/i-have-adhd-cn --ref main
codex plugin add i-have-adhd@i-have-adhd
```

Aktifkan skill ini secara eksplisit dengan mengetik `$i-have-adhd`. Codex ga bakalan memanggilnya secara otomatis.

### Verifikasi

```bash
codex plugin list
```

### Pembaruan

```bash
codex plugin marketplace upgrade i-have-adhd
codex plugin remove i-have-adhd
codex plugin add i-have-adhd@i-have-adhd
```

### Uninstal

```bash
codex plugin remove i-have-adhd
codex plugin marketplace remove i-have-adhd
```

### Selalu Aktif (opsional)

Tambahkan ke `~/.codex/AGENTS.md`:

```markdown
## Gaya Respons

Pembaca memiliki ADHD. Susun setiap respons agar mudah ditindaklanjuti:

1. Mulailah dengan jawaban atau langkah selanjutnya: perintah, jalur file, atau cuplikan kode terlebih dahulu.
2. Beri nomor pada pekerjaan yang memiliki beberapa langkah; batasi satu tindakan jelas per langkah.
3. Akhiri dengan satu tindakan selanjutnya yang bisa diselesaikan dalam waktu kurang dari dua menit.
4. Selesaikan masalah saat ini sebelum membahas masalah lain.
5. Tegaskan kembali progres di setiap giliran (misalnya, "langkah 3 dari 5 selesai").
6. Berikan estimasi waktu dalam satuan yang konkret, jangan pernah menggunakan kata seperti "sebentar".
7. Setelah ada perubahan, tunjukkan apa yang sekarang berhasil berfungsi.
8. Error: jelaskan lokasi, penyebab, dan solusinya, tanpa basa-basi.
9. Batasi daftar hanya hingga 5 item.
10. Tanpa pembukaan, ringkasan ulang, atau salam penutup.

Pengecualian: jelaskan secara lengkap jika diminta. Konfirmasi sebelum melakukan tindakan yang bersifat destruktif. Setelah tiga kali percobaan perbaikan yang gagal, berhentilah dan identifikasi asumsi yang meragukan. Jika permintaan ambigu, ajukan satu pertanyaan singkat.
```

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

Gemini CLI tidak memiliki marketplace plugin, jadi ada dua opsi bawaan: perintah kustom (opt-in, nonaktif sampai dipanggil) atau ekstensi (selalu aktif setelah diinstal). Perintah ini sesuai dengan perilaku bawaan skill ini; pilih ini kecuali Anda ingin aturannya berlaku di semua sesi.

### Instalasi (perintah, opt-in)

```bash
mkdir -p ~/.gemini/commands
curl -fsSL https://raw.githubusercontent.com/aixinwudi/i-have-adhd-cn/main/skills/i-have-adhd/agents/gemini.toml \
  -o ~/.gemini/commands/i-have-adhd.toml
```

Mulai sesi baru dan ketik `/i-have-adhd`. Skill ini akan tetap aktif selama sesi tersebut.

### Instalasi (ekstensi, always-on)

```bash
gemini extensions install https://github.com/aixinwudi/i-have-adhd-cn
```

Ekstensi ini memuat `GEMINI.md`, yang mengimpor skill secara lengkap; dengan demikian, aturannya berlaku sejak pesan pertama. Git harus sudah terinstal.

### Verifikasi

```bash
gemini extensions list          # via ekstensi
ls ~/.gemini/commands           # rute perintah: i-have-adhd.toml ada
```

Atau ketik `/` di dalam sesi dan pastikan `i-have-adhd` muncul dalam daftar.

### Pembaruan

```bash
gemini extensions update i-have-adhd    # via ekstensi
# via perintah: jalankan ulang perintah curl di atas
```

### Uninstal

```bash
gemini extensions uninstall i-have-adhd    # via ekstensi
rm ~/.gemini/commands/i-have-adhd.toml     # rute perintah
```

</details>

<details>
<summary><strong>GitHub Copilot (VS Code dan Copilot CLI)</strong></summary>

Copilot membaca Agent Skills secara native: menggunakan file `SKILL.md` yang sama, tanpa konversi. Di dalam proyek, ia memeriksa `.github/skills/`, `.claude/skills/`, dan `.agents/skills/`; secara global, ia memeriksa `~/.copilot/skills/`, `~/.claude/skills/`, dan `~/.agents/skills/`.

### Instalasi

```bash
npx skills add aixinwudi/i-have-adhd-cn -a github-copilot        # proyek ini
npx skills add aixinwudi/i-have-adhd-cn -a github-copilot -g     # semua proyek
```

Tanpa CLI, salin folder skill ke direktori mana pun yang diperiksa oleh Copilot:

```bash
git clone https://github.com/aixinwudi/i-have-adhd-cn i-have-adhd
mkdir -p ~/.copilot/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.copilot/skills/
```

### Verifikasi

Ketik `/` di kolom obrolan dan pastikan `i-have-adhd` muncul. Atau:

```bash
npx skills list
npx skills ls -g    # jika diinstal secara global
```

### Pembaruan

```bash
npx skills update i-have-adhd
```

Atau salin ulang foldernya setelah `git pull`.

### Uninstal

```bash
npx skills remove i-have-adhd
```

Atau hapus folder `i-have-adhd` dari direktori skill tempat ia diinstal.

### Catatan tentang aktivasi

Copilot menghormati `disable-model-invocation`: tidak ada yang diterapkan sampai Anda memanggil skill tersebut, sama seperti di Claude Code (telah diuji pada [#60](https://github.com/aixinwudi/i-have-adhd-cn/pull/60)).

### Selalu Aktif (opsional)

Tambahkan blok di bawah ini ke `.github/copilot-instructions.md` pada proyek Anda (Copilot akan membacanya di setiap obrolan):

```markdown
## Gaya Respons

Pembaca memiliki ADHD. Susun setiap respons agar mudah ditindaklanjuti:

1. Mulailah dengan jawaban atau langkah selanjutnya: perintah, jalur file, atau cuplikan kode terlebih dahulu.
2. Beri nomor pada pekerjaan yang memiliki beberapa langkah; batasi satu tindakan jelas per langkah.
3. Akhiri dengan satu tindakan selanjutnya yang bisa diselesaikan dalam waktu kurang dari dua menit.
4. Selesaikan masalah saat ini sebelum membahas masalah lain.
5. Tegaskan kembali progres di setiap giliran (misalnya, "langkah 3 dari 5 selesai").
6. Berikan estimasi waktu dalam satuan yang konkret, jangan pernah menggunakan kata seperti "sebentar".
7. Setelah ada perubahan, tunjukkan apa yang sekarang berhasil berfungsi.
8. Error: jelaskan lokasi, penyebab, dan solusinya, tanpa basa-basi.
9. Batasi daftar hanya hingga 5 item.
10. Tanpa pembukaan, ringkasan ulang, atau salam penutup.

Pengecualian: jelaskan secara lengkap jika diminta. Konfirmasi sebelum melakukan tindakan yang bersifat destruktif. Setelah tiga kali percobaan perbaikan yang gagal, berhentilah dan identifikasi asumsi yang meragukan. Jika permintaan ambigu, ajukan satu pertanyaan singkat.
```

</details>

<details>
<summary><strong>Hermes</strong></summary>

### Instalasi

```bash
hermes skills install aixinwudi/i-have-adhd-cn/skills/i-have-adhd
```

Ketik `/i-have-adhd`. Skill ini akan diinstal ke `~/.hermes/skills/` dan tersedia sebagai perintah slash saat sesi berikutnya dimulai.

Lebih suka menjelajah dulu? Tambahkan repositori ini sebagai sumber skill (sebagai "tap"), lalu cari dan instal:

```bash
hermes skills tap add aixinwudi/i-have-adhd-cn
hermes skills search adhd
hermes skills install aixinwudi/i-have-adhd-cn/skills/i-have-adhd
```

### Verifikasi

```bash
hermes skills list
```

### Pembaruan

```bash
hermes skills update i-have-adhd
```

### Uninstal

```bash
hermes skills uninstall i-have-adhd
```

Atau hapus juga tap-nya: `hermes skills tap remove aixinwudi/i-have-adhd-cn`.

### Selalu Aktif (opsional)

Tambahkan ke `AGENTS.md` di direktori kerja Anda (Hermes memuatnya per direktori) atau ke `SOUL.md` pada persona Anda untuk semua sesi:

```markdown
## Gaya Respons

Pembaca memiliki ADHD. Susun setiap respons agar mudah ditindaklanjuti:

1. Mulailah dengan jawaban atau langkah selanjutnya: perintah, jalur file, atau cuplikan kode terlebih dahulu.
2. Beri nomor pada pekerjaan yang memiliki beberapa langkah; batasi satu tindakan jelas per langkah.
3. Akhiri dengan satu tindakan selanjutnya yang bisa diselesaikan dalam waktu kurang dari dua menit.
4. Selesaikan masalah saat ini sebelum membahas masalah lain.
5. Tegaskan kembali progres di setiap giliran (misalnya, "langkah 3 dari 5 selesai").
6. Berikan estimasi waktu dalam satuan yang konkret, jangan pernah menggunakan kata seperti "sebentar".
7. Setelah ada perubahan, tunjukkan apa yang sekarang berhasil berfungsi.
8. Error: jelaskan lokasi, penyebab, dan solusinya, tanpa basa-basi.
9. Batasi daftar hanya hingga 5 item.
10. Tanpa pembukaan, ringkasan ulang, atau salam penutup.

Pengecualian: jelaskan secara lengkap jika diminta. Konfirmasi sebelum melakukan tindakan yang bersifat destruktif. Setelah tiga kali percobaan perbaikan yang gagal, berhentilah dan identifikasi asumsi yang meragukan. Jika permintaan ambigu, ajukan satu pertanyaan singkat.
```

</details>

<details>
<summary><strong>Kimi Code CLI</strong></summary>

### Instalasi

Mulai sesi Kimi Code dan:

1. Jalankan `/plugins`.
2. Pilih **Custom**.
3. Tempel `https://github.com/aixinwudi/i-have-adhd-cn` dan tekan Enter.
4. Pilih **Trust and install**.

Gunakan perintah slash `/skill:i-have-adhd` untuk memanggil skill ini secara eksplisit.

### Pembaruan

Di dalam sesi Kimi Code, jalankan `/plugins`, arahkan kursor ke **I Have ADHD**, dan tekan `R`.

### Uninstal

Di dalam sesi Kimi Code, jalankan `/plugins`, arahkan kursor ke **I Have ADHD**, dan tekan `D`.

</details>

<details>
<summary><strong>Pi</strong></summary>

Pi mengimplementasikan standar Agent Skills, sehingga file `SKILL.md` yang sama dimuat langsung tanpa konversi. Cara pemanggilan di Pi sedikit berbeda: skill dipanggil dengan format `/skill:<nama>`.

### Instalasi

```bash
npx skills add aixinwudi/i-have-adhd-cn -a pi -y
```

Lebih suka menggunakan sistem file? Pi menemukan skill di `~/.pi/agent/skills/` dan `~/.agents/skills/` (global), serta di `.pi/skills/` dan `.agents/skills/` (proyek):

```bash
git clone https://github.com/aixinwudi/i-have-adhd-cn i-have-adhd
mkdir -p ~/.pi/agent/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.pi/agent/skills/
```

Aktifkan perintah slash untuk skill di `settings.json` Pi:

```json
{ "enableSkillCommands": true }
```

Mulai sesi baru dan ketik `/skill:i-have-adhd`.

### Verifikasi

```bash
npx skills list
```

Atau ketik `/skill:` di dalam sesi dan pastikan `i-have-adhd` muncul dalam daftar.

### Pembaruan

```bash
npx skills update i-have-adhd
```

Atau salin ulang foldernya setelah `git pull`.

### Uninstal

```bash
npx skills remove i-have-adhd
```

Atau hapus `~/.pi/agent/skills/i-have-adhd`.

### Selalu Aktif (opsional)

Tambahkan ke `AGENTS.md` pada proyek Anda:

```markdown
## Gaya Respons

Pembaca memiliki ADHD. Susun setiap respons agar mudah ditindaklanjuti:

1. Mulailah dengan jawaban atau langkah selanjutnya: perintah, jalur file, atau cuplikan kode terlebih dahulu.
2. Beri nomor pada pekerjaan yang memiliki beberapa langkah; batasi satu tindakan jelas per langkah.
3. Akhiri dengan satu tindakan selanjutnya yang bisa diselesaikan dalam waktu kurang dari dua menit.
4. Selesaikan masalah saat ini sebelum membahas masalah lain.
5. Tegaskan kembali progres di setiap giliran (misalnya, "langkah 3 dari 5 selesai").
6. Berikan estimasi waktu dalam satuan yang konkret, jangan pernah menggunakan kata seperti "sebentar".
7. Setelah ada perubahan, tunjukkan apa yang sekarang berhasil berfungsi.
8. Error: jelaskan lokasi, penyebab, dan solusinya, tanpa basa-basi.
9. Batasi daftar hanya hingga 5 item.
10. Tanpa pembukaan, ringkasan ulang, atau salam penutup.

Pengecualian: jelaskan secara lengkap jika diminta. Konfirmasi sebelum melakukan tindakan yang bersifat destruktif. Setelah tiga kali percobaan perbaikan yang gagal, berhentilah dan identifikasi asumsi yang meragukan. Jika permintaan ambigu, ajukan satu pertanyaan singkat.
```

</details>

<details>
<summary><strong>Qwen Code</strong></summary>

### Instalasi

```bash
qwen extensions install aixinwudi/i-have-adhd-cn
```

Qwen Code menerima format singkat GitHub dan menginstal repositori sebagai ekstensi native. Ekstensi ini akan menemukan skill di dalam `skills/`.

Ketik `/i-have-adhd` untuk memanggil skill ini secara eksplisit. Menginstal ekstensi gak bakal mengubah keluaran sampai skill tersebut dipanggil.

### Verifikasi

```bash
qwen extensions list
```

Selanjutnya, mulai sesi baru Qwen Code dan jalankan:

```text
/skills
```

Pastikan `i-have-adhd` muncul dalam daftar.

### Pembaruan

```bash
qwen extensions update i-have-adhd
```

### Uninstal

```bash
qwen extensions uninstall i-have-adhd
```

</details>

<details>
<summary><strong>Zed</strong></summary>

Zed Agent membaca Agent Skills secara native: menggunakan file `SKILL.md` yang sama, tanpa konversi. ("Rules" lama di Zed telah digantikan oleh Skills dan instruksi di `AGENTS.md`.)

### Instalasi

Di Agent Panel, buka pengelola Skills, pilih **Create skill from URL** (juga tersedia di palet sebagai `agent: create skill from url`) dan tempel:

```
https://github.com/aixinwudi/i-have-adhd-cn/blob/main/skills/i-have-adhd/SKILL.md
```

Simpan dengan cakupan **User** untuk semua proyek, atau **Project** untuk satu proyek tertentu. Setelah itu, ketik `/i-have-adhd` di Agent Panel.

Lebih suka menggunakan sistem file? Klon repositori dan letakkan folder skill di direktori skill pengguna:

```bash
git clone https://github.com/aixinwudi/i-have-adhd-cn i-have-adhd
mkdir -p ~/.agents/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.agents/skills/
```

### Verifikasi

Buka pengelola Skills di Agent Panel dan pastikan `i-have-adhd` muncul. Atau ketik `/` dan periksa.

### Pembaruan

Impor ulang menggunakan URL yang sama (akan menimpa) atau salin ulang foldernya setelah `git pull`.

### Uninstal

Hapus `i-have-adhd` dari pengelola Skills atau hapus folder `~/.agents/skills/i-have-adhd`.

### Selalu Aktif (opsional)

Tambahkan ke file `~/.config/zed/AGENTS.md` pribadi Anda:

```markdown
## Gaya Respons

Pembaca memiliki ADHD. Susun setiap respons agar mudah ditindaklanjuti:

1. Mulailah dengan jawaban atau langkah selanjutnya: perintah, jalur file, atau cuplikan kode terlebih dahulu.
2. Beri nomor pada pekerjaan yang memiliki beberapa langkah; batasi satu tindakan jelas per langkah.
3. Akhiri dengan satu tindakan selanjutnya yang bisa diselesaikan dalam waktu kurang dari dua menit.
4. Selesaikan masalah saat ini sebelum membahas masalah lain.
5. Tegaskan kembali progres di setiap giliran (misalnya, "langkah 3 dari 5 selesai").
6. Berikan estimasi waktu dalam satuan yang konkret, jangan pernah menggunakan kata seperti "sebentar".
7. Setelah ada perubahan, tunjukkan apa yang sekarang berhasil berfungsi.
8. Error: jelaskan lokasi, penyebab, dan solusinya, tanpa basa-basi.
9. Batasi daftar hanya hingga 5 item.
10. Tanpa pembukaan, ringkasan ulang, atau salam penutup.

Pengecualian: jelaskan secara lengkap jika diminta. Konfirmasi sebelum melakukan tindakan yang bersifat destruktif. Setelah tiga kali percobaan perbaikan yang gagal, berhentilah dan identifikasi asumsi yang meragukan. Jika permintaan ambigu, ajukan satu pertanyaan singkat.
```

</details>

<details>
<summary><strong>Cursor, OpenCode, Amp, dan lingkungan lain yang kompatibel dengan agent-skills</strong></summary>

Berfungsi di lingkungan apa pun yang mendukung pembacaan Agent Skills. Ganti `-a <agent>` dengan agen pilihan Anda.

### Instalasi

```bash
npx skills add aixinwudi/i-have-adhd-cn                  # workspace ini
npx skills add aixinwudi/i-have-adhd-cn -g               # semua proyek
npx skills add aixinwudi/i-have-adhd-cn -a cursor -y     # satu agen saja
npx skills add aixinwudi/i-have-adhd-cn -a opencode -y
```

Buka obrolan agen baru dan ketik `/i-have-adhd`.

Tanpa CLI, salin folder skill ke jalur yang diperiksa oleh agen Anda:

```bash
git clone https://github.com/aixinwudi/i-have-adhd-cn i-have-adhd
mkdir -p ~/.cursor/skills     # Cursor. Gunakan .agents/skills di OpenCode atau jalur khusus agen Anda
cp -R i-have-adhd/skills/i-have-adhd ~/.cursor/skills/
```

### Verifikasi

```bash
npx skills list
npx skills ls -g    # jika diinstal secara global
```

### Pembaruan

```bash
npx skills update i-have-adhd
npx skills update -g    # jika diinstal secara global
```

### Uninstal

```bash
npx skills remove i-have-adhd
npx skills remove i-have-adhd -g    # jika diinstal secara global
```

### Selalu Aktif (opsional)

Tempel ini ke file aturan agen yang persisten. Cursor: **Settings → Rules → User Rules**, atau aturan proyek di `.cursor/rules/` dengan `alwaysApply: true`. OpenCode: `~/.config/opencode/AGENTS.md`.

```markdown
## Gaya Respons

Pembaca memiliki ADHD. Susun setiap respons agar mudah ditindaklanjuti:

1. Mulailah dengan jawaban atau langkah selanjutnya: perintah, jalur file, atau cuplikan kode terlebih dahulu.
2. Beri nomor pada pekerjaan yang memiliki beberapa langkah; batasi satu tindakan jelas per langkah.
3. Akhiri dengan satu tindakan selanjutnya yang bisa diselesaikan dalam waktu kurang dari dua menit.
4. Selesaikan masalah saat ini sebelum membahas masalah lain.
5. Tegaskan kembali progres di setiap giliran (misalnya, "langkah 3 dari 5 selesai").
6. Berikan estimasi waktu dalam satuan yang konkret, jangan pernah menggunakan kata seperti "sebentar".
7. Setelah ada perubahan, tunjukkan apa yang sekarang berhasil berfungsi.
8. Error: jelaskan lokasi, penyebab, dan solusinya, tanpa basa-basi.
9. Batasi daftar hanya hingga 5 item.
10. Tanpa pembukaan, ringkasan ulang, atau salam penutup.

Pengecualian: jelaskan secara lengkap jika diminta. Konfirmasi sebelum melakukan tindakan yang bersifat destruktif. Setelah tiga kali percobaan perbaikan yang gagal, berhentilah dan identifikasi asumsi yang meragukan. Jika permintaan ambigu, ajukan satu pertanyaan singkat.
```
</details>


## Cara Kerja Aktivasi

1. **Terinstal, tetapi tidak dipanggil.** Di Claude Code, Qwen Code, dan Codex, tidak ada yang terjadi sampai Anda memanggil skill ini secara eksplisit. Claude Code dan Qwen Code menghormati `disable-model-invocation: true` di `SKILL.md`; Codex menghormati `policy.allow_implicit_invocation: false` di `agents/openai.yaml`. Lingkungan lain mungkin memuat deskripsi setiap skill saat startup dan mengaktifkannya sendiri.
2. **Anda memanggilnya secara eksplisit.** Ketik `/i-have-adhd` di Claude Code atau Qwen Code, atau `$i-have-adhd` di Codex. Aturan ini bakalan aktif di sesi tersebut. Perintah "stop adhd mode" atau "normal mode" bakal menonaktifkannya.
3. **Anda membuat `~/.claude/.i-have-adhd-always`** (Claude Code). Hook `SessionStart` bakalan memuat (load) semua aturan sejak pesan pertama, di setiap sesi.
4. **Anda menambahkan cuplikan "selalu aktif" di atas** (lingkungan lain). Ini akan menjaga aturan utama tetap berada dalam konteks agen yang persisten.

Di Claude Code, Qwen Code, dan Codex gak ada jalan tengah: jikalau Anda tidak mengaktifkannya, maka skill ini nonaktif.

## Pemecahan Masalah (Troubleshooting)

**`/i-have-adhd` tidak muncul di pelengkapan otomatis (autocomplete).** Mulai ulang agen Anda. Indeks plugin dibaca saat startup.

**Flag selalu aktif tidak berfungsi.** Perbarui plugin (`claude plugin marketplace update i-have-adhd`) dan mulai ulang. Hook dibaca saat startup, dan flag ini memerlukan versi yang menyertakan `hooks/hooks.json`.

**`claude plugin marketplace add` gagal.** Gunakan format `owner/repo`. Jalur lokal harus mengarah ke root repositori, bukan ke `.claude-plugin/`.

**Sudah diinstal, tetapi respons masih memiliki pembukaan (preambulo).** Buka sesi baru. Jika masih terus menyimpang, pertegas teks di `skills/i-have-adhd/SKILL.md`.

**Ingin peraturan yang berbeda?.** Lakukan fork skill ini, edit `skills/i-have-adhd/SKILL.md` sesuai keinginan, lalu ganti dengan salinan Anda sendiri:

```bash
claude plugin uninstall i-have-adhd            # hapus dulu salinan upstream:
claude plugin marketplace remove i-have-adhd   # fork dan upstream menggunakan nama yang sama
claude plugin marketplace add <username-anda>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Mulai ulang dan panggillah `/i-have-adhd` lagi.

**Skill tidak muncul setelah `npx skills add`.** Buka obrolan agen baru. Skill diindeks di awal sesi. Pastikan folder telah diinstal di lokasi yang dicari oleh agen (`~/.cursor/skills/` di Cursor, `.agents/skills/` di OpenCode) dan bahwa `name` di frontmatter sesuai dengan nama folder.