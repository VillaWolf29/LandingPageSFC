
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



// Animación de scroll para la sección de servicios
document.addEventListener('DOMContentLoaded', () => {
  const wrapper = document.querySelector('#seccion-servicios');
  const servicios = document.querySelectorAll('.fila-servicio');

  if (!wrapper || servicios.length === 0) return;

  const total = servicios.length;
  wrapper.style.setProperty('--numcards', total);

  if (typeof ViewTimeline === 'undefined' || typeof CSS === 'undefined' || typeof CSS.percent !== 'function') {
    console.warn('Scroll-driven animations no soportado en este navegador');
    return;
  }

  const timeline = new ViewTimeline({
    subject: wrapper,
    axis: 'block'
  });

  servicios.forEach((servicio, i) => {
    const index = i + 1;
    const reverse = total - index;
    const endScale = 1 - (0.1 * reverse);

    servicio.animate(
      { transform: [ `scale(1)`, `scale(${endScale})` ] },
      {
        timeline: timeline,
        fill: 'forwards',
        rangeStart: `exit-crossing ${CSS.percent((i / total) * 100)}`,
        rangeEnd:   `exit-crossing ${CSS.percent((index / total) * 100)}`
      }
    );
  });
});




    