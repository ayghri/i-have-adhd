# Cách cài đặt

<details>
<summary><strong>Antigravity (<code>agy</code>)</strong></summary>

### Cài đặt

```bash
agy plugin install https://github.com/ayghri/i-have-adhd
```

### Xác minh

```bash
agy plugin list
```

### Cập nhật

```bash
agy plugin uninstall i-have-adhd
agy plugin install https://github.com/ayghri/i-have-adhd
```

### Gỡ cài đặt

```bash
agy plugin uninstall i-have-adhd
```

Hoặc giữ nguyên cài đặt và tắt bằng `agy plugin disable i-have-adhd`.

### Luôn bật (không bắt buộc)

Thêm vào `~/.gemini/GEMINI.md`:

```markdown
## Phong cách đầu ra

Người đọc có ADHD. Hãy định dạng mọi phản hồi để họ có thể hành động ngay:

1. Bắt đầu bằng câu trả lời hoặc hành động tiếp theo: ưu tiên lệnh, đường dẫn hoặc đoạn mã.
2. Đánh số công việc nhiều bước; mỗi bước chỉ có một hành động rõ ràng.
3. Kết thúc bằng một hành động tiếp theo có thể làm trong chưa đến hai phút.
4. Hoàn tất vấn đề hiện tại trước khi nêu vấn đề mới.
5. Nhắc lại tiến độ ở mỗi lượt ("đã xong bước 3/5").
6. Ước tính thời gian bằng đơn vị cụ thể, không nói "một chút".
7. Sau khi thay đổi, hãy cho biết điều gì hiện đã hoạt động.
8. Với lỗi, nêu vị trí, nguyên nhân và cách sửa một cách khách quan.
9. Giới hạn danh sách ở 5 mục.
10. Không mở đầu, không tóm tắt lại, không lời kết.

Ngoại lệ: giải thích đầy đủ khi được yêu cầu. Xác nhận trước thao tác phá hủy dữ liệu. Sau ba lần sửa thất bại, dừng lại và nêu giả định đáng ngờ. Nếu yêu cầu mơ hồ, hãy hỏi một câu ngắn.
```

</details>

<details>
<summary><strong>Claude Code</strong></summary>

### Cài đặt

```bash
claude plugin marketplace add ayghri/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Gõ `/i-have-adhd`.

### Xác minh

```bash
claude plugin list
```

### Cập nhật

```bash
claude plugin marketplace update i-have-adhd
```

### Gỡ cài đặt

```bash
claude plugin uninstall i-have-adhd
claude plugin marketplace remove i-have-adhd
```

Hoặc giữ nguyên cài đặt và tắt bằng `claude plugin disable i-have-adhd`.

### Luôn bật (không bắt buộc)

Hook `SessionStart` tải toàn bộ bộ quy tắc khi bắt đầu mỗi phiên, không cần `/i-have-adhd`:

```bash
touch ~/.claude/.i-have-adhd-always
```

Để trở lại chế độ bật khi cần:

```bash
rm ~/.claude/.i-have-adhd-always
```

Hook chỉ chạy khi tệp cờ tồn tại, vì vậy chỉ cài plugin sẽ không tự thay đổi gì. Hook tôn trọng `$CLAUDE_CONFIG_DIR` nếu bạn đã chuyển thư mục cấu hình. "stop adhd mode" vẫn tắt chế độ này cho phiên hiện tại.

</details>


<details>
<summary><strong>Codex</strong></summary>

### Cài đặt

```bash
codex plugin marketplace add ayghri/i-have-adhd --ref main
codex plugin add i-have-adhd@i-have-adhd
```

Gọi skill một cách rõ ràng bằng cách gõ `$i-have-adhd`. Codex sẽ không tự động kích hoạt skill.

### Xác minh

```bash
codex plugin list
```

### Cập nhật

```bash
codex plugin marketplace upgrade i-have-adhd
codex plugin remove i-have-adhd
codex plugin add i-have-adhd@i-have-adhd
```

### Gỡ cài đặt

```bash
codex plugin remove i-have-adhd
codex plugin marketplace remove i-have-adhd
```

### Luôn bật (không bắt buộc)

Thêm vào `~/.codex/AGENTS.md`:

```markdown
## Phong cách đầu ra

Người đọc có ADHD. Hãy định dạng mọi phản hồi để họ có thể hành động ngay:

1. Bắt đầu bằng câu trả lời hoặc hành động tiếp theo: ưu tiên lệnh, đường dẫn hoặc đoạn mã.
2. Đánh số công việc nhiều bước; mỗi bước chỉ có một hành động rõ ràng.
3. Kết thúc bằng một hành động tiếp theo có thể làm trong chưa đến hai phút.
4. Hoàn tất vấn đề hiện tại trước khi nêu vấn đề mới.
5. Nhắc lại tiến độ ở mỗi lượt ("đã xong bước 3/5").
6. Ước tính thời gian bằng đơn vị cụ thể, không nói "một chút".
7. Sau khi thay đổi, hãy cho biết điều gì hiện đã hoạt động.
8. Với lỗi, nêu vị trí, nguyên nhân và cách sửa một cách khách quan.
9. Giới hạn danh sách ở 5 mục.
10. Không mở đầu, không tóm tắt lại, không lời kết.

Ngoại lệ: giải thích đầy đủ khi được yêu cầu. Xác nhận trước thao tác phá hủy dữ liệu. Sau ba lần sửa thất bại, dừng lại và nêu giả định đáng ngờ. Nếu yêu cầu mơ hồ, hãy hỏi một câu ngắn.
```

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

Gemini CLI không có chợ plugin nên có hai cách tích hợp sẵn: **lệnh tùy chỉnh** (chỉ bật khi gọi) hoặc **extension** (luôn bật sau khi cài). Cách dùng lệnh phù hợp với hành vi mặc định của skill; hãy chọn cách này trừ khi bạn muốn áp dụng quy tắc cho mọi phiên.

### Cài đặt (command, opt-in)

```bash
mkdir -p ~/.gemini/commands
curl -fsSL https://raw.githubusercontent.com/ayghri/i-have-adhd/main/skills/i-have-adhd/agents/gemini.toml \
  -o ~/.gemini/commands/i-have-adhd.toml
```

Bắt đầu phiên mới và gõ `/i-have-adhd`. Skill sẽ bật trong suốt phiên đó.

### Cài đặt (extension, always-on)

```bash
gemini extensions install https://github.com/ayghri/i-have-adhd
```

Extension tải `GEMINI.md`, tệp nhập toàn bộ skill, nên quy tắc được áp dụng từ tin nhắn đầu tiên. Máy phải cài `git`.

### Xác minh

```bash
gemini extensions list          # cách dùng extension
ls ~/.gemini/commands           # command route: i-have-adhd.toml present
```

Hoặc gõ `/` trong một phiên và xác nhận `i-have-adhd` có trong danh sách.

### Cập nhật

```bash
gemini extensions update i-have-adhd    # cách dùng extension
# cách dùng lệnh: chạy lại curl ở trên
```

### Gỡ cài đặt

```bash
gemini extensions uninstall i-have-adhd    # cách dùng extension
rm ~/.gemini/commands/i-have-adhd.toml     # command route
```

</details>

<details>
<summary><strong>GitHub Copilot (VS Code and Copilot CLI)</strong></summary>

Copilot đọc Agent Skills trực tiếp: cùng một `SKILL.md`, không cần chuyển đổi. Trong dự án, Copilot quét `.github/skills/`, `.claude/skills/`, `.agents/skills/`; trên toàn hệ thống, nó quét `~/.copilot/skills/`, `~/.claude/skills/`, `~/.agents/skills/`.

### Cài đặt

```bash
npx skills add ayghri/i-have-adhd -a github-copilot        # dự án này
npx skills add ayghri/i-have-adhd -a github-copilot -g     # mọi dự án
```

Nếu không dùng CLI, hãy sao chép thư mục skill vào bất kỳ thư mục nào Copilot quét:

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.copilot/skills
cp -R i-have-adhd/skills/i-have-adhd ~/.copilot/skills/
```

### Xác minh

Gõ `/` trong ô chat và xác nhận `i-have-adhd` xuất hiện. Hoặc:

```bash
npx skills list
npx skills ls -g    # nếu đã cài toàn cục
```

### Cập nhật

```bash
npx skills update i-have-adhd
```

Hoặc sao chép lại thư mục sau `git pull`.

### Gỡ cài đặt

```bash
npx skills remove i-have-adhd
```

Hoặc xóa thư mục `i-have-adhd` khỏi thư mục skills nơi nó được cài.

### Lưu ý về kích hoạt

Copilot tuân theo `disable-model-invocation`: không có gì được áp dụng cho đến khi bạn gọi skill, giống Claude Code (đã kiểm thử trong [#60](https://github.com/ayghri/i-have-adhd/pull/60)).

### Luôn bật (không bắt buộc)

Thêm khối dưới đây vào `.github/copilot-instructions.md` của dự án (Copilot đọc nó trong mọi cuộc chat):

```markdown
## Phong cách đầu ra

Người đọc có ADHD. Hãy định dạng mọi phản hồi để họ có thể hành động ngay:

1. Bắt đầu bằng câu trả lời hoặc hành động tiếp theo: ưu tiên lệnh, đường dẫn hoặc đoạn mã.
2. Đánh số công việc nhiều bước; mỗi bước chỉ có một hành động rõ ràng.
3. Kết thúc bằng một hành động tiếp theo có thể làm trong chưa đến hai phút.
4. Hoàn tất vấn đề hiện tại trước khi nêu vấn đề mới.
5. Nhắc lại tiến độ ở mỗi lượt ("đã xong bước 3/5").
6. Ước tính thời gian bằng đơn vị cụ thể, không nói "một chút".
7. Sau khi thay đổi, hãy cho biết điều gì hiện đã hoạt động.
8. Với lỗi, nêu vị trí, nguyên nhân và cách sửa một cách khách quan.
9. Giới hạn danh sách ở 5 mục.
10. Không mở đầu, không tóm tắt lại, không lời kết.

Ngoại lệ: giải thích đầy đủ khi được yêu cầu. Xác nhận trước thao tác phá hủy dữ liệu. Sau ba lần sửa thất bại, dừng lại và nêu giả định đáng ngờ. Nếu yêu cầu mơ hồ, hãy hỏi một câu ngắn.
```

</details>

<details>
<summary><strong>Hermes</strong></summary>

### Cài đặt

```bash
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd
```

Gõ `/i-have-adhd`. The skill installs into `~/.hermes/skills/` and is exposed as a slash command at the next session start.

Muốn xem trước? Thêm repo này làm nguồn skill (một "tap"), rồi tìm kiếm và cài đặt:

```bash
hermes skills tap add ayghri/i-have-adhd
hermes skills search adhd
hermes skills install ayghri/i-have-adhd/skills/i-have-adhd
```

### Xác minh

```bash
hermes skills list
```

### Cập nhật

```bash
hermes skills update i-have-adhd
```

### Gỡ cài đặt

```bash
hermes skills uninstall i-have-adhd
```

Hoặc xóa cả tap bằng `hermes skills tap remove ayghri/i-have-adhd`.

### Luôn bật (không bắt buộc)

Thêm vào `AGENTS.md` trong thư mục làm việc (Hermes tải theo từng thư mục), hoặc vào `SOUL.md` của persona để dùng cho mọi phiên:

```markdown
## Phong cách đầu ra

Người đọc có ADHD. Hãy định dạng mọi phản hồi để họ có thể hành động ngay:

1. Bắt đầu bằng câu trả lời hoặc hành động tiếp theo: ưu tiên lệnh, đường dẫn hoặc đoạn mã.
2. Đánh số công việc nhiều bước; mỗi bước chỉ có một hành động rõ ràng.
3. Kết thúc bằng một hành động tiếp theo có thể làm trong chưa đến hai phút.
4. Hoàn tất vấn đề hiện tại trước khi nêu vấn đề mới.
5. Nhắc lại tiến độ ở mỗi lượt ("đã xong bước 3/5").
6. Ước tính thời gian bằng đơn vị cụ thể, không nói "một chút".
7. Sau khi thay đổi, hãy cho biết điều gì hiện đã hoạt động.
8. Với lỗi, nêu vị trí, nguyên nhân và cách sửa một cách khách quan.
9. Giới hạn danh sách ở 5 mục.
10. Không mở đầu, không tóm tắt lại, không lời kết.

Ngoại lệ: giải thích đầy đủ khi được yêu cầu. Xác nhận trước thao tác phá hủy dữ liệu. Sau ba lần sửa thất bại, dừng lại và nêu giả định đáng ngờ. Nếu yêu cầu mơ hồ, hãy hỏi một câu ngắn.
```

</details>

<details>
<summary><strong>Kimi Code CLI</strong></summary>

### Cài đặt

Hãy bắt đầu một phiên Kimi Code, rồi:

1. Chạy `/plugins`.
2. Chọn **Custom**.
3. Dán `https://github.com/ayghri/i-have-adhd` rồi nhấn Enter.
4. Chọn **Trust and install**.

Dùng lệnh slash `/skill:i-have-adhd` để gọi skill một cách rõ ràng.

### Cập nhật

Trong phiên Kimi Code, chạy `/plugins`, đưa con trỏ đến **I Have ADHD**, rồi nhấn `R`.

### Gỡ cài đặt

Trong phiên Kimi Code, chạy `/plugins`, đưa con trỏ đến **I Have ADHD**, rồi nhấn `D`.

</details>


<details>
<summary><strong>Pi</strong></summary>

Pi nhận diện repository này như một gói gốc: `extensions/` cung cấp chế độ tồn tại xuyên phiên, còn `skills/` vẫn giữ điểm vào Agent Skills.

### Cài đặt

```bash
pi install https://github.com/ayghri/i-have-adhd
```

Bắt đầu phiên Pi mới. Bật/tắt đầu ra thân thiện với ADHD cho phiên hiện tại:

```text
/i-have-adhd
```

Thanh chân trang hiển thị `● ADHD ON` khi chế độ đang bật. Chạy lại lệnh để tắt, hoặc chỉ định rõ:

```text
/i-have-adhd on
/i-have-adhd off
stop adhd mode
```

Giống như hook của Claude Code, tiện ích này thêm bộ quy tắc vào cuộc hội thoại một lần thay vì viết lại system prompt ở mỗi yêu cầu, và thêm lại sau khi việc nén (compaction) làm mất nó.

Lệnh Agent Skills hiện có vẫn dùng được như một bí danh:

```text
/skill:i-have-adhd
```

Bắt đầu phiên Pi mới với chế độ bật theo mặc định:

```bash
pi --adhd
```

### Xác minh

```bash
pi list
```

Xác nhận gói GitHub có trong danh sách, sau đó gõ `/i-have-adhd` và kiểm tra `● ADHD ON` xuất hiện ở thanh chân trang.

### Cập nhật

```bash
pi update https://github.com/ayghri/i-have-adhd
```

Hoặc cập nhật mọi gói Pi chưa ghim phiên bản bằng `pi update --extensions`.

### Gỡ cài đặt

```bash
pi remove https://github.com/ayghri/i-have-adhd
```

### Luôn bật (không bắt buộc)

Tạo một tệp cờ trong thư mục cấu hình agent của Pi:

```bash
touch ~/.pi/agent/.i-have-adhd-always
```

Tiện ích kiểm tra tệp cờ này ở mọi phiên mới, tiếp tục, phân nhánh hoặc tải lại. Lựa chọn đã lưu cho phiên hiện tại được ưu tiên hơn giá trị mặc định này, nên "stop adhd mode" vẫn giữ phiên đó ở trạng thái tắt.

Để trở lại chế độ bật khi cần:

```bash
rm ~/.pi/agent/.i-have-adhd-always
```

Nếu đã đặt `PI_CODING_AGENT_DIR`, hãy đặt `.i-have-adhd-always` trong thư mục đó thay thế. Chạy `/reload` hoặc bắt đầu phiên mới sau khi thay đổi tệp cờ.

</details>


<details>
<summary><strong>Qwen Code</strong></summary>

### Cài đặt

```bash
qwen extensions install ayghri/i-have-adhd
```

Qwen Code hỗ trợ dạng viết tắt GitHub và cài kho lưu trữ này dưới dạng extension gốc. Extension sẽ phát hiện skill trong `skills/`.

Gõ `/i-have-adhd` để gọi skill một cách rõ ràng. Chỉ cài extension sẽ không thay đổi đầu ra cho đến khi skill được gọi.

### Xác minh

```bash
qwen extensions list
```

Sau đó, bắt đầu một phiên Qwen Code mới và chạy:

```text
/skills
```

Xác nhận `i-have-adhd` xuất hiện trong danh sách.

### Cập nhật

```bash
qwen extensions update i-have-adhd
```

### Gỡ cài đặt

```bash
qwen extensions uninstall i-have-adhd
```

</details>

<details>
<summary><strong>Zed</strong></summary>

Agent của Zed đọc Agent Skills trực tiếp: cùng một `SKILL.md`, không cần chuyển đổi. ("Rules" cũ của Zed đã được thay bằng Skills cùng hướng dẫn trong `AGENTS.md`.)

### Cài đặt

Trong Agent Panel, mở trình quản lý Skills, chọn **Create skill from URL** (cũng có trong bảng lệnh dưới tên `agent: create skill from url`), rồi dán:

```
https://github.com/ayghri/i-have-adhd/blob/main/skills/i-have-adhd/SKILL.md
```

Lưu ở phạm vi **User** cho mọi dự án hoặc **Project** cho một dự án. Sau đó gõ `/i-have-adhd` trong Agent Panel.

Muốn dùng hệ thống tệp? Clone repo và đặt thư mục skill vào thư mục skills của người dùng:

```bash
git clone https://github.com/ayghri/i-have-adhd
cp -R i-have-adhd/skills/i-have-adhd ~/.config/zed/skills/
```

### Xác minh

Mở trình quản lý Skills trong Agent Panel và xác nhận `i-have-adhd` có trong danh sách. Hoặc gõ `/` và xác nhận nó xuất hiện.

### Cập nhật

Nhập lại từ cùng URL (ghi đè), hoặc sao chép lại thư mục sau `git pull`.

### Gỡ cài đặt

Xóa `i-have-adhd` khỏi trình quản lý Skills, hoặc xóa `~/.config/zed/skills/i-have-adhd`.

### Luôn bật (không bắt buộc)

Thêm vào `~/.config/zed/AGENTS.md` cá nhân:

```markdown
## Phong cách đầu ra

Người đọc có ADHD. Hãy định dạng mọi phản hồi để họ có thể hành động ngay:

1. Bắt đầu bằng câu trả lời hoặc hành động tiếp theo: ưu tiên lệnh, đường dẫn hoặc đoạn mã.
2. Đánh số công việc nhiều bước; mỗi bước chỉ có một hành động rõ ràng.
3. Kết thúc bằng một hành động tiếp theo có thể làm trong chưa đến hai phút.
4. Hoàn tất vấn đề hiện tại trước khi nêu vấn đề mới.
5. Nhắc lại tiến độ ở mỗi lượt ("đã xong bước 3/5").
6. Ước tính thời gian bằng đơn vị cụ thể, không nói "một chút".
7. Sau khi thay đổi, hãy cho biết điều gì hiện đã hoạt động.
8. Với lỗi, nêu vị trí, nguyên nhân và cách sửa một cách khách quan.
9. Giới hạn danh sách ở 5 mục.
10. Không mở đầu, không tóm tắt lại, không lời kết.

Ngoại lệ: giải thích đầy đủ khi được yêu cầu. Xác nhận trước thao tác phá hủy dữ liệu. Sau ba lần sửa thất bại, dừng lại và nêu giả định đáng ngờ. Nếu yêu cầu mơ hồ, hãy hỏi một câu ngắn.
```

</details>

<details>
<summary><strong>Cursor, OpenCode, Amp và mọi môi trường agent-skills khác</strong></summary>

Hoạt động với mọi môi trường đọc Agent Skills. Thay `-a <agent>` bằng agent của bạn.

### Cài đặt

```bash
npx skills add ayghri/i-have-adhd                  # this workspace
npx skills add ayghri/i-have-adhd -g               # mọi dự án
npx skills add ayghri/i-have-adhd -a cursor -y     # one agent only
npx skills add ayghri/i-have-adhd -a opencode -y
```

Mở cuộc chat agent mới và gõ `/i-have-adhd`.

Nếu không dùng CLI, sao chép thư mục skill vào đường dẫn mà agent quét:

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.cursor/skills     # Cursor. Dùng .agents/skills cho OpenCode hoặc đường dẫn riêng của agent
cp -R i-have-adhd/skills/i-have-adhd ~/.cursor/skills/
```

### Xác minh

```bash
npx skills list
npx skills ls -g    # nếu đã cài toàn cục
```

### Cập nhật

```bash
npx skills update i-have-adhd
npx skills update -g    # nếu đã cài toàn cục
```

### Gỡ cài đặt

```bash
npx skills remove i-have-adhd
npx skills remove i-have-adhd -g    # nếu đã cài toàn cục
```

### Luôn bật (không bắt buộc)

Dán nội dung này vào tệp quy tắc lâu dài của agent. Cursor: **Settings → Rules → User Rules**, hoặc quy tắc dự án trong `.cursor/rules/` với `alwaysApply: true`. OpenCode: `~/.config/opencode/AGENTS.md`.

```markdown
## Phong cách đầu ra

Người đọc có ADHD. Hãy định dạng mọi phản hồi để họ có thể hành động ngay:

1. Bắt đầu bằng câu trả lời hoặc hành động tiếp theo: ưu tiên lệnh, đường dẫn hoặc đoạn mã.
2. Đánh số công việc nhiều bước; mỗi bước chỉ có một hành động rõ ràng.
3. Kết thúc bằng một hành động tiếp theo có thể làm trong chưa đến hai phút.
4. Hoàn tất vấn đề hiện tại trước khi nêu vấn đề mới.
5. Nhắc lại tiến độ ở mỗi lượt ("đã xong bước 3/5").
6. Ước tính thời gian bằng đơn vị cụ thể, không nói "một chút".
7. Sau khi thay đổi, hãy cho biết điều gì hiện đã hoạt động.
8. Với lỗi, nêu vị trí, nguyên nhân và cách sửa một cách khách quan.
9. Giới hạn danh sách ở 5 mục.
10. Không mở đầu, không tóm tắt lại, không lời kết.

Ngoại lệ: giải thích đầy đủ khi được yêu cầu. Xác nhận trước thao tác phá hủy dữ liệu. Sau ba lần sửa thất bại, dừng lại và nêu giả định đáng ngờ. Nếu yêu cầu mơ hồ, hãy hỏi một câu ngắn.
```
</details>


## Cơ chế kích hoạt

1. **Đã cài nhưng chưa gọi.** Trong Claude Code, Qwen Code và Codex, không có gì xảy ra cho đến khi bạn gọi skill một cách rõ ràng. Claude Code và Qwen Code tuân theo `disable-model-invocation: true` trong `SKILL.md`; Codex tuân theo `policy.allow_implicit_invocation: false` trong `agents/openai.yaml`. Các môi trường khác có thể tải mô tả của từng skill khi khởi động và tự kích hoạt.
2. **Bạn gọi skill một cách rõ ràng.** Gõ `/i-have-adhd` trong Claude Code hoặc Qwen Code, hoặc `$i-have-adhd` trong Codex. Quy tắc bật trong phiên đó. "stop adhd mode" hoặc "normal mode" sẽ tắt chúng.
3. **Bạn tạo `~/.claude/.i-have-adhd-always`** (Claude Code). Hook `SessionStart` tải toàn bộ quy tắc từ tin nhắn đầu tiên trong mọi phiên.
4. **Bạn thêm đoạn luôn bật ở trên** (các môi trường khác). Điều này giữ quy tắc cốt lõi trong ngữ cảnh lâu dài của agent.

Trong Claude Code, Qwen Code và Codex không có trạng thái trung gian: nếu bạn chưa bật thì nó đang tắt.

## Khắc phục sự cố

**`/i-have-adhd` không có trong tự động hoàn thành.** Khởi động lại agent. Chỉ mục plugin được đọc khi khởi động.

**Cờ luôn bật không có tác dụng.** Cập nhật plugin (`claude plugin marketplace update i-have-adhd`) và khởi động lại. Hook được đọc khi khởi động, và cờ cần phiên bản plugin có `hooks/hooks.json`.

**`claude plugin marketplace add` thất bại.** Dùng dạng `owner/repo`. Đường dẫn cục bộ phải trỏ đến thư mục gốc repo, không phải `.claude-plugin/`.

**Đã cài nhưng phản hồi vẫn có lời mở đầu.** Mở phiên mới. Nếu vẫn lệch, hãy làm chặt hơn cách diễn đạt trong `skills/i-have-adhd/SKILL.md`.

**Muốn quy tắc khác.** Fork repo, sửa `skills/i-have-adhd/SKILL.md`, rồi chuyển sang bản của bạn:

```bash
claude plugin uninstall i-have-adhd            # gỡ bản upstream trước:
claude plugin marketplace remove i-have-adhd   # fork và upstream dùng cùng tên
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Khởi động lại rồi gọi `/i-have-adhd` lần nữa.

**Thiếu skill sau `npx skills add`.** Mở cuộc chat agent mới. Skill được lập chỉ mục khi bắt đầu phiên. Xác nhận thư mục nằm ở nơi agent quét (`~/.cursor/skills/` cho Cursor, `.agents/skills/` cho OpenCode) và `name` trong frontmatter khớp tên thư mục.
