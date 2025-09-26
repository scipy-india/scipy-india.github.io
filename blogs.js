const blogConfig = [
  {
    id: "about",
    title: "About",
    excerpt:
      "Learn about our community, mission, and vision, for advancing Python in scientific computing across India.",
    markdownFile: "blogs/about.md",
    date: "2025-09-26",
    tags: ["Community", "Introduction"],
    icon: "🏛️",
    readTime: "5 min read",
  },
  {
    id: "community-call-july-2025",
    title: "Highlights from the SciPy India Community Call #1",
    excerpt:
      "Key insights and takeaways from our first community call, including upcoming events and community initiatives.",
    markdownFile: "blogs/community-calls/july-2025.md",
    date: "2025-08-01",
    tags: ["Community Call", "Events"],
    icon: "📞",
    readTime: "5 min read",
  },
];

class BlogsRenderer {
  constructor() {
    this.container = document.getElementById("blogs-container");
    if (this.container) {
      this.renderBlogs();
    }
  }

  generateBlogUrl(blogId) {
    return `blogs.html?id=${blogId}`;
  }

  renderBlogs() {
    while (this.container.firstChild) {
      this.container.removeChild(this.container.firstChild);
    }

    if (blogConfig.length === 0) {
      this.renderNoBlogsMessage();
      return;
    }

    // Sort blogs by date (newest first)
    const sortedBlogs = [...blogConfig].sort(
      (a, b) => new Date(b.date) - new Date(a.date)
    );

    sortedBlogs.forEach((blog, index) => {
      const blogCard = this.createBlogCard(blog, index);
      this.container.appendChild(blogCard);
    });
  }

  createBlogCard(blog, index) {
    const card = document.createElement("article");
    card.className = "blog-card";

    // Header
    const header = document.createElement("div");
    header.className = "blog-card-header";

    const icon = document.createElement("div");
    icon.className = "blog-icon";
    icon.textContent = blog.icon;

    const meta = document.createElement("div");
    meta.className = "blog-meta";

    const title = document.createElement("h2");
    title.className = "blog-title";
    title.textContent = blog.title;

    const date = document.createElement("div");
    date.className = "blog-date";
    date.textContent = `📅 ${this.formatDate(blog.date)} • ${blog.readTime}`;

    meta.appendChild(title);
    meta.appendChild(date);
    header.appendChild(icon);
    header.appendChild(meta);
    card.appendChild(header);

    // Excerpt
    const excerpt = document.createElement("p");
    excerpt.className = "blog-excerpt";
    excerpt.textContent = blog.excerpt;
    card.appendChild(excerpt);

    // Tags
    if (blog.tags && blog.tags.length > 0) {
      const tagsContainer = document.createElement("div");
      tagsContainer.className = "blog-tags";

      blog.tags.forEach((tag) => {
        const tagElement = document.createElement("span");
        tagElement.className = "blog-tag";
        tagElement.textContent = tag;
        tagsContainer.appendChild(tagElement);
      });

      card.appendChild(tagsContainer);
    }

    // Actions
    const actions = document.createElement("div");
    actions.className = "event-actions";

    const readBtn = document.createElement("a");
    readBtn.href = this.generateBlogUrl(blog.id);
    readBtn.className = "btn btn-primary";
    readBtn.textContent = "Read article";

    actions.appendChild(readBtn);
    card.appendChild(actions);

    return card;
  }

  formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  }

  renderNoBlogsMessage() {
    const messageDiv = document.createElement("div");
    messageDiv.className = "no-blogs";

    const icon = document.createElement("div");
    icon.className = "no-blogs-icon";
    icon.textContent = "📝";

    const title = document.createElement("h3");
    title.textContent = "No blogs yet";
    title.style.marginBottom = "1rem";
    title.style.color = "var(--text-dark)";

    const description = document.createElement("p");
    description.textContent =
      "We're working on bringing you great content. Check back soon!";

    messageDiv.appendChild(icon);
    messageDiv.appendChild(title);
    messageDiv.appendChild(description);

    this.container.appendChild(messageDiv);
  }

  static getBlogById(id) {
    return blogConfig.find((blog) => blog.id === id);
  }

  static getAllBlogs() {
    return blogConfig;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  new BlogsRenderer();
});

if (typeof module !== "undefined" && module.exports) {
  module.exports = { BlogsRenderer, blogConfig };
}
