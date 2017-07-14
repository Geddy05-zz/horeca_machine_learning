/**
 * Created by Geddy on 13-7-2017.
 */

function calculat_average(){

}

function holtWinters(){
    $("#TableResults").html("");
    var mse = 0;
    var mape = 0;
    var mae = 0;
    var average = 0;
    for(var i = 1; i < 11; i++) {
        $.ajax({
            url: "/holt-winters",
            cache: false,
            async: false,
            success: function (html) {
                $("#TableResults").append(
                    "<tr>" +
                        "<td>" + i + "</td>" +
                        "<td>" + html.average + "</td>" +
                        "<td>" + html.mae + "</td>" +
                        "<td>" + html.mape + "</td>" +
                        "<td>" + html.mse + "</td>" +
                    "</tr>"
                )
                mse += html.mse;
                mape += html.mape;
                mae += html.mae;
                average += html.average;
            }
        });
    }

    $("#average").html((average/10));
    $("#mae").html((mae / 10));
    $("#mape").html((mape/10));
    $("#mse").html((mse/10));
}


function holtWintersParameters(){
    $("#TableParams").html("");
    $.ajax({
        url: "/holt-winters-params",
        cache: false,
        async: false,
        success: function (html) {
            var results =html.all_better_results;
            for(var j = 0; j < results.length; j++){
                $("#TableParams").append(
                    "<tr>" +
                    "<td>" + results[j][0] + "</td>" +
                    "<td>" + results[j][1] + "</td>" +
                    "<td>" + results[j][2] + "</td>" +
                    "<td>" + results[j][3] + "</td>" +
                    "</tr>"
                )
            }
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