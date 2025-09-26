class Renderer {
  constructor() {
    this.allowedTags = new Set([
      "h1",
      "h2",
      "h3",
      "h4",
      "h5",
      "h6",
      "p",
      "br",
      "hr",
      "strong",
      "b",
      "em",
      "i",
      "u",
      "mark",
      "ul",
      "ol",
      "li",
      "blockquote",
      "code",
      "pre",
      "a",
      "img",
      "table",
      "thead",
      "tbody",
      "tr",
      "th",
      "td",
      "div",
      "span",
    ]);

    this.allowedAttributes = {
      a: ["href", "title", "target", "rel"],
      img: ["src", "alt", "title", "width", "height"],
      table: ["class"],
      th: ["align"],
      td: ["align"],
      code: ["class"],
      pre: ["class"],
    };
  }

  // Simple markdown parser (basic implementation)
  parseMarkdown(markdown) {
    // Sanitize input
    const sanitized = this.sanitiseInput(markdown);

    // Create container
    const container = document.createElement("div");

    // Split into lines and process
    const lines = sanitized.split("\n");
    let currentList = null;
    let inCodeBlock = false;
    let codeBlockContent = "";
    let codeBlockLanguage = "";

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      // Handle code blocks
      if (line.startsWith("```")) {
        if (!inCodeBlock) {
          // Start code block
          inCodeBlock = true;
          codeBlockLanguage = line.substring(3).trim();
          codeBlockContent = "";
          currentList = null; // End any current list
        } else {
          // End code block
          inCodeBlock = false;
          const preElement = this.createCodeBlock(
            codeBlockContent,
            codeBlockLanguage
          );
          container.appendChild(preElement);
        }
        continue;
      }

      if (inCodeBlock) {
        codeBlockContent += line + "\n";
        continue;
      }

      // Process regular lines
      const element = this.processLine(line);
      if (element) {
        // Handle lists
        if (element.tagName === "LI") {
          if (
            !currentList ||
            (line.match(/^\d+\./) && currentList.tagName !== "OL") ||
            (line.match(/^[-*+]/) && currentList.tagName !== "UL")
          ) {
            // Create new list
            currentList = line.match(/^\d+\./)
              ? document.createElement("ol")
              : document.createElement("ul");
            container.appendChild(currentList);
          }
          currentList.appendChild(element);
        } else {
          currentList = null; // End current list
          container.appendChild(element);
        }
      } else if (line.trim() === "") {
        currentList = null; // End list on empty line
      }
    }

    return container;
  }

  sanitiseInput(input) {
    return input
      .replace(/<script[^>]*>.*?<\/script>/gis, "")
      .replace(/<iframe[^>]*>.*?<\/iframe>/gis, "")
      .replace(/javascript:/gi, "")
      .replace(/on\w+\s*=/gi, "");
  }

  processLine(line) {
    const trimmed = line.trim();

    if (!trimmed) {
      return null; // Skip empty lines
    }

    // Headers
    if (trimmed.startsWith("#")) {
      return this.createHeader(trimmed);
    }

    // Horizontal rule
    if (trimmed === "---" || trimmed === "***") {
      return document.createElement("hr");
    }

    // Blockquote
    if (trimmed.startsWith(">")) {
      return this.createBlockquote(trimmed.substring(1).trim());
    }

    // Lists
    if (trimmed.match(/^[-*+]\s/) || trimmed.match(/^\d+\.\s/)) {
      return this.createListItem(trimmed);
    }

    // Regular paragraph
    return this.createParagraph(trimmed);
  }

  createHeader(line) {
    const match = line.match(/^(#{1,6})\s+(.+)$/);
    if (!match) return this.createParagraph(line);

    const level = match[1].length;
    const text = match[2];
    const header = document.createElement(`h${level}`);
    this.processInlineElements(text, header);
    return header;
  }

  createParagraph(text) {
    const p = document.createElement("p");
    this.processInlineElements(text, p);
    return p;
  }

  createBlockquote(text) {
    const blockquote = document.createElement("blockquote");
    this.processInlineElements(text, blockquote);
    return blockquote;
  }

  createListItem(text) {
    const li = document.createElement("li");
    const content = text.replace(/^[-*+]\s/, "").replace(/^\d+\.\s/, "");
    this.processInlineElements(content, li);
    return li;
  }

  createCodeBlock(content, language) {
    const pre = document.createElement("pre");
    const code = document.createElement("code");
    code.textContent = content.trim();
    if (language) {
      code.className = `language-${language}`;
    }
    pre.appendChild(code);
    return pre;
  }

  processInlineElements(text, container) {
    let remaining = text;
    let lastIndex = 0;

    // Process bold (**text**)
    const boldRegex = /\*\*(.*?)\*\*/g;
    let match;

    // For now, simple implementation - just add text
    // In production, you'd want to properly parse all inline elements
    this.addTextWithBasicFormatting(text, container);
  }

  addTextWithBasicFormatting(text, container) {
    // Simple implementation - handles basic bold and italic
    let remaining = text;

    // Handle bold
    while (remaining.includes("**")) {
      const start = remaining.indexOf("**");
      const end = remaining.indexOf("**", start + 2);

      if (end === -1) break;

      // Add text before bold
      if (start > 0) {
        const textNode = document.createTextNode(remaining.substring(0, start));
        container.appendChild(textNode);
      }

      // Add bold text
      const bold = document.createElement("strong");
      bold.textContent = remaining.substring(start + 2, end);
      container.appendChild(bold);

      remaining = remaining.substring(end + 2);
    }

    // Handle italic (single *)
    while (remaining.includes("*") && !remaining.includes("**")) {
      const start = remaining.indexOf("*");
      const end = remaining.indexOf("*", start + 1);

      if (end === -1) break;

      // Add text before italic
      if (start > 0) {
        const textNode = document.createTextNode(remaining.substring(0, start));
        container.appendChild(textNode);
      }

      // Add italic text
      const italic = document.createElement("em");
      italic.textContent = remaining.substring(start + 1, end);
      container.appendChild(italic);

      remaining = remaining.substring(end + 1);
    }

    // Add remaining text
    if (remaining) {
      const textNode = document.createTextNode(remaining);
      container.appendChild(textNode);
    }
  }
}

class MarkdownLoader {
  constructor() {
    this.renderer = new Renderer();
    this.contentContainer = document.getElementById("markdown-content");
  }

  async loadMarkdownContent(filePath) {
    if (!this.contentContainer) return;

    try {
      const response = await fetch(filePath);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const markdownContent = await response.text();

      while (this.contentContainer.firstChild) {
        this.contentContainer.removeChild(this.contentContainer.firstChild);
      }

      const renderedContent = this.renderer.parseMarkdown(markdownContent);
      this.contentContainer.appendChild(renderedContent);
    } catch (error) {
      console.error("Error loading markdown content:", error);
      this.showError("Failed to load content. Please try again later.");
    }
  }

  showError(message) {
    if (!this.contentContainer) return;

    while (this.contentContainer.firstChild) {
      this.contentContainer.removeChild(this.contentContainer.firstChild);
    }

    const errorDiv = document.createElement("div");
    errorDiv.className = "error-message";
    errorDiv.textContent = message;
    this.contentContainer.appendChild(errorDiv);
  }
}
