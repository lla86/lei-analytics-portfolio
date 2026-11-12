const navigationLinks = document.querySelectorAll('.case-nav a');
if ('IntersectionObserver' in window && navigationLinks.length) {
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        for (const link of navigationLinks) {
          if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        }
      }
    }
  }, { rootMargin: '-15% 0px -60% 0px' });
  for (const link of navigationLinks) {
    const section = document.querySelector(link.hash);
    if (section) observer.observe(section);
  }
}
