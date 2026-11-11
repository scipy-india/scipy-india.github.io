(() => {
  const openMenus = () =>
    document.querySelectorAll("details.sci-add-to-calendar[open]");

  document.addEventListener("click", (event) => {
    openMenus().forEach((menu) => {
      if (event.target === menu || !menu.contains(event.target)) {
        menu.removeAttribute("open");
      }
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") {
      return;
    }
    openMenus().forEach((menu) => {
      const hadFocus = menu.contains(document.activeElement);
      menu.removeAttribute("open");
      if (hadFocus) {
        menu.querySelector("summary").focus();
      }
    });
  });
})();
