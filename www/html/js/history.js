$(document).ready(function () {
    // Grab Data
    grabData("#tHist", "temp");
    grabData("#pHist", "baro");
    grabData("#hHist", "humid");
    grabData("#lHist", "lux");

    // Show first tab
    $('#tempTab a:first').tab('show');
});


// Makes and AJAX call and refreshes the information on the page.
function grabData(table, type) {
    $.ajax({
        url: "json/history.json",
        dataType: "json",
        success: function (data) {
            var dataObject;
            var dataUnit;
            var dataHtml = "";
            if (type == "temp") {
                dataObject = data.irtemp;
                dataUnit = "&deg; Celcius";
            } else if (type == "baro") {
                dataObject = data.baro;
                dataUnit = " hPa";
            } else if (type == "humid") {
                dataObject = data.humid;
                dataUnit = "&#37 RH";
            } else if (type == "lux") {
                dataObject = data.opti;
                dataUnit = " lux";
            }
            $.each(dataObject, function (index, item) {
                var value;
                if (type == "temp") {
                    value = item.ambtemp;
                } else if (type == "baro") {
                    value = item.pressure;
                } else if (type == "humid") {
                    value = item.humidity;
                } else if (type == "lux") {
                    value = item.light;
                }
                dataHtml += "<tr><td>" +
                    item.time +
                    "</td><td>" +
                    value + dataUnit +
                    "</td></tr>";
            });
            $(table + " tbody").append(dataHtml);
        }
    });
}

// Once the timer runs out, grabs new data.
function refreshData(interval) {
    return setInterval(grabData, interval);
}

// Calls the refresh data function every minute.
var timer = refreshData(60000);


$('#tempTab a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
});

$('#pressureTab a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
});

$('#humidTab a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
});

$('#luxTab a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
});