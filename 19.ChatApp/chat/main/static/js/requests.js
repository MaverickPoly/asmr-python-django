// Scroll to bottom in chat view
document.addEventListener("DOMContentLoaded", function () {
    var container = document.getElementById("messages-container");
    container.scrollTop = container.scrollHeight;
});

// Get cookie by name
function getCookie(name) {
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    }
    return null;
}

// Dynamic function to send requests
function sendRequest(url, method, body, callback, errorCallback) {
    fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: body,
    })
        .then((response) => response.json())
        .then(callback)
        .catch(errorCallback);
}

// Register user to a chat!!
function registerToChat(chatId) {
    console.log(`Chat Id: ${chatId}`);

    sendRequest(
        `/chat/${chatId}/register/`,
        "POST",
        JSON.stringify({ chat_id: chatId }),
        (data) => {
            if (data.success) {
                location.reload();
            } else {
                alert(data.error || "Something went wrong!");
            }
        },
        (error) => console.error("Error: ", error)
    );
}

// Delete message
function deleteMessage(messageId) {
    console.log(`Message id: ${messageId}`);

    sendRequest(
        `/message/${messageId}/delete/`,
        "DELETE",
        JSON.stringify({ message_id: messageId }),
        (data) => {
            if (data.success) {
                location.reload();
            } else {
                alert(data.error || "Something went wrong!");
            }
        },
        (error) => console.error("Error: ", error)
    );
}
