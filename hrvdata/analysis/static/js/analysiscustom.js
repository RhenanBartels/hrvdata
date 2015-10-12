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
})
