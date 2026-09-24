(() => {
  'use strict';

  const header = document.querySelector('.site-header');
  const menuButton = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav');
  const dropdownItems = [...document.querySelectorAll('.nav-item.has-submenu')];
  const mobileMenu = window.matchMedia('(max-width: 1160px)');
  const setDropdownState = (item, open) => {
    item.classList.toggle('open', open);
    const toggle = item.querySelector('.nav-caret');
    const label = item.querySelector('.nav-link')?.textContent?.trim() || 'Menü';
    toggle?.setAttribute('aria-expanded', String(open));
    toggle?.setAttribute('aria-label', `${label} alt menüsünü ${open ? 'kapat' : 'aç'}`);
  };

  const closeDropdowns = () => dropdownItems.forEach((item) => setDropdownState(item, false));
  const openDropdown = (item) => {
    closeDropdowns();
    setDropdownState(item, true);
  };

  const setMenu = (open) => {
    document.body.classList.toggle('nav-open', open);
    menuButton?.setAttribute('aria-expanded', String(open));
    menuButton?.setAttribute('aria-label', open ? 'Menüyü kapat' : 'Menüyü aç');
    if (nav) nav.inert = mobileMenu.matches && !open;
    if (!open) closeDropdowns();
  };

  setMenu(false);
  mobileMenu.addEventListener('change', () => setMenu(false));
  menuButton?.addEventListener('click', () => setMenu(!document.body.classList.contains('nav-open')));
  nav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => setMenu(false)));
  dropdownItems.forEach((item) => {
    const toggle = item.querySelector('.nav-caret');
    toggle?.addEventListener('click', () => item.classList.contains('open') ? closeDropdowns() : openDropdown(item));
    item.addEventListener('mouseenter', () => {
      if (window.matchMedia('(hover: hover) and (min-width: 1161px)').matches) openDropdown(item);
    });
    item.addEventListener('mouseleave', () => {
      if (window.matchMedia('(hover: hover) and (min-width: 1161px)').matches) closeDropdowns();
    });
    item.addEventListener('focusout', (event) => {
      if (!item.contains(event.relatedTarget)) closeDropdowns();
    });
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      const wasOpen = document.body.classList.contains('nav-open');
      setMenu(false);
      closeDropdowns();
      if (wasOpen) menuButton?.focus();
    }
  });
  document.addEventListener('click', (event) => {
    if (!header?.contains(event.target)) { setMenu(false); closeDropdowns(); }
  });
  document.querySelector('.nav-backdrop')?.addEventListener('click', () => setMenu(false));

  const onScroll = () => {
    header?.classList.toggle('scrolled', window.scrollY > 20);
    if (header) document.documentElement.style.setProperty('--nav-top', `${Math.max(0, Math.round(header.getBoundingClientRect().bottom))}px`);
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealItems = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reducedMotion) {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: .12, rootMargin: '0px 0px -35px 0px' });
    revealItems.forEach((item) => revealObserver.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add('visible'));
  }

  const counters = document.querySelectorAll('[data-count]');
  const animateCount = (node) => {
    const end = Number(node.dataset.count);
    if (!Number.isFinite(end)) return;
    if (reducedMotion) { node.textContent = end; return; }
    const start = performance.now();
    const duration = 1300;
    const frame = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      node.textContent = Math.round(end * eased);
      if (progress < 1) requestAnimationFrame(frame);
    };
    requestAnimationFrame(frame);
  };
  if ('IntersectionObserver' in window) {
    const counterObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) { animateCount(entry.target); observer.unobserve(entry.target); }
      });
    }, { threshold: .7 });
    counters.forEach((counter) => counterObserver.observe(counter));
  } else counters.forEach(animateCount);

  const filterButtons = document.querySelectorAll('[data-filter]');
  const projectCards = document.querySelectorAll('[data-category]');
  const setFilter = (filter, updateUrl = false) => {
    if (![...filterButtons].some((button) => button.dataset.filter === filter)) return;
    filterButtons.forEach((button) => { button.classList.toggle('active', button.dataset.filter === filter); button.setAttribute('aria-pressed', String(button.dataset.filter === filter)); });
    projectCards.forEach((card) => { card.hidden = filter !== 'all' && card.dataset.category !== filter; });
    if (updateUrl) history.replaceState(null, '', `${location.pathname}${filter === 'all' ? '' : `?filter=${filter}`}${location.hash}`);
  };
  filterButtons.forEach((button) => button.addEventListener('click', () => setFilter(button.dataset.filter, true)));
  const requestedFilter = new URLSearchParams(location.search).get('filter');
  if (requestedFilter) setFilter(requestedFilter);

  const quotes = [
    { text: 'Mihenk ekibi, karmaşık bir dönüşümü herkesin anlayabileceği bir yol haritasına çevirdi. Bugün daha hızlı karar alıyor ve aynı hedefe birlikte yürüyoruz.', name: 'Selin Arslan', role: 'Genel Müdür, Atlas Grup' },
    { text: 'Bize yalnızca bir strateji sunmadılar; onu hayata geçirecek ritmi ve çalışma biçimini de birlikte kurdular. Sonuçları ilk çeyrekte görmeye başladık.', name: 'Mert Kara', role: 'Kurucu Ortak, Luma Teknoloji' },
    { text: 'Sahadaki gerçekleri dinleyen ve sayıları aynı titizlikle okuyan bir ekip. Büyüme kararlarımızı artık çok daha net bir zeminde veriyoruz.', name: 'Derya Aksoy', role: 'CEO, Vero Retail' }
  ];
  let quoteIndex = 0;
  const quoteText = document.querySelector('[data-quote-text]');
  const quoteName = document.querySelector('[data-quote-name]');
  const quoteRole = document.querySelector('[data-quote-role]');
  document.querySelectorAll('[data-quote-direction]').forEach((button) => button.addEventListener('click', () => {
    quoteIndex = (quoteIndex + Number(button.dataset.quoteDirection) + quotes.length) % quotes.length;
    if (quoteText) quoteText.textContent = `“${quotes[quoteIndex].text}”`;
    if (quoteName) quoteName.textContent = quotes[quoteIndex].name;
    if (quoteRole) quoteRole.textContent = quotes[quoteIndex].role;
  }));

  const form = document.querySelector('[data-contact-form]');
  form?.addEventListener('submit', (event) => {
    event.preventDefault();
    const status = form.querySelector('.form-status');
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const subject = encodeURIComponent(`Mihenk iletişim: ${data.get('subject')}`);
    const body = encodeURIComponent(`Ad Soyad: ${data.get('name')}\nE-posta: ${data.get('email')}\nTelefon: ${data.get('phone') || 'Belirtilmedi'}\n\nMesaj:\n${data.get('message')}`);
    if (status) status.textContent = 'E-posta uygulamanız açılıyor. Göndermek için e-postayı onaylayın.';
    window.location.href = `mailto:merhaba@example.com?subject=${subject}&body=${body}`;
  });

  const blogSearch = document.querySelector('[data-blog-search]');
  const blogCategoryButtons = [...document.querySelectorAll('[data-blog-category]')];
  const blogCards = [...document.querySelectorAll('[data-blog-card]')];
  if (blogSearch && blogCards.length) {
    const count = document.querySelector('[data-blog-result-count]');
    const empty = document.querySelector('[data-blog-empty]');
    let category = 'all';
    const applyBlogFilter = (updateUrl = true) => {
      const query = blogSearch.value.trim().toLocaleLowerCase('tr-TR');
      let visible = 0;
      blogCards.forEach((card) => {
        const matchesCategory = category === 'all' || card.dataset.category === category;
        const matchesQuery = !query || (card.dataset.search || '').toLocaleLowerCase('tr-TR').includes(query);
        card.hidden = !(matchesCategory && matchesQuery);
        if (!card.hidden) visible += 1;
      });
      blogCategoryButtons.forEach((button) => {
        const selected = button.dataset.blogCategory === category;
        button.classList.toggle('active', selected);
        button.setAttribute('aria-pressed', String(selected));
      });
      if (count) count.textContent = `${visible} yazı gösteriliyor`;
      if (empty) empty.hidden = visible !== 0;
      if (updateUrl) {
        const params = new URLSearchParams();
        if (category !== 'all') params.set('category', category);
        if (blogSearch.value.trim()) params.set('q', blogSearch.value.trim());
        history.replaceState(null, '', `${location.pathname}${params.size ? `?${params}` : ''}${location.hash}`);
      }
    };
    const params = new URLSearchParams(location.search);
    if (blogCategoryButtons.some((button) => button.dataset.blogCategory === params.get('category'))) category = params.get('category');
    blogSearch.value = params.get('q') || '';
    applyBlogFilter(false);
    blogSearch.addEventListener('input', () => applyBlogFilter());
    blogCategoryButtons.forEach((button) => button.addEventListener('click', () => {
      category = button.dataset.blogCategory;
      applyBlogFilter();
    }));
    document.querySelector('[data-blog-reset]')?.addEventListener('click', () => {
      category = 'all';
      blogSearch.value = '';
      applyBlogFilter();
      blogSearch.focus();
    });
  }

  const article = document.querySelector('[data-article-slug]');
  if (article) {
    const progressBar = document.querySelector('[data-reading-progress]');
    const updateReadingProgress = () => {
      if (!progressBar) return;
      const top = article.offsetTop;
      const max = Math.max(1, article.offsetHeight - innerHeight);
      const progress = Math.min(1, Math.max(0, (scrollY - top) / max));
      progressBar.style.transform = `scaleX(${progress})`;
    };
    updateReadingProgress();
    window.addEventListener('scroll', updateReadingProgress, { passive: true });
    window.addEventListener('resize', updateReadingProgress, { passive: true });

    const shareStatus = document.querySelector('[data-share-status]');
    document.querySelectorAll('[data-share]').forEach((button) => button.addEventListener('click', async () => {
      const url = location.href.split('#')[0];
      if (button.dataset.share === 'copy') {
        try {
          await navigator.clipboard.writeText(url);
          if (shareStatus) shareStatus.textContent = 'Bağlantı kopyalandı.';
        } catch {
          if (shareStatus) shareStatus.textContent = 'Bağlantı kopyalanamadı; adres çubuğundan kopyalayabilirsiniz.';
        }
        return;
      }
      const encodedUrl = encodeURIComponent(url);
      const title = encodeURIComponent(document.title);
      const shareTarget = button.dataset.share === 'linkedin'
        ? `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`
        : `https://twitter.com/intent/tweet?url=${encodedUrl}&text=${title}`;
      window.open(shareTarget, '_blank', 'noopener,noreferrer');
    }));

    const commentList = document.querySelector('[data-comment-list]');
    const commentForm = document.querySelector('[data-comment-form]');
    const commentStatus = document.querySelector('[data-comment-status]');
    const commentCount = document.querySelector('[data-comment-count]');
    const storageKey = `mihenk-comments-${article.dataset.articleSlug}`;
    let savedComments = [];
    try {
      const stored = JSON.parse(localStorage.getItem(storageKey) || '[]');
      if (Array.isArray(stored)) savedComments = stored.filter((item) => typeof item.name === 'string' && typeof item.comment === 'string');
    } catch { savedComments = []; }
    const renderComment = (entry) => {
      const wrapper = document.createElement('div');
      wrapper.className = 'comment';
      const initials = entry.name.trim().split(/\s+/).slice(0, 2).map((part) => part[0]?.toLocaleUpperCase('tr-TR') || '').join('');
      const avatar = document.createElement('span');
      avatar.className = 'comment-avatar';
      avatar.setAttribute('aria-hidden', 'true');
      avatar.textContent = initials;
      const content = document.createElement('div');
      const top = document.createElement('div');
      top.className = 'comment-top';
      const name = document.createElement('strong');
      name.textContent = entry.name;
      const date = document.createElement('span');
      date.textContent = entry.date;
      const message = document.createElement('p');
      message.textContent = entry.comment;
      top.append(name, date);
      content.append(top, message);
      wrapper.append(avatar, content);
      commentList?.append(wrapper);
    };
    savedComments.forEach(renderComment);
    if (commentCount) commentCount.textContent = String(2 + savedComments.length);
    commentForm?.addEventListener('submit', (event) => {
      event.preventDefault();
      if (!commentForm.reportValidity()) return;
      const data = new FormData(commentForm);
      const entry = {
        name: String(data.get('name') || '').trim().slice(0, 50),
        comment: String(data.get('comment') || '').trim().slice(0, 1000),
        date: new Intl.DateTimeFormat('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }).format(new Date())
      };
      if (!entry.name || entry.comment.length < 10) {
        if (commentStatus) commentStatus.textContent = 'Lütfen adınızı ve en az 10 karakterlik yorumunuzu yazın.';
        return;
      }
      savedComments.push(entry);
      renderComment(entry);
      if (commentCount) commentCount.textContent = String(2 + savedComments.length);
      try {
        localStorage.setItem(storageKey, JSON.stringify(savedComments));
        if (commentStatus) commentStatus.textContent = 'Yorumunuz bu tarayıcıda kaydedildi.';
      } catch {
        if (commentStatus) commentStatus.textContent = 'Yorum eklendi ancak bu tarayıcıda kalıcı olarak saklanamadı.';
      }
      commentForm.reset();
    });
  }

  document.querySelectorAll('[data-year]').forEach((node) => { node.textContent = new Date().getFullYear(); });
})();
