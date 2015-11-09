$(document).ready(function(){
    //Remove the active class from the previous option
    $(".active").removeClass();

    $("#tachogramsubmitsettings").click(function(){
        //TODO: AJAX BOLADAO MUDANDO OS PARAMETROS
    });
    //make the filter order inactive in the beginning
    $("#id_filter_order").prop("disabled", true);

    //Make the Filter order able/disabe if user wants to use filter.
    $("#id_filter_method").change(function(){
        var selectedFilter = $(this).val();
        console.log(selectedFilter);
        if (selectedFilter == 0 || selectedFilter == 1){//None or Quotient Filter
            $("#id_filter_order").prop("disabled", true);
        }else{
            $("#id_filter_order").prop("disabled", false);
        }
    });

    //TODO:When comments is clicked load the previuos comments (if any). If more
    //than X comments show Load more comments
    $("#showcomments").click(function(event){
        event.preventDefault();
        showFirstComments();
        //Get the number of comments. Minus 1 becuase of the submit comment form
    });

    function showFirstComments(){
        if ($("#commentsdiv").is(":visible")){
            hideAllComments();
        }
        else{
            var numberOfComments = $(".commentBox").length - 1;
            $("#commentContainer").children().slice(0, 3).show();

            if (numberOfComments > 3){
                $("#divloadmore").show();
            }

        $("#commentsdiv").show();
        }
    }

    function hideAllComments(){
        $("#commentsdiv").hide();
        $("#divloadmore").hide();
        $("#divloadless").hide();
        $("#commentContainer").children().hide();
    }

    //Load more button
    $("#loadmore").click(function(event){
        event.preventDefault();
        showMore();
    })

    function showMore(){
        var numberOfComments = $(".commentBox").length - 1;
        $("#commentContainer").children().slice(3, numberOfComments).show();
        $("#divloadmore").hide();
        $("#divloadless").show();
    }

    $("#loadless").click(function(event){
        var numberOfComments = $(".commentBox").length - 1;
        event.preventDefault();
        $("#commentContainer").children().slice(3, numberOfComments).hide();
        $("#divloadless").hide();
        $("#divloadmore").show();
    })

    //Submit comment button
    $("#commentbutton").click(function(event){
        event.preventDefault();
        var text = $("#comment").val();
        var filename = getFileName();
        commentAjax(filename, text);
    })

    $(".commentedit").click(function(e){
        e.preventDefault();
        //Show the buttons only with the edition is done
        var nButtons = $(".buttonedit").length;
        var id = this.id.split("_")[1];
        var textArea = $("#textarea_" + id);
        var divComment = $("#divcomment_" + id);
        //Get the old text to find the comment on database
        var oldText = textArea.val();

        if (nButtons == 0){
            //Get the element by Id
            var buttonTemplate = "<button style='margin-right:0.1cm;margin-top:0.2cm;' class='btn btn-default btn-sm buttonedit'></button>";
            var buttonCommentCancel = $(buttonTemplate);
            var buttonCommentSave = $(buttonTemplate.replace("default", "primary"));
            buttonCommentCancel.text("Cancel");
            buttonCommentSave.text("Save");
            textArea.removeAttr("readonly");
            divComment.append(buttonCommentCancel);
            divComment.append(buttonCommentSave);
            //Bind function to each button
            buttonCommentCancel.click(function(){
                removeCommentEditionButtons(buttonCommentCancel, buttonCommentSave, textArea)
            })
            buttonCommentSave.click(function(){
                //Ajax saving updating the text
                var newText = textArea.val();
                var filename = getFileName();
                updateCommentAjax(filename, oldText, newText);
                removeCommentEditionButtons(buttonCommentCancel, buttonCommentSave, textArea)
                //Append tag edited to textarea.
                var nP = $("#p_" + id).length
                console.log(nP);
                if (!nP){
                    divComment.append("<p align='right' style=color:'#9197A3'>Edited</p>");
                }
            })
        }else{
            //Show a message that the user must finish the current edition
            //before edit another comment.
        }
    })

    $(".deletecomment").click(function(e){
        e.preventDefault();
        var id = this.id.split("_")[1];
        var commentBox= $("#commentbox_" + id);
        var textArea = $("#textarea_" + id);
        var oldText = textArea.val()
        var filename = getFileName();
        deleteCommentAjax(filename, oldText, commentBox);
    })

    function removeCommentEditionButtons(buttonCommentCancel, buttonCommentSave, textArea){
        textArea.attr("readonly", true);
        buttonCommentCancel.remove();
        buttonCommentSave.remove();
    }

    function getFileName(){
        var url_name = window.location.pathname.split("/");
        rri_name = url_name[url_name.length - 1];
        return rri_name;
    }

    function commentAjax(filename, text){
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: filename + "/comment",
            type:'post',
            headers: {'X-CSRFToken': csrftoken},
            data: {'text': text, 'action_type': 'create'},
            success:function(data){
                //append a new comment box with the new content.
                showMore();
                var commentClone = $("#comment").clone()
                commentClone.attr("id", "commentclone");
                labelContent = "<label for='comment'>Comment from: " + data.user + ":</label>";
                $("#commentContainer").append(labelContent);
                $("#commentContainer").append("<p>Just now</p>");
                commentClone.appendTo("#commentContainer");
                commentClone.attr("readonly", true);
                commentClone.val(text);
                $("#comment").val("");

            }
        });
    }

    function updateCommentAjax(filename, oldText, newText){
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: filename + "/comment",
            type:'post',
            headers: {'X-CSRFToken': csrftoken},
            data: {'old_text': oldText, 'new_text': newText, 'action_type': 'update'},
            success:function(data){
            }
        });
    }

    function deleteCommentAjax(filename, oldText, commentBox){
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: filename + "/comment",
            type:'post',
            headers: {'X-CSRFToken': csrftoken},
            data: {'old_text': oldText, 'action_type': 'delete'},
            success:function(data){
                commentBox.remove();
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
})
