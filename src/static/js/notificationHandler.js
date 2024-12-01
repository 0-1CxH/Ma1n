const notifications = [];

function addNotification(message, level) {
    const timestamp = Date.now();
    const notification = {
        message: message,
        id: timestamp,
        lv: level
    };

    notifications.push(notification);
    console.log(notification)
    renderNotifications();
    removeNotificationAsync(timestamp);
}

function renderNotifications() {
    const messageBar = document.getElementById('page-notification-bar');
    messageBar.innerHTML = notifications.map(notification => `
        <div class="page-notification page-notification-${notification.lv}">
            ${notification.message}
        </div>
    `).join('');
}

async function removeNotificationAsync(id) {
    await new Promise(resolve => setTimeout(resolve, 10000)); // Await timeout
    const index = notifications.findIndex(notification => notification.id === id);
    if (index !== -1) {
        notifications.splice(index, 1);
        renderNotifications();
    }
}
