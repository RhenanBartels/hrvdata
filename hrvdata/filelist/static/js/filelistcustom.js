$(document).ready(function(){
    //Remove the active class from the previous option
    $(".active").removeClass();
    $("#filelist_li").addClass("active");

    $(".del_btn").hover(function(){
        $(this).css("cursor", "pointer");
    });

    $(".del_btn").click(function(){
        //Check if the user really want to delete the file
        var confirm_delete = confirm("Are you sure you wanna delete this file?");
        if (confirm_delete){
            doAjax(this.id);
        }
    })

    $(".shareimage").hover(function(){
        $(this).css("cursor", "pointer");
    });

    $(".shareimage").click(function(){
        var formId = "#div_"  + this.id;
        $(formId).toggle();
    });

    function doAjax(filename){
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: "delete/",
            type: "post",
            data: {'filename': filename},
            headers: {'X-CSRFToken': csrftoken},
            beforeSend: function(){
                console.log("ta indo");

            },
            success: function(){
                $("#" + filename).hide();
                isEmpty();
            }

        });
    }

   function isEmpty(){
       console.log($(".inline").length);
       if($(".inline").length == 0) {
       }
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

})
