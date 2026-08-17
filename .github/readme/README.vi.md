<p align="center">
  <img src="../../logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">Đầu ra thân thiện với người có ADHD. Không cần chẩn đoán ADHD!</strong>
</p>
<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/github/license/ayghri/i-have-adhd?style=flat" alt="Giấy phép"></a>
</p>

<p align="center">
  <a href="../../README.md" title="English" aria-label="English">🇬🇧</a> ·
  <a href="README.zh-CN.md" title="简体中文" aria-label="简体中文">🇨🇳</a> ·
  <a href="README.pt-BR.md" title="Português (Brasil)" aria-label="Português (Brasil)">🇧🇷</a> ·
  <a href="README.ja.md" title="日本語" aria-label="日本語">🇯🇵</a> ·
  <strong title="Tiếng Việt" aria-label="Tiếng Việt">🇻🇳</strong> ·
  <a href="README.ko.md" title="한국어" aria-label="한국어">🇰🇷</a>
</p>


## Cài đặt

🔗 [Hướng dẫn cài đặt](../install/INSTALL.vi.md)

## Skill này làm gì

Một skill dành cho trợ lý lập trình, giúp câu trả lời đi thẳng vào trọng tâm thay vì bị chôn vùi trong những đoạn văn dài. Hành động trước. Đánh số các bước. Không có câu “Hy vọng điều này hữu ích!”


## Những gì thay đổi


<table>
<tr>
<td width="50%">

## Trước khi dùng

> Câu hỏi rất hay! Để tôi suy nghĩ về điều này. Luồng xác thực của bạn gồm vài thành phần liên quan: middleware, việc xác minh token và xử lý cookie. Nhìn vào `src/auth.ts`, hàm `verifyToken` (khoảng dòng 42-58) có vẻ đang dùng API `jsonwebtoken` cũ hơn. Một cách tiếp cận là cập nhật package và viết lại hàm đó. Sau khi thay đổi, bạn sẽ muốn chạy các bài kiểm thử phần xác thực để xác nhận không có gì bị hỏng. Nhân tiện, bạn cũng có thể muốn xem xét tổng thể phiên bản các dependency. Hy vọng điều này hữu ích! Cho tôi biết nếu bạn muốn đi sâu hơn.

</td>

<td width="50%">

## Sau khi dùng

> Chạy `npm install jsonwebtoken@latest`, sau đó sửa `src/auth.ts:42`.
>
> 1. Mở `src/auth.ts`
> 2. Thay thế `verifyToken` (dòng 42–58) bằng đoạn mã bên dưới
> 3. Chạy `npm test -- auth.spec.ts`
>
> Bước tiếp theo: dán dòng báo lỗi đầu tiên nếu có bài kiểm tra nào thất bại.

</td>
</tr>
</table>


## Các quy tắc

10 quy tắc. Nội dung chi tiết tại [SKILL.md](../../skills/i-have-adhd/SKILL.md).

1. Bắt đầu ngay bằng hành động tiếp theo.
2. Đánh số các công việc gồm nhiều bước.
3. Kết thúc bằng một bước tiếp theo cụ thể.
4. Loại bỏ các nội dung lan man.
5. Nhắc lại trạng thái hiện tại ở mỗi lượt.
6. Ước tính thời gian cụ thể (tính bằng phút, không nói chung chung).
7. Làm nổi bật những kết quả đã đạt được.
8. Báo lỗi một cách khách quan, thẳng thắn.
9. Giới hạn danh sách tối đa 5 mục.
10. Không lời mở đầu. Không tóm tắt. Không lời chào kết.

## Tùy chỉnh

Fork repo, chỉnh sửa `skills/i-have-adhd/SKILL.md`, sau đó chuyển sang dùng bản của bạn:

```bash
claude plugin uninstall i-have-adhd            # gỡ bản chính trước:
claude plugin marketplace remove i-have-adhd   # bản fork và bản chính dùng chung tên
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Khởi động lại Claude Code, sau đó gọi lại `/i-have-adhd`.

## Ghi nhận tác giả (Credits)

Lấy cảm hứng một phần từ cuốn *The Adult ADHD Tool Kit* của J. Russell Ramsay và Anthony L. Rostain. Được điều chỉnh cho cách một LLM nên phản hồi, chứ không phải cách con người nên tổ chức một ngày của mình.

## Giấy phép

MIT.

Hãy ⭐ repo nếu nó giúp bạn khỏi phải cuộn qua thêm một câu “Câu hỏi rất hay!”
