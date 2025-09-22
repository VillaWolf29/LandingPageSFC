
document.addEventListener('DOMContentLoaded', function () {
    var el = document.getElementById('carrusel-servicios');
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
    

// Asegura que las flechas del teclado muevan el carrusel cuando esté enfocado o haga click en él
    document.addEventListener('DOMContentLoaded', function () {
    var el = document.getElementById('carrusel-servicios');
        if (!el) return;

        // Inicializa el carousel de Bootstrap (defensivo)
        if (typeof bootstrap !== 'undefined' && !el._bsCarousel) {
            el._bsCarousel = new bootstrap.Carousel(el, { wrap: false, keyboard: false, ride: false });
        }

        // Permitir foco y que al hacer click tome foco
        el.setAttribute('tabindex', '0');
        el.addEventListener('click', function () { el.focus(); });

        el.addEventListener('keydown', function (e) {
            if (!el._bsCarousel) return;
            if (e.key === 'ArrowLeft') {
                e.preventDefault();
                el._bsCarousel.prev();
            } else if (e.key === 'ArrowRight') {
                e.preventDefault();
                el._bsCarousel.next();
            }
    });
    });
    
    