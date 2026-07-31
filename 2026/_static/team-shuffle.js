(() => {
  const shuffle = () => {
    document.querySelectorAll(".sci-team-grid .sd-row").forEach((row) => {
      const children = Array.from(row.children);
      const cards = children.filter((el) => !el.matches(".sci-team-open"));
      const pinned = children.filter((el) => el.matches(".sci-team-open"));
      for (let i = cards.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [cards[i], cards[j]] = [cards[j], cards[i]];
      }
      row.append(...cards, ...pinned);
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", shuffle);
  } else {
    shuffle();
  }
})();
