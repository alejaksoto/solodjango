window.fbAsyncInit = function () {
    FB.init({
        appId: '824951679639133', // Reemplaza con tu appId
        autoLogAppEvents: true,
        xfbml: true,
        version: 'v21.0'
    });
    FB.AppEvents.logPageView();
};

(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) { return; }
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

// Verifica el estado de login
window.onload = function () {
    FB.getLoginStatus(function (response) {
        statusChangeCallback(response);
    });
};

function statusChangeCallback(response) {
    console.log('Login status:', response);
    if (response.status === 'connected') {
        const userID = response.authResponse.userID;
        const accessToken = response.authResponse.accessToken;

        console.log('Usuario conectado con ID:', userID);
        console.log('Access Token:', accessToken);
        window.location.href = '/app-logged-in';
    } else if (response.status === 'not_authorized') {
        console.log('Usuario no autorizado en la app.');
        showLoginButton();
    } else {
        console.log('Usuario no conectado.');
        showLoginButton();
    }
}

function showLoginButton() {
    document.getElementById('loginButton').style.display = 'block';
}

// Lógica para lanzar el registro embebido de WhatsApp
window.launchWhatsAppSignup = () => {
    FB.login(fbLoginCallback, {
        config_id: '517700577931165',
        response_type: 'code',
        override_default_response_type: true,
        extras: {
            setup: {},
            featureType: '',
            sessionInfoVersion: '3',
        }
    });
};

const fbLoginCallback = (response) => {
    if (response.authResponse) {
        const code = response.authResponse.code;
        console.log('Respuesta de inicio de sesión: ', code);
    } else {
        console.log('Error en la respuesta: ', response);
    }
};
