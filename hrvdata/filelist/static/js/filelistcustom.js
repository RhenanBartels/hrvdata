$(document).ready(function(){
    //Remove the active class from the previous option
    $(".active").removeClass();
    $("#filelist_li").addClass("active");

    $(".del_btn").hover(function(){
        $(this).css("cursor", "pointer");
    });

    $(".del_btn_share").hover(function(){
        $(this).css("cursor", "pointer");
    });

    $(".del_btn").click(function(){
        //Check if the user really want to delete the file
        var confirm_delete = confirm("Are you sure you wanna delete this file?");
        if (confirm_delete){
            doAjax(this.id);
        }
    })

    $(".del_btn_share").click(function(){
        //Check if the user really want to delete the file
        var confirm_delete = confirm("Are you sure you wanna remove this file from you file list?");
        if (confirm_delete){
            deleteShareAjax(this.id);
        }
    })

    $(".shareimage").hover(function(){
        $(this).css("cursor", "pointer");
    });

    $(".shareimage").click(function(){
        var formId = "#div_"  + this.id;
        $(formId).toggle();
    });

    $(".emailform").submit(function(event) {
        event.preventDefault();
        var email = $(this).serialize();
        email = decodeURIComponent(email).split("=")[1];
        var id = this.id.split("_")[1];
        shareAjax(email, id);
    });

    function doAjax(filename){
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: "delete/",
            type: "post",
            data: {'filename': filename},
            headers: {'X-CSRFToken': csrftoken},
            beforeSend: function(){

            },
            success: function(){
                $("#" + filename).hide();
                isEmpty();
            }

        });
    }

    function deleteShareAjax(filename){
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: "/share/delete/",
            type: "post",
            data: {'filename': filename},
            headers: {'X-CSRFToken': csrftoken},
            beforeSend: function(){

            },
            success: function(){
                 $("#" + filename).hide();
            }

        });
    }

    function shareAjax(email, filename){
        var csrftoken = getCookie('csrftoken');
        var button = $("#btn_" + filename);
        $.ajax({
            url: "/share/",
            type: "post",
            data: {'receiver_email': email, 'filename': filename},
            headers: {'X-CSRFToken': csrftoken},
            beforeSend: function(){
                button.val("Sharing...");
            },
            success: function(response){
            var error_log = $("#error_" + filename);
            if (response.log == "Success"){
                $("#success_" + filename).show();
                $("#div_" + filename).delay(2000).fadeToggle();
                error_log.text("");
            }
            else if (response.log == "notvalid"){
                error_log.text("Email not valid!");
                error_log.show();
            }
            else if (response.log == "sameuser"){
                error_log.text("You need to inform a different email!");
                error_log.show();
            }
            else if (response.log == "notuser"){
                   // questionDialog();
                    var hasConfirmed = confirm("There is no User with this" +
                            " email.\nDo you want to send by email?");

                    if (hasConfirmed){
                        $.ajax({url: 'share/email/',
                                headers: {'X-CSRFToken': csrftoken},
                                type: 'post',
                                data: {"usermail": email},
                                success: function() {
                                    alert('Dicom shared successfully');
                                    var btnId = "#btn_" + dicomId;
                                    $(btnId).val("Share");
                                },


                        });
                    }
                }
            error_log.delay(2000).fadeOut();
            button.val("Share");
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
