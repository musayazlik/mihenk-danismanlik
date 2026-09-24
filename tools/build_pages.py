"""Generate the standalone Turkish consulting and editorial HTML pages."""

from html import escape
from pathlib import Path
from textwrap import dedent

from blog_content import POSTS


ROOT = Path(__file__).resolve().parent.parent


def arrow():
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 19 19 5M7 5h12v12"/></svg>'


def social_links():
    return '''<a href="https://www.linkedin.com/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M5.3 8.2H2.1V22h3.2V8.2ZM3.7 2a1.86 1.86 0 1 0 0 3.72A1.86 1.86 0 0 0 3.7 2Zm18.2 11.9c0-3.7-2-5.4-4.7-5.4a4 4 0 0 0-3.6 2V8.2h-3.2V22h3.2v-7.7c0-2 .4-3.3 2.5-3.3s2.5 1.5 2.5 3.4V22h3.3v-8.1Z"/></svg></a><a href="https://www.instagram.com/" target="_blank" rel="noopener noreferrer" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor" stroke="none"/></svg></a>'''


def nav_dropdown(href, label, key, submenu_id, items, active):
    active_class = ' active' if key == active else ''
    current = ' aria-current="page"' if key == active else ''
    entries = ''.join(f'<a href="{target}">{text}<span aria-hidden="true">↗</span></a>' for target, text in items)
    return f'<div class="nav-item has-submenu"><a class="nav-link{active_class}" href="{href}"{current}>{label}</a><button class="nav-caret" type="button" aria-label="{label} alt menüsünü aç" aria-expanded="false" aria-controls="{submenu_id}"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m5 7 5 5 5-5"/></svg></button><div class="submenu" id="{submenu_id}"><div class="submenu-panel">{entries}</div></div></div>'


def header(active):
    home_current = ' aria-current="page"' if active == 'home' else ''
    contact_current = ' aria-current="page"' if active == 'contact' else ''
    nav = f'<a class="nav-link{" active" if active == "home" else ""}" href="index.html"{home_current}>Ana Sayfa</a>'
    nav += nav_dropdown('about.html', 'Hakkımızda', 'about', 'submenu-about', [('about.html', 'Genel bakış'), ('about.html#degerler', 'Değerlerimiz'), ('about.html#yaklasim', 'Çalışma yaklaşımımız')], active)
    nav += nav_dropdown('services.html', 'Hizmetler', 'services', 'submenu-services', [('services.html', 'Tüm hizmetler'), ('services.html#strateji', 'Strateji & Büyüme'), ('services.html#donusum', 'Dijital Dönüşüm'), ('services.html#operasyon', 'Operasyonel Mükemmellik'), ('services.html#finans', 'Finansal Danışmanlık')], active)
    nav += nav_dropdown('projects.html', 'Projeler', 'projects', 'submenu-projects', [('projects.html', 'Tüm projeler'), ('projects.html?filter=strategy', 'Strateji projeleri'), ('projects.html?filter=digital', 'Dijital projeler'), ('projects.html?filter=operations', 'Operasyon projeleri')], active)
    nav += nav_dropdown('blog.html', 'Blog', 'blog', 'submenu-blog', [('blog.html', 'Tüm yazılar'), ('blog.html?category=strateji', 'Strateji'), ('blog.html?category=dijital', 'Dijital dönüşüm'), ('blog.html?category=operasyon', 'Operasyon'), ('blog.html?category=liderlik', 'Liderlik')], active)
    nav += f'<a class="nav-link{" active" if active == "contact" else ""}" href="contact.html"{contact_current}>İletişim</a>'
    return dedent(f'''\
    <a class="skip-link" href="#main">İçeriğe geç</a>
    <div class="topbar"><div class="container topbar-inner"><div class="topbar-left"><a href="mailto:merhaba@example.com">merhaba@example.com</a><span>İstanbul, Türkiye</span></div><div class="topbar-right"><span>Birlikte daha ileriye.</span><a href="contact.html">Bize ulaşın ↗</a></div></div></div>
    <header class="site-header"><div class="container header-inner">
      <a class="logo" href="index.html" aria-label="Mihenk ana sayfa"><span class="logo-mark" aria-hidden="true"></span>mihenk<span class="dot">.</span></a>
      <nav class="nav" id="primary-navigation" aria-label="Ana menü"><div class="nav-list">{nav}</div><div class="mobile-nav-footer"><span class="mobile-nav-label">BİZİ TAKİP EDİN</span><div class="mobile-nav-social">{social_links()}</div><a class="mobile-nav-mail" href="mailto:merhaba@example.com">merhaba@example.com</a></div></nav>
      <a class="btn btn-dark header-cta" href="contact.html">Birlikte konuşalım {arrow()}</a>
      <button class="menu-toggle" type="button" aria-label="Menüyü aç" aria-controls="primary-navigation" aria-expanded="false"><span></span></button>
    </div></header><div class="nav-backdrop" aria-hidden="true"></div>''')


def footer():
    return dedent(f'''\
    <footer class="site-footer"><div class="container">
      <div class="footer-grid">
        <div class="footer-brand"><a class="logo" href="index.html" aria-label="Mihenk ana sayfa"><span class="logo-mark" aria-hidden="true"></span>mihenk<span class="dot">.</span></a><p>Değişimin karmaşasında yön bulmanıza, doğru kararları almanıza ve kalıcı değer yaratmanıza yardımcı oluyoruz.</p><div class="footer-social" aria-label="Sosyal medya">{social_links()}</div></div>
        <div class="footer-column"><h3>Keşfedin</h3><a href="about.html">Hakkımızda</a><a href="services.html">Hizmetlerimiz</a><a href="projects.html">Projelerimiz</a><a href="blog.html">Blog</a><a href="contact.html">İletişim</a></div>
        <div class="footer-column"><h3>Uzmanlıklar</h3><a href="services.html#strateji">Strateji & Büyüme</a><a href="services.html#donusum">Dijital Dönüşüm</a><a href="services.html#operasyon">Operasyonel Mükemmellik</a><a href="services.html#finans">Finansal Danışmanlık</a></div>
        <div class="footer-column"><h3>Birlikte başlayalım</h3><a href="mailto:merhaba@example.com">merhaba@example.com</a><a href="tel:+902120000000">+90 212 000 00 00</a><span>Levent, İstanbul / Türkiye</span><a class="text-link" href="contact.html">İletişime geçin ↗</a></div>
      </div>
      <div class="footer-bottom"><span>© <span data-year>2026</span> Mihenk Danışmanlık. Tüm hakları saklıdır.</span><span>Stratejiye yön, değişime güç.</span></div>
    </div></footer>
    <script src="assets/js/main.js" defer></script>''')


def layout(title, description, active, body):
    preload = '<link rel="preload" href="assets/images/hero-team.webp" as="image" type="image/webp">' if active == 'home' else ''
    select_assets = '<link rel="stylesheet" href="assets/css/select.css"><script src="assets/js/select.js" defer></script>' if active == 'contact' else ''
    return dedent(f'''\
    <!doctype html>
    <html lang="tr">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta name="theme-color" content="#071821">
      <meta name="description" content="{description}">
      <title>{title} | Mihenk Danışmanlık</title>
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link rel="icon" href="assets/images/favicon.svg" type="image/svg+xml">
      {preload}
      <link rel="stylesheet" href="assets/css/style.css">
      <link rel="stylesheet" href="assets/css/blog.css?v=2">
      {select_assets}
    </head>
    <body>
    {header(active)}
    <main id="main">{body}</main>
    {footer()}
    </body>
    </html>''')


def page_hero(kicker, title, current):
    return dedent(f'''\
    <section class="page-hero"><div class="container"><span class="eyebrow light">{kicker}</span><h1>{title}</h1><nav class="breadcrumbs" aria-label="Konum"><a href="index.html">Ana Sayfa</a><span aria-hidden="true">/</span><span aria-current="page">{current}</span></nav></div></section>''')


def cta():
    return dedent(f'''\
    <section class="cta-band"><div class="container cta-content"><div><span class="eyebrow">Bir sonraki adım</span><h2>Geleceğinizi birlikte<br>şekillendirelim.</h2></div><a class="btn btn-dark" href="contact.html">Projeyi konuşalım {arrow()}</a></div></section>''')


icons = {
    'strategy': '<path d="M3 20V7l6-4 6 4v13M15 10l6-4v14M3 20h18M7 10h2M7 14h2M17 12h2M17 16h2"/>',
    'digital': '<rect x="3" y="4" width="18" height="14" rx="1"/><path d="M8 22h8M12 18v4M7 12l3-3 3 2 4-4"/>',
    'operations': '<path d="M4 7h16M4 12h10M4 17h16"/><circle cx="17" cy="12" r="3"/><path d="M6 4v6M18 14v6"/>',
    'finance': '<path d="M4 20V4M4 20h16M8 16l4-5 3 2 5-7"/><path d="M16 6h4v4"/>',
    'people': '<circle cx="9" cy="8" r="3"/><circle cx="18" cy="9" r="2"/><path d="M3 20v-2a6 6 0 0 1 12 0v2M15 15a4 4 0 0 1 6 4v1"/>',
    'risk': '<path d="M12 2 3 6v6c0 6 4 9 9 10 5-1 9-4 9-10V6l-9-4Z"/><path d="m8 12 3 3 5-6"/>',
}


def service_card(number, icon, title, text):
    return f'<a class="service-card reveal" href="services.html"><span class="service-no">{number} / HİZMET</span><span class="service-icon"><svg viewBox="0 0 24 24" aria-hidden="true">{icons[icon]}</svg></span><h3>{title}</h3><p>{text}</p></a>'


def project_card(image, category, title, tag, alt, listing=False):
    destination = 'contact.html' if listing else 'projects.html'
    action = 'Benzer projeyi konuşalım' if listing else 'Projeleri inceleyin'
    return f'<a class="project-card reveal" href="{destination}" data-category="{category}" aria-label="{title} — {action}"><img src="assets/images/{image}" alt="{alt}" loading="lazy" width="1536" height="1024"><div class="project-card-content"><div><small>{tag}</small><h3>{title}</h3><span class="project-card-cta">{action}</span></div><span class="round-arrow" aria-hidden="true">↗</span></div></a>'


def partner_logos():
    return '''<div class="partner-logo partner-aurel" role="img" aria-label="Aurel temsili marka logosu"><svg viewBox="0 0 42 42" fill="none" aria-hidden="true"><path d="M5 35 20.5 6 37 35M11 26h20" stroke="currentColor" stroke-width="4" stroke-linecap="square"/></svg><strong>AUREL</strong></div><div class="partner-logo partner-velora" role="img" aria-label="Velora temsili marka logosu"><svg viewBox="0 0 42 42" fill="none" aria-hidden="true"><circle cx="21" cy="21" r="16" stroke="currentColor" stroke-width="3"/><path d="M8 24c8-2 13-9 18-18M16 36c3-9 11-15 18-17" stroke="currentColor" stroke-width="3"/></svg><strong>velora</strong></div><div class="partner-logo partner-koro" role="img" aria-label="Koro temsili marka logosu"><svg viewBox="0 0 42 42" fill="none" aria-hidden="true"><path d="M21 3 38 21 21 39 4 21 21 3Z" stroke="currentColor" stroke-width="3"/><path d="m13 21 8-8 8 8-8 8-8-8Z" fill="currentColor"/></svg><strong>KORO</strong></div><div class="partner-logo partner-mondo" role="img" aria-label="Mondo temsili marka logosu"><svg viewBox="0 0 42 42" fill="none" aria-hidden="true"><circle cx="21" cy="21" r="16" stroke="currentColor" stroke-width="3"/><path d="M5 21h32M21 5c-7 8-7 24 0 32M21 5c7 8 7 24 0 32" stroke="currentColor" stroke-width="2"/></svg><strong>mondo</strong></div><div class="partner-logo partner-stride" role="img" aria-label="Stride temsili marka logosu"><svg viewBox="0 0 42 42" fill="none" aria-hidden="true"><path d="M5 31h18l14-20H19L5 31Z" fill="currentColor"/><path d="m16 31 13-20" stroke="#fff" stroke-width="3"/></svg><strong>STRIDE</strong></div>'''


def blog_card(post):
    href = f'blog-{post["slug"]}.html'
    search_text = escape(f'{post["title"]} {post["excerpt"]} {post["category_label"]}', quote=True)
    return f'''<article class="blog-card reveal" data-blog-card data-category="{post['category']}" data-search="{search_text}"><a class="blog-card-link" href="{href}" aria-label="{escape(post['title'], quote=True)} yazısını oku"><div class="blog-card-image"><img src="assets/images/{post['image']}" alt="{escape(post['alt'], quote=True)}" loading="lazy" width="1672" height="941"></div><div class="blog-card-content"><div class="blog-card-meta"><span>{post['category_label']}</span><span>{post['read_time']} okuma</span></div><h3>{escape(post['title'])}</h3><p>{escape(post['excerpt'])}</p><div class="blog-card-bottom"><time datetime="{post['datetime']}">{post['date']}</time><span class="blog-card-arrow" aria-hidden="true">↗</span></div></div></a></article>'''


def blog_sections(post):
    sections = []
    for section in post['sections']:
        parts = [f'<section><h2>{escape(section["heading"])}</h2>']
        parts.extend(f'<p>{escape(paragraph)}</p>' for paragraph in section['paragraphs'])
        if section.get('bullets'):
            parts.append('<ul>' + ''.join(f'<li>{escape(item)}</li>' for item in section['bullets']) + '</ul>')
        if section.get('quote'):
            parts.append(f'<blockquote>{escape(section["quote"])}</blockquote>')
        parts.append('</section>')
        sections.append(''.join(parts))
    return '\n'.join(sections)


def blog_detail(post):
    related = [item for item in POSTS if item['slug'] != post['slug']][:3]
    popular = [item for item in POSTS if item['slug'] != post['slug']][:3]
    popular_links = ''.join(f'<a href="blog-{item["slug"]}.html"><span>{item["category_label"]} · {item["read_time"]}</span><strong>{escape(item["title"])}</strong><small>Yazıyı oku ↗</small></a>' for item in popular)
    related_cards = ''.join(blog_card(item) for item in related)
    return dedent(f'''\
    <div class="reading-progress" aria-hidden="true"><span data-reading-progress></span></div>
    <article class="article-page" data-article-slug="{post['slug']}">
      <header class="article-hero"><div class="container article-hero-inner"><nav class="breadcrumbs" aria-label="Konum"><a href="index.html">Ana Sayfa</a><span aria-hidden="true">/</span><a href="blog.html">Blog</a><span aria-hidden="true">/</span><span aria-current="page">{post['category_label']}</span></nav><a class="article-category" href="blog.html?category={post['category']}">{post['category_label']} ↗</a><h1>{escape(post['title'])}</h1><p>{escape(post['excerpt'])}</p><div class="article-meta"><span class="author-avatar" aria-hidden="true">{''.join(part[0] for part in post['author'].split()[:2])}</span><strong>{post['author']}</strong><span class="meta-divider" aria-hidden="true"></span><time datetime="{post['datetime']}">{post['date']}</time><span class="meta-divider" aria-hidden="true"></span><span>{post['read_time']} okuma</span></div></div></header>
      <div class="container article-cover"><img src="assets/images/{post['image']}" alt="{escape(post['alt'], quote=True)}" width="1672" height="941"></div>
      <div class="container article-layout"><div class="article-main"><div class="article-share"><span>BU YAZIYI PAYLAŞ</span><div><button type="button" data-share="copy" aria-label="Yazı bağlantısını kopyala">Bağlantıyı kopyala ↗</button><button type="button" data-share="linkedin" aria-label="LinkedIn'de paylaş">in</button><button type="button" data-share="x" aria-label="X'te paylaş">X</button></div><p data-share-status role="status" aria-live="polite"></p></div><div class="article-body"><p class="article-lead">{escape(post['excerpt'])}</p>{blog_sections(post)}</div><div class="article-endnote"><span>MIHENK JOURNAL</span><p>İyi fikirler paylaşıldıkça büyür. Bu yazıyı ekibinizle paylaşın veya düşüncelerinizi yorumlarda anlatın.</p><a class="text-link" href="blog.html">Tüm yazılara dön {arrow()}</a></div>
      <section class="comments" id="yorumlar" aria-labelledby="comments-title"><div class="comments-heading"><span class="eyebrow">Sohbete katılın</span><h2 id="comments-title">Yorumlar <span data-comment-count>2</span></h2></div><div class="comment-list" data-comment-list><div class="comment"><span class="comment-avatar" aria-hidden="true">AT</span><div><div class="comment-top"><strong>Ayşe T.</strong><span>Örnek yorum</span></div><p>Özellikle küçük ama düzenli adımlarla ilerleme fikri çok değerli. Ekibimizde paylaşacağım.</p></div></div><div class="comment"><span class="comment-avatar" aria-hidden="true">BK</span><div><div class="comment-top"><strong>Burak K.</strong><span>Örnek yorum</span></div><p>Konuyu pratik sorularla anlatmanız güzel olmuş. Bir sonraki planlama toplantımız için iyi bir başlangıç.</p></div></div></div><form class="comment-form" data-comment-form><h3>Bir yorum bırakın</h3><p>Görüşünüzü paylaşın. Yorumunuz yalnızca bu tarayıcıda saklanır.</p><div class="field"><label for="comment-name">Adınız *</label><input id="comment-name" name="name" type="text" autocomplete="name" maxlength="50" required></div><div class="field"><label for="comment-text">Yorumunuz *</label><textarea id="comment-text" name="comment" minlength="10" maxlength="1000" required></textarea></div><button class="btn btn-dark" type="submit">Yorumu ekle {arrow()}</button><p class="form-status" data-comment-status role="status" aria-live="polite"></p></form></section></div>
      <aside class="article-aside" aria-label="Popüler içerikler"><div class="article-aside-inner"><span class="eyebrow">Daha fazla keşfedin</span><h2>Popüler içerikler</h2><div class="popular-list">{popular_links}</div><div class="aside-cta"><span>Bir fikriniz mi var?</span><strong>Gelin, birlikte düşünelim.</strong><a href="contact.html">İletişime geçin ↗</a></div></div></aside></div>
    </article>
    <section class="section related-section"><div class="container"><div class="section-intro"><div><span class="eyebrow">Okumaya devam edin</span><h2 class="section-heading">İlginizi çekebilecek <em>yazılar.</em></h2></div><a class="text-link" href="blog.html">Tüm yazılar {arrow()}</a></div><div class="blog-grid">{related_cards}</div></div></section>''')


home = dedent(f'''\
<section class="hero" aria-labelledby="hero-title"><div class="container hero-grid"><div class="hero-copy"><span class="eyebrow light">Strateji · Dönüşüm · Büyüme</span><h1 id="hero-title">Bugünün kararları,<br><em>yarının gücü.</em></h1><p>Karmaşık iş problemlerini net fırsatlara dönüştürüyoruz. İddialı hedeflerinize birlikte, sağlam adımlarla ilerleyelim.</p><div class="hero-actions"><a class="btn btn-primary" href="services.html">Hizmetlerimizi keşfedin {arrow()}</a><a class="btn btn-outline" href="projects.html">Projelerimizi inceleyin {arrow()}</a></div></div><span class="hero-side">Mihenk Danışmanlık · İstanbul</span><div class="hero-index"><strong>01</strong><i></i><span>05</span></div></div></section><div class="hero-stat-wrap"><div class="container"><div class="hero-stat"><strong>18<span aria-hidden="true">+</span></strong><span>YILLIK<br>SEKTÖR DENEYİMİ</span></div></div></div>
<section class="trust-band"><div class="container trust-grid"><div class="trust-title"><span>Marka vitrini</span><strong>Birlikte büyüyen markalar</strong></div><div class="trust-logos" aria-label="Temsili marka logoları">{partner_logos()}</div></div><div class="container trust-disclaimer">* Temsili marka logoları</div></section>
<section class="section"><div class="container intro-grid"><div class="photo-stack reveal"><img src="assets/images/strategy-team.webp" alt="Danışmanların strateji toplantısında ortak çalışma yürütmesi" loading="lazy" width="1672" height="941"><div class="photo-badge"><strong>18+</strong><span>Yıllık<br>deneyim</span></div></div><div class="intro-copy reveal"><span class="eyebrow">Biz kimiz?</span><h2 class="section-heading">Değişimi fırsata <em>dönüştüren</em> bakış açısı.</h2><p class="lead">Mihenk, iş dünyasının en kritik kararlarında kurumlara eşlik eden bağımsız bir strateji ve dönüşüm danışmanlığıdır.</p><p>Hazır reçeteler yerine sizi dinler, veriyi sahayla buluşturur ve uygulanabilir çözümler tasarlarız. Çünkü iyi bir stratejinin değeri, hayata geçtiğinde anlaşılır.</p><ul class="check-list"><li>Ölçülebilir ve sürdürülebilir sonuçlar</li><li>İşinize özel, birlikte geliştirilen çözümler</li><li>Başlangıçtan uygulamaya kesintisiz destek</li></ul><a class="btn btn-dark" href="about.html">Mihenk'i tanıyın {arrow()}</a></div></div></section>
<section class="section services-section"><div class="container"><div class="section-intro reveal"><div><span class="eyebrow">Uzmanlık alanlarımız</span><h2 class="section-heading">İhtiyacınız olan<br><em>doğru perspektif.</em></h2></div><p class="lead">Stratejiden uygulamaya uzanan hizmetlerimizle işinizin potansiyelini açığa çıkarıyoruz.</p></div><div class="service-grid">
{service_card('01','strategy','Strateji & Büyüme','Yeni fırsatları keşfedin, rekabet avantajınızı kalıcı bir değere dönüştürün.')}
{service_card('02','digital','Dijital Dönüşüm','Teknolojiyi hedeflerinize bağlayan insan odaklı dönüşüm yolculukları.')}
{service_card('03','operations','Operasyonel Mükemmellik','Süreçleri sadeleştirin; kaliteyi, hızı ve verimliliği birlikte artırın.')}
{service_card('04','finance','Finansal Danışmanlık','Kaynaklarınızı doğru yönetin, güçlü kararları sağlam verilerle alın.')}
{service_card('05','people','İnsan & Organizasyon','Yeteneği ve kültürü stratejinizin merkezine taşıyan organizasyonlar kurun.')}
{service_card('06','risk','Risk & Sürdürülebilirlik','Belirsizliği yönetin ve uzun vadeli dayanıklılığınızı güçlendirin.')}
</div><div class="service-footer"><a class="text-link" href="services.html">Tüm hizmetleri inceleyin {arrow()}</a></div></div></section>
<section class="stat-strip"><div class="container stat-grid"><div class="stat-item"><strong><span data-count="18">18</span><em>+</em></strong><span>Yıllık sektör deneyimi</span></div><div class="stat-item"><strong><span data-count="240">240</span><em>+</em></strong><span>Tamamlanan proje</span></div><div class="stat-item"><strong><span data-count="32">32</span><em>+</em></strong><span>Uzman iş ortağı</span></div><div class="stat-item"><strong><span data-count="96">96</span><em>%</em></strong><span>Müşteri memnuniyeti</span></div></div></section>
<section class="section"><div class="container process-grid"><div class="reveal"><span class="eyebrow">Nasıl çalışıyoruz?</span><h2 class="section-heading">Fikirden etkiye,<br><em>yan yana.</em></h2><p class="lead">Her projede netlik, birlikte üretim ve ölçülebilir etkiyi merkezde tutuyoruz.</p><a class="text-link" href="about.html">Çalışma yaklaşımımız {arrow()}</a></div><div class="process-steps reveal"><div class="process-step"><span>01</span><div><h3>Dinler ve anlarız</h3><p>Hedeflerinizi, işinizin gerçeklerini ve önünüzdeki engelleri birlikte tanımlarız.</p></div></div><div class="process-step"><span>02</span><div><h3>Yol haritası kurarız</h3><p>Veri ve deneyimi birleştirerek uygulanabilir bir strateji tasarlarız.</p></div></div><div class="process-step"><span>03</span><div><h3>Birlikte hayata geçiririz</h3><p>Değişimi ekiplerinizle sahiplenir, sonuçları takip edip geliştiririz.</p></div></div></div></div></section>
<section class="section services-section"><div class="container"><div class="section-intro reveal"><div><span class="eyebrow">Seçili çalışmalar</span><h2 class="section-heading">Sonuçları konuşan<br><em>iş birlikleri.</em></h2></div><a class="text-link" href="projects.html">Tüm projeleri görün {arrow()}</a></div><div class="project-grid">{project_card('architecture.webp','strategy','Yeni bir büyüme rotası','Strateji / Gayrimenkul','Modern cam cepheli iş merkezi')}{project_card('operations.webp','operations','Operasyonda yeni ritim','Operasyon / Perakende','Modern operasyon merkezinde çalışan yönetici')}</div></div></section>
<section class="section quote-section"><div class="container quote-layout"><div class="reveal"><span class="eyebrow">Müşterilerimiz anlatıyor</span><h2 class="section-heading">Birlikte daha<br><em>güçlüyüz.</em></h2></div><div class="reveal"><div class="quote-mark" aria-hidden="true">“</div><p class="testimonial" data-quote-text>“Mihenk ekibi, karmaşık bir dönüşümü herkesin anlayabileceği bir yol haritasına çevirdi. Bugün daha hızlı karar alıyor ve aynı hedefe birlikte yürüyoruz.”</p><div class="quote-author"><div><strong data-quote-name>Selin Arslan</strong><span data-quote-role>Genel Müdür, Atlas Grup</span></div><div class="quote-controls"><button type="button" data-quote-direction="-1" aria-label="Önceki yorum">←</button><button type="button" data-quote-direction="1" aria-label="Sonraki yorum">→</button></div></div></div></div></section>
<section class="section home-blog-section"><div class="container"><div class="section-intro reveal"><div><span class="eyebrow">Mihenk Journal</span><h2 class="section-heading">Düşünmeye değer <em>fikirler.</em></h2></div><div class="home-blog-intro"><p>Strateji, dönüşüm ve iş dünyasına dair sahadan notlar.</p><a class="text-link" href="blog.html">Tüm yazıları keşfedin {arrow()}</a></div></div><div class="blog-grid">{''.join(blog_card(post) for post in POSTS[:3])}</div></div></section>
{cta()}''')


about = dedent(f'''\
{page_hero('Mihenk hakkında','İleriye bakışımız <em>ortak.</em>','Hakkımızda')}
<section class="section" id="hikaye"><div class="container about-feature"><div class="reveal"><span class="eyebrow">Bizim hikâyemiz</span><h2 class="section-heading">Sorular zorlaştığında, <em>netlik</em> gerekir.</h2><p class="lead">Mihenk, şirketlerin yalnızca nereye gideceklerini değil, oraya nasıl ulaşacaklarını da birlikte tasarlamak için kuruldu.</p><p>Farklı sektörlerden uzmanları, analitik bakışı ve uygulama disiplinini aynı masaya getiriyoruz. Yönetim ekipleriyle omuz omuza çalışıyor; fikirleri gerçek etkiye dönüştürüyoruz.</p><ul class="check-list"><li>Bağımsız, dürüst ve cesur bakış açısı</li><li>İnsanı ve veriyi birlikte okuyan yaklaşım</li><li>Her aşamada açık iletişim ve sahiplenme</li></ul><a class="btn btn-dark" href="contact.html">Tanışalım {arrow()}</a></div><img class="reveal" src="assets/images/strategy-team.webp" alt="Mihenk ekibinin birlikte strateji geliştirdiği toplantı" width="1672" height="941"></div></section>
<section class="stat-strip"><div class="container stat-grid"><div class="stat-item"><strong><span data-count="18">18</span><em>+</em></strong><span>Yıllık deneyim</span></div><div class="stat-item"><strong><span data-count="240">240</span><em>+</em></strong><span>Tamamlanan proje</span></div><div class="stat-item"><strong><span data-count="12">12</span></strong><span>Farklı sektör</span></div><div class="stat-item"><strong><span data-count="96">96</span><em>%</em></strong><span>Memnuniyet oranı</span></div></div></section>
<section class="section services-section" id="degerler"><div class="container"><div class="section-intro reveal"><div><span class="eyebrow">Bizi biz yapan</span><h2 class="section-heading">Değerlerimiz, çalışma<br><em>biçimimizdir.</em></h2></div><p class="lead">Her iş birliğinde aynı üç ilkeye bağlı kalıyoruz.</p></div><div class="value-grid"><div class="value-card reveal"><b>01 / MERAK</b><h3>Önce doğru soruyu sorarız.</h3><p>Varsayımları sorgular, işinizin görünmeyen taraflarını anlamaya çalışırız.</p></div><div class="value-card reveal"><b>02 / CESARET</b><h3>Açık ve net konuşuruz.</h3><p>Zor kararların da masada olmasını sağlarız; daha iyiye giden yolu birlikte buluruz.</p></div><div class="value-card reveal"><b>03 / SAHİPLENME</b><h3>Sonucu beraber üretiriz.</h3><p>Sunum bittiğinde değil, gerçek değişim başladığında işimizin değeri ortaya çıkar.</p></div></div></div></section>
<section class="image-statement"><div class="container reveal"><span class="eyebrow light">Mihenk yaklaşımı</span><blockquote>“İyi strateji, bugün aldığınız kararların yarın yarattığı farktır.”</blockquote></div></section>
<section class="section" id="yaklasim"><div class="container process-grid"><div class="reveal"><span class="eyebrow">Beraber nasıl çalışırız?</span><h2 class="section-heading">Sizin ekibinizin <em>bir parçası</em> gibi.</h2><p class="lead">Her işi içerden anlayarak, gerçek hayatın temposuna uyan çözümlerle ilerleriz.</p></div><div class="process-steps reveal"><div class="process-step"><span>01</span><div><h3>Derinlemesine keşif</h3><p>Verileri, insanları ve süreçleri aynı resimde buluştururuz.</p></div></div><div class="process-step"><span>02</span><div><h3>Ortak tasarım</h3><p>Kararları sizinle birlikte verir, yol haritasını beraber sahipleniriz.</p></div></div><div class="process-step"><span>03</span><div><h3>Ölçülebilir ilerleme</h3><p>Sonuçları düzenli izler, öğrendiklerimizle rotayı sürekli iyileştiririz.</p></div></div></div></div></section>
{cta()}''')


services = dedent(f'''\
{page_hero('Çözümlerimiz','Her zorlukta <em>yanınızdayız.</em>','Hizmetler')}
<section class="section"><div class="container"><div class="section-intro reveal"><div><span class="eyebrow">Uzmanlıklarımız</span><h2 class="section-heading">Bugünün ihtiyacına,<br><em>yarının çözümü.</em></h2></div><p class="lead">Farklı disiplinleri bir araya getirerek kurumunuzun tüm dönüşüm yolculuğuna eşlik ediyoruz.</p></div><div class="services-list">
<a id="strateji" class="service-row reveal" href="contact.html"><span>01</span><h2>Strateji & Büyüme</h2><p>Pazar fırsatları, büyüme planları, iş modeli ve rekabet stratejisi.</p><span class="round-arrow" aria-hidden="true">↗</span></a>
<a id="donusum" class="service-row reveal" href="contact.html"><span>02</span><h2>Dijital Dönüşüm</h2><p>Dijital yol haritası, veri odaklı kararlar ve yeni müşteri deneyimleri.</p><span class="round-arrow" aria-hidden="true">↗</span></a>
<a id="operasyon" class="service-row reveal" href="contact.html"><span>03</span><h2>Operasyonel Mükemmellik</h2><p>Süreç iyileştirme, verimlilik, tedarik zinciri ve performans yönetimi.</p><span class="round-arrow" aria-hidden="true">↗</span></a>
<a id="finans" class="service-row reveal" href="contact.html"><span>04</span><h2>Finansal Danışmanlık</h2><p>Finansal planlama, yatırım değerlendirme ve kaynak optimizasyonu.</p><span class="round-arrow" aria-hidden="true">↗</span></a>
<a id="insan" class="service-row reveal" href="contact.html"><span>05</span><h2>İnsan & Organizasyon</h2><p>Organizasyon tasarımı, liderlik gelişimi ve kültürel dönüşüm.</p><span class="round-arrow" aria-hidden="true">↗</span></a>
<a id="risk" class="service-row reveal" href="contact.html"><span>06</span><h2>Risk & Sürdürülebilirlik</h2><p>Kurumsal dayanıklılık, risk yönetimi ve sürdürülebilir değer yaratma.</p><span class="round-arrow" aria-hidden="true">↗</span></a>
</div></div></section>
<section class="section services-section"><div class="container about-feature"><img class="reveal" src="assets/images/operations.webp" alt="Operasyon alanında dijital araçla çalışan yönetici" loading="lazy" width="1672" height="941"><div class="reveal"><span class="eyebrow">Yaklaşımımız</span><h2 class="section-heading">Danışmanlıktan <em>daha fazlası.</em></h2><p class="lead">Her çözümümüz, stratejik netliği uygulama gücüyle buluşturur.</p><p>Çalışma biçimimiz, kısa vadeli kazanımları uzun vadeli kapasiteyle dengeler. Ekibinizin gerçekten kullanacağı sistemleri, birlikte kurarız.</p><ul class="check-list"><li>Kuruma özel kapsam ve öncelikler</li><li>Şeffaf kilometre taşları</li><li>Kalıcı yetkinlik aktarımı</li></ul><a class="btn btn-dark" href="projects.html">Sonuçlarımızı görün {arrow()}</a></div></div></section>
<section class="section"><div class="container faq-grid"><div class="reveal"><span class="eyebrow">Sık sorulan sorular</span><h2 class="section-heading">Merak ettiklerinize <em>net cevaplar.</em></h2><p class="lead">Doğru iş birliği, açık bir konuşmayla başlar.</p></div><div class="faq-list reveal"><details><summary>Projeleriniz nasıl başlıyor?</summary><p>Önce kısa bir tanışma görüşmesi yapıyoruz. Hedefleri ve ihtiyaçları birlikte netleştirip kapsam, ekip ve takvimi içeren bir çalışma önerisi paylaşıyoruz.</p></details><details><summary>Hangi büyüklükte şirketlerle çalışıyorsunuz?</summary><p>Büyüme aşamasındaki girişimlerden köklü kurumlara kadar farklı ölçeklerde şirketlerle çalışıyoruz. Yaklaşımımızı her kurumun ihtiyacına göre şekillendiriyoruz.</p></details><details><summary>Çalışmalar yalnızca strateji hazırlamakla mı sınırlı?</summary><p>Hayır. Stratejinin hayata geçirilmesi, performans takibi ve ekiplere yetkinlik aktarımı da çalışma kapsamımıza girebilir.</p></details><details><summary>Uzaktan çalışma mümkün mü?</summary><p>Evet. Projenin gereksinimine göre yüz yüze, uzaktan veya hibrit çalışma düzeni kurabiliyoruz.</p></details></div></div></section>
{cta()}''')


projects = dedent(f'''\
{page_hero('Seçili projeler','Etki yaratan <em>iş birlikleri.</em>','Projeler')}
<section class="section"><div class="container"><div class="section-intro reveal"><div><span class="eyebrow">Çalışmalarımız</span><h2 class="section-heading">Her projede<br><em>somut ilerleme.</em></h2></div><p class="lead">Farklı sektörlerdeki iş ortaklarımızla tasarladığımız dönüşüm yolculuklarından seçili örnekler.</p></div><div class="filter-bar" role="group" aria-label="Projeleri filtrele"><button type="button" class="active" data-filter="all" aria-pressed="true">Tümü</button><button type="button" data-filter="strategy" aria-pressed="false">Strateji</button><button type="button" data-filter="digital" aria-pressed="false">Dijital</button><button type="button" data-filter="operations" aria-pressed="false">Operasyon</button></div><div class="project-grid">
{project_card('architecture.webp','strategy','Yeni bir büyüme rotası','Strateji / Gayrimenkul','Modern cam cepheli iş merkezi', True)}
{project_card('operations.webp','operations','Operasyonda yeni ritim','Operasyon / Perakende','Modern operasyon alanında çalışan yönetici', True)}
{project_card('strategy-team.webp','strategy','Kararları veriye bağlamak','Strateji / Finans','Danışmanların iş planını incelediği toplantı', True)}
{project_card('hero-team.webp','digital','Deneyimi yeniden tasarlamak','Dijital / Hizmetler','Pencere önünde çalışan danışmanlık ekibi', True)}
{project_card('operations.webp','digital','Akıllı tedarik ağı','Dijital / Lojistik','Çağdaş tedarik merkezinin iç mekânı', True)}
{project_card('architecture.webp','operations','Ölçeklenebilir bir gelecek','Operasyon / Teknoloji','Şehirde çağdaş ofis binası', True)}
</div></div></section>
<section class="section services-section"><div class="container about-feature"><div class="reveal"><span class="eyebrow">Örnek sonuç</span><h2 class="section-heading">İyi stratejinin <em>ölçülebilir</em> karşılığı.</h2><p class="lead">Bir perakende iş ortağımızın operasyonlarını uçtan uca yeniden ele aldık.</p><p>İş akışlarını sadeleştirip karar noktalarını görünür kılarak ekiplerin daha hızlı ve tutarlı çalışmasına yardımcı olduk.</p><div class="case-metric"><strong>%28</strong><span>örnek süreç verimliliği artışı<br><small>Temsili proje verisi</small></span></div></div><img class="reveal" src="assets/images/operations.webp" alt="Perakende operasyonuna ait temsili modern çalışma alanı" loading="lazy" width="1672" height="941"></div></section>
{cta()}''')


contact = dedent(f'''\
{page_hero('İletişim','Konuşarak <em>başlayalım.</em>','İletişim')}
<section class="section"><div class="container contact-layout"><div class="reveal"><span class="eyebrow">Bize ulaşın</span><h2 class="section-heading">Bir fikriniz mi var?<br><em>Dinliyoruz.</em></h2><p class="lead">Yeni bir proje, çözülecek bir problem ya da yalnızca tanışmak için bize yazın.</p><div class="contact-detail"><strong>E-posta</strong><a href="mailto:merhaba@example.com">merhaba@example.com</a></div><div class="contact-detail"><strong>Telefon</strong><a href="tel:+902120000000">+90 212 000 00 00</a></div><div class="contact-detail"><strong>Ofis</strong><span>Levent, İstanbul / Türkiye</span></div></div><form class="contact-form reveal" data-contact-form><h2>Mesaj bırakın</h2><p>Form, e-posta uygulamanızda gönderilmeye hazır bir ileti oluşturur.</p><div class="form-grid"><div class="field"><label for="name">Ad Soyad *</label><input id="name" name="name" type="text" autocomplete="name" required placeholder="Adınız ve soyadınız"></div><div class="field"><label for="email">E-posta *</label><input id="email" name="email" type="email" autocomplete="email" required placeholder="ornek@firma.com"></div><div class="field"><label for="phone">Telefon</label><input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="+90 ..."></div><div class="field"><label for="subject">Konu *</label><select id="subject" name="subject" required><option value="" disabled selected>Bir konu seçin</option><option value="Strateji ve büyüme">Strateji ve büyüme</option><option value="Dijital dönüşüm">Dijital dönüşüm</option><option value="Operasyonel dönüşüm">Operasyonel dönüşüm</option><option value="Diğer">Diğer</option></select></div><div class="field full"><label for="message">Mesajınız *</label><textarea id="message" name="message" required minlength="10" placeholder="Biraz projenizden bahsedin..."></textarea></div></div><div class="form-actions"><button type="submit" class="btn btn-primary">Mesajı hazırla {arrow()}</button><span class="form-note">* Zorunlu alanlar. Gönderim için cihazınızda e-posta uygulaması gerekir.</span></div><p class="form-status" role="status" aria-live="polite"></p></form></div></section>
<section class="section-tight services-section"><div class="container"><div class="section-intro reveal"><div><span class="eyebrow">Bizi bulun</span><h2 class="section-heading">İstanbul'dan<br><em>her yere.</em></h2></div><p class="lead">Projelerin ihtiyaçlarına göre yüz yüze, uzaktan veya hibrit çalışıyoruz.</p></div><div class="map-panel reveal" role="img" aria-label="Mihenk ofisini temsil eden modern iş merkezi görseli"><div><strong>İstanbul ofisi</strong><span>Levent, İstanbul / Türkiye<br>Görüşmeler randevu ile yapılır.</span></div></div></div></section>''')


blog = dedent(f'''\
{page_hero('Mihenk Journal','İyi fikirler <em>yol açar.</em>','Blog')}
<section class="section blog-list-section" id="yazilar"><div class="container"><div class="section-intro reveal"><div><span class="eyebrow">Düşünce & İçgörü</span><h2 class="section-heading">Bakış açınızı<br><em>genişletin.</em></h2></div><p class="lead">İş dünyasının değişen sorularına birlikte bakıyor; deneyim, veri ve merakı aynı sayfada buluşturuyoruz.</p></div><div class="blog-controls"><div class="blog-search"><label for="blog-search">Yazılarda ara</label><div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></svg><input id="blog-search" type="search" placeholder="Bir konu veya kelime yazın..." autocomplete="off" data-blog-search></div></div><div class="blog-categories" role="group" aria-label="Blog kategorileri"><button type="button" class="active" data-blog-category="all" aria-pressed="true">Tümü</button><button type="button" data-blog-category="strateji" aria-pressed="false">Strateji</button><button type="button" data-blog-category="dijital" aria-pressed="false">Dijital</button><button type="button" data-blog-category="operasyon" aria-pressed="false">Operasyon</button><button type="button" data-blog-category="liderlik" aria-pressed="false">Liderlik</button><button type="button" data-blog-category="surdurulebilirlik" aria-pressed="false">Sürdürülebilirlik</button></div></div><p class="blog-result-count" data-blog-result-count role="status" aria-live="polite">6 yazı gösteriliyor</p><div class="blog-grid" data-blog-grid>{''.join(blog_card(post) for post in POSTS)}</div><div class="blog-empty" data-blog-empty hidden><span aria-hidden="true">⌕</span><h3>Bu aramaya uygun yazı bulunamadı.</h3><p>Farklı bir kelime deneyin veya tüm kategorileri görüntüleyin.</p><button type="button" class="btn btn-dark" data-blog-reset>Tüm yazıları göster {arrow()}</button></div></div></section>
{cta()}''')


pages = {
    'index.html': ('Ana Sayfa', 'Mihenk Danışmanlık: strateji, dönüşüm ve sürdürülebilir büyüme için yanınızda.', 'home', home),
    'about.html': ('Hakkımızda', 'Mihenk Danışmanlık ekibi, yaklaşımı ve değerleriyle tanışın.', 'about', about),
    'services.html': ('Hizmetler', 'Strateji, dijital dönüşüm, operasyon, finans ve sürdürülebilirlik danışmanlığı.', 'services', services),
    'projects.html': ('Projeler', 'Mihenk Danışmanlık seçili çalışmalarını ve dönüşüm projelerini inceleyin.', 'projects', projects),
    'contact.html': ('İletişim', 'Mihenk Danışmanlık ile iletişime geçin ve projenizi birlikte konuşalım.', 'contact', contact),
    'blog.html': ('Blog', 'Mihenk Journal: strateji, dönüşüm, operasyon ve liderlik üzerine fikirler.', 'blog', blog),
}

for post in POSTS:
    pages[f'blog-{post["slug"]}.html'] = (post['title'], post['excerpt'], 'blog', blog_detail(post))

for filename, (title, description, active, body) in pages.items():
    (ROOT / filename).write_text(layout(title, description, active, body) + '\n', encoding='utf-8')
    print(filename)
