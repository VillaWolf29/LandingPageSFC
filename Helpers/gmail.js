const btn = document.getElementById('button');

document.getElementById('form')
 .addEventListener('submit', function(event) {
   event.preventDefault();

   btn.value = 'Enviar Consulta';

   const serviceID = 'default_service';
   const templateID = 'template_ypg4sw3';

   emailjs.sendForm(serviceID, templateID, this)
    .then(() => {
      btn.value = 'Consulta Enviada';
      alert('Enviando!');
      form.reset();
    }, (err) => {
      btn.value = 'Consulta Enviada';
      alert(JSON.stringify(err));
    });
});