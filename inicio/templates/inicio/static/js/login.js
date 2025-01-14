/**
 * Inicialización del SDK de Facebook para su uso en autenticación y eventos de la aplicación.
 */
window.fbAsyncInit = function () {
    FB.init({
        appId: '824951679639133', // ID de la aplicación configurada en Facebook Developer
        autoLogAppEvents: true, // Habilita el registro automático de eventos
        xfbml: true, // Procesa los plugins de Facebook declarados en la página
        version: 'v21.0' // Versión del SDK de Facebook
    });
    FB.AppEvents.logPageView(); // Registra la visualización de la página
};

/**
 * Carga asíncrona del SDK de Facebook mediante la creación de un script dinámico.
 * @param {Document} d - Referencia al documento HTML
 * @param {string} s - Tipo de elemento a crear ('script')
 * @param {string} id - ID único para el script cargado
 */
(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) { return; } // Verifica si el script ya está cargado
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js"; // URL del SDK de Facebook
    fjs.parentNode.insertBefore(js, fjs); // Inserta el script antes del primer script existente
}(document, 'script', 'facebook-jssdk'));

/**
 * Verifica el estado de inicio de sesión de Facebook al cargar la página.
 */
window.onload = function () {
    FB.getLoginStatus(function (response) {
        statusChangeCallback(response); // Maneja la respuesta del estado de inicio de sesión
    });
};

/**
 * Maneja los cambios en el estado de autenticación del usuario.
 * @param {Object} response - Objeto de respuesta del estado de inicio de sesión
 */
function statusChangeCallback(response) {
    console.log('Login status:', response);
    if (response.status === 'connected') {
        const userID = response.authResponse.userID;
        const accessToken = response.authResponse.accessToken;

        console.log('Usuario conectado con ID:', userID);
        console.log('Access Token:', accessToken);
        window.location.href = '/app-logged-in'; // Redirige al usuario a la aplicación autenticada
    } else if (response.status === 'not_authorized') {
        console.log('Usuario no autorizado en la app.');
        showLoginButton(); // Muestra el botón de inicio de sesión
    } else {
        console.log('Usuario no conectado.');
        showLoginButton(); // Muestra el botón de inicio de sesión
    }
}

/**
 * Muestra el botón de inicio de sesión en la interfaz de usuario.
 */
function showLoginButton() {
    document.getElementById('loginButton').style.display = 'block'; // Despliega el botón de inicio de sesión
}

/**
 * Lanza el registro embebido para WhatsApp Business mediante el SDK de Facebook.
 */
window.launchWhatsAppSignup = () => {
    FB.login(fbLoginCallback, {
        config_id: '517700577931165', // Configuración de la app de WhatsApp Business
        response_type: 'code', // Tipo de respuesta esperado
        override_default_response_type: true, // Fuerza el tipo de respuesta definido
        extras: {
            setup: {},
            featureType: '',
            sessionInfoVersion: '3', // Versión de información de sesión
        }
    });
};

/**
 * Callback para manejar la respuesta del inicio de sesión en Facebook.
 * @param {Object} response - Objeto de respuesta de autenticación
 */
const fbLoginCallback = (response) => {
    if (response.authResponse) {
        const code = response.authResponse.code;
        console.log('Respuesta de inicio de sesión: ', code); // Log de código de respuesta
    } else {
        console.log('Error en la respuesta: ', response); // Log de error en la autenticación
    }
};
