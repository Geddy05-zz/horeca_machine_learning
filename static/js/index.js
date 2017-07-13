/**
 * Created by Geddy on 13-7-2017.
 */

function holtWinters(){
    $.ajax({
        url: "/holt-winters",
        cache: false,
        success: function(html){
            console.log(html.error);
            $("#SSE").html(html.error);
        }
    });
}


function ARIMA(){
    $("#SSE").html("");
}

function mlr(){
    $("#SSE").html("");
}

function nn(){
    $("#SSE").html("");
}