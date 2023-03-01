import Cookies from './js.cookie.min.mjs'

$(document).ready(function(){
    $("#wrongLogin").hide();
    $("#disclaimer").modal('show');
    $("#loginForm").submit(function(e){
        e.preventDefault();
        var inputs = {};
            $.each(($('#loginForm').serializeArray()), function(k, v){
                inputs[v.name]= v.value;
            });
        let r = $.ajax({
            type: "POST",
            url: 'http://127.0.0.1:8000/token',
            data: {
                username: inputs.username,
                password: inputs.password
            },
            success: function(data, status, xhr){
                Cookies.set("access_token", data.access_token);
                Cookies.set("token_type", data.token_type);
                Cookies.set('username', inputs.username);
                window.location.replace("main.html");
            },
            error: function(data, status, xhr){
                $("#wrongLogin").show(500);
                console.log("wrong user or pass");
            }
        });
    })
});