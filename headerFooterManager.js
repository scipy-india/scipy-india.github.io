class SpecialHeader extends HTMLElement {
  connectedCallback() {
      const logo = document.createElement('img');
      logo.src = 'assets/SciPy-India-logo.png';
      logo.alt = 'SciPy India Logo';
      logo.className = 'logo';

      const title = document.createElement('h1');
      title.textContent = 'SciPy India';

      const nav = document.createElement('nav');
      const ul = document.createElement('ul');
      ul.className = 'navbar';

      const links = [
        { href: 'index.html', text: 'Home' },
        { href: 'about.html', text: 'About' },
        { href: 'blogs.html', text: 'Blogs' },
        { href: 'coc.html', text: 'Code of Conduct' },
        { href: 'contact.html', text: 'Contact' }
      ];

      links.forEach(link => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = link.href;
        a.textContent = link.text;
        li.appendChild(a);
        ul.appendChild(li);
      });

      nav.appendChild(ul);

      this.appendChild(logo);
      this.appendChild(title);
      this.appendChild(nav);
  }
}

class SpecialFooter extends HTMLElement {
  connectedCallback() {
      const hr = document.createElement('hr');
      const p = document.createElement('p');
      p.textContent = 'Connect with us:';

      const links = [
        { href: 'https://scipyindia.zulipchat.com/join/4mesdxfbbpl4titgtdzx4iwv/', text: 'Zulip' },
        { href: 'https://bsky.app/profile/scipyindia.bsky.social', text: 'Bluesky' },
        { href: 'https://www.linkedin.com/company/scipyindia', text: 'LinkedIn' },
        { href: 'https://fosstodon.org/@scipyindia', text: 'Mastodon' },
        { href: 'https://github.com/orgs/scipy-india/discussions', text: 'GitHub Discussions' }
      ];

      const fragment = document.createDocumentFragment();
      links.forEach((link, idx) => {
        const a = document.createElement('a');
        a.href = link.href;
        a.textContent = link.text;
        a.target = '_blank';
        fragment.appendChild(a);
        if (idx < links.length - 1) {
          fragment.appendChild(document.createTextNode(' | '));
        }
      });

      this.appendChild(hr);
      this.appendChild(p);
      this.appendChild(fragment);
  }
}

customElements.define('special-header', SpecialHeader);
customElements.define('special-footer', SpecialFooter);