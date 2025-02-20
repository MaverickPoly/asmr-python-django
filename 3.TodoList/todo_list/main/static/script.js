function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}


// Delete Todo
function deleteTodo(todoId) {
    console.log(todoId)
    fetch("/delete/", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({id: todoId}),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            document.getElementById(`todo-${todoId}`).remove();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}


// Toggle Completed
function toggleTodo(todoId) {
    const checkbox = document.querySelector(`#todo-${todoId} input[type="checkbox"]`);
    const completed = checkbox.checked;
    fetch("/toggle_complete/", {
       method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({id: todoId, completed: completed},)
    })
    .then(response => response.json())
    .then(data => {
        // DO Something...
    })
    .catch(error => console.error("Error: ", error));
}
