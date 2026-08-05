<p align="center">
  <a href="https://github.com/ayghri/i-have-adhd"> <img src="/logo.png" alt="i-have-adhd" width="140" /></a>
</p>
<p align="center">
  <strong align="center">ตอบได้ใจความไม่ยืดเยื้อ จะสมาธิสั้นหรือไม่ก็เข้าใจได้!</strong>
</p>
<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/ayghri/i-have-adhd?style=flat" alt="License"></a>
</p>

<p align="center">
  <a href="/README.md">English</a> ·
  <a href=".github/readme/README.zh-CN.md">简体中文</a> ·
  <a href=".github/readme/README.ja.md">日本語</a> ·
  <a href=".github/readme/README.ko.md">한국어</a> ·
  <a href=".github/readme/README.vi.md">Tiếng Việt</a> ·
  <a href=".github/readme/README.pt-BR.md">Português (BR)</a> ·
  <strong>ภาษาไทย</strong> 
</p>


## การติดตั้ง

<details>
<summary><strong>Claude Code</strong></summary>

```bash
claude plugin marketplace add ayghri/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

จากนั้นพิมพ์ `/i-have-adhd` โดยไม่ต้องโคลนโปรเจกต์มาไว้ในเครื่อง เพราะ Claude Code จะคอยโหลดโปรเจกต์นี้และอัปเดตอยู่ตลอด

ต้องการเปิดใช้งานให้ทุกเซลซั่นงั้นหรอ? ใช้คำสั่ง `touch ~/.claude/.i-have-adhd-always` ดูสิ (ดูเพิ่มเติมได้ใน [INSTALL.md](./INSTALL.md)).

</details>

<details>
<summary><strong>Codex</strong></summary>

```bash
codex plugin marketplace add ayghri/i-have-adhd --ref main
codex plugin add i-have-adhd@i-have-adhd
```

จากนั้นพิมพ์ `$i-have-adhd` เพื่อเปิดใช้รูปแบบคำตอบนี้ นอกจากนี้ Skill จะถูกเรียกใช้งานอัตโนมัติ เมื่อ Codex ตรวจพบว่างานนั้นเหมาะสมกับรูปแบบนี้

</details>

ส่วนคำแนะนำการติดตั้งใน coding agents อื่น ๆ สามารถดูได้ใน [INSTALL.md](./INSTALL.md).

## มันทำอะไรได้บ้าง

เป็น Skill ให้สำหรับผู้ช่วยเขียนโค้ดของคุณ ซึ่งช่วยไม่ให้คำตอบสำคัญ ๆ ถูกพล่ามหายไปในข้อความยาว ๆ โดยจะแสดงสิ่งที่ต้องทำก่อน มีขั้นตอนและเลขกำกับ และไม่มีประโยคอย่าง "หวังว่าจะช่วยได้นะ!"


## มันเปลี่ยนยังไงบ้าง


<table>
<tr>
<td width="50%">

## ก่อนใช้

> เป็นคำถามที่ดีมาก! ขอผมคิดดูก่อนนะ ขั้นตอนการยืนยันตัวตนของคุณมีองค์ประกอบอยู่หลายส่วน ได้แก่ Middleware การตรวจสอบ Token และการจัดการ Cookie จากที่ดูไฟล์ `src/auth.ts` ฟังก์ชัน `verifyToken` (บริเวณบรรทัด 42–58) ดูเหมือนว่าจะใช้ API รุ่นเก่าของ `jsonwebtoken` วิธีหนึ่งคืออัปเดตแพ็กเกจและเขียนฟังก์ชันนั้นใหม่ หลังจากแก้ไขแล้ว คุณควรรันการทดสอบระบบยืนยันตัวตนเพื่อให้แน่ใจว่าไม่มีอะไรเสีย นอกจากนี้คุณอาจลองตรวจสอบเวอร์ชันของ Dependency ตัวอื่นด้วย หวังว่าจะช่วยได้นะ! บอกได้เลยถ้าต้องการให้ช่วยดูเพิ่มเติม

</td>

<td width="50%">

## หลังใช้

> รัน `npm install jsonwebtoken@latest` แล้วแก้ไขไฟล์ `src/auth.ts:42`.
>
> 1. เปิดไฟล์ `src/auth.ts`
> 2. แทนที่ฟังก์ชัน `verifyToken` (บรรทัดที่ 42–58) ด้วยโค้ดด้านล่าง
> 3. รัน `npm test -- auth.spec.ts`
>
> ถัดไป: หากทดสอบไม่ผ่าน ให้นำบรรทัดแรกที่เกิดข้อผิดพลาดมาวาง

</td>
</tr>
</table>


## กฎการตอบ

มีทั้งหมด 10 ข้อ อ่านฉบับเต็มได้ใน [SKILL.md](./skills/i-have-adhd/SKILL.md).

1. เริ่มต้นด้วยสิ่งที่ทำถัดไป
2. ใช้หมายเลขกำกับในกรณีที่งานมีหลายขั้นตอน
3. จบด้วยขั้นตอนถัดไปที่ชัดเจนหนึ่งอย่าง
4. ตัดเนื้อหานอกประเด็นออก
5. ทบทวนสถานะปัจจุบันในทุก ๆ ข้อความ
6. ต้องระบุเวลาอย่างชัดเจน (ระบุเป็นจำนวนนาที ไม่ใช่แค่คำว่า "สักพักนะ")
7. ทำให้ความสำเร็จและความคืบหน้าชัดเจน
8. อธิบายข้อผิดพลาดอย่างตรงไปตรงมา
9. จำกัดรายการไม่เกิน 5 ข้อ
10. ไม่มีคำนำ ไม่ต้องสรปซ้ำ และไม่มีคำลงท้ายที่ไม่จำเป็น

## ปรับแต่งเพิ่มเติม

Fork โปรเจกต์นี้ และแก้ไขไฟล์ `skills/i-have-adhd/SKILL.md` จากนั้นเปลี่ยนไปใช้เวอร์ชันของคุณด้วยคำสั่งต่อไปนี้:

```bash
claude plugin uninstall i-have-adhd            # drop the upstream copy first:
claude plugin marketplace remove i-have-adhd   # fork and upstream share both names
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

รีสตาร์ต Claude Code จากนั้นเรียกใช้ `/i-have-adhd` อีกครั้ง

## เครดิต

สร้างขึ้นโดยอ้างอิงแนวคิดบางส่วนจากหนังสือ *The Adult ADHD Tool Kit* โดย J. Russell Ramsay และ Anthony L. Rostain และนำมาปรับแต่งให้เหมาะสมที่ LLM ควรตอบ ไม่ใช่นำมาเป็นคู่มือมนุษย์ช่วยจัดการแทนชีวิตประจำวัน 

## License

MIT.

กดดาว ⭐ ให้ด้วย หากมันช่วยให้คุณไม่ต้องเลื่อนผ่านแล้วเจอคำว่า "เป็นคำถามที่ดีมาก!"
