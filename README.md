# Mihenk — Business Consulting HTML Template

Düz HTML/CSS ve küçük bir JavaScript dosyasıyla çalışan, Türkçe danışmanlık ve blog sitesi şablonu.

## Sayfalar

- `index.html` — ana sayfa
- `about.html` — hakkımızda
- `services.html` — hizmetler ve SSS
- `projects.html` — filtrelenebilir proje vitrini
- `contact.html` — iletişim formu
- `blog.html` — arama, kategori filtreleri ve boş sonuç görünümü olan blog arşivi
- `blog-*.html` — altı ayrı yazı detayı; okuma süresi, paylaşım, popüler içerikler, ilgili yazılar ve yorumlar
- `login.html`, `register.html`, `forgot-password.html`, `reset-password.html` — yönetim alanı giriş ve parola arayüzleri
- `dashboard.html`, `settings.html`, `profile.html` — temel yönetim paneli sayfaları
- `inquiries.html`, `blog-admin.html`, `projects-admin.html`, `services-admin.html`, `testimonials-admin.html`, `media-admin.html`, `users.html`, `seo.html` — iletişim, içerik, medya, ekip ve SEO yönetimi arayüzleri

## Önizleme

`index.html` dosyasını doğrudan açabilir veya proje klasöründe `python3 -m http.server 8000` komutunu çalıştırıp `http://localhost:8000` adresine gidebilirsiniz. Derleme, Bootstrap veya başka bir çatı gerektirmez.

## Özelleştirme

- Renkler, tipografi ve aralıklar: `assets/css/style.css` içindeki `:root` değişkenleri.
- İçerik: ilgili `.html` dosyaları. Genel site ve blog sayfalarını yeniden üretmek için `python3 tools/build_pages.py` kullanılabilir; bu komut üretilmiş HTML değişikliklerini yeniden yazar. Blog yazıları `tools/blog_content.py` dosyasında düzenlenir.
- Yönetim alanının temel sayfaları `python3 tools/build_portal.py`, yeni içerik ekranları `python3 tools/build_cms_pages.py` ile yeniden üretilebilir. Tasarım stilleri `assets/css/portal.css` ve `assets/css/cms.css`, etkileşimler `assets/js/portal.js` ve `assets/js/cms.js` içindedir.
- Etkileşimler: `assets/js/main.js`. Mobil menü, açılır alt menüler, görünürlük animasyonu, sayaçlar, proje ve blog filtreleri, paylaşım ve yorum davranışı burada.
- Blog görünümü: `assets/css/blog.css`.
- Görseller: `assets/images/`.

**Yayına almadan önce:** `merhaba@example.com`, örnek telefon numarası, sosyal medya adresleri, ofis bilgisi, müşteri yorumları, metrikler ve proje anlatımlarını gerçek bilgilerle değiştirin. Proje ve müşteri içerikleri bu şablonda temsili verilerdir. İletişim formu bir sunucuya veri göndermez; ziyaretçinin e-posta uygulamasında taslak açar. Sunucuya kayıt/gönderim isteniyorsa form için ayrıca bir backend bağlanmalıdır.

Blog yazıları ve ilk iki yorum örnek içeriktir. Ziyaretçinin eklediği yorumlar yalnızca kendi tarayıcısının `localStorage` alanında tutulur; diğer ziyaretçilere görünmez. Ortak yorum alanı veya içerik yönetimi için backend gerekir. Paylaşım düğmeleri yayımlanan sayfanın güncel URL'sini kullanır.

Yönetim alanı statik bir arayüz önizlemesidir. Giriş, kayıt ve parola sıfırlama formları gerçek kimlik doğrulama veya e-posta gönderimi yapmaz. İçerik, talep, medya, ekip, SEO, profil ve ayar örnekleri yalnızca tarayıcının `localStorage` alanında saklanır; genel site sayfalarına yansımaz. Arama, filtre, düzenleme ve silme pencereleri tasarımı deneyimlemek için çalışır. Gerçek kullanım için kimlik doğrulama, yetkilendirme, sunucu API'leri ve site içerikleriyle bağlantı gerekir.

## Görsel üretimi

Görseller yerel projeye dahil edilmiş özgün yapay zekâ üretimleridir; ImageGen yerleşik aracıyla oluşturulup WebP olarak optimize edildi. Son istemler:

- `hero-team.webp`: “Confident, contemporary consulting team in a refined modern office; one senior Black woman leader in a charcoal tailored suit in sharp focus on the right, two colleagues softly visible by a window. Wide editorial photograph with dark negative space on the left for a headline, warm concrete and glass, late afternoon light, midnight blue shadows and restrained amber. Natural skin detail; no text, logos, watermark or UI.”
- `strategy-team.webp`: “Three senior consultants collaborating over printed charts and a tablet in a sophisticated office; diverse team, candid and engaged. Wide architectural editorial photography, believable faces and hands, soft daylight, warm neutrals and graphite navy; no text, logos, watermark or UI.”
- `architecture.webp`: “Modern glass office tower facade seen from street level looking upward, clear geometric rhythm and faint sky reflections. Wide landscape with tower on the right and sky on the left, crisp morning light, navy and slate palette; no text, logos, people or watermark.”
- `operations.webp`: “Modern industrial design and logistics space with warm wood and dark metal shelving receding into the distance; an employee in silhouette reviews a tablet. Landscape editorial photography, architectural leading lines, cinematic side light, blue-gray shadows and amber practical lights; no text, logos or watermark.”

Blogdaki altı yazının her biri için ayrıca farklı bir görsel üretildi: `blog-strategy.webp`, `blog-digital.webp`, `blog-operations.webp`, `blog-leadership.webp`, `blog-data.webp` ve `blog-sustainability.webp`. Bu görsellerin tam ImageGen istemleri `tools/blog_image_prompts.md` dosyasındadır.

## Erişilebilirlik ve hareket

Klavyeyle erişilebilir menü ve filtreler, görünür odak stili, form etiketleri, anlamlı alternatif metinler ve `prefers-reduced-motion` desteği bulunur.
