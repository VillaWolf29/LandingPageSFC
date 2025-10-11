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

// Animación de scroll para la sección de servicios
document.addEventListener('DOMContentLoaded', () => {
  const wrapper = document.querySelector('#seccion-servicios');
  const servicios = Array.from(document.querySelectorAll('.fila-servicio'));

  if (!wrapper || servicios.length === 0) return;

  const options = { root: null, threshold: 0.25 };
  let observer = null;

  const isDesktop = () => window.innerWidth >= 768;

  const handleEntries = (entries) => {
    entries.forEach(entry => {
      const el = entry.target;
      if (entry.isIntersecting) {
        // efecto con stagger basado en el índice (solo desktop)
        const idx = servicios.indexOf(el);
        const delay = Math.min(600, idx * 120); // cap en 600ms
        el.style.transitionDelay = `${delay}ms`;
        el.classList.add('in-view');
      } else {
        // quitar estado cuando sale del viewport
        el.style.transitionDelay = '';
        el.classList.remove('in-view');
      }
    });
  };

  const createObserver = () => {
    if (observer) observer.disconnect();
    if (!isDesktop()) return;
    observer = new IntersectionObserver(handleEntries, options);
    servicios.forEach(s => observer.observe(s));
  };

  // init y reconstruir al redimensionar (debounced)
  createObserver();
  let rTimer = null;
  window.addEventListener('resize', () => {
    clearTimeout(rTimer);
    rTimer = setTimeout(createObserver, 120);
  });
});

// Respuestas predefinidas del bot
const respuestas = {
  "hola": "¡Hola! 👋 Soy SmartBot, ¿en qué puedo ayudarte?",
  "servicios": "Ofrecemos Soluciones 4.0, Desarrollo de Apps y Videojuegos 🎮",
  "contacto": "Puedes contactarnos al 📞 +51 942 149 115 o en ✉️ contacto@smartfactorychain.com",
  "tecnologias": "Dominamos IoT, Big Data, Inteligencia Artificial, Blockchain y más 🚀",
  "default": "No entendí tu mensaje 🤔. Escribe 'servicios', 'tecnologias' o 'contacto'."
};

const toggleBtn = document.getElementById("chatbot-toggle");
const chatContainer = document.getElementById("chatbot-container");
const closeBtn = document.getElementById("close-chat");
const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const messages = document.getElementById("chatbot-messages");

// Abrir y cerrar chatbot
toggleBtn.onclick = () => chatContainer.style.display = "flex";
closeBtn.onclick = () => chatContainer.style.display = "none";

// Enviar mensaje
function enviarMensaje() {
  const msg = userInput.value.trim().toLowerCase();
  if(msg === "") return;

  // Mostrar mensaje del usuario
  messages.innerHTML += `<div class="user-msg">${msg}</div>`;

  // Buscar respuesta
  const respuesta = respuestas[msg] || respuestas["default"];
  setTimeout(() => {
    messages.innerHTML += `<div class="bot-msg">${respuesta}</div>`;
    messages.scrollTop = messages.scrollHeight;
  }, 500);

  userInput.value = "";
}

sendBtn.onclick = enviarMensaje;
userInput.addEventListener("keypress", e => {
  if(e.key === "Enter") enviarMensaje();
});
