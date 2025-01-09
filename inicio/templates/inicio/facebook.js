document.addEventListener("DOMContentLoaded", () => {
    FB.getLoginStatus(function (response) {
        statusChangeCallback(response);
    });
});

function statusChangeCallback(response) {
    console.log('Login status:', response);
    if (response.status === 'connected') {
        const userID = response.authResponse.userID;
        const accessToken = response.authResponse.accessToken;
        console.log('Usuario conectado con ID:', userID);
        console.log('Access Token:', accessToken);
        window.location.href = '/app-logged-in';
    } else {
        showLoginButton();
    }
}

function showLoginButton() {
    document.getElementById('loginButton').style.display = 'block';
}
