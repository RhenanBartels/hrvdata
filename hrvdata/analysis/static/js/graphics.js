$(document).ready(function() {

    var rri_name = getFileName();
    doAjax(rri_name);

    function getFileName(){
        var url_name = window.location.pathname.split("/");
        rri_name = url_name[url_name.length - 1];
        return rri_name;
    }

    function doAjax(rri_code){
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: rri_code,
            type:'post',
            headers: {'X-CSRFToken': csrftoken},
            success:function(data){
                plot(data);
//                changeIndexDropDownMenu(data);
            }
        });
    }

    function plot(data){
        var optionspsd = {
            colors:["#0097ff","#81d8d0", "#b0e0e6"],
            lines:{
                show:true,
                fill:true,
            },
            xaxis: {
                       min:0,
                       max:0.4,
            },
        };
        var optionstv = {
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
        $.plot(("#rri"), [data.rri]);
        $.plot(("#time-varying"), [data.rmssdi], optionstv);
        $.plot(("#psd"), [data.vlfpsd, data.lfpsd, data.hfpsd], optionspsd);

        //TODO: Create a function to make this plot and avoid repetion (DRY)
        window.onresize = function(event) {
            $.plot(("#rri"), [data.rri]);
            $.plot(("#time-varying"), [data.rmssdi], optionstv);
            $.plot(("#psd"), [data.vlfpsd, data.lfpsd, data.hfpsd], optionspsd);
            var xaxisLabel = $("<div class='axisLabel xaxisLabel'></div>").text("Time (s)").appendTo($('#rri'));

            var yaxisLabel = $("<div class='axisLabel yaxisLabel'></div>").text("RRi (ms)").appendTo($('#rri'));
            yaxisLabel.css("margin-top", yaxisLabel.width() / 2 - 20);
            var xaxisLabel = $("<div class='axisLabel xaxisLabel'></div>").text("Frequency (Hz)").appendTo($('#psd'));

            var yaxisLabel = $("<div class='axisLabel yaxisLabel'></div>").text("PSD (ms/Hz)").appendTo($('#psd'));
            yaxisLabel.css("margin-top", yaxisLabel.width() / 2 - 20);
            var xaxisLabel = $("<div class='axisLabel xaxisLabel'></div>").text("Time (s)").appendTo($('#time-varying'));

            var yaxisLabel = $("<div class='axisLabel yaxisLabel'></div>").text("RMSSD (ms)").appendTo($('#time-varying'));
            yaxisLabel.css("margin-top", yaxisLabel.width() / 2 - 20);
        }
     //   $.plot(("#psd"), [data.psd.slice(0, 11), data.psd.slice(10, 20), data.psd.slice(19)], optionspsd);
    var xaxisLabel = $("<div class='axisLabel xaxisLabel'></div>").text("Time (s)").appendTo($('#rri'));

    var yaxisLabel = $("<div class='axisLabel yaxisLabel'></div>").text("RRi (ms)").appendTo($('#rri'));
    yaxisLabel.css("margin-top", yaxisLabel.width() / 2 - 20);
    var xaxisLabel = $("<div class='axisLabel xaxisLabel'></div>").text("Frequency (Hz)").appendTo($('#psd'));

    var yaxisLabel = $("<div class='axisLabel yaxisLabel'></div>").text("PSD (ms/Hz)").appendTo($('#psd'));
    yaxisLabel.css("margin-top", yaxisLabel.width() / 2 - 20);
    var xaxisLabel = $("<div class='axisLabel xaxisLabel'></div>").text("Time (s)").appendTo($('#time-varying'));

    var yaxisLabel = $("<div class='axisLabel yaxisLabel'></div>").text("RMSSD (ms)").appendTo($('#time-varying'));
    yaxisLabel.css("margin-top", yaxisLabel.width() / 2 - 20);
        }

    function changeIndexDropDownMenu(data){
        if (data.time_varying_index == "rmssd"){
            $("#mainindexdropdown").text("RMSSDi");
            //Replace the little arrow on the dropdown menu
            $("#mainindexdropdown").append("<b class='caret'></b>");
            $("#rmssdi_li").hide();
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
});
