# Xuất PowerPoint có Morph

`scripts/export-pptx.py` ghi một file .pptx **sửa được**, có hiệu ứng **Morph** khi chuyển slide và hiệu ứng xuất hiện bám theo bản HTML. Chỉ dùng thư viện chuẩn của Python 3.10+, không cần trình duyệt, không cần cài gói.

```bash
python "$SK/scripts/export-pptx.py" deck.html deck.pptx
python "$SK/scripts/install-fonts.py" deck.html     # một lần trên máy trình chiếu (Windows): cài font của style
```

Đầu vào là file nguồn (có `<link>` tới CSS) hoặc file đã gộp bằng `inline-assets.py`, cả hai đều được.

## Vì sao Morph chạy được

PowerPoint Morph khớp hai hình ở hai slide liền nhau khi chúng **cùng tên bắt đầu bằng `!!`**: hình trượt, đổi cỡ, đổi màu sang chỗ mới. Đây đúng là cơ chế diễn viên của SlideFly:

- Mỗi diễn viên của style thành một hình tên `!!<tên diễn viên>` trên **mọi** slide, đặt đúng tư thế của slide đó (`--x --y --w --h --r --s --o`, xoay và phóng quanh tâm như CSS). Diễn viên ngoài khung thì hình vẫn nằm ngoài khung để Morph có chỗ bay vào, bay ra.
- Logo xuyên suốt (`.brand`) thành `!!brand-ico` và `!!brand-name`: to ở bìa và slide kết, nhỏ ở góc, ẩn ở trích dẫn.
- Đổi đơn vị: 1px = 6350 EMU; cỡ chữ px × 0,5 = pt.
- Mọi slide gắn chuyển cảnh Morph (theo đối tượng). PowerPoint đời cũ không có Morph thì dùng fade.

## Hiệu ứng xuất hiện

Mỗi hộp chữ được dò ngược về phần tử HTML sinh ra nó, rồi lấy đúng hiệu ứng, thứ tự và độ trễ:

| HTML | PowerPoint |
|---|---|
| `reveal` | hiện dần, trượt nhẹ lên |
| `reveal-left`, `reveal-right`, `fx-right`, `fx-left` | hiện dần, trượt ngang |
| `reveal-scale`, `fx-pop`, `slam` | phóng to (hoặc thu về) |
| `type` (khung giao diện) | hiện từng chữ |
| `draw` (nét SVG) | vẽ quét từ trái |
| `data-step="n"` | chờ cú bấm thứ n, giống phím mũi tên trong bản HTML |
| `--i`, `--d` | thứ tự và độ trễ |

Gạch đầu dòng, danh sách hiện lần lượt từng dòng. Tiêu đề và diễn viên bay bằng Morph nên không có hiệu ứng riêng.

## Giữ được

- Chữ sửa được ở mọi kiểu slide, 12 khung `data-frame`, màu riêng của style cho tiêu đề, nhãn, số; chữ in hoa (`text-transform`), cụm `<mark>` được tô, số chương viền rỗng, nút bấm của slide `cta`.
- **Font của style** được nhúng vào file (định dạng EOT như PowerPoint tự làm). Bản PowerPoint nào không đọc font nhúng thì chạy `install-fonts.py` để cài font Google của style cho tài khoản Windows (không cần quyền admin, gỡ được trong Settings, Fonts).
- **Hoa văn** (giấy kẻ ô, chấm, sọc lặp, gradient thẳng, tròn và hình quạt `conic`, ảnh SVG nhúng, mask, bo góc, cắt chéo, nhiều lớp có vị trí và cỡ riêng trong `background`) thành ảnh SVG, PowerPoint 365 vẽ dạng vector, vẫn mang tên `!!` để Morph.
- **Làm mờ và bóng đổ**: `filter: blur()` thành viền mờ (soft edges), `box-shadow` thành bóng đổ của PowerPoint.
- Vị trí viết bằng `calc()` và luật nhóm diễn viên (`[data-actor^="b"]`) được tính như trình duyệt.
- **Hình SVG tự vẽ** trong slide (mặt bằng, đường nối, con đường, minh họa của style hai lớp) thành ảnh SVG thật trên mọi layout, kể cả bìa, chương, trích dẫn và kết, lấy màu và nét từ CSS của deck.
- **Khung giao diện**: cửa sổ có thanh tiêu đề ba chấm, terminal tối có dấu `$` xanh, bong bóng chat; mỗi khối một hộp để hiện theo nhịp riêng.
- **Slide tự thiết kế**: khối đặt bằng `left/top` (trong `style` hoặc trong CSS của deck) giữ chỗ, nền, viền, khoảng đệm, cỡ chữ, font tiêu đề hay font mono theo class CSS.
- Icon Tabler thành hình vẽ của PowerPoint (đổi màu, phóng to không vỡ); ảnh nền, ảnh chia đôi, nguồn ảnh.

## Còn đơn giản hóa

| Phần | Trong PowerPoint |
|---|---|
| Sơ đồ tự vẽ bằng JS (`.viz`: funnel, donut, network...) | khung có danh sách nhãn |
| Chữ gõ dần có con trỏ nhấp nháy, chấm "đang nghĩ" | hiện từng chữ, không con trỏ |
| Quy tắc style phụ thuộc nội dung (`:has(...)`) | hình giữ tư thế chuẩn của kiểu slide |
| Khoảng cách dòng, chữ ngắt dòng | gần giống, có thể lệch vài px vì PowerPoint tự ngắt dòng |

## Sau khi xuất

- Mở bằng PowerPoint 2019 hoặc 365 để có Morph và ảnh SVG. Google Slides và Keynote không có Morph.
- Kiểm nhanh (Windows): mở file, bấm **Slide Show**, đi qua vài slide xem hình bay, chữ hiện dần và các bước chờ bấm.
