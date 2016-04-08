var currType;
var currUnit;

$(document).ready(function () {
    // Show first tab
    $('#tempTab a').click();

    // Calls the refresh data function every minute.
    refreshData(60000);
});


// Parse date/time to properly display in charts
function formatDateTime(raw) {
    var result = new Date.parse(raw.replace(/\.(.*)/, ""));
    var format;
    if (result.getYear() == Date.today().getYear()) {
        if (result.getDay() == Date.today()) {
            format = "hh:mmtt";
        }
        else {
            format = "hh:mmtt MM/dd";
        }
    } else {
        format = "hh:mmtt MM/dd/yy";
    }
    return result.toString(format);
}

// Draw chart from data given by using HighCharts
function drawChart(dataObject) {
    var dataList = [];
    var timeList = [];
    $.each(dataObject, function (index, item) {
        var value;
        if (currType == "Temperature") {
            value = item.ambtemp;
        } else if (currType == "Pressure") {
            value = item.pressure;
        } else if (currType == "Humidity") {
            value = item.humidity;
        } else if (currType == "Luxometer") {
            value = item.light;
        }
        dataList.push(parseFloat(value));
        timeList.push(formatDateTime(item.time));
    });

    $("#dataContent").highcharts({
        title: {
            text: currType + " (" + currUnit.trim() + ")",
            x: -20
        },
        xAxis: {
            categories: timeList
        },
        yAxis: {
            title: {
                text: ''
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        chart: {
            marginLeft: 60,
            marginRight: 60
        },
        tooltip: {
            valueSuffix: currUnit
        },
        legend: {
            enabled: false
        },
        series: [{
            name: currType,
            data: dataList
        }]
    });
}

// Makes and AJAX call and refreshes the information on the page.
function grabData() {
    $.ajax({
        url: "json/history.json",
        dataType: "json",
        success: function (data) {
            if (currType == "Temperature") {
                drawChart(data.irtemp);
            }
            else if (currType == "Pressure") {
                drawChart(data.baro);
            }
            else if (currType == "Humidity") {
                drawChart(data.humid);
            }
            else if (currType == "Luxometer") {
                drawChart(data.opti);
            }
        }
    });
}

// Once the timer runs out, grabs new data.
function refreshData(interval) {
    setInterval(grabData, interval)
}


// Main Contents
$('#tempTab a').click(function (e) {
    e.preventDefault();
    if (currType == "Temperature") {
        return
    }
    $(this).tab('show');
    currUnit = " Celcius";
    currType = "Temperature";
    grabData();
});

$('#pressureTab a').click(function (e) {
    e.preventDefault();
    if (currType == "Pressure") {
        return
    }
    $(this).tab('show');
    currUnit = " hPa";
    currType = "Pressure";
    grabData();
});

$('#humidTab a').click(function (e) {
    e.preventDefault();
    if (currType == "Humidity") {
        return
    }
    $(this).tab('show');
    currUnit = "% RH";
    currType = "Humidity";
    grabData();
});

$('#luxTab a').click(function (e) {
    e.preventDefault();
    if (currType == "Luxometer") {
        return
    }
    $(this).tab('show');
    currUnit = " lux";
    currType = "Luxometer";
    grabData();
});