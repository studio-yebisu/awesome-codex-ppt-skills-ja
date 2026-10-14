/* MORPH-SLIDES ICONS: Tabler Icons (MIT, Paweł Kuna) for decks being edited.
   <i class="ico" data-icon="database"></i>, data-style="filled" for the solid set.
   While a deck is a source file, empty icons are fetched from jsDelivr (pinned
   version). inline-assets.py embeds the SVGs, so the final deck needs no network
   and this script then has nothing to do. A name that does not exist gets
   data-missing, which deck.audit() reports. Load anywhere after the slides. */
(() => {
  const VERSION = '3.48.0';
  const CDN = `https://cdn.jsdelivr.net/npm/@tabler/icons@${VERSION}/icons`;
  const cache = new Map();
  const load = (name, style) => {
    const key = `${style}/${name}`;
    if (!cache.has(key)) {
      cache.set(key, fetch(`${CDN}/${key}.svg`).then((r) => (r.ok ? r.text() : Promise.reject(new Error(r.status)))));
    }
    return cache.get(key);
  };
  document.querySelectorAll('.ico[data-icon]').forEach(async (el) => {
    if (el.querySelector('svg')) return;
    const name = el.dataset.icon;
    const style = el.dataset.style === 'filled' ? 'filled' : 'outline';
    if (!/^[a-z0-9-]+$/.test(name)) { el.dataset.missing = ''; return; }
    try {
      const svg = (await load(name, style))
        .replace(/\s(width|height)="24"/g, '')
        .replace(/\sclass="[^"]*"/, ' aria-hidden="true" focusable="false"');
      el.innerHTML = svg;
    } catch {
      el.dataset.missing = '';
      console.warn('morph-icons: không tải được icon', name, style);
    }
  });
})();
