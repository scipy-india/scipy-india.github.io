class SpecialHeader extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
    <img src="assets/SciPy-India-logo.png" alt="SciPy India Logo" class="logo">
    <h1>SciPy India</h1>
    <nav>
      <ul class="navbar">
        <li><a href="index.html">Home</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="coc.html">Code of Conduct</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
    </nav>
    `;
  }
}

class SpecialFooter extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
    <hr>
    <p>Connect with us:</p>
    <a href="https://scipyindia.zulipchat.com/join/4mesdxfbbpl4titgtdzx4iwv/" target="_blank">Zulip</a> |
    <a href="https://bsky.app/profile/scipyindia.bsky.social" target="_blank">Bluesky</a> |
    <a href="https://www.linkedin.com/company/scipyindia" target="_blank">LinkedIn</a> |
    <a href="https://fosstodon.org/@scipyindia" target="_blank">Mastodon</a> |
    <a href="https://github.com/orgs/scipy-india/discussions" target="_blank">GitHub Discussions</a>
    `;
  }
}

customElements.define('special-header', SpecialHeader);
customElements.define('special-footer', SpecialFooter);