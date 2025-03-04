// Common functionality across the application
document.addEventListener('DOMContentLoaded', function() {
  // Add any global event listeners or functionality here
  
  // Example: Add active class to current nav link
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-links a');
  
  navLinks.forEach(link => {
    const linkPath = link.getAttribute('href');
    if (currentPath === linkPath || 
        (linkPath !== '/' && currentPath.startsWith(linkPath))) {
      link.classList.add('active');
    }
  });
}); 