function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}

function borrowBook(book_id) {
    fetch("/borrow_book/", {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ id: book_id }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
            else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
}


function returnBook(book_id) {
    fetch("/return_book/", {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ id: book_id }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
            else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
}   