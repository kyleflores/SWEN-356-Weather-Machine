var currList = [];
var unreadNoti = [];

// request permission on page load
document.addEventListener('DOMContentLoaded', function () {
    grabNotifications();

    // Calls the refresh data function every minute.
    refreshData(5000);

    // Animate accordion if notification list is not empty
    if (currList.length != 0) {

    }
    if (Notification.permission !== "granted")
        Notification.requestPermission();
});


// Read and display data from JSON
function grabNotifications() {
    $("#notificationList").empty();
    $.ajax({
        url: "json/notifications.json",
        dataType: "json",
        success: function (data) {
            var newList = [];
            if (currList.length == 0) {
                $.each(data, function (index, noti) {
                    currList.push(noti);
                });
            }
            // make a temp list to check which notifications are unread
            $.each(data, function (index, noti) {
                newList.push(noti);
            });
            for (i = 0; i < newList.length; i++) {
                noti = newList[i];
                notiHtml = "<li class='list-group-item list-group-item-"
                if (noti.priority.toLowerCase() == "high") {
                    notiHtml += "danger'>";
                } else if (noti.priority.toLowerCase() == "medium") {
                    notiHtml += "warning'>";
                } else if (noti.priority.toLowerCase() == "low") {
                    notiHtml += "success'>";
                }
                notiHtml += noti.id + "</li>";

                $("#notificationList").append(notiHtml);
            }

            // check if notification is new or not
            for (j = 0; j < newList.length; j++) {
                if (currList[j]) {
                    if (currList[j].id == newList[j].id) {
                        newList.splice(j, 1, null);
                    }
                }
            }
            // remove if null
            unreadNoti = newList.filter(function (element) {
                return element != null;
            });
            // display number of notifications unread
            console.log(unreadNoti);
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
    setInterval(grabNotifications, interval)
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
            body: "Hey there! You've been notified!"
        });
        setTimeout(notification.close.bind(notification), 3000);

        notification.onclick = function () {
            notification.close();
        };

        //notification.onclose = function () {
        //}
    }
}
