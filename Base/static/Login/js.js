// Validación Bootstrap
    (() => {
      const forms = document.querySelectorAll('.needs-validation');
      Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
          if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
          }
          form.classList.add('was-validated');
        }, false);
      });
    })();

    // Mostrar/ocultar contraseña
    const toggle = document.getElementById('togglePwd');
    const pwd = document.getElementById('password');
    toggle.addEventListener('click', () => {
      const isText = pwd.type === 'text';
      pwd.type = isText ? 'password' : 'text';
      toggle.innerHTML = isText ? '<i class="bi bi-eye"></i>' : '<i class="bi bi-eye-slash"></i>';
    });