---
name: slidefly
description: Tạo slide HTML có hiệu ứng chuyển cảnh kiểu PowerPoint Morph (hình trang trí trượt, phóng to, đổi màu liền mạch giữa các slide), 85 style (34 style hai lớp có minh họa vẽ riêng từng slide), 21 kiểu slide, 17 khung bố cục, sơ đồ tự vẽ, và xuất ra file PowerPoint .pptx sửa được vẫn giữ Morph. Dùng khi người dùng xin làm slide, bài thuyết trình, trình chiếu, deck, presentation, hoặc nói "slide morph", "slide animation đẹp", "slide HTML có hiệu ứng chuyển cảnh", "làm deck chuyển động", "xuất pptx có morph", "/slidefly", "SlideFly", hoặc muốn chuyển một mẫu PowerPoint Morph sang web. Không dùng khi chỉ cần một file Word/Excel, hay slide HTML hiệu ứng xuất hiện đơn giản (frontend-slides).
---

# SlideFly: slide biết bay

Slide HTML một file, trình chiếu bằng Chrome/Edge, và xuất được sang PowerPoint. Hình trang trí ("diễn viên") sống trên một sân khấu chung; mỗi kiểu slide là một "tư thế". Chuyển slide thì diễn viên trượt sang tư thế mới, đúng tinh thần Morph: cùng tên là cùng một vật.

Skill dir (gọi tắt `$SK`): thư mục chứa chính file SKILL.md này. Tùy app đang chạy skill, thường là `~/.claude/skills/slidefly/` (Claude Code, Claude Desktop), `~/.agents/skills/slidefly/` (Codex app, CLI, IDE), `~/.gemini/config/skills/slidefly/` (Antigravity). Script chỉ dùng thư viện chuẩn của Python 3.10+, không cần cài gì thêm; trên máy chỉ có `python3` thì gọi `python3` thay cho `python`.

**Tinh thần:** đây là bộ đồ nghề, không phải khuôn. Mỗi deck phải mang dáng riêng của nội dung đó. Hai người gõ cùng một đề tài vẫn phải ra hai deck khác nhau. Dùng đồ nghề có sẵn cho phần việc lặp lại, dành công sáng tạo cho những slide đáng nhớ.

## 1. Luật không đổi (độ tin cậy, không thương lượng)

- **Số liệu có nguồn.** Không bịa số, tên, ngày. Số trên slide ghi nguồn ngay cạnh hoặc ở `data-source`. Không có số thật thì dùng ý, hình, câu chốt. Tính năng, giá, lệnh của công cụ AI phải tra tài liệu chính thức và ghi ngày tra.
- **Chữ đọc được:** tương phản ít nhất 3:1 với thứ nằm dưới nó; không tràn khung; không đè chữ khác; không để một dòng vắt qua hai nền khác màu.
- **Tiếng Việt có dấu, câu ngắn, không dùng ký tự gạch ngang dài.**
- **HTML trước, PowerPoint khi được xin:** mặc định chỉ giao file HTML. Chỉ chạy `export-pptx.py` (và chỉ viết thêm vị trí inline, thuộc tính phục vụ PPTX) khi người dùng xin file PowerPoint; xuất PPTX tốn thời gian.
- **Giao một file:** gộp bằng `inline-assets.py`, đặt tên theo quy tắc đánh số của thư mục đích, sao lưu bản cũ vào `_backup/` trước khi ghi đè.

## 2. Nguyên tắc thiết kế (hướng dẫn, tự quyết theo nội dung)

- **Mỗi slide một ý.** Ý dài thì tách slide. Thuyết trình thì ít chữ, tài liệu để đọc thì được dày hơn.
- **Hình theo ý:** quy trình, so sánh, tỷ lệ, phân loại, lọc dần... mỗi loại một dạng hình (`references/hieu-ung-va-so-do.md` mục 2). Không phải ý nào cũng là gạch đầu dòng.
- **Đổi dáng, không chỉ đổi màu.** Mọi style dùng chung một bộ khung chữ (tiêu đề góc trên trái, thân bên dưới); đổi style không làm slide khác dáng. Dáng đến từ kiểu slide và khung (`data-frame`). Xen kẽ slide dày và slide nghỉ (câu chốt, ảnh, con số lớn).
- **Ngân sách dáng (deck.audit() bắt lỗi):** deck có từ 8 slide bên trong thì một dáng dùng tối đa max(3, 20%) lần; từ 10 slide bên trong (không tính slide `diagram`) thì dùng ít nhất 3 khung. Gợi ý theo ý của slide:
  - có hình, khung giao diện, sơ đồ cần nhìn rõ: `media-left` / `media-right` (hình chiếm nửa slide), đừng thu hình vào một ô nhỏ bên phải;
  - thông điệp chính, nguyên tắc: `spotlight`, `poster`, `statement`;
  - so sánh, giải thích có kết luận: `magazine`, `compare-table`, `split-*`;
  - các bước, lộ trình: `stairs`, `process`, `timeline`, `numbered`;
  - danh sách ngắn: `zigzag`, `rail`, `bento`.
- **Cỡ chữ cho thuyết trình:** chữ thân từ 32px; slide chốt dùng tiêu đề lớn (khung `spotlight`, `poster`, `magazine`) thay vì tiêu đề 64px mặc định.
- **Slide tự thiết kế:** deck từ 10 slide nên có 2 đến 4 slide do chính bạn thiết kế cho đúng nội dung (bìa, con số quan trọng nhất, slide chốt), dùng `data-layout="free"` và CSS riêng trong `<style>` của deck. Cách làm và 4 công thức gợi ý: `references/tu-thiet-ke.md`.
- **Hình phục vụ ý:** icon chỉ cho ý chính (không gắn vào từng gạch đầu dòng); khung giao diện giả khi cần cho thấy phần mềm chạy; ảnh nền khi cần điểm nghỉ (ảnh có giấy phép, ghi nguồn).
- **Đừng để slide trống trơn hay chật cứng.** Slide content có thể dùng khối điểm nhấn `.highlight`, một hình, một con số, hoặc một bố cục riêng: tùy ý, không bắt buộc cái nào.

## 3. Đồ nghề (tham khảo, dùng khi hợp)

```
assets/morph-base.css, morph-layouts.css   khung 1920x1080, diễn viên, reveal; 9 kiểu gốc tự co chữ theo số ý
assets/morph-layouts-plus.css   12 kiểu mới: big-number, bento, split-photo, qa, before-after, process, compare-table, portrait-quote, chapter, countdown, statement, cta
assets/morph-frames.css/.js     17 khung phá lưới: data-frame="split-left|split-right|poster|band|rail|bottom|stack|corner|diagonal|frame|zigzag|numbered|media-left|media-right|magazine|spotlight|stairs"
assets/morph-engine.js, morph-nav.js, morph-audit.js   engine, điều hướng (nút hai rìa, phím, vuốt), deck.audit()
assets/morph-motion.css, morph-viz*.{css,js}, morph-steps.js   hiệu ứng theo động từ, 8 dạng sơ đồ tự vẽ, bấm từng bước
assets/morph-brand.css, morph-mock.css/.js, morph-photo.css, morph-icons.css/.js   logo xuyên suốt, khung giao diện giả, ảnh nền, icon Tabler
assets/styles/*.css (85) + index.json   style; đổi style = đổi một dòng link; style hai lớp có thêm <slug>.art.md
templates/deck-mau, deck-bo-cuc, deck-khung, deck-giao-dien, deck-so-do .html   deck mẫu để xem cách viết markup
scripts/inline-assets.py   gộp thành 1 file      scripts/export-pptx.py   xuất PowerPoint có Morph (install-fonts.py: cài font style)
scripts/pick-styles.py     gợi ý style + cách kể (--parts N cho deck dài)      scripts/icons.py   tìm, gợi ý icon
```

Biến thể nhanh trên slide: `data-title="center|side"` (vị trí tiêu đề), `data-stage="clear|<kiểu>"` (tư thế hình trang trí), `data-frame`, `data-brand`, `data-step` (bấm từng bước), `data-morph-id` (chữ bay giữa hai slide), `data-layer` (lớp cố ý chồng lên hình).

Đọc thêm khi cần: `references/layouts.md` (markup từng kiểu, khung), `references/tu-thiet-ke.md` (slide tự thiết kế), `references/hieu-ung-va-so-do.md` (sơ đồ, hiệu ứng), `references/logo-va-giao-dien.md` (logo, khung giao diện, ảnh nền, lưới icon), `references/icon-tabler.md`, `references/style-presets.md`, `references/co-che-morph.md` (cơ chế, viết style mới), `references/vu-dao-morph.md`, `references/xuat-pptx.md` (xuất PowerPoint).

## Quy trình

### Bước 1. Hiểu nội dung
- File `.docx/.pdf/.pptx` thì convert bằng markitdown trước khi đọc.
- Hỏi gộp một lượt những gì còn thiếu (mục đích và người xem; số slide; ít hay nhiều chữ; chất mong muốn). Bỏ câu người dùng đã trả lời.
- Lập dàn ý thành bảng: số slide, ý, **dáng** (kiểu slide + khung, hoặc tự thiết kế). Đếm cột dáng trước khi dựng: dáng nào vượt ngân sách (mục 2) thì đổi bớt. Deck bài giảng dài dễ trượt về một công thức lặp (ví dụ "các bước bên trái, khung giao diện bên phải"): rải đều các khung.

### Bước 2. Chọn style
- Người dùng nêu tên style thì dùng style đó.
- Chưa có thì chạy `python "$SK/scripts/pick-styles.py" "<mục đích, người xem, chất mong muốn>"` để có 3 gợi ý (hợp, khác nền, bất ngờ) và một cách kể. Xem đó là gợi ý để thoát lối mòn, không bắt buộc; có thể đề xuất style khác nếu hợp nội dung hơn (`references/style-presets.md`).
- Khi người dùng muốn xem trước: dựng 3 slide của chính nội dung (bìa, mục lục, một slide nội dung) ở 2 đến 3 style, gộp và gửi để họ chọn hoặc trộn.

### Bước 3. Dựng deck
- Thứ tự nạp: trong `<head>` là `morph-base.css`, `morph-layouts.css`, (`morph-layouts-plus.css`, `morph-frames.css`, các css phụ khi dùng), một file style, rồi `<style>` riêng của deck. Cuối body: các js phụ trước (`morph-frames.js`, `morph-mock.js`, `morph-viz-diagrams.js`, `morph-viz.js`), rồi `morph-engine.js`, `morph-nav.js`, `morph-audit.js`, `morph-steps.js`, `morph-icons.js`. Href tuyệt đối tới `$SK/assets/...` khi file nằm ngoài skill. Các deck trong `templates/` là ví dụ đầy đủ.
- Không viết khối `.actors`: engine tự tạo diễn viên từ style.
- Mỗi slide là `<section class="slide" data-layout="...">`; phần tử nội dung gắn `reveal` (hoặc `reveal-left/right/scale/blur`).
- **Style hai lớp** (có thêm file `assets/styles/<slug>.art.md`, nhãn `art: true` trong `index.json`): ngoài lớp sân khấu CSS, style có bản luật minh họa. Đọc file `.art.md` trước khi dựng.
  - Chế độ **đẹp** (mặc định với style hai lớp): bìa và mỗi slide mang ý chính có **một minh họa SVG inline vẽ riêng theo nội dung slide đó** (vật thể, sơ đồ, cảnh), đúng bảng màu, nét, hình mẫu trong `.art.md`. Không lặp cùng một hình ở hai slide. Chữ cần sửa được thì để ngoài SVG.
  - Chế độ **nhanh** (người dùng nói "nhanh", "ít token", hoặc deck trên 25 slide): chỉ dùng lớp sân khấu như style thường, thêm minh họa cho bìa và slide chốt.
  - Khi người dùng xin PPTX: SVG inline xuất thành hình vector (`export-pptx.py`), vẫn giữ Morph cho diễn viên.

### Bước 4. Gộp thành 1 file
```bash
python "$SK/scripts/inline-assets.py" nguon.html "<thu-muc-dich>/NN_ten-deck.html"
```

### Bước 5. Tự xem lại
- Mở file bằng trình duyệt mà app cho điều khiển (Claude Browser trong Claude Desktop, trình duyệt của agent trong Antigravity, trình duyệt tích hợp của Codex nếu có). App không có trình duyệt thì giao file và nhờ người dùng mở bằng Chrome, nhấn F12, gõ `deck.audit()` rồi gửi lại kết quả. Đi qua từng slide, chụp vài slide tiêu biểu để nhìn bằng mắt: chữ đè hình, tương phản, lệch, chỗ trống, dáng lặp.
- Gõ `deck.audit()` trong trang (javascript của trình duyệt): báo khoảng trống, tràn chữ, chữ khó đọc trên hình, slide lặp dáng, biểu đồ thiếu nguồn, icon lỗi. Sửa tới khi không còn lỗi.

| Báo lỗi | Hướng sửa |
|---|---|
| `trống dọc` / `trống ngang` | ưu tiên đổi sang khung lấp chỗ theo ý (`media-*`, `spotlight`, `magazine`, `stairs`) thay vì nhét thêm một ô bên phải; hoặc gộp slide thưa, thêm hình, số |
| `chữ khó đọc trên hình X` | dời hoặc thu hẹp khối chữ khỏi hình X, hoặc đổi màu chữ ở slide đó |
| `tràn khung` / `chữ tràn hộp` | rút gọn, tách slide, hoặc `data-density="sm"` |
| `nhàm: giống hệt 2 slide trước` | đổi dáng, khung hoặc hiệu ứng của slide đó |
| `nhàm toàn deck: dáng ... lần thứ N` | đổi khung của slide đó theo gợi ý ở mục 2 (đổi màu hay hiệu ứng không tính) |
| `ít khung` | gắn `data-frame` khác nhau cho vài slide bên trong |
| `biểu đồ ... thiếu data-source` | ghi nguồn; không có nguồn thì bỏ biểu đồ có số |

### Bước 6. Bàn giao
- Nêu đường dẫn tuyệt đối, số slide, style.
- Trình chiếu: mũi tên, Space hoặc nút `‹ ›` ở hai rìa; `F` toàn màn hình; bấm vào thân slide không chuyển nên chép chữ thoải mái.
- Chỉ khi người dùng xin file PowerPoint: `python "$SK/scripts/export-pptx.py" deck.html deck.pptx` ra file .pptx sửa được: hình trang trí và logo bay bằng Morph, chữ hiện theo đúng hiệu ứng và cú bấm của bản HTML, font và hoa văn của style đi kèm (`references/xuat-pptx.md`). Mở bằng PowerPoint 2019/365; máy trình chiếu chưa có font của style thì chạy `python "$SK/scripts/install-fonts.py" deck.html`.
- File HTML cần mạng để tải font Google; không mạng thì dùng font dự phòng.

## Thay nội dung mẫu Morph Đại Học
Dùng style `xanh-dai-hoc` (tư thế `dh1`..`dh4`, xem `references/co-che-morph.md` §6).
