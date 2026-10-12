"use strict";

const genres = {
  pptx: { title: "編集できるPowerPoint", description: "文字や図形をあとから編集できる、PowerPoint制作のプロジェクト。" },
  image: { title: "見た目で伝える画像スライド", description: "ページ全体を画像として仕上げる、ビジュアル重視のスライド制作。" },
  html: { title: "動きも使えるWebスライド", description: "ブラウザで発表できる、アニメーションや演出を使ったスライド制作。" },
  business: { title: "提案・報告のためのビジネス資料", description: "企画提案、経営報告、ピッチなどの資料制作を支援するプロジェクト。" },
  convert: { title: "論文・文書から発表資料をつくる", description: "論文、PDF、記事、原稿をもとに、発表用のスライドをつくるプロジェクト。" },
  general: { title: "資料制作をまとめる総合ツール", description: "構成、デザイン、出力など、資料づくりの流れを支援するツールやフレームワーク。" }
};

const parameters = new URLSearchParams(location.search);
const requestedGenre = parameters.get("genre") || "pptx";
const validGenre = Object.hasOwn(genres, requestedGenre);
const activeGenre = validGenre ? requestedGenre : null;
const list = document.querySelector("#project-list");
const query = document.querySelector("#project-query");
const order = document.querySelector("#project-order");
const count = document.querySelector("#result-count");
const empty = document.querySelector("#project-empty");
const error = document.querySelector("#project-error");
let projects = [];
let previews = {};

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function repositoryUrl(project) {
  if (!/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(project.repo_full_name || "")) {
    throw new Error("Invalid repository name in catalog");
  }
  return "https://github.com/" + project.repo_full_name.split("/").map(encodeURIComponent).join("/");
}

function render() {
  const term = query.value.trim().normalize("NFKC").toLocaleLowerCase("ja");
  const shown = projects.filter((project) =>
    (project.repo_full_name + " " + project.description_ja).normalize("NFKC").toLocaleLowerCase("ja").includes(term)
  ).sort((a, b) => {
    if (order.value === "stars" && a.stars !== b.stars) return b.stars - a.stars;
    return a.repo_full_name.localeCompare(b.repo_full_name, "en", { sensitivity: "base" });
  });
  const fragment = document.createDocumentFragment();
  for (let index = 0; index < shown.length; index += 1) {
    const project = shown[index];
    const [owner, name] = project.repo_full_name.split("/");
    const card = element("a", "project-card genre-" + activeGenre);
    card.href = repositoryUrl(project);
    card.target = "_blank";
    card.rel = "noopener noreferrer";
    card.id = project.repo_full_name.replace("/", "--");
    card.dataset.repo = project.repo_full_name;
    card.dataset.stars = String(project.stars);
    card.setAttribute("aria-label", project.repo_full_name + "：" + project.description_ja + " 元のGitHubを新しいタブで開く");
    const topline = element("div", "project-topline");
    topline.append(element("span", "project-rank", String(index + 1).padStart(2, "0")));
    const stars = element("span", "project-stars", "★ " + project.stars.toLocaleString("ja-JP"));
    stars.setAttribute("aria-label", "GitHubスター " + project.stars.toLocaleString("ja-JP") + "件");
    topline.append(stars);
    card.append(topline, element("p", "project-owner", owner), element("h2", "project-name", name),
      element("p", "project-description", project.description_ja));
    const preview = previews[project.repo_full_name];
    if (preview && /^assets\/project-previews\/[A-Za-z0-9_.-]+\.jpg$/.test(preview.src)) {
      const visual = element("div", "project-visual");
      const image = element("img", "project-preview");
      image.src = preview.src;
      image.alt = preview.alt;
      image.width = 520;
      image.height = 293;
      image.loading = index < 3 ? "eager" : "lazy";
      image.decoding = "async";
      visual.append(image);
      card.insertBefore(visual, topline);
    } else {
      card.classList.add("project-card--text-only");
    }
    const footer = element("div", "project-card-footer");
    footer.append(element("span", "project-format", genres[activeGenre].title), element("span", "project-open", "GitHubを見る ↗"));
    card.append(footer);
    fragment.append(card);
  }
  list.replaceChildren(fragment);
  list.setAttribute("aria-busy", "false");
  empty.hidden = shown.length > 0;
  count.textContent = term ? projects.length + "件中 " + shown.length + "件" : shown.length + "件のプロジェクト";
}

async function loadProjects() {
  if (!activeGenre) {
    document.querySelector("#project-title").textContent = "ジャンルを選んでください";
    document.querySelector("#genre-description").textContent = "下の6つのジャンルから、つくりたい資料を選べます。";
    count.textContent = "ジャンルが指定されていません";
    list.setAttribute("aria-busy", "false");
    document.querySelector(".project-controls").hidden = true;
    return;
  }
  const genre = genres[activeGenre];
  document.title = genre.title + "のプロジェクト一覧｜AIスライド制作ガイド";
  document.querySelector("#project-title").textContent = genre.title;
  document.querySelector("#genre-description").textContent = genre.description;
  document.querySelector('[data-genre="' + activeGenre + '"]').setAttribute("aria-current", "page");
  document.querySelector("#fallback-catalog").href = "https://github.com/studio-yebisu/awesome-codex-ppt-skills-ja#type-" + activeGenre;
  try {
    const response = await fetch("./data/skills.json");
    if (!response.ok) throw new Error("Catalog HTTP " + response.status);
    const catalog = await response.json();
    if (!Array.isArray(catalog.skills)) throw new Error("Catalog is missing skills");
    try {
      const previewResponse = await fetch("./data/previews.json");
      if (previewResponse.ok) previews = (await previewResponse.json()).images || {};
    } catch {
      // 紹介文と並び順は、画像データを取得できない場合も使えます。
    }
    projects = catalog.skills.filter((project) => project.kind === activeGenre);
    for (const project of projects) {
      repositoryUrl(project);
      if (!Number.isFinite(project.stars) || project.stars < 0 || typeof project.description_ja !== "string") {
        throw new Error("Invalid project data");
      }
    }
    const counts = Object.create(null);
    for (const project of catalog.skills) counts[project.kind] = (counts[project.kind] || 0) + 1;
    document.querySelectorAll("[data-genre-count]").forEach((node) => {
      node.textContent = String(counts[node.dataset.genreCount] || 0);
    });
    if (/^\d{4}-\d{2}-\d{2}$/.test(catalog.generated || "")) {
      const [year, month, day] = catalog.generated.split("-").map(Number);
      document.querySelector("#star-source").textContent = "人気順：GitHubスター数 · " + year + "年" + month + "月" + day + "日の原版データ";
    } else {
      document.querySelector("#star-source").textContent = "人気順：GitHubスター数 · 取得日は原版データに未記載";
    }
    query.value = parameters.get("q") || "";
    render();
    if (location.hash) {
      const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (target) target.scrollIntoView({ block: "center" });
    }
  } catch (failure) {
    console.error("Project catalog could not be loaded", failure);
    error.hidden = false;
    document.querySelector(".project-controls").hidden = true;
    count.textContent = "一覧を読み込めませんでした";
    list.setAttribute("aria-busy", "false");
  }
}

query.addEventListener("input", render);
order.addEventListener("change", render);
document.querySelector("#clear-search").addEventListener("click", () => {
  query.value = "";
  render();
  query.focus();
});
loadProjects();
