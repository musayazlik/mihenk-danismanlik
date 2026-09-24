(() => {
  'use strict';

  let sequence = 0;
  const instances = new WeakMap();
  let opened = null;

  function close(instance, restoreFocus = false) {
    if (!instance) return;
    instance.list.hidden = true;
    instance.wrapper.classList.remove('is-open', 'opens-up');
    instance.trigger.setAttribute('aria-expanded', 'false');
    if (opened === instance) opened = null;
    if (restoreFocus) instance.trigger.focus();
  }

  function position(instance) {
    const bounds = instance.trigger.getBoundingClientRect();
    const scrollArea = instance.trigger.closest('.cms-dialog-main');
    const bottom = scrollArea ? Math.min(window.innerHeight - 12, scrollArea.getBoundingClientRect().bottom) : window.innerHeight - 12;
    const top = scrollArea ? Math.max(12, scrollArea.getBoundingClientRect().top) : 12;
    const roomBelow = bottom - bounds.bottom;
    const roomAbove = bounds.top - top;
    const opensUp = roomBelow < 225 && roomAbove > roomBelow;
    instance.wrapper.classList.toggle('opens-up', opensUp);
    instance.list.style.maxHeight = `${Math.max(80, Math.min(240, (opensUp ? roomAbove : roomBelow) - 10))}px`;
  }

  function optionButtons(instance) {
    return [...instance.list.querySelectorAll('.custom-select-option')];
  }

  function focusOption(instance, index) {
    const buttons = optionButtons(instance);
    if (!buttons.length) return;
    let target = Math.max(0, Math.min(index, buttons.length - 1));
    while (target < buttons.length - 1 && buttons[target].disabled) target++;
    while (target > 0 && buttons[target].disabled) target--;
    if (!buttons[target].disabled) buttons[target].focus();
  }

  function open(instance, focusIndex = null) {
    if (opened && opened !== instance) close(opened);
    instance.refresh();
    instance.list.hidden = false;
    instance.wrapper.classList.add('is-open');
    instance.trigger.setAttribute('aria-expanded', 'true');
    position(instance);
    opened = instance;
    if (focusIndex !== null) focusOption(instance, focusIndex);
  }

  function selectOption(instance, value) {
    if (instance.select.value !== value) {
      instance.select.value = value;
      instance.select.dispatchEvent(new Event('input', { bubbles: true }));
      instance.select.dispatchEvent(new Event('change', { bubbles: true }));
    }
    instance.trigger.removeAttribute('aria-invalid');
    instance.error.hidden = true;
    instance.refresh();
    close(instance, true);
  }

  function enhance(select) {
    if (instances.has(select)) return instances.get(select);
    if (select.multiple || select.size > 1 || select.disabled || !select.parentNode) return null;

    const wrapper = document.createElement('div');
    wrapper.className = 'custom-select';
    select.parentNode.insertBefore(wrapper, select);
    wrapper.append(select);
    select.classList.add('custom-select-native');
    select.tabIndex = -1;
    select.setAttribute('aria-hidden', 'true');

    const trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'custom-select-trigger';
    trigger.setAttribute('role', 'combobox');
    trigger.setAttribute('aria-haspopup', 'listbox');
    trigger.setAttribute('aria-expanded', 'false');
    if (select.required) trigger.setAttribute('aria-required', 'true');
    const label = select.id ? document.querySelector(`label[for="${CSS.escape(select.id)}"]`) : null;
    trigger.setAttribute('aria-label', select.getAttribute('aria-label') || label?.textContent.trim() || select.closest('label')?.querySelector('span')?.textContent.trim() || 'Seçenek seçin');
    const value = document.createElement('span');
    value.className = 'custom-select-value';
    const chevron = document.createElement('span');
    chevron.className = 'custom-select-chevron';
    chevron.setAttribute('aria-hidden', 'true');
    trigger.append(value, chevron);

    const list = document.createElement('div');
    list.className = 'custom-select-list';
    list.id = `custom-select-list-${++sequence}`;
    list.setAttribute('role', 'listbox');
    list.hidden = true;
    trigger.setAttribute('aria-controls', list.id);
    wrapper.append(trigger, list);

    const error = document.createElement('small');
    error.className = 'custom-select-error';
    error.id = `custom-select-error-${sequence}`;
    error.textContent = 'Lütfen bir seçenek seçin.';
    error.hidden = true;
    wrapper.append(error);
    trigger.setAttribute('aria-describedby', error.id);

    const instance = { select, wrapper, trigger, list, error, refresh() {
      const selected = select.selectedOptions[0];
      value.textContent = selected?.textContent || 'Seçin';
      list.replaceChildren(...[...select.options].map((option, index) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'custom-select-option';
        button.setAttribute('role', 'option');
        button.setAttribute('aria-selected', option.selected ? 'true' : 'false');
        button.dataset.index = String(index);
        button.textContent = option.textContent;
        button.disabled = option.disabled;
        button.addEventListener('click', () => selectOption(instance, option.value));
        return button;
      }));
    } };
    instances.set(select, instance);
    instance.refresh();

    select.addEventListener('change', () => {
      if (select.validity.valid) {
        trigger.removeAttribute('aria-invalid');
        error.hidden = true;
      }
      instance.refresh();
    });
    select.addEventListener('focus', () => trigger.focus());
    select.addEventListener('invalid', (event) => {
      event.preventDefault();
      trigger.setAttribute('aria-invalid', 'true');
      error.hidden = false;
      trigger.focus();
    });
    label?.addEventListener('click', (event) => { event.preventDefault(); trigger.focus(); });
    trigger.addEventListener('click', () => opened === instance ? close(instance) : open(instance, Math.max(0, select.selectedIndex)));
    trigger.addEventListener('keydown', (event) => {
      if (['ArrowDown', 'ArrowUp', 'Home', 'End', ' '].includes(event.key)) {
        event.preventDefault();
        const index = event.key === 'End' ? select.options.length - 1 : event.key === 'Home' ? 0 : Math.max(0, select.selectedIndex + (event.key === 'ArrowUp' ? -1 : event.key === 'ArrowDown' ? 1 : 0));
        open(instance, index);
      } else if (event.key === 'Escape') { event.preventDefault(); event.stopPropagation(); close(instance); }
    });
    list.addEventListener('keydown', (event) => {
      const buttons = optionButtons(instance);
      const current = buttons.indexOf(document.activeElement);
      if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
        event.preventDefault();
        focusOption(instance, current + (event.key === 'ArrowDown' ? 1 : -1));
      } else if (event.key === 'Home' || event.key === 'End') {
        event.preventDefault();
        focusOption(instance, event.key === 'Home' ? 0 : buttons.length - 1);
      } else if (event.key === 'Escape') {
        event.preventDefault();
        event.stopPropagation();
        close(instance, true);
      } else if (event.key === 'Tab') close(instance);
    });
    return instance;
  }

  function enhanceAll(scope = document) {
    scope.querySelectorAll('select').forEach(enhance);
  }

  document.addEventListener('pointerdown', (event) => {
    if (opened && !opened.wrapper.contains(event.target)) close(opened);
  });
  document.addEventListener('focusin', (event) => {
    if (opened && !opened.wrapper.contains(event.target)) close(opened);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && opened) close(opened);
  });
  window.addEventListener('resize', () => { if (opened) position(opened); });
  window.MihenkSelect = { enhanceAll, refresh(select) { instances.get(select)?.refresh(); }, closeOpen() { close(opened); } };
  enhanceAll();
})();
