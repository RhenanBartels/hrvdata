$(document).ready(function (){
//TODO: populate the settings popup dialog with database information
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

//Change the Time Varying Settings
$("#timevaryingsubmitsettings").click(function(){
    var filename = getFileName();
    var settings = getTimeVaryingSettings();
    settingsAjax(filename, settings, 'timevarying');
});

function getTimeVaryingSettings(){
    var segmentSize = $("#id_segment_size").val();
    var overlapSize = $("#id_overlap_size").val();
    var timeVaryingSettings = [segmentSize, overlapSize];
    return timeVaryingSettings;
}

function settingsAjax(filename, settings, method){
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: filename + "/settings",
        type: "post",
        data: {'segmentsize': settings[0], 'overlapsize': settings[1],
            'method': method},
        headers: {'X-CSRFToken': csrftoken},
        beforeSend: function(){

        },
        success: function(results){
            $("#settingstv").modal('hide');
            plot(results);
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
            grid: {
              hoverable: true,
              clickable: true
                  }
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

    $(function() {
		$("<div id='tooltip'></div>").css({
			position: "absolute",
			display: "none",
			border: "1px solid #fdd",
			padding: "2px",
			"background-color": "#fee",
			opacity: 0.80
		}).appendTo("body");
    });
		$("#time-varying").bind("plothover", function (event, pos, item) {

                        if (item) {
                                var x = item.datapoint[0].toFixed(2),
                                        y = item.datapoint[1].toFixed(2);

                                $("#tooltip").html("Value" + " of " + x + " = " + y)
                                        .css({top: item.pageY+5, left: item.pageX+5})
                                        .fadeIn(200);
                        } else {
                                $("#tooltip").hide();
                        }
		});

		$("#time-varying").bind("plotclick", function (event, pos, item) {
			if (item) {
				$("#clickdata").text(" - click point " + item.dataIndex + " in " + item.series.label);
                                console.log(item.dataIndex);
			}
		});

})
