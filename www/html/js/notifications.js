var notiList = [];

// request permission on page load
document.addEventListener('DOMContentLoaded', function () {
    $.ajax({
        url: "json/notifications.json",
        dataType: "json",
        success: function (data) {
            console.log(data);
            $.each(data, function (index, noti) {
                notiHtml = "<li class='list-group-item list-group-item-"
                if (noti.priority.toLowerCase() == "high") {
                    notiHtml += "danger'>";
                } else if (noti.priority.toLowerCase() == "medium") {
                    notiHtml += "warning'>";
                } else if (noti.priority.toLowerCase() == "low") {
                    notiHtml += "info'>";
                }
                notiHtml += noti.id + "</li>";

                $("#notificationList").append(notiHtml);
            });
        }
    });

    // animate if notification is not empty
    if (notiList.length != 0) {

    }
    if (Notification.permission !== "granted")
        Notification.requestPermission();
});

function readNotifications() {
    notiList = [];
    document.title = "The Weather Machine";
}

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
        notiList.push(notification);

        notification.onshow = function () {
            document.title = "(" + notiList.length + ") The Weather Machine";
        }

        notification.onclick = function () {
            notification.close();
        };

        //notification.onclose = function () {
        //}
    }
}
