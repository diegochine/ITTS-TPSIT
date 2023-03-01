import Cookies from './js.cookie.min.mjs'


$(document).ready(function(){
  if (!Cookies.get("access_token")) window.location.replace("index.html");
  $("#welcome").text('Welcome back, ' + Cookies.get('username'))
});