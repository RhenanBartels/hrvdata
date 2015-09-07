$(document).ready(function (){

    $(".chooseindex").click(function(event) {
        var rriName = getFileName();
        var elementId = $(this).attr("id");
        doAjax(rriName, elementId);
    });

    function getFileName(){
        var url_name = window.location.pathname.split("/");
        rri_name = url_name[url_name.length - 1];
        return rri_name;
    }

    function doAjax(filename, index_name){
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: filename + "/" + index_name + "/",
            type:'post',
            headers: {'X-CSRFToken': csrftoken},
            success:function(data){
                plot(data);
            }
        });
    }

    function plot(data){
        var options = {
            colors:["#0022FF"],
            lines:{
                show:true,
            },
            points:{
                show:true,
                fill:true,
                fillColor:false,
            },
        };
        $.plot(("#time-varying"), [data.time_varying_index], options);

        var index_name = "RMSSD (ms)";
        if (data.time_varying_name == "sdnn"){
            index_name = "SDNN (ms)";
        }
        else if (data.time_varying_name == "pnn50"){
            index_name = "pNN50 (%)";
        }
        else if (data.time_varying_name == "mrrii"){
            index_name = "Mean RRi (ms)";
        }
        else if (data.time_varying_name == "mhri"){
            index_name = "Mean HR (bpm)";
        }
    var xaxisLabel = $("<div class='axisLabel xaxisLabel'></div>").text("Time (s)").appendTo($('#time-varying'));

    var yaxisLabel = $("<div class='axisLabel yaxisLabel'></div>").text(index_name).appendTo($('#time-varying'));
    yaxisLabel.css("margin-top", yaxisLabel.width() / 2 - 20);
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
