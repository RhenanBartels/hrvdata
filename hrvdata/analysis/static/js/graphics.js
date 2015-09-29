$(document).ready(function() {
    var rri_name = getFileName();
    //Check if the analysis is of shared file
    if (rri_name.search("shared")){
        sharedAjax(rri_name);
    }
    else{
        doAjax(rri_name);
    }

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

    function sharedAjax(rri_code){
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
        var optionsrri = {
            xaxis: {
                   zoomRange: [-100000, 100000],
                   panRange: [-100000, 100000]
            },
            yaxis: {
                    zoomRange: [-100000, 100000],
                    panRange: [-100000, 100000]
            },
            zoom: {
                      interactive: true
            },
            pan: {
                     interactive: true
            },
        };
        var optionsnavigation = {
            xaxis: {
               ticks: []
            },
            yaxis: {
               ticks: []
            },
            selection: {
               mode: "x"
           },
        };
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
            grid: {
                      hoverable: true,
                      clickable: true
            },
        };
        $.plot(("#rri"), [data.rri], optionsrri);
        $.plot(("#navigation"), [data.rri], optionsnavigation);
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

    $("#navigation").bind("plotselected", function (event, ranges) {
        //TODO: Every time that the user select a range go to the server
        //access the settings model, change the start and end signal
        //analyse the signal again, test if there is enough signal to
        //analyze frequency domain e time varying and finally refresh the
        //indices
        console.log("From: " + ranges.xaxis.from + " To: " + ranges.xaxis.to);
    });
});
