$(document).ready(function(){
    var user = $('#user').val();
    var pass = $('#pass').val();
    $.ajax({
        url: 'http://10.42.0.61:5000/student/auth',
        type: 'GET',
        data: {'user': user, 'pass': pass},
        success: function(data) {
            var result = JSON.stringify(data);
            if (result == "\'Access Denied. Cause: Wrong Password\'") {
                alert("Invalid login details");
            }
            else {
                $(document).load("http://localhost:9000/home", result);
            }
        }
    });
});