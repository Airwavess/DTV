window.onload = function() {
  window.fbAsyncInit = function() {
    FB.init({
      appId: '184948092027840',
      xfbml: true,
      version: 'v2.9'
    });
    FB.AppEvents.logPageView();
    getLogin()
  };

  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {
      return;
    }
    js = d.createElement(s);
    js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));

  function getLogin() {
    FB.getLoginStatus(function(response) {
      if (response.status === 'connected') {
        console.log(response.authResponse.accessToken);
        var accessToken = response.authResponse.accessToken
        FB.api(
          '/me',
          'GET', {
            "access_token": accessToken,
            "fields": "name,picture",
          },
          function(response) {
            document.getElementsByClassName('user-login')[0] = "<p>"+ response.name +"</p>"
          }
        );
      }
    });
  }
}

function fb_login() {
  FB.login(function(response) {
    if (response.authResponse) {
      var accessToken = response.authResponse.accessToken
      FB.api(
        '/me',
        'GET', {
          "access_token": accessToken,
          "fields": "name,picture",
        },
        function(response) {
          console.log(JSON.stringify(response));
        }
      );
    } else {
      console.log('User cancelled login or did not fully authorize.');
    }
  });
}
