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

  parseMarkdown(markdown) {
    // Sanitise input
    const sanitised = this.sanitiseInput(markdown);
    const container = document.createElement("div");

    const lines = sanitised.split("\n");
    let currentList = null;
    let inCodeBlock = false;
    let codeBlockContent = "";
    let codeBlockLanguage = "";

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      // Skip markdown comments
      if (line.trim().startsWith("%") || line.trim().match(/^<!--.*-->$/)) {
        continue;
      }

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

      // Handle tables
      if (this.isTableLine(line)) {
        currentList = null;
        const tableLines = [line];

        while (i + 1 < lines.length && this.isTableLine(lines[i + 1])) {
          i++;
          tableLines.push(lines[i]);
        }

        const tableElement = this.createTable(tableLines);
        if (tableElement) {
          container.appendChild(tableElement);
        }
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
    let sanitised = input
      .replace(/<script[^>]*>.*?<\/script>/gis, "")
      .replace(/<iframe[^>]*>.*?<\/iframe>/gis, "")
      .replace(/javascript:/gi, "")
      .replace(/on\w+\s*=/gi, "");

    // Remove HTML comments, but keep markdown comments for processing.
    sanitised = sanitised.replace(/<!--[\s\S]*?-->/g, "");

    return sanitised;
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

  isTableLine(line) {
    const trimmed = line.trim();
    // A table line should contain at least one pipe character,
    // and should start/end with pipes or have pipes in between.
    return trimmed.includes("|") && trimmed.length > 0;
  }

  createTable(lines) {
    if (lines.length < 2) return null;

    // Parse header row,
    // Check if second line is a separator,
    // Parse alignment from separator row,
    // Create table element,
    // Create thead,
    // Create tbody,
    // Parse data rows (skip header and separator).
    const headerCells = this.parseTableRow(lines[0]);
    if (!headerCells || headerCells.length === 0) return null;

    const separatorMatch = lines[1].match(/^\s*\|?(\s*:?-+:?\s*\|)+\s*:?-+:?\s*\|?\s*$/);
    if (!separatorMatch) return null;

    const alignments = this.parseTableAlignment(lines[1], headerCells.length);

    const table = document.createElement("table");

    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");

    headerCells.forEach((cellContent, index) => {
      const th = document.createElement("th");
      if (alignments[index]) {
        th.setAttribute("align", alignments[index]);
      }
      this.processInlineElements(cellContent, th);
      headerRow.appendChild(th);
    });

    thead.appendChild(headerRow);
    table.appendChild(thead);

    const tbody = document.createElement("tbody");

    for (let i = 2; i < lines.length; i++) {
      const cells = this.parseTableRow(lines[i]);
      if (!cells) continue;

      const row = document.createElement("tr");
      cells.forEach((cellContent, index) => {
        const td = document.createElement("td");
        if (alignments[index]) {
          td.setAttribute("align", alignments[index]);
        }
        this.processInlineElements(cellContent, td);
        row.appendChild(td);
      });

      tbody.appendChild(row);
    }

    table.appendChild(tbody);
    return table;
  }

  parseTableRow(line) {
    const trimmed = line.trim();

    // Remove leading and trailing pipes
    let content = trimmed;
    if (content.startsWith("|")) {
      content = content.substring(1);
    }
    if (content.endsWith("|")) {
      content = content.substring(0, content.length - 1);
    }

    // Split by pipes and trim each cell.
    const cells = content.split("|").map((cell) => cell.trim());

    return cells.length > 0 ? cells : null;
  }

  parseTableAlignment(separatorLine, columnCount) {
    const cells = this.parseTableRow(separatorLine);
    const alignments = [];

    for (let i = 0; i < columnCount; i++) {
      const cell = cells[i] || "";
      const trimmed = cell.trim();

      const startsWithColon = trimmed.startsWith(":");
      const endsWithColon = trimmed.endsWith(":");

      if (startsWithColon && endsWithColon) {
        alignments.push("center");
      } else if (endsWithColon) {
        alignments.push("right");
      } else if (startsWithColon) {
        alignments.push("left");
      } else {
        alignments.push("left"); // left is our default alignment
      }
    }

    return alignments;
  }

  processInlineElements(text, container) {
    const elements = this.parseInlineMarkdown(text);

    elements.forEach((element) => {
      container.appendChild(element);
    });
  }

  parseInlineMarkdown(text) {
    const elements = [];
    let remaining = text;
    let position = 0;

    while (position < remaining.length) {
      // Find the next markdown element
      const nextMarkdown = this.findNextInlineMarkdown(remaining, position);

      if (nextMarkdown === null) {
        // No more markdown, add remaining text
        if (position < remaining.length) {
          const textNode = document.createTextNode(
            remaining.substring(position)
          );
          elements.push(textNode);
        }
        break;
      }

      // Add text before the markdown element
      if (nextMarkdown.start > position) {
        const textNode = document.createTextNode(
          remaining.substring(position, nextMarkdown.start)
        );
        elements.push(textNode);
      }

      // Create the markdown element
      const element = this.createInlineElement(
        nextMarkdown.type,
        nextMarkdown.content,
        nextMarkdown.url
      );
      elements.push(element);

      position = nextMarkdown.end;
    }

    return elements;
  }

  findNextInlineMarkdown(text, startPos) {
    const patterns = [
      { regex: /!\[([^\]]*)\]\(([^)]+)\)/g, type: "image" }, // ![alt](url)
      { regex: /\[([^\]]+)\]\(([^)]+)\)/g, type: "link" }, // [text](url)
      { regex: /`([^`]+)`/g, type: "code" }, // `text`
      { regex: /\*\*([^*]+)\*\*/g, type: "bold" }, // **text**
      { regex: /\*([^*]+)\*/g, type: "italic" }, // *text*
      { regex: /_([^_]+)_/g, type: "italic" }, // _text_
    ];

    let earliest = null;

    patterns.forEach((pattern) => {
      pattern.regex.lastIndex = startPos;
      const match = pattern.regex.exec(text);

      if (match && (earliest === null || match.index < earliest.start)) {
        earliest = {
          start: match.index,
          end: match.index + match[0].length,
          type: pattern.type,
          content: match[1],
          url: match[2] || null, // For links
          fullMatch: match[0],
        };
      }
    });

    return earliest;
  }

  createInlineElement(type, content, url = null) {
    switch (type) {
      case "image":
        const img = document.createElement("img");
        img.src = this.sanitiseUrl(url);
        img.alt = content || "Image";
        img.loading = "lazy";
        img.style.maxWidth = "100%";
        img.style.height = "auto";

        // Add error handling
        img.onerror = function () {
          this.alt = `Image failed to load: ${content || "Unknown"}`;
          this.style.display = "inline";
          this.style.backgroundColor = "#f0f0f0";
          this.style.padding = "0.5rem";
          this.style.border = "1px dashed #ccc";
          this.style.borderRadius = "4px";
        };

        return img;

      case "link":
        const link = document.createElement("a");
        link.href = this.sanitiseUrl(url);

        // Parse link content; we need to deal with nested formatting
        // like [**bold link**](url) or [*italic link*](url) in links.
        const linkElements = this.parseInlineMarkdown(content);
        linkElements.forEach((element) => {
          link.appendChild(element);
        });

        link.target = "_blank";
        link.rel = "noopener noreferrer";
        return link;

      case "bold":
        const bold = document.createElement("strong");

        const boldElements = this.parseInlineMarkdown(content);
        boldElements.forEach((element) => {
          bold.appendChild(element);
        });

        return bold;

      case "italic":
        const italic = document.createElement("em");

        const italicElements = this.parseInlineMarkdown(content);
        italicElements.forEach((element) => {
          italic.appendChild(element);
        });

        return italic;

      case "code":
        const code = document.createElement("code");
        code.textContent = content;
        return code;

      default:
        return document.createTextNode(content);
    }
  }

  sanitiseUrl(url) {
    if (!url) return "#";

    // Allow base64 images before sanitisation
    if (url.startsWith("data:image/")) {
      return url;
    }

    const cleaned = url
      .trim()
      .replace(/javascript:/gi, "")
      .replace(/data:/gi, "")
      .replace(/vbscript:/gi, "");
    if (
      cleaned.startsWith("http://") ||
      cleaned.startsWith("https://") ||
      cleaned.startsWith("/") ||
      cleaned.startsWith("./") ||
      cleaned.startsWith("../")
    ) {
      return cleaned;
    }

    // If it doesn't start with a protocol, assume it's a relative URL
    return cleaned.startsWith("#") ? cleaned : `#${cleaned}`;
  }

  addTextWithBasicFormatting(text, container) {
    // This method is now replaced by processInlineElements
    // I'm keeping it for backward compatibility, but it will delegate
    // to the new system.
    this.processInlineElements(text, container);
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
