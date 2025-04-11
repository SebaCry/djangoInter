/**
 * Cambia la cantidad de un producto en el carrito
 * @param {int} id: PK del registro del producto en el carrito
 */

// function cambiarCantidad(id) {
//     let cantidad = document.getElementById('cantidad_'+id).value;
//     let valorUnit = document.getElementById('cantidad_'+id).dataset.preciou;

//     let url = "http://localhost:8000/productos/cambiarCantidad/";
//     let datos = {
//         'id' : id,
//         'cantidad' : cantidad
//     };

//     let total = parseFloat(cantidad) * parseFloat(valorUnit)
//     document.getElementById('total_'+id).innerText = '$' + total;
//     mensajeAjax(url, datos, cambiarCantidadResp)
// }

// function cambiarCantidadResp(data) {
//     document.getElementById('subtotal').innerText = '$' + data['subtotal'];
//     document.getElementById('iva').innerText = '$' + data['iva'];
//     document.getElementById('envio').innerText = '$' + data['envio'];
//     document.getElementById('total').innerText = '$' + data['total'];
// }

// /**
//  * Consulta AJAX al servidor por metodo POST
//  * @param {*} urlserver :Direccion de envio
//  * @param {*} datos :Datos en formato JavaScript object
//  * @param {*} callBackFunction :Funcion de retorno
//  */

// function mensajeAjax(urlserver, datos, callBackFunction){
//     const csrftoken = getCookie('csrftoken')
//     fetch(urlserver, {
//         method: 'POST',
//         credentials: 'same-origin',
//         headers: {
//             'Accept' : 'application/json',
//             'X-Requested-With' : 'XMLHttpRequest',
//             'X-CSRFToken' : csrftoken
//         },
//         body : JSON.stringify(datos)
//     })
//         .then(response => response.json())
//         .then(data => {
//             callBackFunction(data)
//         })

//         .catch((err) => {
//             console.log('Error', JSON.stringify(err))
//         })
// }

// /**
// * @param {*} name Nombre de la cookie
// * @returns el cvontenido de la cookie
// */

// function getCookie(name) {
//     let cookieValue = null
//     if (document.cookie && document.cookie !== ""){
//         const cookies = document.cookie.split(';')
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim()
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

function cambiarCantidad(id) {
    const cantidadInput = document.getElementById(`cantidad_${id}`)
    const cantidad = parseInt(cantidadInput.value, 10)

    if (cantidad < 1){
        alert('La cantidad no puede ser menor que 1')
        cantidadInput.value = 1
        return
    }

    const url = "http://127.0.0.1:8000/productos/cambiarCantidad/"
    const datos = {
        id : id,
        cantidad : cantidad
    }

    mensajeAjax(url, datos, (data) => {
        if (data && data.carrito) {
            document.getElementById("subtotal").innerText = `$${data.subtotal}`;
            document.getElementById("iva").innerText = `$${data.iva}`;
            document.getElementById("envio").innerText = `$${data.envio}`;
            document.getElementById("total").innerText = `$${data.total}`;

            const totalElement = document.getElementById(`total_${id}`);
            totalElement.innerText = `$${data.carrito.find(p => p.id === id).total}`;
        } else {
            console.error("Respuesta inválida del servidor:", data);
        }
    })
}