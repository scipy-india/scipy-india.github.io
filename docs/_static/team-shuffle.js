// Shuffle the team cards on the contact page
(() => {
  const shuffle = () => {
    document.querySelectorAll(".sci-team-grid .sd-row").forEach((row) => {
      const cards = Array.from(row.children);
      for (let i = cards.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [cards[i], cards[j]] = [cards[j], cards[i]];
      }
      row.append(...cards);
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", shuffle);
  } else {
    shuffle();
  }
})();
