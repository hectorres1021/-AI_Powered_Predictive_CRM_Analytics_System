/* ============================================================
   SERENITY SPA — JavaScript
   - Mobile navigation toggle
   - Booking form submission
   - Smooth active nav highlighting
   ============================================================ */

(function () {
  'use strict';

  /* ---------- Mobile Nav ---------- */
  const navToggle = document.querySelector('.nav-toggle');
  const navMenu   = document.getElementById('nav-menu');

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      const isOpen = navMenu.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
      // Swap icon between hamburger and close
      navToggle.innerHTML = isOpen
        ? `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true" focusable="false"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`
        : `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true" focusable="false"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>`;
    });

    // Close nav when a link is clicked (mobile)
    navMenu.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.innerHTML = `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true" focusable="false"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>`;
      });
    });

    // Close nav on outside click
    document.addEventListener('click', (e) => {
      if (!navMenu.contains(e.target) && !navToggle.contains(e.target)) {
        navMenu.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---------- Set min date for booking calendar ---------- */
  const dateInput = document.getElementById('preferred-date');
  if (dateInput) {
    const today = new Date();
    const yyyy  = today.getFullYear();
    const mm    = String(today.getMonth() + 1).padStart(2, '0');
    const dd    = String(today.getDate()).padStart(2, '0');
    dateInput.setAttribute('min', `${yyyy}-${mm}-${dd}`);
  }

  /* ---------- Booking Form ---------- */
  const bookingForm = document.getElementById('booking-form');
  const formSuccess = document.getElementById('form-success');

  if (bookingForm && formSuccess) {
    bookingForm.addEventListener('submit', (e) => {
      e.preventDefault();

      // Basic HTML5 validation check
      if (!bookingForm.checkValidity()) {
        bookingForm.reportValidity();
        return;
      }

      // Simulate async submission
      const submitBtn = bookingForm.querySelector('[type="submit"]');
      submitBtn.disabled  = true;
      submitBtn.textContent = 'Sending…';

      setTimeout(() => {
        bookingForm.hidden  = true;
        formSuccess.hidden  = false;
        formSuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 900);
    });
  }

  /* ---------- Active section highlighting in nav ---------- */
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');

  if (sections.length && navLinks.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            navLinks.forEach((link) => {
              const href = link.getAttribute('href');
              link.classList.toggle(
                'nav-link--active',
                href === `#${entry.target.id}`
              );
            });
          }
        });
      },
      { rootMargin: '-40% 0px -55% 0px' }
    );

    sections.forEach((s) => observer.observe(s));
  }

})();
