var setAlarms = []; // user-input alarm time
var localDataObject = {}; // a temporary copy of the json data grabbed
var isFirstTimeLoaded = true;
var notified = [];

var currList = []; // notif list storage to check against


/** On load **/
document.addEventListener('DOMContentLoaded', function () {
    //checkAlarms();
    grabNotifications();

    // Calls the refresh data function every minute.
    refreshData(5000);

    // Animate accordion if notification list is not empty
    if (currList.length != 0) {

    }

    // Request permission
    if (Notification.permission !== "granted")
        Notification.requestPermission();
});


/** Grab data that matches the allowed time **/
function checkAlarms(notificationList) {
    $("#notificationList").empty();
    // Check settings for allowed time
    $.ajax({
        url: "json/settings.json",
        dataType: "json",
        success: function (data) {
            $.each(data, function (index, setting) {
                setAlarms.push(setting.alarm);
            });

            var now = new Date.today().setTimeToNow();
            var justBeforeNow = now.clone();
            justBeforeNow.addMinutes(-5);
            var justAfterNow = now.clone();
            justAfterNow.addMinutes(5);


            for (var i in setAlarms) {
                if (setAlarms[i].meridiem == "morning") {
                    setAlarms[i].parsedTime = new Date.parse(setAlarms[i].time + "am");

                } else {
                    setAlarms[i].parsedTime = new Date.parse(setAlarms[i].time + "pm");
                }
                //console.log(time);
                // check if now is the time to alarm the user
                //if (time.between(justBeforeNow, justAfterNow)) {
                //    for (var i in notificationList) {
                //        //notifyMe("title", toNotify[i].message);
                //        //notified.push(toNotify[i]);
                //        console.log(notificationList[i].time);
                //    }
                //}
            }
            /*  for each notif, check if the time is around now
             if true
             for each alarm, check if alarm time is around now
             if true, check if notif's priority is equal to each other
             break to prevent duplicates
             */
            for (var i in notificationList) {
                notifTime = new Date.parse(notificationList[i].time.replace(/\.(.*)/, ""));
                if (notifTime.between(justBeforeNow, justAfterNow)) {
                    for (var j in setAlarms) {
                        if (setAlarms[j].parsedTime.between(justBeforeNow, justAfterNow)) {
                            if (notificationList[i].priority == setAlarms[j].priority) {
                                notifyMe("title", notificationList[i].message);
                                notified.push(notificationList[i]);
                                break;
                            }
                        }
                    }
                }
            }


        }
    });
}

/** Grab notifications data and output accordingly **/
function grabNotifications() {
    $.ajax({
        url: "json/notifications.json",
        dataType: "json",
        success: function (data) {
            var toNotify = [];
            localDataObject = data;

            // display the new list in Homepage
            $("#notificationList").empty();
            for (var i in localDataObject) {
                toNotify.push(localDataObject[i]);
                noti = localDataObject[i];
                // display if not viewed
                if (noti.viewed == 0) {
                    notiHtml = "<li class='list-group-item";
                    if (noti.priority == 3) {
                        notiHtml += " list-group-item-danger'>";
                    } else if (noti.priority == 2) {
                        notiHtml += " list-group-item-warning'>";
                    } else if (noti.priority == 1) {
                        notiHtml += " list-group-item-success'>";
                    } else if (noti.priority == 0) {
                        notiHtml += "'>";
                    }
                    notiHtml += noti.message + "</li>";
                    $("#notificationList").append(notiHtml);
                }
            }
            // don't notify on page load
            if (isFirstTimeLoaded) {
                toNotify = [];
                for (i in localDataObject) {
                    notified.push(localDataObject[i]);
                }
            }
            // set to null then filter out if already notified
            if (!isFirstTimeLoaded) {
                for (i in toNotify) {
                    for (j in notified) {
                        if (toNotify[i] != null && toNotify[i].id == notified[j].id) {
                            toNotify.splice(i, 1, null);
                        }
                    }
                }
            }
            toNotify = toNotify.filter(function (element) {
                return element != null;
            });

            // notify
            checkAlarms(toNotify);

            // display number of notifications unread
            var unreadNoti = [];
            for (var i in localDataObject) {
                if (localDataObject[i].viewed == 0) {
                    unreadNoti.push(localDataObject[i]);
                }
            }
            if (unreadNoti.length > 0) {
                $("#notiNum").html('<span class="badge">' +
                    unreadNoti.length +
                    '</span>');
                document.title = "(" + unreadNoti.length + ") The Weather Machine";
            }

            isFirstTimeLoaded = false;
        }
    });
}

/** Once the timer runs out, grabs new data **/
function refreshData(interval) {
    setInterval(grabNotifications, interval)
}

function openNotifications() {
    // TODO don't delete them just yet
    $("#notiNum").empty();
    document.title = "The Weather Machine";
    // TODO send viewed data back to the json file HERE
}


/** Notification Web API **/
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
