var currType;

$(document).ready(function () {
    // Show first tab
    $('#tempTab a').click();

    // Calls the refresh data function every minute.
    refreshData(60000);
});


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
        timeList.push(item.time);
    });

    $("#dataContent").highcharts({
        title: {
            text: "",
            x: -20 //center
        },
        xAxis: {
            categories: timeList
        },
        yAxis: {
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '°C'
        },
        series: [{
            name: 'data',
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

//Once the timer runs out, grabs new data.
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
    currType = "Temperature";
    grabData();
});

$('#pressureTab a').click(function (e) {
    e.preventDefault();
    if (currType == "Pressure") {
        return
    }
    $(this).tab('show');
    currType = "Pressure";
    grabData();
});

$('#humidTab a').click(function (e) {
    e.preventDefault();
    if (currType == "Humidity") {
        return
    }
    $(this).tab('show');
    currType = "Humidity";
    grabData();
});

$('#luxTab a').click(function (e) {
    e.preventDefault();
    if (currType == "Luxometer") {
        return
    }
    $(this).tab('show');
    currType = "Luxometer";
    grabData();
});