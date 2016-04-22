$(document).ready(function () {
    $("#tInfo").hide();
    $("#pInfo").hide();
    $("#hInfo").hide();
    $("#lInfo").hide();
    $.ajax({
        url: "json/current.json",
        dataType: "json",
        success: function (data) {
            var weatherdata = data;

            $('#tempData').html(weatherdata.irtemp.ambtemp + "&deg;" + " Celsius");
            $('#baroData').html(weatherdata.baro.pressure + " hPa");
            $('#humidData').html(weatherdata.humid.humidity + "&#37;" + " RH");
            $('#luxData').html(weatherdata.opti.light + " lux");

            // Calls the refresh data function every minute.
            refreshData(60000);
        }
    });
});


/** Makes and AJAX call and refreshes the information on the page **/
function grabData() {
    $.ajax({
        url: "json/current.json",
        dataType: "json",
        success: function (data) {
            var weatherdata = data;

            $('#tempData').html(weatherdata.irtemp.ambtemp + "&deg;" + " Celsius");
            $('#baroData').html(weatherdata.baro.pressure + " hPa");
            $('#humidData').html(weatherdata.humid.humidity + "&#37;" + " RH");
            $('#luxData').html(weatherdata.opti.light + " lux");
        }
    });
}

/** Once the timer runs out, grabs new data **/
function refreshData(interval) {
    return setInterval(grabData, interval);
}


/** Main Contents **/
function hideAll() {
    $("#tInfo").hide();
    $("#pInfo").hide();
    $("#hInfo").hide();
    $("#lInfo").hide();
};

$("#temp").click(function () {
    if ($("#tInfo").is(":visible")) {
        $("#tInfo").hide();
    } else {
        hideAll();
        $("#tInfo").toggle();
    }
});

$("#pressure").click(function () {
    if ($("#pInfo").is(":visible")) {
        $("#pInfo").hide();
    } else {
        hideAll();
        $("#pInfo").toggle();
    }
});

$("#humid").click(function () {
    if ($("#hInfo").is(":visible")) {
        $("#hInfo").hide();
    } else {
        hideAll();
        $("#hInfo").toggle();
    }
});

$("#lux").click(function () {
    if ($("#lInfo").is(":visible")) {
        $("#lInfo").hide();
    } else {
        hideAll();
        $("#lInfo").toggle();
    }
});