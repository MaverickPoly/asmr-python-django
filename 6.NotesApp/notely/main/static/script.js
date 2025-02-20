// CSRF Token
function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}


// Delete a note with ID
function deleteNote(noteId, url) {
    console.log(url);
    console.log(noteId);
    fetch("/delete_note/", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ id: noteId }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = "/";
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

// Clear all notes
function clearNotes() {
    fetch("/clear-notes/", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
}