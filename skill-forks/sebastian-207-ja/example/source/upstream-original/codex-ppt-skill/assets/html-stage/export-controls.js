(function () {
  const deck = document.querySelector("[data-deck-stage]");
  if (!deck) return;

  function scaleDeck() {
    const scale = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    deck.style.transform = `scale(${scale})`;
    document.body.style.width = `${1920 * scale}px`;
    document.body.style.height = `${1080 * scale}px`;
  }

  window.addEventListener("resize", scaleDeck);
  scaleDeck();
})();
