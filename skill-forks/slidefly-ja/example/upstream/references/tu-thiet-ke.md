# Tự thiết kế slide (data-layout="free")

Kiểu slide và khung có sẵn giúp dựng nhanh, nhưng dùng mãi thì deck nào cũng na ná nhau. Mỗi deck nên có vài **slide đinh** do chính AI thiết kế cho đúng nội dung đó: bìa, slide chốt, con số quan trọng nhất, khoảnh khắc "à ra thế". Gợi ý: deck từ 10 slide có 2 đến 4 slide tự thiết kế.

## Cách làm

- Đặt slide là `<section class="slide" data-layout="free">`. Engine cho sân khấu trống (hình trang trí của style lui ra) và không ép vùng thân. `deck.audit()` chỉ kiểm tràn khung và chữ khó đọc.
- Viết CSS riêng trong khối `<style>` của deck. Mọi selector gắn với một lớp riêng của slide (ví dụ `.s-hero`) để không ảnh hưởng slide khác.
- Dùng token của style để vẫn hợp màu: `var(--bg) var(--fg) var(--muted) var(--accent) var(--font-display) var(--font-body)`. Sân khấu rộng 1920×1080px, đặt phần tử bằng `position: absolute` theo px.
- Vẫn dùng được `reveal`, `reveal-left`, `fx-*`, `data-step`, icon `.ico`, `data-morph-id` (chữ bay từ slide trước sang).
- Giữ luật không đổi: số có nguồn; chữ tương phản ít nhất 3:1 với thứ nằm dưới nó; không tràn khung (lề 80px hai bên, 60px trên dưới); mỗi slide một ý.
- Muốn giữ hình trang trí của style ở viền thì thêm `data-stage="agenda"` (hoặc tên một kiểu khác) để mượn tư thế của kiểu đó.

## Bốn công thức để bắt đầu (biến tấu, đừng chép nguyên)

**1. Chữ khổng lồ cắt mép:** một con số hay một từ chiếm gần hết slide, tràn ra mép một bên; câu giải thích nhỏ đặt trong khoảng trống còn lại.

```html
<section class="slide s-giant" data-layout="free">
  <p class="g-word reveal-scale">90%</p>
  <p class="g-say reveal">kiện hàng thông quan không cần người can thiệp</p>
  <p class="g-src">Nguồn: ...</p>
</section>
<style>
.s-giant .g-word { position: absolute; left: -40px; top: 40px; margin: 0; font: 800 760px/0.8 var(--font-display); color: var(--accent); letter-spacing: -0.06em; }
.s-giant .g-say { position: absolute; right: 120px; bottom: 200px; width: 560px; font: 600 44px/1.2 var(--font-display); color: var(--fg); }
.s-giant .g-src { position: absolute; right: 120px; bottom: 90px; width: 560px; font-size: 20px; color: var(--muted); }
</style>
```
Giữ chữ đọc được: con số chỉ nằm trên nền trơn; câu giải thích không đè lên con số.

**2. Lưới bất đối xứng:** một ô lớn và ba ô nhỏ lệch tầng, mỗi ô một ý, ô lớn cho ý chính.

```css
.s-grid .cells { position: absolute; inset: 200px 120px 90px; display: grid; grid-template-columns: 1.6fr 1fr 1fr; grid-template-rows: 1fr 1.3fr; gap: 20px; }
.s-grid .cells > :first-child { grid-row: 1 / 3; background: var(--accent); color: var(--bg); }
.s-grid .cells > * { border-radius: 20px; padding: 36px; background: color-mix(in srgb, var(--fg) 6%, var(--bg)); }
```

**3. Dòng thời gian uốn lượn:** các mốc nằm trên một đường cong vẽ bằng SVG (`<path class="draw" pathLength="1">` để nét tự vẽ), mỗi mốc là một nhãn đặt tuyệt đối gần đường.

**4. Ảnh và chữ chồng lớp:** ảnh chiếm hai phần ba bên phải; một khối màu nhấn chồng lên mép ảnh mang tiêu đề; nguồn ảnh bắt buộc (`.photo-credit`).

## Xuất PowerPoint

Phần này chỉ cần khi người dùng xin file PowerPoint; deck chỉ giao HTML thì bỏ qua. Slide tự thiết kế vẫn xuất được bằng `export-pptx.py`. Phần chữ vào hộp chữ sửa được, đặt theo `left/top/width/height` ghi trong thuộc tính `style` của phần tử (CSS ở khối `<style>` riêng không được đọc). Nên ghi vị trí của các khối chữ chính ngay trong `style="..."` nếu deck cần xuất PPTX.

Script đọc thêm trong `style`: `font-size` (px), `color` và `background` dạng `var(--accent|fg|muted|bg|on-accent|tint)`, `font-weight` từ 600 trở lên (đậm), `text-align: center|right`, `var(--font-display)`. Mỗi khối thành một đoạn: chữ đậm làm tiêu đề khối (`<b>` hiển thị kiểu block) thì thêm `<br class="pp">` ngay sau nó và ẩn bằng CSS (`br.pp { display: none }`) để bản PPTX xuống dòng. Hình SVG tự vẽ sang PPTX thành ảnh vector khi `<svg>` là con trực tiếp của slide, có `left/top` trong `style` và thuộc tính `width`, `height` trên chính thẻ `<svg>` (ghi trong `style` thì bị bỏ qua). Màu nét nên ghi thẳng `fill`/`stroke` trên từng hình, hoặc dùng lớp có selector cuối là tên lớp; chỉ khai bằng selector lồng trong CSS của deck thì PPTX có thể vẽ thành hình đen đặc. Khối `<pre>` cần `<br class="pp">` cuối mỗi dòng để PPTX giữ xuống dòng.
