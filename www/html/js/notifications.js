var notiList = [];


// request permission on page load
document.addEventListener('DOMContentLoaded', function () {
    if (Notification.permission !== "granted")
        Notification.requestPermission();
});

var notification;

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
        notiList.push(notification);

        notification.onshow = function () {
            document.title = "(" + notiList.length + ") The Weather Machine";
        }

        //notification.onclick = function () {
        //    window.open("http://stackoverflow.com/a/13328397/1269037");
        //};

        notification.onclose = function () {
            document.title = "The Weather Machine";
        }
    }
}
