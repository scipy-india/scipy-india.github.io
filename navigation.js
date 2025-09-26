class NavigationManager {
  constructor() {
    this.navToggle = document.querySelector(".nav-toggle");
    this.navMenu = document.querySelector("nav ul");
    this.initializeNavigation();
    this.initializeSmoothScrolling();
  }

  initializeNavigation() {
    if (this.navToggle && this.navMenu) {
      this.navToggle.addEventListener("click", () => {
        this.navMenu.classList.toggle("active");
      });

      document.addEventListener("click", (e) => {
        if (!e.target.closest("nav") && !e.target.closest(".nav-toggle")) {
          this.navMenu.classList.remove("active");
        }
      });

      this.navMenu.addEventListener("click", (e) => {
        if (e.target.tagName === "A") {
          this.navMenu.classList.remove("active");
        }
      });
    }
  }

  initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute("href"));
        if (target) {
          target.scrollIntoView({
            behavior: "smooth",
          });
        }
      });
    });
  }

  // Method to set active nav item based on current page
  setActiveNavItem() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll("nav a");

    navLinks.forEach((link) => {
      link.classList.remove("active");
      const href = link.getAttribute("href");

      if (
        currentPath.includes(href) ||
        (currentPath === "/" && href === "index.html") ||
        (currentPath.endsWith("/") && href === "index.html")
      ) {
        link.classList.add("active");
      }
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const navManager = new NavigationManager();
  navManager.setActiveNavItem();
});
