
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
    