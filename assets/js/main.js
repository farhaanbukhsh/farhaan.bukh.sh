document.addEventListener('DOMContentLoaded', () => {
  /* ── Nav toggle (mobile) ─────────────────────────────────────── */
  const navToggle = document.querySelector('[data-nav-toggle]');
  const navLinks = document.querySelector('[data-nav-links]');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      const isOpen = navLinks.dataset.open === 'true';
      navLinks.dataset.open = String(!isOpen);
      navToggle.setAttribute('aria-expanded', String(!isOpen));
    });
  }

  /* ── Inventory tray ──────────────────────────────────────────── */
  const inventoryToggle = document.querySelector('[data-inventory-toggle]');
  const inventoryOverlay = document.querySelector('[data-inventory-overlay]');
  const inventoryClose = document.querySelector('[data-inventory-close]');
  const inventoryTray = document.querySelector('[data-inventory-tray]');

  const openInventory = () => {
    if (!inventoryOverlay) return;
    inventoryOverlay.dataset.open = 'true';
    inventoryOverlay.classList.add('is-open');
    inventoryOverlay.removeAttribute('aria-hidden');
    if (inventoryToggle) inventoryToggle.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  };

  const closeInventory = () => {
    if (!inventoryOverlay) return;
    inventoryOverlay.dataset.open = 'false';
    inventoryOverlay.classList.remove('is-open');
    inventoryOverlay.setAttribute('aria-hidden', 'true');
    if (inventoryToggle) inventoryToggle.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  };

  if (inventoryToggle) {
    inventoryToggle.addEventListener('click', openInventory);
  }

  if (inventoryClose) {
    inventoryClose.addEventListener('click', closeInventory);
  }

  // Prevent overlay-close when clicking inside the tray
  if (inventoryTray && inventoryOverlay) {
    inventoryTray.addEventListener('click', (e) => e.stopPropagation());
  }

  // Close on overlay backdrop click
  if (inventoryOverlay) {
    inventoryOverlay.addEventListener('click', (e) => {
      if (e.target === inventoryOverlay) closeInventory();
    });
  }

  // Close on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && inventoryOverlay?.dataset.open === 'true') {
      closeInventory();
    }
  });

  /* ── Year stamp ──────────────────────────────────────────────── */
  document.querySelectorAll('[data-current-year]').forEach((el) => {
    el.textContent = new Date().getFullYear();
  });
});
