// IEI Jharkhand State Centre – Main JS

document.addEventListener('DOMContentLoaded', function() {

  // Auto-dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(function(alert) {
    setTimeout(function() {
      const bsAlert = new bootstrap.Alert(alert);
      if (bsAlert) { try { bsAlert.close(); } catch(e) {} }
    }, 5000);
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Add active state to current nav links
  const currentPath = window.location.pathname;
  document.querySelectorAll('.main-nav .nav-link').forEach(function(link) {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // Table-navy responsive
  const tables = document.querySelectorAll('.table');
  tables.forEach(function(table) {
    if (!table.parentElement.classList.contains('table-responsive')) {
      const wrapper = document.createElement('div');
      wrapper.className = 'table-responsive';
      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    }
  });

});
