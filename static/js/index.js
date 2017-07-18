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
                );
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

function mlr(){
    $("#TableParams").hide();
    $("#TableResults").html("");
    var mse = 0;
    var mape = 0;
    var mae = 0;
    var average = 0;
    for(var i = 1; i < 11; i++) {
        $.ajax({
            url: "/multi",
            cache: false,
            async: false,
            success: function (html) {
                console.log(html);
                $("#TableResults").append(
                    "<tr>" +
                        "<td>" + i + "</td>" +
                        "<td>" + html.average + "</td>" +
                        "<td>" + html.mae + "</td>" +
                        "<td>" + html.mape + "</td>" +
                        "<td>" + html.mse + "</td>" +
                    "</tr>"
                );
                $("#TableCoef").append(
                    "<tr>" +
                        "<td>" + html.coef[0]  + "</td>" +
                        "<td>" + html.coef[1]  + "</td>" +
                        "<td>" + html.coef[2]  + "</td>" +
                        "<td>" + html.coef[3]  + "</td>" +
                        "<td>" + html.coef[4]  + "</td>" +
                        "<td>" + html.coef[5]  + "</td>" +
                        "<td>" + html.coef[6]  + "</td>" +
                        "<td>" + html.coef[7]  + "</td>" +
                        "<td>" + html.coef[8]  + "</td>" +
                        "<td>" + html.coef[9]  + "</td>" +
                    "</tr>"
                );

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
    $("#TableParams").show();
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

function avg(average,mae, mape, mse) {
    $("#average").html((average/10));
    $("#mae").html((mae / 10));
    $("#mape").html((mape/10));
    $("#mse").html((mse/10));
}

function ARIMA(){
    $("#TableResults").html("");
    var mse = 0;
    var mape = 0;
    var mae = 0;
    var average = 0;
    for(var i = 1; i < 11; i++) {
        $.ajax({
            url: "/arima",
            success: function (html) {
                $("#TableResults").append(
                    "<tr>" +
                        "<td>" + i + "</td>" +
                        "<td>" + html.average + "</td>" +
                        "<td>" + html.mae + "</td>" +
                        "<td>" + html.mape + "</td>" +
                        "<td>" + html.mse + "</td>" +
                    "</tr>"
                );
                mse += html.mse;
                mape += html.mape;
                mae += html.mae;
                average += html.average;
                avg(average,mae,mape,mse);
            }
        });
    }
}

function nn(){
    $("#SSE").html("");
}