# Cơ chế Morph trong SlideFly

## 1. Diễn viên và tư thế
- **Diễn viên** (`.actor[data-actor="ten"]`): hình trang trí nằm trên MỘT sân khấu chung, phía sau nội dung. Engine tạo chúng từ biến `--actors` của style; thứ tự trong danh sách là thứ tự chồng lớp (đầu danh sách nằm dưới cùng).
- **Tư thế**: chỉ là biến CSS trên diễn viên: `--x --y --w --h` (px, `--h` mặc định bằng `--w`), `--r` (độ xoay), `--s` (tỷ lệ), `--o` (độ mờ), `--bw` (độ dày viền, nằm giữa mép giống PowerPoint). Màu, viền, bóng đổi bằng thuộc tính thường.
- **Chuyển cảnh**: engine đổi `data-layout`, `data-parity` (odd/even), `data-pose` trên `.deck-stage`. CSS chọn tư thế mới, `transition` 1,2 giây với easing expo tạo chuyển động mượt. Không có thư viện ngoài.
- Ưu tiên tư thế: `[data-layout][data-parity="even"]` > `[data-layout]` > mặc định (trạng thái mở màn: diễn viên bay vào khi tải trang). Rule `[data-pose]` cùng độ ưu tiên với `[data-layout]` nên **phải viết sau** các rule layout; slide có `data-pose` được engine đặt parity `none` nên không bị rule parity tranh.
- **Biến thể (`data-variant` 1, 2, 3):** engine đếm lần thứ mấy một kiểu slide xuất hiện (mở phần thứ 1, 2, 3, rồi quay vòng) và gắn lên cả slide lẫn sân khấu. Style viết `[data-layout="section"][data-variant="2"] [data-actor="x"]` để slide lặp lại có dáng khác; nội dung chỉnh theo `.slide[data-layout="section"][data-variant="2"]`. Phần dùng chung đã cho chữ vào khung khác nhau: biến thể 2 trượt từ trái, biến thể 3 phóng nhẹ. Ví dụ đầy đủ: `stencil-tablet.css` (mở phần, nội dung, hai cột đều có 3 dáng). Ghi đè thủ công: `<section data-variant="3">`.
- Mỗi slide cũng mang `data-parity` của chính nó: tinh chỉnh nội dung theo chẵn/lẻ viết `.slide[data-layout="content"][data-parity="even"]`, không viết theo parity của sân khấu.
- Tọa độ âm hoặc quá 1920/1080 là cố ý: diễn viên "chờ sau cánh gà" để bay vào ở slide sau.

## 2. Chữ bay giữa hai slide (FLIP)
Phần tử có cùng `data-morph-id` ở slide cũ và slide mới: engine đo vị trí cũ, đặt phần tử mới về đó rồi cho trượt và co giãn về vị trí thật (First, Last, Invert, Play). Chữ co giãn đều theo tỷ lệ cỡ chữ để không méo.

## 3. Nội dung xuất hiện
Các lớp `reveal*` ẩn phần tử và cho hiện lần lượt sau khi slide active, trễ `--reveal-base` (0,45 giây) để diễn viên chuyển động trước, mỗi phần tử cách nhau `--reveal-step`. Engine tự đánh số thứ tự `--i`.

## 4. Giảm chuyển động
Khi hệ điều hành bật giảm chuyển động (Windows: tắt Animation effects), `--morph-dur` còn 0,7 giây, bỏ hiệu ứng mờ. Không tắt hẳn vì chuyển động chính là nội dung của deck.

## 5. Viết style mới (checklist)
1. Tạo `assets/styles/<ten>.css`, dưới 200 dòng, `@import` font Google **có bộ chữ tiếng Việt** (kiểm: tải `https://fonts.googleapis.com/css2?family=<Font>` với User-Agent Chrome, tìm chuỗi `/* vietnamese */`). Font đã kiểm có tiếng Việt: Montserrat, Open Sans, Be Vietnam Pro, Space Grotesk, Archivo, Inter, Cormorant, Cormorant Garamond, IBM Plex Sans, Chakra Petch, Source Serif 4, Fraunces, Unbounded, JetBrains Mono. KHÔNG có: Archivo Black, Syne.
2. Trên `.deck-stage`: `--actors`, token `--font-display --font-body --bg --fg --muted --accent --card-bg --card-fg --title-weight --title-tracking` (tùy chọn `--card-radius --bullet-radius --title-case --title-style`).
3. Mỗi diễn viên có tư thế cho đủ 9 layout và `content` parity even. Mỗi lần đổi layout phải có diễn viên đổi chỗ, đổi cỡ hoặc đổi màu.
4. Giữ trống: hàng tiêu đề y 90..165, vùng highlight x 1260..1800 của `content`, trục timeline y 630. Diễn viên tràn nền (full màn hình) thì đổi `--fg --muted --accent` theo layout trên `.deck-stage[data-layout=...]`.
5. Mẹo đã kiểm qua 41 style:
   - Diễn viên đổi tư thế theo nội dung slide đang hiện: `.deck-stage:has(.slide.active .takeaway) [data-actor="x"]`.
   - Thứ tự trong `--actors` là lớp chồng: diễn viên đứng sau trong danh sách che diễn viên đứng trước.
   - Hình phức tạp (hoa, ghim, sticker) vẽ bằng SVG data URI trong `background` hoặc `mask` (đổi màu bằng `background-color`).
   - Chữ in hoa tiếng Việt cần `line-height` từ 1.2; Playfair cần `lining-nums` cho số lớn; tránh chữ nghiêng có nét lạ (Fraunces italic) cho đoạn văn.
   - Agenda mặc định (gap 640px, cột phải căn phải) dễ bị "trống ngang": đặt `--agenda-gap` 140-360px nếu không cần khoảng giữa.
6. Dựng `templates/deck-mau.html` với style mới, mở bằng trình duyệt, gõ `deck.audit()` và đi qua từng slide, sửa tới khi audit không báo lỗi và nhìn đẹp.
7. Thêm style vào `assets/styles/index.json` và nhóm phù hợp trong `references/style-presets.md`.

## 6. Port một mẫu PowerPoint Morph
- Đổi tọa độ: **px = EMU / 6350** (slide 16:9 rộng 12192000 EMU = 1920px). Cỡ chữ: **px = pt x 2**.
- Độ dày viền `<a:ln w>`: EMU / 6350. Bóng `outerShdw`: blur và dist chia 6350, hướng `dir` (đơn vị 1/60000 độ) đổi sang dx, dy.
- `custGeom` đổi sang SVG path: giữ `w/h` làm viewBox, M/L/C/Z giữ nguyên. Hình đứng yên dùng SVG nền (data URI) trong CSS như diễn viên `flower` của `xanh-dai-hoc.css`.
- Tên `!!Tên` của PowerPoint ứng với `data-actor`; mỗi slide mẫu thành một `data-pose`. Ví dụ: phần `dh1..dh4` trong `xanh-dai-hoc.css`.
- `advClick="0" advTm="1000"` của mẫu là tự chuyển slide; skill này mặc định người trình bày bấm (phím hoặc nút rìa) mới chuyển.
- Chiều ngược lại (deck SlideFly ra file .pptx có Morph): `scripts/export-pptx.py`, xem `references/xuat-pptx.md`.

## 7. Nguồn và giấy phép
- Khung co giãn và lớp reveal lấy ý từ `frontend-slides` (zarazhangrui, MIT). Style Swiss Modern, Dark Botanical, Neon Cyber, Paper & Ink phỏng theo bộ preset của repo này, font thay bằng font có tiếng Việt.
- Icon: Lucide (ISC).
