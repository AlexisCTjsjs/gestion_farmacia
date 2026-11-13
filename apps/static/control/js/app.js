/* FarmaSalud — JavaScript Interactivo */
document.addEventListener('DOMContentLoaded', function () {
  // Confirmación elegante antes de borrar registros
  document.querySelectorAll('.formulario-eliminar').forEach(function (formulario) {
    formulario.addEventListener('submit', function (evento) {
      var confirmacion = window.confirm('⚠️ ¿Estás seguro de que deseas eliminar este registro?\n\nEsta operación no se puede deshacer y podría afectar recetas o citas asociadas.');
      if (!confirmacion) {
        evento.preventDefault();
      }
    });
  });

  // Ocultar mensajes de éxito automáticamente después de 5 segundos
  var alertas = document.querySelectorAll('.aviso.success');
  alertas.forEach(function (alerta) {
    setTimeout(function () {
      alerta.style.transition = 'opacity 0.5s ease';
      alerta.style.opacity = '0';
      setTimeout(function () {
        alerta.remove();
      }, 500);
    }, 5000);
  });
});
