function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

function toggleFavourite(quoteId) {
    fetch(`/toggle_favourite/${quoteId}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert("Error: " + data.message);
        }
    })
    .catch(error => console.error("Error:", error));
}