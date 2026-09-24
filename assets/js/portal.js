(() => {
  'use strict';

  const read = (key, fallback = {}) => {
    try { return JSON.parse(localStorage.getItem(`mihenk-${key}`)) || fallback; }
    catch { return fallback; }
  };
  const write = (key, value) => {
    try { localStorage.setItem(`mihenk-${key}`, JSON.stringify(value)); }
    catch { /* Önizleme depolaması kullanılamıyorsa sayfa yine çalışır. */ }
  };
  const initials = (name) => name.trim().split(/\s+/).slice(0, 2).map((part) => part[0]?.toLocaleUpperCase('tr-TR') || '').join('');
  const setFeedback = (form, message, error = false) => {
    const feedback = form.querySelector('.form-feedback');
    if (feedback) { feedback.textContent = message; feedback.classList.toggle('is-error', error); }
  };

  document.querySelectorAll('[data-password-toggle]').forEach((button) => {
    button.addEventListener('click', () => {
      const input = button.parentElement.querySelector('input');
      const visible = input.type === 'password';
      input.type = visible ? 'text' : 'password';
      button.textContent = visible ? 'Gizle' : 'Göster';
      button.setAttribute('aria-label', visible ? 'Parolayı gizle' : 'Parolayı göster');
    });
  });

  const remembered = read('remember');
  const loginForm = document.querySelector('[data-auth-form="login"]');
  if (loginForm && remembered.email) {
    loginForm.elements.namedItem('email').value = remembered.email;
    loginForm.elements.namedItem('remember').checked = true;
  }
  document.querySelectorAll('[data-auth-form]').forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const kind = form.dataset.authForm;
      const data = Object.fromEntries(new FormData(form));
      if ((kind === 'register' || kind === 'reset') && data.password !== data.confirmPassword) {
        setFeedback(form, 'Parolalar eşleşmiyor.', true);
        return;
      }
      if (kind === 'login') {
        write('remember', data.remember ? { email: data.email } : {});
        location.href = 'dashboard.html';
      } else if (kind === 'register') {
        write('profile', { firstName: data.firstName, lastName: data.lastName, name: `${data.firstName} ${data.lastName}`, email: data.email, title: '', bio: '' });
        location.href = 'dashboard.html';
      } else if (kind === 'forgot') {
        setFeedback(form, 'Önizleme adımı hazır. E-posta gönderilmedi.');
        const link = form.querySelector('[data-reset-link]');
        if (link) link.hidden = false;
      } else if (kind === 'reset') setFeedback(form, 'Parola görünümü tamamlandı. Gerçek parola değiştirilmedi.');
    });
  });

  const profile = read('profile', { firstName: 'Ayşe', lastName: 'Yılmaz', name: 'Ayşe Yılmaz', email: 'ayse.yilmaz@mihenk.com', title: 'Strateji Direktörü', bio: 'Strateji, dönüşüm ve güçlü ekipler üzerine çalışıyorum.' });
  const showIdentity = () => {
    const name = profile.name || `${profile.firstName} ${profile.lastName}`.trim() || 'Ayşe Yılmaz';
    document.querySelectorAll('[data-profile-name]').forEach((node) => { node.textContent = name; });
    document.querySelectorAll('[data-greeting-name]').forEach((node) => { node.textContent = name.split(' ')[0]; });
    document.querySelectorAll('[data-avatar]').forEach((node) => { node.textContent = initials(name); });
  };
  showIdentity();

  const profileForm = document.querySelector('[data-profile-form]');
  if (profileForm) {
    ['firstName', 'lastName', 'email', 'title', 'bio'].forEach((key) => {
      const field = profileForm.elements.namedItem(key);
      if (field && profile[key] !== undefined) field.value = profile[key];
    });
    profileForm.addEventListener('submit', (event) => {
      event.preventDefault();
      if (!profileForm.reportValidity()) return;
      Object.assign(profile, Object.fromEntries(new FormData(profileForm)));
      profile.name = `${profile.firstName} ${profile.lastName}`.trim();
      write('profile', profile);
      showIdentity();
      setFeedback(profileForm, 'Profil bilgileri bu tarayıcıda kaydedildi.');
    });
  }

  const settingsForm = document.querySelector('[data-settings-form]');
  if (settingsForm) {
    const settings = read('settings');
    ['workspaceName', 'workspaceEmail', 'timezone', 'language'].forEach((key) => {
      const field = settingsForm.elements.namedItem(key);
      if (field && settings[key] !== undefined) field.value = settings[key];
    });
    const toggles = [...document.querySelectorAll('[data-setting-toggle]')];
    toggles.forEach((input) => {
      if (settings[input.dataset.settingToggle] !== undefined) input.checked = settings[input.dataset.settingToggle];
      input.addEventListener('change', () => write('settings', { ...read('settings'), [input.dataset.settingToggle]: input.checked }));
    });
    settingsForm.addEventListener('submit', (event) => {
      event.preventDefault();
      if (!settingsForm.reportValidity()) return;
      write('settings', { ...read('settings'), ...Object.fromEntries(new FormData(settingsForm)) });
      setFeedback(settingsForm, 'Ayarlar bu tarayıcıda kaydedildi.');
    });
  }

  const menuButton = document.querySelector('[data-menu-open]');
  const menu = document.querySelector('#admin-sidebar');
  const backdrop = document.querySelector('.admin-backdrop');
  const closeMenu = () => {
    menu?.classList.remove('is-open');
    backdrop?.classList.remove('is-open');
    menuButton?.setAttribute('aria-expanded', 'false');
  };
  menuButton?.addEventListener('click', () => {
    menu?.classList.add('is-open');
    backdrop?.classList.add('is-open');
    menuButton.setAttribute('aria-expanded', 'true');
  });
  document.querySelectorAll('[data-menu-close]').forEach((node) => node.addEventListener('click', closeMenu));
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') closeMenu(); });

  const now = new Date();
  document.querySelectorAll('[data-year]').forEach((node) => { node.textContent = now.getFullYear(); });
  document.querySelectorAll('[data-today]').forEach((node) => { node.textContent = new Intl.DateTimeFormat('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }).format(now); });
})();
