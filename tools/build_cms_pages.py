"""Generate the eight browser-local Mihenk admin UI screens."""

from pathlib import Path
from build_portal import ROOT, admin_shell, icon, shell


def action(label):
    return f'<button class="admin-action" type="button" data-cms-new>{icon("plus")}{label}</button>'


def media_picker_dialog():
    return f'''<dialog class="cms-dialog media-picker" data-media-picker aria-labelledby="media-picker-title">
      <header class="cms-dialog-header"><div><span class="portal-kicker">MEDYA KÜTÜPHANESİ</span><h2 id="media-picker-title">Görsel seçin</h2><p class="cms-dialog-intro">İçeriğiniz için bir görsel seçin.</p></div><button class="cms-dialog-close" type="button" data-dialog-close aria-label="Pencereyi kapat">{icon('close')}</button></header>
      <div class="cms-dialog-main"><div class="picker-grid" data-picker-grid></div></div>
      <footer class="cms-dialog-footer"><button class="cms-secondary" type="button" data-dialog-close>Vazgeç</button></footer>
    </dialog>'''


def dialogs(kind):
    return f'''<dialog class="cms-dialog" data-cms-editor aria-labelledby="cms-dialog-title">
      <header class="cms-dialog-header"><div><span class="portal-kicker">MİHENK / İÇERİK</span><h2 id="cms-dialog-title" data-dialog-title>Kayıt düzenle</h2><p class="cms-dialog-intro" data-dialog-intro></p></div><button class="cms-dialog-close" type="button" data-dialog-close aria-label="Pencereyi kapat">{icon('close')}</button></header>
      <form data-cms-form class="cms-dialog-form"><div class="cms-dialog-main"><div class="cms-form-fields" data-cms-fields></div><p class="cms-form-error" role="alert" data-form-error></p></div><footer class="cms-dialog-footer"><button class="cms-secondary" type="button" data-dialog-close>Vazgeç</button><button class="portal-button" type="submit">Kaydet {icon('arrow')}</button></footer></form>
    </dialog><dialog class="cms-confirm" data-cms-confirm aria-labelledby="cms-confirm-title">
      <header class="cms-dialog-header"><div><span class="portal-kicker">SİLME ONAYI</span><h2 id="cms-confirm-title">Bu kaydı sil?</h2></div></header>
      <div class="cms-dialog-main"><p data-confirm-copy>Bu işlem geri alınamaz.</p></div>
      <footer class="cms-dialog-footer"><button class="cms-secondary" type="button" data-dialog-close>Vazgeç</button><button class="cms-danger" type="button" data-confirm-delete>Kalıcı olarak sil</button></footer>
    </dialog>{media_picker_dialog()}'''


def list_page(kind, eyebrow, label, description, new_label=None, filters=True, media=False, side=""):
    options = {
        'inquiries': [('all', 'Tüm durumlar'), ('new', 'Yeni'), ('in_progress', 'İşlemde'), ('done', 'Tamamlandı'), ('archived', 'Arşiv')],
        'users': [('all', 'Tüm roller'), ('admin', 'Yönetici'), ('editor', 'Editör'), ('viewer', 'Görüntüleyici')],
    }.get(kind, [('all', 'Tüm durumlar'), ('published', 'Yayında'), ('draft', 'Taslak')])
    filters_markup = '<select data-cms-filter aria-label="Filtrele">' + ''.join(f'<option value="{value}">{title}</option>' for value, title in options) + '</select>' if filters else ''
    content = f'''<section class="cms-intro-strip"><span>{eyebrow}</span><strong data-cms-count>—</strong><p>{description}</p></section><div class="cms-layout"><section class="admin-panel cms-panel"><div class="panel-heading"><div><span class="panel-eyebrow">{eyebrow}</span><h2>{label} listesi</h2></div><span class="cms-updated" data-cms-updated>Örnek veriler</span></div><div class="cms-toolbar"><label class="cms-search">{icon('search')}<span class="sr-only">Ara</span><input type="search" data-cms-search placeholder="{label} içinde ara"></label>{filters_markup}</div><div class="{'cms-media-grid' if media else 'cms-list'}" data-cms-list></div><p class="cms-empty" data-cms-empty hidden>Bu filtreyle eşleşen kayıt bulunamadı.</p><div class="cms-panel-footer"><span data-cms-visible></span><span>Değişiklikler yalnızca bu tarayıcıda görünür</span></div></section>{side}</div>{dialogs(kind)}<p class="cms-toast" role="status" aria-live="polite" data-cms-toast></p>'''
    return f'<div data-cms-page="{kind}">{content}</div>', action(new_label) if new_label else ''


inquiry_side = '''<aside class="cms-side-card"><span class="panel-eyebrow">TALEP AKIŞI</span><h3>Her görüşme bir başlangıç.</h3><p>Yeni talepleri okuyun, sorumlu kişiyi atayın ve yanıt sürecini takip edin.</p><div class="cms-side-step"><span>01</span>Yeni talep</div><div class="cms-side-step"><span>02</span>İşlemde</div><div class="cms-side-step"><span>03</span>Tamamlandı</div></aside>'''
role_side = '''<aside class="cms-side-card role-card"><span class="panel-eyebrow">YETKİ MATRİSİ</span><h3>Doğru erişim,<br>net sorumluluk.</h3><div class="role-matrix"><div><strong>Yönetici</strong><span>Tüm içerikler, talepler, ekip ve SEO</span></div><div><strong>Editör</strong><span>İçerikler, medya ve talepler</span></div><div><strong>Görüntüleyici</strong><span>Okuma erişimi</span></div></div><p>Bu ekrandaki roller arayüz önizlemesidir; gerçek yetki kontrolü için sunucu gerekir.</p></aside>'''


pages = {}

for filename, kind, eyebrow, title, subtitle, label, new_label, side, filters, media in [
    ("inquiries.html", "inquiries", "GELEN KUTUSU", "İletişim talepleri", "Örnek mesajları inceleyin ve takip durumunu düzenleyin.", "Talep", None, inquiry_side, True, False),
    ("blog-admin.html", "blog", "MİHENK JOURNAL", "Blog yönetimi", "Yazıları hazırlayın, önizleyin ve yayınlayın.", "Yazı", "Yeni yazı", "", True, False),
    ("projects-admin.html", "projects", "SEÇİLİ ÇALIŞMALAR", "Proje yönetimi", "Vaka çalışmalarını ve proje vitrininizi güncelleyin.", "Proje", "Yeni proje", "", True, False),
    ("services-admin.html", "services", "UZMANLIK ALANLARI", "Hizmetler", "Hizmet açıklamalarını ve görünürlük durumunu yönetin.", "Hizmet", "Yeni hizmet", "", True, False),
    ("testimonials-admin.html", "testimonials", "MÜŞTERİ SESİ", "Müşteri yorumları", "Ana sayfadaki müşteri yorumlarını düzenleyin.", "Yorum", "Yeni yorum", "", True, False),
    ("media-admin.html", "media", "GÖRSEL ARŞİVİ", "Medya kütüphanesi", "Görselleri önizleyin ve içerik taslaklarında kullanın.", "Görsel", "Görsel yükle", "", False, True),
    ("users.html", "users", "EKİP YÖNETİMİ", "Ekip ve rol yetkileri", "Hesapları, durumları ve erişim rollerini yönetin.", "Üye", "Üye ekle", role_side, True, False),
]:
    content, actions = list_page(kind, eyebrow, label, subtitle, new_label, filters, media, side)
    pages[filename] = (title, subtitle, admin_shell(kind, title, title, subtitle, content, actions))

seo_content = f'''<div data-cms-page="seo"><div class="seo-layout"><section class="admin-panel seo-editor"><div class="panel-heading"><div><span class="panel-eyebrow">ARAMA GÖRÜNÜRLÜĞÜ</span><h2>Sayfa meta bilgileri</h2></div></div><p>Arama ve paylaşım önizlemelerinde görünen metinleri düzenleyin.</p><label class="portal-field"><span>Sayfa</span><select data-seo-page aria-label="SEO sayfası seçin"></select></label><form data-seo-form class="admin-form"><div class="portal-field"><label for="seoTitle">Meta başlık</label><input id="seoTitle" name="title" required maxlength="180"><small><span data-title-count>0</span> / 180 karakter</small></div><div class="portal-field"><label for="seoDescription">Meta açıklama</label><textarea id="seoDescription" name="description" rows="4" required maxlength="300"></textarea><small><span data-description-count>0</span> / 300 karakter</small></div><div class="portal-field"><label for="seoImage">Paylaşım görseli URL</label><input id="seoImage" name="ogImage" placeholder="assets/images/hero-team.webp"><button class="cms-inline-button" type="button" data-choose-media>Medya kütüphanesinden seç</button></div><p class="cms-form-error" role="alert" data-form-error></p><button class="portal-button" type="submit">SEO ayarlarını kaydet {icon('arrow')}</button></form></section><aside class="admin-panel seo-preview"><span class="panel-eyebrow">CANLI ÖNİZLEME</span><div class="search-preview"><small data-seo-url>mihenk.com</small><strong data-seo-preview-title>Mihenk Danışmanlık</strong><p data-seo-preview-description>Sayfa açıklaması burada görünür.</p></div><div class="seo-share-preview"><div class="seo-share-image" data-seo-share-image></div><div><small>PAYLAŞIM KARTI</small><strong data-seo-share-title>Mihenk Danışmanlık</strong><p data-seo-share-description></p></div></div><p class="seo-tip">Başlık ve açıklama arama motorlarınca farklı uzunluklarda gösterilebilir. Önizleme yaklaşık görünümü gösterir.</p></aside></div>{media_picker_dialog()}<p class="cms-toast" role="status" aria-live="polite" data-cms-toast></p></div>'''
pages["seo.html"] = ("SEO ayarları", "Sayfa başlıklarını ve paylaşım görsellerini düzenleyin.", admin_shell("seo", "SEO ayarları", "SEO ayarları", "Sayfalarınızın arama ve paylaşım görünümünü yönetin.", seo_content))

for filename, (title, description, body) in pages.items():
    (ROOT / filename).write_text(shell(title, description, body, "admin") + "\n", encoding="utf-8")
    print(filename)
