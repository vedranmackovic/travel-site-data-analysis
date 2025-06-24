document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('[data-target="#loginModal"], [data-target="#signupModal"]').forEach(el => {
    el.addEventListener('click', function(e) {
      e.preventDefault();
      const target = this.getAttribute('data-target');
      document.querySelector(target).style.display = 'flex';
    });
  });

  document.querySelectorAll('.custom-modal .close').forEach(btn => {
    btn.addEventListener('click', function() {
      this.closest('.custom-modal').style.display = 'none';
    });
  });

  document.querySelectorAll('.custom-modal').forEach(modal => {
    modal.addEventListener('click', function(e) {
      if (e.target === this) {
        this.style.display = 'none';
      }
    });
  });
});