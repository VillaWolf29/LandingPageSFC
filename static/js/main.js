// Inicializar EmailJS
(function() {
    // Inicializar con tu Public Key
    emailjs.init("Hhct1Okd4T7Ji_81I");
})();

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form');
    const successMessage = document.getElementById('success-message');
    const errorMessage = document.getElementById('error-message');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Obtener los datos del formulario
        const formData = {
            empresa: document.getElementById('empresa').value,
            email: document.getElementById('email').value,
            telefono: document.getElementById('telefono').value,
            servicio: document.getElementById('servicio').value,
            empleados: document.getElementById('empleados').value,
            mensaje: document.getElementById('mensaje').value
        };

        // Añadir fecha actual para el correo
        const fechaActual = new Date().toLocaleString('es-ES');
        
        // Enviar el formulario usando EmailJS
        emailjs.send(
            'service_oda6i2e', // Tu Service ID de EmailJS
            'template_ypg4sw3', // Tu Template ID de EmailJS
            {
                empresa: formData.empresa,
                email: formData.email,
                telefono: formData.telefono,
                servicio: formData.servicio,
                empleados: formData.empleados,
                mensaje: formData.mensaje,
                fecha: fechaActual
            }
        )
        .then(function() {
            // Guardar los datos en el backend
            fetch('/api/guardar-mensaje', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (response.ok) {
                    // Mostrar mensaje de éxito
                    form.reset();
                    successMessage.style.display = 'block';
                    errorMessage.style.display = 'none';
                    
                    // Ocultar el mensaje de éxito después de 5 segundos
                    setTimeout(() => {
                        successMessage.style.display = 'none';
                    }, 5000);
                } else {
                    throw new Error('Error en el backend');
                }
            })
            .catch(err => {
                console.error('Error al guardar los datos:', err);
                errorMessage.style.display = 'block';
                successMessage.style.display = 'none';
            });
        })
        .catch(function(error) {
            console.error('Error de EmailJS:', error);
            errorMessage.style.display = 'block';
            successMessage.style.display = 'none';
        });
    });
});