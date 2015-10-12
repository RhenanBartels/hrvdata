$(document).ready(function(){
    //Remove the active class from the previous option
    console.log("ass");
    $(".active").removeClass();
    $("#share_li").addClass("active");

    $(".shareform").submit(function(event){
        event.preventDefault()
        var email = $(this).serialize();
        email = decodeURIComponent(email).split("=")[1];
        var filename = this.id.split("_")[1];
        doAjax(email, filename);
    })
    //TODO: Remove the email from the dropdown menu after deletion.
    //TODO: Remove the filename if it no longer shared with no user
    //TODO: flot start small plot all selected.
    //TODO: make small plot select all when user give single click.
    function doAjax(email, filename){
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: "delete/",
            type: "post",
            data: {'email': email,
                   'filename': filename
            },
            headers: {'X-CSRFToken': csrftoken},
            beforeSend: function(){

            },
            success: function(){
                 $("#option_" + filename).remove();
                 isDropDownEmpty(filename);
             }
        });
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function isDropDownEmpty(filename){
       var numberOfOptions = $("#select_" + filename).size();
       if (numberOfOptions == 0){
           $("#li_" + filename).remove();
           $("#select_" + filename).remove();
           $("#form_" + filename).remove();
       }
    }

})
