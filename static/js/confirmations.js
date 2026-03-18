/**
 * Sistema de confirmaciones para acciones destructivas.
 */
document.addEventListener('DOMContentLoaded', function() {
    // Confirmar antes de eliminar usando SweetAlert2
    const deleteLinks = document.querySelectorAll('a[href*="delete"], button[type="submit"][class*="delete"], form[action*="delete"]');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const element = this;
            
            Swal.fire({
                title: '¿Estás seguro?',
                text: "Esta acción no se puede deshacer.",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#EF4444',
                cancelButtonColor: '#6B7280',
                confirmButtonText: 'Sí, eliminar',
                cancelButtonText: 'Cancelar',
                customClass: {
                    popup: 'rounded-xl',
                    confirmButton: 'rounded-lg font-semibold',
                    cancelButton: 'rounded-lg font-semibold'
                }
            }).then((result) => {
                if (result.isConfirmed) {
                    if (element.tagName === 'FORM') {
                        element.submit();
                    } else if (element.tagName === 'A') {
                        window.location.href = element.href;
                    }
                }
            });
        });
    });
    
    // Confirmar antes de procesar pagos usando SweetAlert2
    const processPaymentForms = document.querySelectorAll('form[action*="create"], form[action*="process"]');
    processPaymentForms.forEach(form => {
        // Remover el atributo onsubmit original del HTML si existe
        if (form.hasAttribute('onsubmit')) {
            form.removeAttribute('onsubmit');
        }
        
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            Swal.fire({
                title: 'Confirmar Pago',
                text: '¿Deseas registrar este pago como completado con la fecha de hoy?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#10B981',
                cancelButtonColor: '#6B7280',
                confirmButtonText: 'Sí, registrar pago',
                cancelButtonText: 'Cancelar',
                customClass: {
                    popup: 'rounded-xl',
                    confirmButton: 'rounded-lg font-semibold px-4 py-2',
                    cancelButton: 'rounded-lg font-semibold px-4 py-2'
                }
            }).then((result) => {
                if (result.isConfirmed) {
                    form.submit();
                }
            });
        });
    });
});

/**
 * Muestra un loading spinner en botones al hacer submit.
 */
function showLoading(button) {
    if (!button) return;
    
    button.disabled = true;
    const originalText = button.innerHTML;
    button.dataset.originalText = originalText;
    button.innerHTML = `
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Procesando...
    `;
}

/**
 * Restaura el texto original del botón.
 */
function hideLoading(button) {
    if (!button || !button.dataset.originalText) return;
    
    button.disabled = false;
    button.innerHTML = button.dataset.originalText;
}

/**
 * Agrega loading states a todos los formularios.
 */
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitButton && !submitButton.disabled) {
                const submitText = submitButton.querySelector('.submit-text');
                const submitSpinner = submitButton.querySelector('.submit-spinner');
                
                if (submitText && submitSpinner) {
                    submitText.classList.add('hidden');
                    submitSpinner.classList.remove('hidden');
                    submitButton.disabled = true;
                } else {
                    showLoading(submitButton);
                }
            }
        });
    });
    
    // Restaurar botones si hay error de validación
    window.addEventListener('pageshow', function(event) {
        if (event.persisted) {
            const submitButtons = document.querySelectorAll('button[type="submit"]:disabled');
            submitButtons.forEach(button => {
                const submitText = button.querySelector('.submit-text');
                const submitSpinner = button.querySelector('.submit-spinner');
                if (submitText && submitSpinner) {
                    submitText.classList.remove('hidden');
                    submitSpinner.classList.add('hidden');
                    button.disabled = false;
                }
            });
        }
    });
});
