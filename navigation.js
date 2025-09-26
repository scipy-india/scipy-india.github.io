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
    const urlParams = new URLSearchParams(window.location.search);
    const blogId = urlParams.get("id");
    const navContext = urlParams.get("nav");
    const navLinks = document.querySelectorAll("nav a");

    navLinks.forEach((link) => {
      link.classList.remove("active");
    });

    // Handling for blogs.html...
    // This is terrible tbh but let's hope we get rid of it
    // when switching to Hugo. The idea is that we highlight:
    // "Blogs" when About is accessed from blogs page
    // "About" when accessed from navbar (no nav parameter)
    // "Blogs" for all other blog posts and blog listing
    if (currentPath.includes("blogs.html")) {
      if (blogId === "about" && navContext === "blogs") {
        // Highlight "Blogs" when About is accessed from blogs page
        const blogsLink = document.querySelector('nav a[href="blogs.html"]');
        if (blogsLink) blogsLink.classList.add("active");
      } else if (blogId === "about") {
        const aboutLink = document.querySelector('nav a[href*="id=about"]');
        if (aboutLink) aboutLink.classList.add("active");
      } else if (blogId) {
        //
        const blogsLink = document.querySelector('nav a[href="blogs.html"]');
        if (blogsLink) blogsLink.classList.add("active");
      } else {
        const blogsLink = document.querySelector('nav a[href="blogs.html"]');
        if (blogsLink) blogsLink.classList.add("active");
      }
      return;
    }

    navLinks.forEach((link) => {
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
