"""Generate the static Mihenk auth and admin preview pages."""

from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent.parent


def icon(name):
    paths = {
        "grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
        "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
        "settings": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06-2.12 2.12-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.52V21h-3v-.09a1.65 1.65 0 0 0-1-1.52 1.65 1.65 0 0 0-1.82.33l-.06.06-2.12-2.12.06-.06A1.65 1.65 0 0 0 7.2 15a1.65 1.65 0 0 0-1.52-1H5v-3h.68A1.65 1.65 0 0 0 7.2 10a1.65 1.65 0 0 0-.33-1.82l-.06-.06L8.93 6l.06.06A1.65 1.65 0 0 0 10.81 6a1.65 1.65 0 0 0 1-1.52V4h3v.48a1.65 1.65 0 0 0 1 1.52 1.65 1.65 0 0 0 1.82-.33l.06-.06 2.12 2.12-.06.06A1.65 1.65 0 0 0 19.4 10a1.65 1.65 0 0 0 1.52 1H21v3h-.08A1.65 1.65 0 0 0 19.4 15Z"/>',
        "profile": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
        "arrow": '<path d="M5 12h14m-6-6 6 6-6 6"/>',
        "external": '<path d="M7 17 17 7M8 7h9v9"/>',
        "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
        "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
        "close": '<path d="M5 5l14 14M19 5 5 19"/>',
        "plus": '<path d="M12 5v14M5 12h14"/>',
    }
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'


def logo():
    return '<a class="logo" href="index.html" aria-label="Mihenk ana sayfa"><span class="logo-mark" aria-hidden="true"></span>mihenk<span class="dot">.</span></a>'


def shell(title, description, body, kind):
    admin_scripts = '<link rel="stylesheet" href="assets/css/select.css"><link rel="stylesheet" href="assets/css/cms.css"><script src="assets/js/select.js" defer></script><script src="assets/js/cms.js" defer></script>' if kind == 'admin' else ''
    return dedent(f'''\
    <!doctype html>
    <html lang="tr">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta name="theme-color" content="#071821">
      <meta name="description" content="{description}">
      <title>{title} | Mihenk Danışmanlık</title>
      <link rel="icon" href="assets/images/favicon.svg" type="image/svg+xml">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link rel="stylesheet" href="assets/css/style.css">
      <link rel="stylesheet" href="assets/css/portal.css">
      <script src="assets/js/portal.js" defer></script>
      {admin_scripts}
    </head>
    <body class="portal-{kind}">
      <a class="skip-link" href="#main">İçeriğe geç</a>
      {body}
    </body>
    </html>''')


def field(label, name, typ="text", autocomplete=None, placeholder="", extra=""):
    auto = f' autocomplete="{autocomplete}"' if autocomplete else ""
    return f'<div class="portal-field"><label for="{name}">{label}</label><input id="{name}" name="{name}" type="{typ}"{auto} placeholder="{placeholder}" {extra}></div>'


def auth_page(number, kicker, title, intro, content, aside):
    body = f'''<div class="auth-shell">
      <aside class="auth-art"><div class="auth-art-inner"><div class="auth-art-top">{logo()}<span>YÖNETİM PORTALI / {number}</span></div><div class="auth-art-copy"><span class="portal-kicker">MİHENK DANIŞMANLIK</span><h2>Kararlarınız için<br><em>daha net bir alan.</em></h2><p>İşinizi ileri taşıyan veriler, ekipler ve önemli adımlar tek bir yerde.</p></div><div class="auth-art-bottom"><span>STRATEJİDEN UYGULAMAYA</span><span>{number} / 04</span></div></div></aside>
      <main class="auth-main" id="main"><div class="auth-top"><span class="auth-top-label">Mihenk çalışma alanı</span><span class="auth-mobile-brand">{logo()}</span><a href="index.html">Siteye dön {icon('external')}</a></div><div class="auth-card"><span class="portal-kicker">{kicker}</span><h1>{title}</h1><p class="auth-intro">{intro}</p>{content}<p class="demo-note">Bu alan arayüz önizlemesidir. Gerçek kimlik doğrulama veya e-posta gönderimi yapılmaz.</p></div><div class="auth-bottom">{aside}</div></main>
    </div>'''
    return body


login = auth_page(
    "01", "TEKRAR HOŞ GELDİNİZ", "Hesabınıza giriş yapın.",
    "Çalışma alanınıza devam etmek için bilgilerinizi girin.",
    f'''<form data-auth-form="login" class="portal-form">
      {field('E-posta adresi', 'email', 'email', 'email', 'adiniz@firma.com', 'required')}
      <div class="portal-field"><div class="field-heading"><label for="password">Parola</label><a href="forgot-password.html">Parolamı unuttum</a></div><div class="password-wrap"><input id="password" name="password" type="password" autocomplete="current-password" placeholder="Parolanız" required minlength="8"><button type="button" class="password-toggle" data-password-toggle aria-label="Parolayı göster">Göster</button></div></div>
      <label class="check-row"><input type="checkbox" name="remember"><span>E-postamı hatırla</span></label>
      <button class="portal-button" type="submit">Panele geç {icon('arrow')}</button><p class="form-feedback" role="status" aria-live="polite"></p>
    </form>''',
    'Henüz hesabınız yok mu? <a href="register.html">Hesap oluşturun <span aria-hidden="true">↗</span></a>'
)

register = auth_page(
    "02", "YENİ BAŞLANGIÇ", "Hesabınızı oluşturun.",
    "Ekibiniz için Mihenk çalışma alanına ilk adımı atın.",
    f'''<form data-auth-form="register" class="portal-form">
      <div class="portal-form-grid">{field('Ad', 'firstName', 'text', 'given-name', 'Adınız', 'required')}{field('Soyad', 'lastName', 'text', 'family-name', 'Soyadınız', 'required')}</div>
      {field('İş e-postası', 'email', 'email', 'email', 'adiniz@firma.com', 'required')}
      <div class="portal-field"><label for="password">Parola</label><div class="password-wrap"><input id="password" name="password" type="password" autocomplete="new-password" placeholder="En az 8 karakter" required minlength="8"><button type="button" class="password-toggle" data-password-toggle aria-label="Parolayı göster">Göster</button></div></div>
      <div class="portal-field"><label for="confirmPassword">Parola tekrar</label><input id="confirmPassword" name="confirmPassword" type="password" autocomplete="new-password" placeholder="Parolanızı yeniden girin" required minlength="8"></div>
      <button class="portal-button" type="submit">Önizleme panelini aç {icon('arrow')}</button><p class="form-feedback" role="status" aria-live="polite"></p>
    </form>''',
    'Zaten hesabınız var mı? <a href="login.html">Giriş yapın <span aria-hidden="true">↗</span></a>'
)

forgot = auth_page(
    "03", "ERİŞİM DESTEĞİ", "Parolanızı mı unuttunuz?",
    "E-posta adresinizi girin. Bu şablonda gönderim adımı örnek olarak gösterilir.",
    f'''<form data-auth-form="forgot" class="portal-form">{field('E-posta adresi', 'email', 'email', 'email', 'adiniz@firma.com', 'required')}<button class="portal-button" type="submit">Sıfırlama adımını göster {icon('arrow')}</button><p class="form-feedback" role="status" aria-live="polite"></p><a class="auth-text-link" href="reset-password.html" data-reset-link hidden>Yeni parola ekranına geç →</a></form>''',
    'Parolanızı hatırladınız mı? <a href="login.html">Girişe dön <span aria-hidden="true">↗</span></a>'
)

reset = auth_page(
    "04", "YENİ PAROLA", "Yeni bir parola belirleyin.",
    "Güçlü ve kolay hatırlayacağınız bir parola seçin.",
    f'''<form data-auth-form="reset" class="portal-form"><div class="portal-field"><label for="password">Yeni parola</label><div class="password-wrap"><input id="password" name="password" type="password" autocomplete="new-password" placeholder="En az 8 karakter" required minlength="8"><button type="button" class="password-toggle" data-password-toggle aria-label="Parolayı göster">Göster</button></div></div>{field('Yeni parola tekrar', 'confirmPassword', 'password', 'new-password', 'Parolayı yeniden girin', 'required minlength="8"')}<button class="portal-button" type="submit">Parola adımını tamamla {icon('arrow')}</button><p class="form-feedback" role="status" aria-live="polite"></p></form>''',
    'Hesabınıza dönmek için <a href="login.html">giriş yapın <span aria-hidden="true">↗</span></a>'
)


def admin_shell(active, breadcrumb, title, subtitle, content, actions=""):
    groups = [
        ("GENEL", [("dashboard", "dashboard.html", "Genel bakış", "grid")]),
        ("İÇERİK", [("blog", "blog-admin.html", "Blog yönetimi", "grid"), ("projects", "projects-admin.html", "Projeler", "grid"), ("services", "services-admin.html", "Hizmetler", "settings"), ("testimonials", "testimonials-admin.html", "Müşteri yorumları", "users"), ("media", "media-admin.html", "Medya kütüphanesi", "grid")]),
        ("İLETİŞİM", [("inquiries", "inquiries.html", "İletişim talepleri", "users")]),
        ("YÖNETİM", [("users", "users.html", "Ekip ve roller", "users"), ("seo", "seo.html", "SEO ayarları", "settings"), ("settings", "settings.html", "Ayarlar", "settings"), ("profile", "profile.html", "Profilim", "profile")]),
    ]
    links = ''.join('<div class="sidebar-label admin-group-label">' + group + '</div>' + ''.join(f'<a class="admin-nav-link{" is-active" if active == key else ""}" href="{href}"{" aria-current=\"page\"" if active == key else ""}>{icon(glyph)}<span>{label}</span><span class="nav-link-arrow">↗</span></a>' for key, href, label, glyph in items) for group, items in groups)
    return f'''<div class="admin-shell"><aside class="admin-sidebar" id="admin-sidebar"><div class="sidebar-top">{logo()}<button class="sidebar-close" type="button" data-menu-close aria-label="Menüyü kapat">{icon('close')}</button></div><div class="sidebar-workspace"><span class="workspace-symbol">M</span><span><strong>Mihenk Workspace</strong><small>Kurumsal alan</small></span><span class="workspace-chevron">⌄</span></div><nav class="admin-nav" aria-label="Yönetim menüsü">{links}</nav><div class="sidebar-lower"><div class="sidebar-insight"><span>✳ &nbsp; MİHENK İÇGÖRÜ</span><p>İyi kararlar, net bir görünümle başlar.</p><a href="projects.html">Projeleri incele ↗</a></div><a class="sidebar-user" href="profile.html"><span class="avatar avatar-small" data-avatar>AY</span><span><strong data-profile-name>Ayşe Yılmaz</strong><small>Yönetici</small></span><span aria-hidden="true">↗</span></a></div></aside><div class="admin-backdrop" data-menu-close></div><div class="admin-main"><header class="admin-topbar"><div class="topbar-left-admin"><button class="admin-menu-button" type="button" data-menu-open aria-label="Menüyü aç" aria-controls="admin-sidebar" aria-expanded="false">{icon('menu')}</button><span class="breadcrumb-main">Çalışma alanı</span><span class="breadcrumb-separator">/</span><span>{breadcrumb}</span></div><div class="topbar-right-admin"><span class="today-label" data-today></span><span class="topbar-divider"></span><a href="profile.html" class="topbar-profile" aria-label="Profilim"><span class="avatar" data-avatar>AY</span><span data-profile-name>Ayşe Yılmaz</span></a></div></header><main id="main" class="admin-content"><div class="admin-page-head"><div><span class="portal-kicker">MİHENK / YÖNETİM</span><h1>{title}</h1><p>{subtitle}</p></div>{actions}</div>{content}<div class="admin-footer"><span>© <span data-year>2026</span> Mihenk Danışmanlık</span><span>Arayüz önizlemesi · Veriler bu tarayıcıda saklanır</span></div></main></div></div>'''


def metric(label, value, trend, bars, accent=False, dynamic=False):
    count_attr = f' data-summary-kind="{dynamic}"' if dynamic else ''
    return f'<article class="metric-card{" metric-accent" if accent else ""}"><div class="metric-top"><span>{label}</span><span class="metric-mark">↗</span></div><strong{count_attr}>{value}</strong><div class="metric-bottom"><span>{trend}</span><span class="mini-bars" aria-hidden="true">{"".join(f"<i style=\"height:{b}%\"></i>" for b in bars)}</span></div></article>'


dashboard_content = f'''<section class="welcome-panel"><div><span class="welcome-overline">24 EYLÜL 2026 / ÇALIŞMA ALANI</span><h2>Bugünün odağı,<br><em>yarının etkisi.</em></h2><p>Ekibinizin durumunu ve projelerin son adımlarını tek bakışta görün.</p></div><div class="welcome-decoration" aria-hidden="true"><span>01</span><span>02</span><span>03</span></div></section>
<section class="metrics-grid" aria-label="Özet göstergeler">
{metric('Projeler', '03', 'Örnek çalışmalar', [25, 35, 48, 40, 57, 63, 78], True, 'projects')}
{metric('Ekip üyeleri', '04', 'Örnek hesaplar', [27, 34, 40, 52, 54, 67, 81], dynamic='users')}
{metric('Tamamlanan işler', '86', '%18 artış', [27, 42, 35, 56, 63, 70, 90])}
{metric('Bekleyen görevler', '07', '3 öncelikli', [70, 53, 63, 40, 46, 31, 22])}
</section>
<div class="admin-two-col"><section class="admin-panel"><div class="panel-heading"><div><span class="panel-eyebrow">PROJE TAKİBİ</span><h2>Devam eden çalışmalar</h2></div><a href="projects.html" class="panel-link">Tüm projeler ↗</a></div><div class="project-list"><div class="project-list-head"><span>PROJE</span><span>EKİP</span><span>İLERLEME</span><span>DURUM</span></div><div class="project-list-row"><div><strong>Dijital dönüşüm yol haritası</strong><small>Teknoloji · #M-024</small></div><div class="avatar-stack"><i>AY</i><i>MK</i><i>SA</i></div><div class="progress-line"><span style="width:78%"></span><small>%78</small></div><span class="status-pill status-progress">Devam ediyor</span></div><div class="project-list-row"><div><strong>Operasyonel verimlilik</strong><small>Perakende · #M-019</small></div><div class="avatar-stack"><i>DA</i><i>EC</i></div><div class="progress-line"><span style="width:54%"></span><small>%54</small></div><span class="status-pill status-progress">Devam ediyor</span></div><div class="project-list-row"><div><strong>Büyüme stratejisi 2027</strong><small>Finans · #M-031</small></div><div class="avatar-stack"><i>SY</i><i>AY</i></div><div class="progress-line"><span style="width:92%"></span><small>%92</small></div><span class="status-pill status-review">İncelemede</span></div></div></section><section class="admin-panel activity-panel"><div class="panel-heading"><div><span class="panel-eyebrow">SON HAREKETLER</span><h2>Akış</h2></div><span class="activity-dot"></span></div><ol class="activity-list"><li><span class="activity-icon">↗</span><div><strong>Yeni proje aşaması tamamlandı</strong><p>Dijital dönüşüm yol haritası</p><small>Bugün · 10:42</small></div></li><li><span class="activity-icon">✳</span><div><strong>Ekibe yeni üye katıldı</strong><p>Elif Çetin, Proje Yöneticisi</p><small>Dün · 16:18</small></div></li><li><span class="activity-icon">✓</span><div><strong>Rapor onaylandı</strong><p>Büyüme stratejisi 2027</p><small>22 Eylül · 09:30</small></div></li></ol></section></div>'''


user_rows = [
    ("Ayşe Yılmaz", "ayse.yilmaz@mihenk.com", "AY", "Yönetici", "Aktif", "24 Eyl 2026"),
    ("Mert Kara", "mert.kara@mihenk.com", "MK", "Editör", "Aktif", "23 Eyl 2026"),
    ("Selin Arslan", "selin.arslan@mihenk.com", "SA", "Editör", "Aktif", "21 Eyl 2026"),
    ("Derya Aksoy", "derya.aksoy@mihenk.com", "DA", "Görüntüleyici", "Aktif", "18 Eyl 2026"),
    ("Emre Can", "emre.can@mihenk.com", "EC", "Görüntüleyici", "Davet edildi", "15 Eyl 2026"),
    ("Seda Yıldız", "seda.yildiz@mihenk.com", "SY", "Editör", "Aktif", "12 Eyl 2026"),
]


def user_row(name, email, initials, role, status, date):
    return f'<tr data-user-row data-role="{role}"><td><div class="user-cell"><span class="avatar avatar-table">{initials}</span><span><strong>{name}</strong><small>{email}</small></span></div></td><td><span class="role-text">{role}</span></td><td><span class="status-pill {"status-invite" if status != "Aktif" else "status-active"}">{status}</span></td><td>{date}</td></tr>'


users_content = f'''<section class="admin-panel users-panel"><div class="panel-heading"><div><span class="panel-eyebrow">EKİP YÖNETİMİ</span><h2>Kullanıcı listesi <span class="count-badge" data-user-count>06</span></h2></div></div><div class="table-toolbar"><label class="search-box">{icon('search')}<span class="sr-only">Kullanıcı ara</span><input type="search" data-user-search placeholder="İsim veya e-posta ara"></label><label class="filter-select"><span class="sr-only">Role göre filtrele</span><select data-role-filter><option value="all">Tüm roller</option><option value="Yönetici">Yönetici</option><option value="Editör">Editör</option><option value="Görüntüleyici">Görüntüleyici</option></select></label></div><div class="table-scroll"><table class="users-table"><thead><tr><th scope="col">KULLANICI</th><th scope="col">ROL</th><th scope="col">DURUM</th><th scope="col">SON ETKİNLİK</th></tr></thead><tbody data-users-body>{''.join(user_row(*row) for row in user_rows)}</tbody></table></div><p class="empty-state" data-users-empty hidden>Aramanızla eşleşen kullanıcı bulunamadı.</p><div class="table-footer"><span data-users-visible>6 kullanıcı gösteriliyor</span><span>Veriler örnektir</span></div></section><dialog class="invite-dialog" data-invite-dialog><form method="dialog" class="dialog-close-form"><button type="submit" aria-label="Pencereyi kapat">{icon('close')}</button></form><span class="portal-kicker">EKİBE KATILIM</span><h2>Kullanıcı ekle</h2><p>Yeni kullanıcı bu önizlemede yalnızca tarayıcınıza eklenir.</p><form data-invite-form class="portal-form">{field('Ad Soyad', 'inviteName', 'text', None, 'Ad ve soyad', 'required')}{field('E-posta', 'inviteEmail', 'email', None, 'adiniz@firma.com', 'required')}<div class="portal-field"><label for="inviteRole">Rol</label><select id="inviteRole" name="inviteRole"><option>Editör</option><option>Görüntüleyici</option><option>Yönetici</option></select></div><button class="portal-button" type="submit">Kullanıcıyı ekle {icon('plus')}</button><p class="form-feedback" role="status" aria-live="polite"></p></form></dialog>'''


settings_content = f'''<div class="settings-grid"><section class="admin-panel form-panel"><div class="panel-heading"><div><span class="panel-eyebrow">GENEL AYARLAR</span><h2>Çalışma alanı</h2></div></div><p class="panel-description">Ekip ve kurum bilgilerini güncel tutun.</p><form data-settings-form class="admin-form"><div class="portal-field"><label for="workspaceName">Çalışma alanı adı</label><input id="workspaceName" name="workspaceName" value="Mihenk Danışmanlık" required></div><div class="portal-field"><label for="workspaceEmail">İletişim e-postası</label><input id="workspaceEmail" name="workspaceEmail" type="email" value="merhaba@mihenk.com" required></div><div class="portal-field"><label for="timezone">Saat dilimi</label><select id="timezone" name="timezone"><option value="Europe/Istanbul">İstanbul (GMT+3)</option><option value="Europe/London">Londra (GMT+1)</option><option value="Europe/Berlin">Berlin (GMT+2)</option></select></div><div class="portal-field"><label for="language">Dil</label><select id="language" name="language"><option value="tr">Türkçe</option><option value="en">English</option></select></div><div class="form-panel-actions"><button type="submit" class="portal-button">Değişiklikleri kaydet {icon('arrow')}</button><p class="form-feedback" role="status" aria-live="polite"></p></div></form></section><section class="settings-side"><div class="admin-panel preferences-panel"><div class="panel-heading"><div><span class="panel-eyebrow">TERCİHLER</span><h2>Bildirimler</h2></div></div><label class="toggle-row"><span><strong>E-posta özetleri</strong><small>Haftalık çalışma alanı özeti</small></span><input type="checkbox" data-setting-toggle="emailSummary" checked><span class="switch" aria-hidden="true"></span></label><label class="toggle-row"><span><strong>Proje güncellemeleri</strong><small>Önemli aşamalar ve değişiklikler</small></span><input type="checkbox" data-setting-toggle="projectUpdates" checked><span class="switch" aria-hidden="true"></span></label><label class="toggle-row"><span><strong>Ekip hareketleri</strong><small>Yeni üyeler ve rol değişiklikleri</small></span><input type="checkbox" data-setting-toggle="teamUpdates"><span class="switch" aria-hidden="true"></span></label></div><div class="help-card"><span>YARDIMA MI İHTİYACINIZ VAR?</span><h3>Birlikte çözelim.</h3><p>Ekibimizle iletişime geçerek çalışma alanınızla ilgili sorularınızı paylaşın.</p><a href="contact.html">İletişime geçin ↗</a></div></section></div>'''


profile_content = f'''<div class="profile-grid"><section class="admin-panel form-panel"><div class="panel-heading"><div><span class="panel-eyebrow">KİŞİSEL BİLGİLER</span><h2>Profil detayları</h2></div></div><div class="profile-identity"><span class="avatar avatar-large" data-avatar>AY</span><div><strong data-profile-name>Ayşe Yılmaz</strong><span>Yönetici hesabı</span></div></div><form data-profile-form class="admin-form"><div class="portal-form-grid"><div class="portal-field"><label for="profileFirstName">Ad</label><input id="profileFirstName" name="firstName" value="Ayşe" required></div><div class="portal-field"><label for="profileLastName">Soyad</label><input id="profileLastName" name="lastName" value="Yılmaz" required></div></div><div class="portal-field"><label for="profileEmail">E-posta adresi</label><input id="profileEmail" name="email" type="email" value="ayse.yilmaz@mihenk.com" required></div><div class="portal-field"><label for="profileTitle">Görev</label><input id="profileTitle" name="title" value="Strateji Direktörü"></div><div class="portal-field"><label for="profileBio">Kısa açıklama</label><textarea id="profileBio" name="bio" rows="4" placeholder="Kendinizden kısaca bahsedin">Strateji, dönüşüm ve güçlü ekipler üzerine çalışıyorum.</textarea></div><div class="form-panel-actions"><button type="submit" class="portal-button">Profili kaydet {icon('arrow')}</button><p class="form-feedback" role="status" aria-live="polite"></p></div></form></section><aside class="profile-side"><div class="admin-panel profile-summary"><span class="panel-eyebrow">HESAP ÖZETİ</span><div class="profile-summary-mark">M</div><h2>Her karar<br>bir iz bırakır.</h2><p>Profiliniz ekibinizle paylaştığınız çalışma alanının bir parçası.</p><div class="summary-line"><span>Rol</span><strong>Yönetici</strong></div><div class="summary-line"><span>Üyelik</span><strong>Aktif</strong></div></div><a class="profile-security" href="reset-password.html"><span>Parola ekranı</span><strong>Yeni parola görünümünü aç ↗</strong></a></aside></div>'''


pages = {
    "login.html": ("Giriş Yap", "Mihenk yönetim alanına giriş arayüzü.", login, "auth"),
    "register.html": ("Hesap Oluştur", "Mihenk yönetim alanı kayıt arayüzü.", register, "auth"),
    "forgot-password.html": ("Parolamı Unuttum", "Mihenk parola sıfırlama isteği arayüzü.", forgot, "auth"),
    "reset-password.html": ("Yeni Parola", "Mihenk yeni parola belirleme arayüzü.", reset, "auth"),
    "dashboard.html": ("Genel Bakış", "Mihenk yönetim paneli genel bakış önizlemesi.", admin_shell("dashboard", "Genel bakış", "Genel bakış", "Merhaba, <span data-greeting-name>Ayşe</span>. Çalışma alanınızın son durumu burada.", dashboard_content), "admin"),
    "settings.html": ("Ayarlar", "Mihenk yönetim paneli ayarlar önizlemesi.", admin_shell("settings", "Ayarlar", "Ayarlar", "Çalışma alanınızı ekibinizin ihtiyaçlarına göre düzenleyin.", settings_content), "admin"),
    "profile.html": ("Profilim", "Mihenk yönetim paneli profil önizlemesi.", admin_shell("profile", "Profilim", "Profilim", "Kişisel bilgilerinizi ve hesap görünümünüzü yönetin.", profile_content), "admin"),
}

if __name__ == "__main__":
    for filename, (title, description, body, kind) in pages.items():
        (ROOT / filename).write_text(shell(title, description, body, kind) + "\n", encoding="utf-8")
        print(filename)
