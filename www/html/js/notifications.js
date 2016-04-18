var currList = [];
var unreadNoti = [];

// request permission on page load
document.addEventListener('DOMContentLoaded', function () {
    checkAlarms();

    // Calls the refresh data function every minute.
    refreshData(5000);

    // Animate accordion if notification list is not empty
    if (currList.length != 0) {

    }
    if (Notification.permission !== "granted")
        Notification.requestPermission();
});


// Grab data that matches the allowed time
function checkAlarms() {
    $("#notificationList").empty();
    // Check settings for allowed time
    var setAlarms = [];
    $.ajax({
        url: "json/settings.json",
        dataType: "json",
        success: function (data) {
            $.each(data, function (index, setting) {
                setAlarms.push(setting.alarm);
            })

            for (i in setAlarms) {
                var time = setAlarms[i].time;
                if (setAlarms[i].meridiem == "morning") {
                    time += "am"
                } else {
                    time += "pm"
                }
                time = new Date.parse(time);

                // check if now is the time to alarm the user
                var now = new Date.today().setTimeToNow();
                var justBeforeNow = now.clone();
                justBeforeNow.addMinutes(-5);
                var justAfterNow = now.clone();
                justAfterNow.addMinutes(5);
                if (time.between(justBeforeNow, justAfterNow)) {
                    grabNotifications();
                }
            }
        }
    });
}

// Grab notifications data and output accordingly
function grabNotifications() {
    $.ajax({
        url: "json/notifications.json",
        dataType: "json",
        success: function (data) {
            if (currList.length == 0) {
                $.each(data, function (index, noti) {
                    currList.push(noti);
                });
            }

            // make a new list to check which notifications are unread
            var newList = [];
            $.each(data, function (index, noti) {
                newList.push(noti);
            });

            // display the new list
            for (i in newList) {
                noti = newList[i];
                notiHtml = "<li class='list-group-item list-group-item-"
                if (noti.priority.toLowerCase() == "high") {
                    notiHtml += "danger'>";
                } else if (noti.priority.toLowerCase() == "medium") {
                    notiHtml += "warning'>";
                } else if (noti.priority.toLowerCase() == "low") {
                    notiHtml += "success'>";
                }
                notiHtml += noti.message + "</li>";
                $("#notificationList").append(notiHtml);
            }

            // remove if notification isn't new
            for (i in newList) {
                if (currList[i]) {
                    if (currList[i].id == newList[i].id) {
                        newList.splice(i, 1, null);
                    }
                }
            }
            newList = newList.filter(function (element) {
                return element != null;
            });

            // check if already in unreadList; else notify
            for (i in newList) {
                if (!unreadNoti[i]) {
                    console.log("notify " + newList[i].message)
                    notifyMe("title", newList[i].message)
                }
            }

            // display number of notifications unread
            unreadNoti = newList;
            if (unreadNoti.length > 0) {
                $("#notiNum").html('<span class="badge">' +
                    unreadNoti.length +
                    '</span>');
                document.title = "(" + unreadNoti.length + ") The Weather Machine";
            }
        }
    });
}

// Once the timer runs out, grabs new data.
function refreshData(interval) {
    setInterval(checkAlarms, interval)
}

function openNotifications() {
    unreadNoti.forEach(function (element) {
        currList.push(element);
    });
    unreadNoti = [];
    $("#notiNum").empty();
    document.title = "The Weather Machine";
}


// Notification Web API
function notifyMe(messageTitle, messageBody) {
    if (!Notification) {
        alert('Desktop notifications not available in your browser. Try Chromium.');
        return;
    }
    if (Notification.permission !== "granted")
        Notification.requestPermission();
    else {
        notification = new Notification('Notification title', {
            icon: 'http://cdn.sstatic.net/stackexchange/img/logos/so/so-icon.png',
            body: messageBody
        });
        setTimeout(notification.close.bind(notification), 3000);

        notification.onclick = function () {
            notification.close();
        };

        //notification.onclose = function () {
        //}
    }
}
