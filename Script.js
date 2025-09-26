
document.addEventListener('DOMContentLoaded', function () {
    var el = document.getElementById('carrusel-caracteristicas');
    if (!el || typeof bootstrap === 'undefined') return;

    // Explicitly initialize the carousel with wrap disabled
    var carousel = new bootstrap.Carousel(el, { wrap: false, keyboard: false, ride: false });

    // Wire up prev/next buttons (defensive in case data attributes don't work)
    var prevBtn = el.querySelector('.carousel-control-prev');
    var nextBtn = el.querySelector('.carousel-control-next');
    if (prevBtn) prevBtn.addEventListener('click', function (e) { e.preventDefault(); carousel.prev(); });
    if (nextBtn) nextBtn.addEventListener('click', function (e) { e.preventDefault(); carousel.next(); });

    // Keyboard navigation: left/right arrows when the carousel has focus
    el.setAttribute('tabindex', '0');
    el.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowLeft') carousel.prev();
        if (e.key === 'ArrowRight') carousel.next();
    });
});    

  // Seleccionamos todos los enlaces del navbar
  const enlaces = document.querySelectorAll('.navbar-nav .nav-link');

  enlaces.forEach(enlace => {
    enlace.addEventListener('click', function() {
      // quitar 'activo' de todos
      enlaces.forEach(e => e.classList.remove('activo'));
      
      // agregar 'activo' al clicado
      this.classList.add('activo');
    });
  });

    