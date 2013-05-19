window.fbAsyncInit = function() {
    FB.init({
            appId      : '284783798323209', // App ID
            channelUrl : 'https://apps.facebook.com/284783798323209/?fb_source=appcenter&fb_appcenter=1#_=_', // Channel File
            status     : true, // check login status
            cookie     : true, // enable cookies to allow the server to access the session
            xfbml      : true  // parse XFBML
            });
};
// Load the SDK Asynchronously
(function(d, s, id){
 var js, fjs = d.getElementsByTagName(s)[0];
 if (d.getElementById(id)) {return;}
 js = d.createElement(s); js.id = id;
 js.src = "//connect.facebook.net/en_US/all.js";
 fjs.parentNode.insertBefore(js, fjs);
 }(document, 'script', 'facebook-jssdk'));

console.log('Facebook done')