"use strict";

const previews = {
  pptx: { title: "パワーポイント", project: "siril9/presentation-skill", caption: "グラフ・表・数値を整理したプレゼン資料の作例。" },
  image: { title: "画像スライド", project: "ningzimu/codex-ppt-skill", caption: "手描き風のビジュアルを用いた技術解説スライドの作例。" },
  html: { title: "ウェブスライド", project: "code-on-sunday/slide-deck-generator", caption: "ブラウザで表示するプレゼン資料の作例。" },
  business: { title: "ビジネス資料", project: "GZPengyuyan/PengyuyanPPT", caption: "青を基調にした企業向け提案資料の作例。" },
  convert: { title: "発表資料", project: "M1n-n9/academic-ppt-master", caption: "研究論文を発表用の資料に整理した作例。" },
  general: { title: "資料制作総合ツール", project: "touying-typ/seaslides", caption: "TypstとTouyingで制作したプレゼン資料の作例。" }
};

const dialog = document.querySelector(".preview-dialog");
const largeImage = document.querySelector("#preview-large");
const previewTitle = document.querySelector("#preview-title");
const previewCaption = document.querySelector("#preview-caption");
const previewSource = document.querySelector("#preview-source");
let previewTrigger = null;

document.querySelectorAll("[data-preview]").forEach((link) => {
  link.addEventListener("click", (event) => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
    if (typeof dialog.showModal !== "function") return;
    const preview = previews[link.dataset.preview];
    if (!preview) return;
    event.preventDefault();
    const image = link.closest(".genre-card").querySelector(".preview-image img");
    previewTrigger = link;
    previewTitle.textContent = preview.title;
    largeImage.src = image.src;
    largeImage.alt = image.alt;
    previewCaption.textContent = preview.caption + " 出典：" + preview.project;
    previewSource.href = "https://github.com/" + preview.project;
    dialog.showModal();
    document.documentElement.classList.add("dialog-open");
  });
});

document.querySelector(".dialog-close").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", (event) => {
  if (event.target !== dialog) return;
  const rect = dialog.getBoundingClientRect();
  if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
});
dialog.addEventListener("close", () => {
  document.documentElement.classList.remove("dialog-open");
  if (previewTrigger) previewTrigger.focus({ preventScroll: true });
});

async function updateCatalogCounts() {
  try {
    const response = await fetch("./data/skills.json");
    if (!response.ok) return;
    const catalog = await response.json();
    if (!Array.isArray(catalog.skills)) return;
    const counts = Object.create(null);
    for (const skill of catalog.skills) counts[skill.kind] = (counts[skill.kind] || 0) + 1;
    document.querySelector("[data-total-count]").textContent = String(catalog.skills.length);
    document.querySelectorAll("[data-count], [data-action-count]").forEach((element) => {
      const kind = element.dataset.count || element.dataset.actionCount;
      if (Object.hasOwn(counts, kind)) element.textContent = String(counts[kind]);
    });
    if (/^\d{4}-\d{2}-\d{2}$/.test(catalog.generated || "")) {
      const [year, month, day] = catalog.generated.split("-").map(Number);
      document.querySelector("[data-source-date]").textContent = "原版データ：" + year + "年" + month + "月" + day + "日";
    }
  } catch {
    // 通信できない場合も、HTMLに記載した件数と一覧へのリンクを利用できます。
  }
}
updateCatalogCounts();
