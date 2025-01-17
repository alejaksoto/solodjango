document.getElementById('cliente-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const telefono = document.getElementById('telefono').value;
    const direccion = document.getElementById('direccion').value;

    const response = await fetch('/guardar-datos-adicionales/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ telefono, direccion }),
    });

    const data = await response.json();
    if (data.success) {
        alert('Datos guardados con éxito');
    } else {
        alert('Error al guardar los datos');
    }
});