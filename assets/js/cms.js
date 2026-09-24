(() => {
  'use strict';

  const root = document.querySelector('[data-cms-page]');
  const page = root?.dataset.cmsPage || '';
  let session = null;
  let items = [];
  let editing = null;
  let removing = null;
  let pickerTarget = null;
  let toastTimer = null;

  const labels = { blog: 'yazı', projects: 'proje', services: 'hizmet', testimonials: 'yorum', inquiries: 'talep', media: 'görsel', users: 'üye' };
  const roleLabels = { admin: 'Yönetici', editor: 'Editör', viewer: 'Görüntüleyici' };
  const statusLabels = { published: 'Yayında', draft: 'Taslak', new: 'Yeni', in_progress: 'İşlemde', done: 'Tamamlandı', archived: 'Arşiv', active: 'Aktif', passive: 'Pasif' };
  const contentKinds = new Set(['blog', 'projects', 'services', 'testimonials']);

  const schema = {
    blog: [
      { key: 'title', label: 'Yazı başlığı', required: true, full: true },
      { key: 'category', label: 'Kategori', type: 'select', options: [['strateji', 'Strateji'], ['dijital', 'Dijital dönüşüm'], ['operasyon', 'Operasyon'], ['liderlik', 'Liderlik'], ['surdurulebilirlik', 'Sürdürülebilirlik']] },
      { key: 'author', label: 'Yazar', required: true },
      { key: 'excerpt', label: 'Kısa özet', type: 'textarea', required: true, full: true },
      { key: 'body', label: 'Yazı içeriği', type: 'textarea', required: true, full: true, large: true, hint: 'Paragrafları boş satırla ayırın. Başlıklar ve madde işaretleri düz metin olarak yazılabilir.' },
      { key: 'image', label: 'Kapak görseli', type: 'media', full: true },
      { key: 'publishedAt', label: 'Yayın tarihi', type: 'date' },
      { key: 'sortOrder', label: 'Sıralama', type: 'number' },
      { key: 'status', label: 'Durum', type: 'select', options: [['draft', 'Taslak'], ['published', 'Yayında']] },
    ],
    projects: [
      { key: 'title', label: 'Proje başlığı', required: true, full: true },
      { key: 'category', label: 'Kategori', type: 'select', options: [['strategy', 'Strateji'], ['digital', 'Dijital'], ['operations', 'Operasyon']] },
      { key: 'sector', label: 'Sektör', required: true },
      { key: 'summary', label: 'Proje özeti', type: 'textarea', required: true, full: true },
      { key: 'image', label: 'Proje görseli', type: 'media', full: true },
      { key: 'progress', label: 'İlerleme (%)', type: 'number', min: 0, max: 100 },
      { key: 'sortOrder', label: 'Sıralama', type: 'number' },
      { key: 'status', label: 'Görünürlük', type: 'select', options: [['draft', 'Taslak'], ['published', 'Yayında']] },
    ],
    services: [
      { key: 'title', label: 'Hizmet adı', required: true, full: true },
      { key: 'category', label: 'Alan kodu', required: true, hint: 'Örnek: strateji, dijital, finans' },
      { key: 'sortOrder', label: 'Sıralama', type: 'number' },
      { key: 'summary', label: 'Kısa açıklama', type: 'textarea', required: true, full: true },
      { key: 'body', label: 'Detay', type: 'textarea', full: true },
      { key: 'status', label: 'Görünürlük', type: 'select', options: [['draft', 'Taslak'], ['published', 'Yayında']] },
    ],
    testimonials: [
      { key: 'title', label: 'Müşteri adı', required: true, full: true },
      { key: 'role', label: 'Unvan / kurum', required: true, full: true },
      { key: 'quote', label: 'Yorum', type: 'textarea', required: true, full: true, large: true },
      { key: 'sortOrder', label: 'Sıralama', type: 'number' },
      { key: 'status', label: 'Görünürlük', type: 'select', options: [['draft', 'Taslak'], ['published', 'Yayında']] },
    ],
    inquiries: [
      { key: 'name', label: 'Ad Soyad', readonly: true },
      { key: 'email', label: 'E-posta', readonly: true },
      { key: 'phone', label: 'Telefon', readonly: true },
      { key: 'subject', label: 'Konu', readonly: true },
      { key: 'message', label: 'Mesaj', type: 'textarea', readonly: true, full: true, large: true },
      { key: 'status', label: 'Durum', type: 'select', options: [['new', 'Yeni'], ['in_progress', 'İşlemde'], ['done', 'Tamamlandı'], ['archived', 'Arşiv']] },
      { key: 'assignee', label: 'Sorumlu kişi' },
      { key: 'notes', label: 'Dahili notlar', type: 'textarea', full: true },
    ],
    users: [
      { key: 'name', label: 'Ad Soyad', required: true, full: true },
      { key: 'email', label: 'E-posta', type: 'email', required: true, full: true },
      { key: 'role', label: 'Rol', type: 'select', options: [['viewer', 'Görüntüleyici'], ['editor', 'Editör'], ['admin', 'Yönetici']] },
      { key: 'active', label: 'Hesap durumu', type: 'select', options: [['1', 'Aktif'], ['0', 'Pasif']] },
    ],
    media: [
      { key: 'file', label: 'Görsel dosyası', type: 'file', required: true, full: true, hint: 'JPEG, PNG veya WebP · önizleme için en çok 1 MB' },
      { key: 'name', label: 'Dosya adı / başlık', required: true, full: true },
      { key: 'alt', label: 'Alternatif metin', full: true, hint: 'Görselin içeriğini kısa ve anlamlı biçimde anlatın.' },
    ],
  };

  const demoData = {
    blog: [
      { id: 1, title: 'Belirsizlikte net kararlar', status: 'published', data: { category: 'strateji', author: 'Mihenk Editör', excerpt: 'Değişen koşullarda doğru karar için bir çerçeve.', body: 'Strateji, iyi sorularla başlar.\n\nEkiplerin birlikte karar almasını sağlayan ritimler kurun.', image: 'assets/images/blog-strategy.webp', publishedAt: '2026-09-18', sortOrder: 1 } },
      { id: 2, title: 'Dijital dönüşüm insanla başlar', status: 'published', data: { category: 'dijital', author: 'Mihenk Editör', excerpt: 'Teknolojinin kalıcı etki üretmesi için insan odağı.', body: 'Dönüşüm, teknoloji seçiminin ötesinde bir kültür işidir.', image: 'assets/images/blog-digital.webp', publishedAt: '2026-09-12', sortOrder: 2 } },
      { id: 3, title: 'Veriyle karar alma kültürü', status: 'draft', data: { category: 'operasyon', author: 'Mihenk Editör', excerpt: 'Veriyi ortak bir karar diline dönüştürmek.', body: 'Ölçümün değeri, doğru soruyu yanıtlamasında saklıdır.', image: 'assets/images/blog-data.webp', sortOrder: 3 } },
    ],
    projects: [
      { id: 1, title: 'Dijital dönüşüm yol haritası', status: 'published', data: { category: 'digital', sector: 'Teknoloji', summary: 'Kurum genelinde öncelikleri netleştiren dönüşüm programı.', image: 'assets/images/architecture.webp', progress: 78, sortOrder: 1 } },
      { id: 2, title: 'Operasyonel verimlilik', status: 'published', data: { category: 'operations', sector: 'Perakende', summary: 'Süreçler ve ekipler arasında daha yalın bir çalışma modeli.', image: 'assets/images/operations.webp', progress: 54, sortOrder: 2 } },
      { id: 3, title: 'Büyüme stratejisi 2027', status: 'draft', data: { category: 'strategy', sector: 'Finans', summary: 'Yeni pazarlara açılma ve odak alanlarını belirleme.', image: 'assets/images/strategy-team.webp', progress: 92, sortOrder: 3 } },
    ],
    services: [
      { id: 1, title: 'Strateji Danışmanlığı', status: 'published', data: { category: 'strateji', summary: 'Geleceğe yönelik net yön ve öncelikler.', body: 'Hedefleri, fırsatları ve uygulama adımlarını birlikte tasarlarız.', sortOrder: 1 } },
      { id: 2, title: 'Dijital Dönüşüm', status: 'published', data: { category: 'dijital', summary: 'Teknoloji ve insan odağında dönüşüm.', body: 'Dönüşüm yol haritasını ölçülebilir adımlara ayırırız.', sortOrder: 2 } },
      { id: 3, title: 'Operasyonel Mükemmellik', status: 'draft', data: { category: 'operasyon', summary: 'Daha verimli süreç ve ekip yapısı.', body: 'Süreçleri analiz eder ve iyileştirme fırsatlarını belirleriz.', sortOrder: 3 } },
    ],
    testimonials: [
      { id: 1, title: 'Deniz Arslan', status: 'published', data: { role: 'Genel Müdür · Teknoloji', quote: 'Mihenk ekibi karmaşık kararları net bir yol haritasına dönüştürmemize yardımcı oldu.', sortOrder: 1 } },
      { id: 2, title: 'Selin Demir', status: 'published', data: { role: 'Operasyon Direktörü · Perakende', quote: 'Birlikte oluşturduğumuz çalışma modeli ekiplerimiz için somut sonuçlar üretti.', sortOrder: 2 } },
    ],
    inquiries: [
      { id: 1, name: 'Ece Aydın', email: 'ece@ornek.com', phone: '+90 555 000 00 01', subject: 'Strateji görüşmesi', message: 'Yeni dönem planlamamız için danışmanlık teklifi almak istiyoruz.', status: 'new', assignee: '', notes: '' },
      { id: 2, name: 'Mert Yıldız', email: 'mert@ornek.com', phone: '+90 555 000 00 02', subject: 'Dijital dönüşüm', message: 'Ekiplerimiz için dönüşüm yol haritası hakkında görüşebilir miyiz?', status: 'in_progress', assignee: 'Ayşe Yılmaz', notes: 'İlk görüşme planlanacak.' },
      { id: 3, name: 'Aslı Çetin', email: 'asli@ornek.com', phone: '', subject: 'Proje iş birliği', message: 'Kurumumuz adına iş birliği seçeneklerini öğrenmek istiyorum.', status: 'done', assignee: 'Mert Kara', notes: 'Örnek çalışma paylaşıldı.' },
    ],
    users: [
      { id: 1, name: 'Ayşe Yılmaz', email: 'ayse.yilmaz@mihenk.com', role: 'admin', active: true },
      { id: 2, name: 'Mert Kara', email: 'mert.kara@mihenk.com', role: 'editor', active: true },
      { id: 3, name: 'Selin Arslan', email: 'selin.arslan@mihenk.com', role: 'editor', active: true },
      { id: 4, name: 'Derya Aksoy', email: 'derya.aksoy@mihenk.com', role: 'viewer', active: true },
    ],
    media: ['hero-team.webp', 'strategy-team.webp', 'architecture.webp', 'operations.webp', 'blog-strategy.webp', 'blog-digital.webp', 'blog-operations.webp', 'blog-data.webp'].map((name, index) => ({ id: index + 1, name, alt: name.replace('.webp', '').replaceAll('-', ' '), url: `assets/images/${name}`, size: 0, system: true })),
    seo: [
      ['index.html', 'Ana Sayfa'], ['about.html', 'Hakkımızda'], ['services.html', 'Hizmetler'], ['projects.html', 'Projeler'], ['blog.html', 'Blog'], ['contact.html', 'İletişim']
    ].map(([page, label]) => ({ page, title: `${label} | Mihenk Danışmanlık`, description: 'Mihenk Danışmanlık ile strateji, dönüşüm ve sürdürülebilir büyüme için net adımlar atın.', og_image: 'assets/images/hero-team.webp' })),
  };

  function readCollection(kind) {
    try { return JSON.parse(localStorage.getItem(`mihenk-cms-${kind}`)) || structuredClone(demoData[kind]); }
    catch { return structuredClone(demoData[kind]); }
  }

  function writeCollection(kind, collection) {
    try { localStorage.setItem(`mihenk-cms-${kind}`, JSON.stringify(collection)); }
    catch { throw new Error('Tarayıcı depolama alanı dolu. Daha küçük bir görsel deneyin.'); }
  }

  async function request(path, options = {}) {
    if (path === '/api/auth/session') return { authenticated: true, user: { id: 1, name: readProfileName(), role: 'admin' } };
    if (path === '/api/summary') return { totals: Object.fromEntries(['projects', 'users', 'inquiries', 'blog'].map((kind) => [kind, readCollection(kind).length])) };
    const match = path.match(/^\/api\/(?:content\/)?(blog|projects|services|testimonials|inquiries|media|users|seo)(?:\/(.+))?$/);
    if (!match) throw new Error('Önizleme işlemi bulunamadı.');
    const [, kind, id] = match;
    const collection = readCollection(kind);
    const method = options.method || 'GET';
    if (method === 'GET') return { items: collection };
    const body = options.body || {};
    const index = collection.findIndex((item) => String(kind === 'seo' ? item.page : item.id) === id);
    if (method === 'DELETE') {
      if (index < 0) throw new Error('Kayıt bulunamadı.');
      collection.splice(index, 1);
      writeCollection(kind, collection);
      return { ok: true };
    }
    if (method === 'PUT' && index < 0) throw new Error('Kayıt bulunamadı.');
    let item;
    if (kind === 'seo') item = { page: id, title: body.title, description: body.description, og_image: body.ogImage };
    else if (kind === 'media') item = method === 'POST'
      ? { id: Date.now(), name: body.name, alt: body.alt, url: `data:${body.mime};base64,${body.base64}`, size: Math.round(body.base64.length * .75), system: false }
      : { ...collection[index], name: body.name, alt: body.alt };
    else if (kind === 'inquiries') item = { ...collection[index], ...body };
    else item = { ...(method === 'PUT' ? collection[index] : { id: Date.now() }), ...body };
    if (method === 'PUT') collection[index] = item;
    else collection.unshift(item);
    writeCollection(kind, collection);
    return { item };
  }

  function readProfileName() {
    try { return JSON.parse(localStorage.getItem('mihenk-profile') || '{}').name || 'Ayşe Yılmaz'; }
    catch { return 'Ayşe Yılmaz'; }
  }

  function toast(message, error = false) {
    const node = document.querySelector('[data-cms-toast]');
    if (!node) return;
    node.textContent = message;
    node.classList.toggle('is-error', error);
    node.classList.add('is-visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => node.classList.remove('is-visible'), 4200);
  }

  function element(tag, className = '', text = '') {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== '') node.textContent = text;
    return node;
  }

  const dateText = (value) => {
    if (!value) return '—';
    const date = new Date(value);
    return Number.isNaN(date.valueOf()) ? value : new Intl.DateTimeFormat('tr-TR', { day: 'numeric', month: 'short', year: 'numeric' }).format(date);
  };
  const safeImage = (value) => /^(assets\/images\/|data:image\/(?:png|jpeg|webp);base64,)/.test(value || '') ? value : '';
  const initials = (value) => (value || 'M').trim().split(/\s+/).slice(0, 2).map((part) => part[0]?.toLocaleUpperCase('tr-TR') || '').join('');
  const canWrite = () => session?.user?.role === 'admin' || (session?.user?.role === 'editor' && page !== 'users' && page !== 'seo');
  const canDelete = () => session?.user?.role === 'admin' || (session?.user?.role === 'editor' && contentKinds.has(page) || session?.user?.role === 'editor' && page === 'media');

  function endpoint() {
    if (contentKinds.has(page)) return `/api/content/${page}`;
    return `/api/${page}`;
  }

  function statusOf(item) {
    if (page === 'inquiries') return item.status;
    if (page === 'users') return item.active ? 'active' : 'passive';
    if (page === 'media') return item.system ? 'system' : 'uploaded';
    return item.status;
  }

  function visibleItems() {
    const query = (root.querySelector('[data-cms-search]')?.value || '').trim().toLocaleLowerCase('tr-TR');
    const filter = root.querySelector('[data-cms-filter]')?.value || 'all';
    return items.filter((item) => {
      const match = !query || JSON.stringify(item).toLocaleLowerCase('tr-TR').includes(query);
      const typeMatch = filter === 'all' || (page === 'users' ? item.role === filter : statusOf(item) === filter);
      return match && typeMatch;
    });
  }

  function itemDetails(item) {
    if (page === 'blog') return [item.data?.excerpt || '', item.data?.category || ''];
    if (page === 'projects') return [item.data?.summary || '', item.data?.sector || ''];
    if (page === 'services') return [item.data?.summary || '', item.data?.category || ''];
    if (page === 'testimonials') return [item.data?.quote || '', item.data?.role || ''];
    if (page === 'inquiries') return [item.subject || '', item.email || ''];
    if (page === 'users') return [item.email || '', roleLabels[item.role] || item.role];
    return [item.alt || '', `${Math.round(item.size / 1024)} KB`];
  }

  function itemTitle(item) {
    if (page === 'inquiries' || page === 'users') return item.name;
    if (page === 'media') return item.name;
    return item.title;
  }

  function itemImage(item) {
    if (page === 'media') return item.url;
    return item.data?.image || '';
  }

  function previewLink(item) {
    if (page === 'blog' && item.status === 'published' && item.id <= 3) return ['','blog-belirsizlikte-net-kararlar.html','blog-dijital-donusum-insanla-baslar.html','blog-veriyle-karar-almak.html'][item.id];
    return '';
  }

  function iconButton(symbol, label, handler, danger = false) {
    const button = element('button', `cms-icon-button${danger ? ' danger' : ''}`, symbol);
    button.type = 'button';
    button.setAttribute('aria-label', label);
    button.title = label;
    button.addEventListener('click', handler);
    return button;
  }

  function renderRow(item) {
    const row = element('div', 'cms-item');
    row.dataset.kind = page;
    const thumb = element('span', 'cms-thumb');
    const image = safeImage(itemImage(item));
    if (image) {
      const img = document.createElement('img');
      img.src = image;
      img.alt = '';
      img.loading = 'lazy';
      thumb.append(img);
    } else thumb.textContent = initials(itemTitle(item));
    const main = element('span', 'cms-main');
    main.append(element('strong', '', itemTitle(item)), element('small', '', itemDetails(item)[0]));
    const meta = element('span', 'cms-meta', itemDetails(item)[1] || dateText(item.updatedAt || item.updated_at || item.created_at));
    const status = statusOf(item);
    const pill = element('span', `cms-pill ${status === 'draft' || status === 'passive' ? 'draft' : status === 'new' ? 'new' : status === 'archived' ? 'archived' : ''}`,
      page === 'users' ? statusLabels[status] : page === 'media' ? (item.system ? 'Site görseli' : 'Yüklendi') : statusLabels[status] || status);
    const actions = element('span', 'cms-row-actions');
    const preview = previewLink(item);
    if (preview) {
      const link = element('a', 'cms-icon-button', '↗');
      link.href = preview;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.setAttribute('aria-label', 'Sitede görüntüle');
      link.title = 'Sitede görüntüle';
      actions.append(link);
    }
    if (canWrite()) actions.append(iconButton('✎', 'Düzenle', () => openEditor(item)));
    if (canDelete() && !(page === 'media' && item.system) && !(page === 'users' && item.id === session.user.id)) {
      actions.append(iconButton('×', 'Sil', () => openConfirm(item), true));
    }
    row.append(thumb, main, meta, pill, actions);
    return row;
  }

  function renderMediaCard(item) {
    const card = element('article', 'cms-media-card');
    const imageWrap = element('div', 'cms-media-image');
    const image = document.createElement('img');
    image.src = safeImage(item.url);
    image.alt = item.alt || item.name;
    image.loading = 'lazy';
    imageWrap.append(image);
    const body = element('div', 'cms-media-card-body');
    body.append(element('strong', '', item.name), element('small', '', item.system ? 'Site görseli' : `${Math.round(item.size / 1024)} KB · Önizleme görseli`));
    const actions = element('div', 'cms-media-card-actions');
    const copy = element('button', '', 'URL kopyala');
    copy.type = 'button';
    copy.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(item.system ? new URL(item.url, location.href).href : item.url); toast('Görsel adresi kopyalandı.'); }
      catch { toast('Kopyalama başarısız. URL: ' + item.url, true); }
    });
    actions.append(copy);
    if (canWrite()) {
      const edit = element('button', '', 'Düzenle');
      edit.type = 'button';
      edit.addEventListener('click', () => openEditor(item));
      actions.append(edit);
    }
    if (canDelete() && !item.system) {
      const remove = element('button', '', 'Sil');
      remove.type = 'button';
      remove.addEventListener('click', () => openConfirm(item));
      actions.append(remove);
    }
    body.append(actions);
    card.append(imageWrap, body);
    return card;
  }

  function render() {
    const list = root?.querySelector('[data-cms-list]');
    if (!list) return;
    const filtered = visibleItems();
    const fragment = document.createDocumentFragment();
    filtered.forEach((item) => fragment.append(page === 'media' ? renderMediaCard(item) : renderRow(item)));
    list.replaceChildren(fragment);
    root.querySelector('[data-cms-count]').textContent = String(items.length).padStart(2, '0');
    root.querySelector('[data-cms-visible]').textContent = `${filtered.length} ${labels[page] || 'kayıt'} gösteriliyor`;
    root.querySelector('[data-cms-empty]').hidden = filtered.length !== 0;
  }

  function fieldValue(item, key) {
    if (!item) return '';
    if (key === 'title') return item.title || '';
    if (key === 'status') return item.status || 'draft';
    if (contentKinds.has(page)) return item.data?.[key] ?? '';
    if (key === 'active') return item.active ? '1' : '0';
    return item[key] ?? '';
  }

  function createField(field, item) {
    const wrap = element('div', `portal-field${field.full ? ' full' : ''}`);
    const id = `cms-${field.key}`;
    const label = element('label', '', field.label);
    label.htmlFor = id;
    wrap.append(label);
    let control;
    if (field.type === 'textarea') {
      control = document.createElement('textarea');
      control.rows = field.large ? 9 : 4;
      if (field.large) control.className = 'large-textarea';
    } else if (field.type === 'select') {
      control = document.createElement('select');
      field.options.forEach(([value, text]) => {
        const option = new Option(text, value);
        control.add(option);
      });
    } else {
      control = document.createElement('input');
      control.type = field.type === 'media' ? 'text' : field.type || 'text';
      if (field.type === 'number') {
        control.min = field.min ?? 0;
        if (field.max != null) control.max = field.max;
      }
      if (field.type === 'file') control.accept = 'image/jpeg,image/png,image/webp';
    }
    control.id = id;
    control.name = field.key;
    control.required = !!field.required && !(field.type === 'file' && item);
    control.readOnly = !!field.readonly;
    if (field.type !== 'file') control.value = String(fieldValue(item, field.key));
    wrap.append(control);
    if (field.type === 'media') {
      const choose = element('button', 'cms-inline-button', 'Medya kütüphanesinden seç');
      choose.type = 'button';
      choose.addEventListener('click', () => openPicker(control));
      wrap.append(choose);
    }
    if (field.hint) wrap.append(element('small', '', field.hint));
    if (field.type === 'file') {
      const preview = element('div', 'media-file-preview', item ? 'Yeni dosya seçmeden başlık ve alternatif metni düzenleyebilirsiniz.' : 'Görsel önizlemesi');
      control.addEventListener('change', () => {
        preview.replaceChildren();
        const file = control.files?.[0];
        if (!file) { preview.textContent = 'Görsel önizlemesi'; return; }
        const image = document.createElement('img');
        const url = URL.createObjectURL(file);
        image.src = url;
        image.alt = 'Seçilen görsel önizlemesi';
        image.onload = () => URL.revokeObjectURL(url);
        preview.append(image);
        const name = wrap.closest('form')?.elements.namedItem('name');
        if (name && !name.value) name.value = file.name;
      });
      wrap.append(preview);
    }
    return wrap;
  }

  function openEditor(item = null) {
    if (!canWrite()) return;
    editing = item;
    const dialog = root.querySelector('[data-cms-editor]');
    const fields = root.querySelector('[data-cms-fields]');
    const form = root.querySelector('[data-cms-form]');
    form.reset();
    root.querySelector('[data-form-error]').textContent = '';
    root.querySelector('[data-dialog-title]').textContent = item ? `${labels[page]} düzenle` : `Yeni ${labels[page]}`;
    root.querySelector('[data-dialog-intro]').textContent = page === 'media' ? 'Görseli yükleyin ve açıklayıcı alternatif metnini ekleyin.' : page === 'users' ? 'Rol ve erişim durumunu buradan yönetin.' : page === 'inquiries' ? 'Talep ayrıntılarını ve takip durumunu güncelleyin.' : 'İçeriği düzenleyip taslak olarak saklayabilir veya yayınlayabilirsiniz.';
    const selectedSchema = page === 'media' && item ? schema.media.filter((field) => field.key !== 'file') : schema[page];
    fields.replaceChildren(...selectedSchema.map((field) => createField(field, item)));
    window.MihenkSelect?.enhanceAll(fields);
    dialog.showModal();
    fields.querySelector('input:not([readonly]), textarea:not([readonly]), select')?.focus();
  }

  function openConfirm(item) {
    removing = item;
    root.querySelector('[data-confirm-copy]').textContent = `“${itemTitle(item)}” kaydı kalıcı olarak silinecek. Bu işlem geri alınamaz.`;
    root.querySelector('[data-cms-confirm]').showModal();
  }

  async function fileAsBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(String(reader.result).split(',')[1] || '');
      reader.onerror = () => reject(new Error('Dosya okunamadı.'));
      reader.readAsDataURL(file);
    });
  }

  async function saveEditor(event) {
    event.preventDefault();
    const form = event.currentTarget;
    if (!form.reportValidity()) return;
    const errorNode = root.querySelector('[data-form-error]');
    errorNode.textContent = '';
    const data = Object.fromEntries(new FormData(form));
    let body;
    if (contentKinds.has(page)) {
      const { title, status, ...fields } = data;
      fields.sortOrder = Number(fields.sortOrder || 999);
      if (page === 'projects') fields.progress = Number(fields.progress || 0);
      if (page === 'testimonials') fields.name = title;
      body = { title, status, data: fields };
    } else if (page === 'inquiries') {
      body = { status: data.status, assignee: data.assignee || '', notes: data.notes || '' };
    } else if (page === 'users') {
      body = { name: data.name, email: data.email, role: data.role, active: data.active === '1' };
    } else if (page === 'media') {
      if (editing) body = { name: data.name, alt: data.alt || '' };
      else {
        const file = form.elements.namedItem('file')?.files?.[0];
        if (!file) { errorNode.textContent = 'Görsel dosyası seçin.'; return; }
        if (!['image/png', 'image/jpeg', 'image/webp'].includes(file.type)) { errorNode.textContent = 'JPEG, PNG veya WebP seçin.'; return; }
        if (file.size > 1024 * 1024) { errorNode.textContent = 'Önizleme görseli 1 MB sınırını aşıyor.'; return; }
        body = { name: data.name || file.name, alt: data.alt || '', mime: file.type, base64: await fileAsBase64(file) };
      }
    }
    const button = form.querySelector('[type="submit"]');
    button.disabled = true;
    try {
      await request(`${endpoint()}${editing ? `/${editing.id}` : ''}`, { method: editing ? 'PUT' : 'POST', body });
      root.querySelector('[data-cms-editor]').close();
      await loadItems();
      toast(`${labels[page]} kaydedildi.`);
    } catch (error) { errorNode.textContent = error.message; }
    finally { button.disabled = false; }
  }

  async function deleteItem() {
    if (!removing) return;
    const button = root.querySelector('[data-confirm-delete]');
    button.disabled = true;
    try {
      await request(`${endpoint()}/${removing.id}`, { method: 'DELETE' });
      root.querySelector('[data-cms-confirm]').close();
      removing = null;
      await loadItems();
      toast('Kayıt silindi.');
    } catch (error) { root.querySelector('[data-confirm-copy]').textContent = error.message; }
    finally { button.disabled = false; }
  }

  async function openPicker(target) {
    pickerTarget = target;
    const dialog = root.querySelector('[data-media-picker]');
    const grid = root.querySelector('[data-picker-grid]');
    grid.textContent = 'Görseller yükleniyor…';
    dialog.showModal();
    try {
      const data = await request('/api/media');
      const fragment = document.createDocumentFragment();
      data.items.forEach((item) => {
        const button = element('button');
        button.type = 'button';
        const image = document.createElement('img');
        image.src = safeImage(item.url);
        image.alt = item.alt || item.name;
        button.append(image, element('span', '', item.name));
        button.addEventListener('click', () => {
          pickerTarget.value = item.url;
          pickerTarget.dispatchEvent(new Event('input', { bubbles: true }));
          dialog.close();
        });
        fragment.append(button);
      });
      grid.replaceChildren(fragment);
    } catch (error) { grid.textContent = error.message; }
  }

  async function loadItems() {
    const data = await request(endpoint());
    items = data.items || [];
    render();
  }

  function initList() {
    const newButton = document.querySelector('[data-cms-new]');
    if (newButton && !canWrite()) newButton.hidden = true;
    newButton?.addEventListener('click', () => openEditor());
    root.querySelector('[data-cms-search]')?.addEventListener('input', render);
    root.querySelector('[data-cms-filter]')?.addEventListener('change', render);
    root.querySelector('[data-cms-form]')?.addEventListener('submit', saveEditor);
    root.querySelector('[data-confirm-delete]')?.addEventListener('click', deleteItem);
    loadItems().catch((error) => toast(error.message, true));
  }

  const seoLabels = { 'index.html': 'Ana sayfa', 'about.html': 'Hakkımızda', 'services.html': 'Hizmetler', 'projects.html': 'Projeler', 'blog.html': 'Blog', 'contact.html': 'İletişim', 'article.html': 'Blog yazısı şablonu' };
  let seoItems = [];

  function updateSeoPreview() {
    const form = root.querySelector('[data-seo-form]');
    const title = form.elements.namedItem('title').value;
    const description = form.elements.namedItem('description').value;
    const image = form.elements.namedItem('ogImage').value;
    root.querySelector('[data-title-count]').textContent = title.length;
    root.querySelector('[data-description-count]').textContent = description.length;
    root.querySelector('[data-seo-preview-title]').textContent = title || 'Sayfa başlığı';
    root.querySelector('[data-seo-share-title]').textContent = title || 'Sayfa başlığı';
    root.querySelector('[data-seo-preview-description]').textContent = description || 'Sayfa açıklaması burada görünür.';
    root.querySelector('[data-seo-share-description]').textContent = description;
    root.querySelector('[data-seo-share-image]').style.backgroundImage = safeImage(image) ? `url("${safeImage(image)}")` : 'none';
    root.querySelector('[data-seo-url]').textContent = `mihenk.com/${root.querySelector('[data-seo-page]').value}`;
  }

  function showSeo(pageName) {
    const item = seoItems.find((entry) => entry.page === pageName);
    const form = root.querySelector('[data-seo-form]');
    form.elements.namedItem('title').value = item?.title || '';
    form.elements.namedItem('description').value = item?.description || '';
    form.elements.namedItem('ogImage').value = item?.og_image || '';
    root.querySelector('[data-form-error]').textContent = '';
    updateSeoPreview();
  }

  async function initSeo() {
    if (session.user.role !== 'admin') { location.replace('dashboard.html'); return; }
    const data = await request('/api/seo');
    seoItems = data.items || [];
    const select = root.querySelector('[data-seo-page]');
    select.replaceChildren(...seoItems.map((item) => new Option(seoLabels[item.page] || item.page, item.page)));
    window.MihenkSelect?.refresh(select);
    select.addEventListener('change', () => showSeo(select.value));
    root.querySelector('[data-seo-form]').addEventListener('input', updateSeoPreview);
    root.querySelector('[data-seo-form]').addEventListener('submit', async (event) => {
      event.preventDefault();
      const form = event.currentTarget;
      if (!form.reportValidity()) return;
      const payload = { title: form.elements.namedItem('title').value, description: form.elements.namedItem('description').value, ogImage: form.elements.namedItem('ogImage').value };
      const errorNode = root.querySelector('[data-form-error]');
      errorNode.textContent = '';
      try {
        const result = await request(`/api/seo/${select.value}`, { method: 'PUT', body: payload });
        const index = seoItems.findIndex((item) => item.page === select.value);
        if (index >= 0) seoItems[index] = result.item;
        toast('SEO ayarları kaydedildi.');
      } catch (error) { errorNode.textContent = error.message; }
    });
    root.querySelector('[data-choose-media]').addEventListener('click', () => openPicker(root.querySelector('#seoImage')));
    showSeo(select.value);
  }

  async function initDashboard() {
    const data = await request('/api/summary');
    const totals = data.totals || {};
    document.querySelectorAll('[data-summary-kind]').forEach((node) => { node.textContent = String(totals[node.dataset.summaryKind] ?? 0).padStart(2, '0'); });
  }

  async function init() {
    try { session = await request('/api/auth/session'); }
    catch (error) {
      document.querySelector('.admin-content')?.prepend(element('p', 'cms-connection-error', error.message));
      return;
    }
    const name = session.user.name || 'Mihenk Kullanıcısı';
    document.querySelectorAll('[data-profile-name]').forEach((node) => { node.textContent = name; });
    document.querySelectorAll('[data-greeting-name]').forEach((node) => { node.textContent = name.split(' ')[0]; });
    document.querySelectorAll('[data-avatar]').forEach((node) => { node.textContent = initials(name); });
    if (session.user.role !== 'admin') document.querySelectorAll('a[href="users.html"],a[href="seo.html"]').forEach((node) => { node.hidden = true; });
    document.querySelectorAll('[data-dialog-close]').forEach((button) => button.addEventListener('click', () => button.closest('dialog')?.close()));
    if (page === 'seo') await initSeo();
    else if (page) initList();
    else if (document.querySelector('[data-summary-kind]')) await initDashboard();
  }

  init().catch((error) => toast(error.message, true));
})();
